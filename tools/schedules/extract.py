#!/usr/bin/env python3
"""Refresh KiCad-linked rows while retaining CSV-owned purchasing data."""
import argparse
from collections import defaultdict
import csv
from decimal import Decimal, InvalidOperation
import io
import json
from pathlib import Path
import re
import sys

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'tools/wiring'))
from model import Schematic, atomic_write, digest
from source import nodes, one, parse, prop
from generate import DEFAULT_SCH, DEFAULT_PCB, generate

# Generic row ownership lives in the shared reviewer; the adapter supplies
# current project-specific KiCad inventory and physical wire validation.
sys.path.insert(0,str(PROJECT.parents[1]/'bom_review'))
from bom_sources import BOM_HEADERS as HEADERS, TAG_HEADERS, normalized, tag_rows, merge_rows


def properties(node):
    return {p[1]: p[2] for p in nodes(node,'property')}


def bom_rows(schematic_text, pcb_text, include_excluded=False):
    schematic = Schematic(schematic_text)
    fps = nodes(parse(pcb_text), 'footprint')
    placed = {prop(f,'Reference'): f for f in fps if prop(f,'Reference') not in ['',None,'REF**']}
    parts, seen = [], set()
    excluded = 0
    for ref, symbols in schematic.by_ref.items():
        if ref.startswith('#'):
            continue
        seen.add(ref)
        symbol = symbols[0]
        if one(symbol,'in_bom') == ['in_bom','no'] or one(symbol,'dnp') == ['dnp','yes']:
            excluded += 1
            continue
        data = properties(symbol)
        f = placed.get(ref)
        if f and prop(f,'Wire.MetadataOnly') != 'yes':
            board_data = properties(f)
            if data.get('MPN') and board_data.get('MPN') and data['MPN'] != board_data['MPN']:
                raise ValueError(f'{ref}: schematic and PCB MPN differ; reconcile before BOM extraction.')
            # Schematic fields lead; placed footprint data fills absent fields.
            data = {**board_data, **{k:v for k,v in data.items() if v}}
        data['_auto_add'] = bool(data.get('MPN'))
        parts.append((ref,data))
    for f in fps:
        ref = prop(f,'Reference')
        if ref in seen:
            continue
        attrs = one(f,'attr') or []
        if prop(f,'Wire.MetadataOnly') == 'yes' or ('exclude_from_bom' in attrs and not include_excluded):
            excluded += 1
            continue
        data = properties(f)
        data['_auto_add'] = 'exclude_from_bom' not in attrs and bool(data.get('MPN'))
        if not data.get('MPN'):
            data['_model_part'] = re.sub(r'_(?:\d+(?:\.\d+)?mm|Front|Top|LeftWall|BottomWall|Open)(?:_.*)?$', '',data.get('Value',''))
        parts.append((ref or one(f,'uuid')[1],data))
    grouped = defaultdict(list)
    for ref,data in parts:
        identity = normalized(data.get('MPN') or data.get('_model_part') or data.get('Value') or ref)
        grouped[identity].append((ref,data))
    rows, audit = [], []
    for identity, instances in grouped.items():
        def choose(*names):
            values = {next((data[n] for n in names if data.get(n)), '') for _,data in instances}
            values.discard('')
            if len(values)>1:
                raise ValueError(f'{identity}: conflicting BOM field {names}: {sorted(values)}')
            return next(iter(values),'')
        category = choose('Category','Type')
        choose('Manufacturer')  # Reject collisions between different manufacturers.
        name = choose('Part Name') or choose('Value') or identity
        name = ' '.join(name.split())
        mpn = choose('MPN')
        if mpn and mpn not in name:
            name += ' ('+mpn+')'
        quantity = str(len(instances))
        pack,unit,cost = choose('BOM.PACK'),choose('BOM.UNIT'),choose('BOM.COST')
        line = '0.00'
        if cost:
            try:
                number = Decimal(cost)
                if not number.is_finite():
                    raise InvalidOperation
                line = f'{number*len(instances):.2f}'
            except InvalidOperation:
                raise ValueError(f'{identity}: BOM.COST must be a finite number.')
        supplier = choose('Supplier')
        spn = choose('Supplier PN','SupplierPartNumber')
        rows.append([category,name,quantity,pack,unit,cost,line,supplier,spn])
        part=mpn or choose('_model_part') or choose('Value') or identity
        audit.append({'part':part,'key':'part:'+identity,'references':[ref for ref,_ in instances],
                      'quantity':len(instances),'cost_recorded':bool(cost),'row':rows[-1],
                      'auto_add':any(d.get('_auto_add') for _,d in instances),
                      'identifiers':sorted({d.get(k,'') for _,d in instances for k in
                          ['MPN','Supplier PN','SupplierPartNumber','_model_part'] if d.get(k)}),
                      'names':sorted({d.get('Part Name','') for _,d in instances if d.get('Part Name')}),
                      'explicit_bom_fields':{k:choose('BOM.'+k) for k in ['PACK','UNIT','COST'] if choose('BOM.'+k)}})
    rows.sort(key=lambda r:(r[0].casefold(),r[1].casefold(),r[-1]))
    return rows,{'part_groups':len(rows),'component_instances':len(parts),
                 'excluded_instances':excluded,'groups':audit}


def extract_bom(output,existing_path=None,tags_only=False):
    sch,pcb = DEFAULT_SCH.read_bytes(),DEFAULT_PCB.read_bytes()
    _,report = bom_rows(sch.decode(),pcb.decode(),include_excluded=True)
    existing_path=existing_path or PROJECT/'Powermatic_BOM_revP.csv'
    existing_bytes=existing_path.read_bytes()
    with io.StringIO(existing_bytes.decode('utf-8-sig'),newline='') as stream:
        existing=list(csv.DictReader(stream))
    tagged=tag_rows(existing,report['groups'])
    rows,removed=(tagged,[]) if tags_only else merge_rows(tagged,report['groups'])
    if digest(DEFAULT_SCH.read_bytes())!=digest(sch) or digest(DEFAULT_PCB.read_bytes())!=digest(pcb):
        raise ValueError('KiCad files changed during extraction; save and refresh again.')
    if existing_path.read_bytes()!=existing_bytes:
        raise ValueError('The BOM changed during extraction; its newer data was preserved.')
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,HEADERS+TAG_HEADERS,lineterminator='\r\n')
    writer.writeheader();writer.writerows(rows)
    atomic_write(output,stream.getvalue().encode(),
                 expected=digest(existing_bytes) if output.resolve()==existing_path.resolve() else None)
    report.update(schematic_sha256=digest(sch),pcb_sha256=digest(pcb))
    report.update(linked_rows=sum(r.get('SOURCE')=='KiCad' for r in rows),
                  local_rows=sum(r.get('SOURCE')!='KiCad' for r in rows),removed_linked_rows=removed)
    return report


def extract_wires(output):
    return generate(DEFAULT_SCH,DEFAULT_PCB,output)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['bom','wire'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--tag-existing',action='store_true',help='add provenance without changing any existing BOM values')
    parser.add_argument('--existing',type=Path,help='current live BOM, for CSV-owned purchasing rows and fields')
    args=parser.parse_args()
    try:
        config=json.loads((PROJECT/'kicad_schedules.json').read_text())
        if config.get('paused',{}).get(args.mode):
            raise ValueError(config['paused'][args.mode])
        report=extract_bom(args.output,existing_path=args.existing,tags_only=args.tag_existing) if args.mode=='bom' else extract_wires(args.output)
        print(json.dumps(report))
    except (ValueError,OSError,KeyError) as error:
        parser.exit(2,f'KiCad {args.mode} extraction failed: {error}\n')


if __name__=='__main__':
    main()
