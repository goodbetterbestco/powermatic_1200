"""Project metadata/validation adapter for the shared trace-to-wire engine."""
from collections import Counter,defaultdict
import json
import math
from pathlib import Path
import re
import subprocess
import sys

from model import Schematic
from source import nodes,one,prop
from presentation import pin_label,termination_code

SHARED=Path(__file__).resolve().parents[4]/'bom_review'
sys.path.insert(0,str(SHARED))
from kicad_routes import extract_routes


def native_board(path,work):
    reader=SHARED/'native_kicad_tracks.py'
    python=Path('/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3')
    runtime=str(python) if python.exists() else sys.executable
    result_path=Path(work)/'native_routes.json'
    try:
        result=subprocess.run([runtime,str(reader),str(path),str(result_path)],capture_output=True,text=True,timeout=45)
    except subprocess.TimeoutExpired:
        raise ValueError('Native KiCad trace extraction timed out; the CSV was not replaced.')
    if result.returncode or not result_path.exists():
        raise ValueError('Native KiCad trace extraction failed: '+(result.stderr or result.stdout).strip()[-1000:])
    return json.loads(result_path.read_text())


def sizes(schematic,pin_nets,warnings=None):
    warnings = warnings if warnings is not None else []
    result={}
    for symbol in schematic.symbols:
        value=prop(symbol,'Wire.Sizes')
        if not value:continue
        payload=json.loads(value);ref=prop(symbol,'Reference')
        if payload.get('owner_uuid')!=one(symbol,'uuid')[1]:
            raise ValueError(ref+': copied or replaced Wire.Sizes owner.')
        for entry in payload.get('entries',[]):
            endpoint=(ref,entry['pin'])
            if endpoint not in pin_nets or entry['net']!=pin_nets[endpoint]:
                warnings.append(ref+'.'+entry['pin']+
                                ': stale sizing net; its gauge declaration was ignored. Reconcile Wire.Sizes with the saved schematic.')
                continue
            if isinstance(entry.get('awg'),int):result[endpoint]=entry['awg']
    return result


def pad_name(pad,board):
    ref=pad['ref'];fields=pad['fields']
    if re.fullmatch(r'TB\d+',ref):return 'Terminal '+ref[2:]
    name=' '.join((fields.get('Part Name') or fields.get('Value') or ref).split())
    matching={p['ref'] for p in board['pads'] if ' '.join((p['fields'].get('Part Name') or p['fields'].get('Value') or p['ref']).split())==name}
    return name+' '+ref if len(matching)>1 else name


def termination(pad,count,warnings):
    text=pad['termination']
    if not text.strip():
        raise ValueError(pad['ref']+'.'+pad['pin']+': footprint termination field is missing.')
    capability,separator,preparation=text.partition(';')
    suffix=separator+preparation if separator else ''
    if capability=='Ferrule or twin ferrule as required':
        if count==1:return 'Ferrule'+suffix
        if count==2:return 'Twin ferrule'+suffix
        warnings.append(pad['ref']+'.'+pad['pin']+f': {count} wires share one clamp; allocate additional clamps.')
    elif capability=='Single ferrule' and count>1:
        warnings.append(pad['ref']+'.'+pad['pin']+f': {count} wires share a single-conductor clamp; allocate separate clamps.')
    return text


def rows_from_traces(board,schematic,pin_nets,slack_mm=100,round_mm=10):
    if not math.isfinite(slack_mm) or not math.isfinite(round_mm) or slack_mm<0 or round_mm<=0:
        raise ValueError('Trace cut allowance must be nonnegative and rounding must be positive.')
    routes,warnings=extract_routes(board)
    declared=sizes(schematic,pin_nets,warnings)
    supplied={frozenset(c['pad_ids']):c for c in board.get('supplied_connections',[])}
    counts=Counter(p['id'] for route in routes
                   if frozenset([route['from']['id'],route['to']['id']]) not in supplied
                   for p in [route['from'],route['to']])
    assigned=defaultdict(set);rows=[];details=[];unknown=set()
    for route in routes:
        pair=[route['from'],route['to']];nets=set();gauges=set()
        boundary = [p for p in pair if p.get('pass_through')]
        if boundary:
            warnings.append('Route stops at cable gland '+', '.join(p['ref']+'.'+p['pin'] for p in boundary)+
                            '; scheduled length covers the drawn section only, not the unrecorded external run.')
        if route['net']:nets.add(route['net'])
        for pad in pair:
            ref,pin=pad['ref'],pad['pin']
            scope=pad['fields'].get('Wire.LengthScope')
            if scope:warnings.append(ref+': '+scope)
            if not ref or ref=='REF**' or '?' in ref:
                raise ValueError('Assign a unique reference to a terminal block before routing it.')
            if pad['net']:nets.add(pad['net'])
            native=pin_nets.get((ref,pin))
            if ref in schematic.by_ref and native is None:
                raise ValueError(ref+'.'+pin+': footprint terminal does not exist in the saved schematic.')
            if native and native.startswith('unconnected-'):
                raise ValueError(ref+'.'+pin+': schematic marks this terminal unconnected; reconcile the drawing.')
            if native:nets.add(native)
            value=pad['fields'].get('Wire.AWG.'+pin)
            if value:
                if not value.isdigit() or not 1<=int(value)<=40:
                    raise ValueError(ref+'.'+pin+': invalid footprint Wire.AWG value.')
                gauges.add(int(value))
            elif (ref,pin) in declared:
                gauges.add(declared[ref,pin])
            else:
                # Old fixed selections can supply their recorded size. Generic
                # block capabilities intentionally do not imply any gauge.
                gauges.update(int(n) for n in re.findall(r'\b(\d+)\s*AWG\b',pad['termination']))
        if len(nets)>1:
            raise ValueError('Routed endpoints/net disagree: '+', '.join(p['ref']+'.'+p['pin'] for p in pair)+' -> '+', '.join(sorted(nets)))
        net=next(iter(nets),'')
        if not net:warnings.append('Unassigned electrical net on '+pair[0]['ref']+'.'+pair[0]['pin']+' -> '+pair[1]['ref']+'.'+pair[1]['pin'])
        for pad in pair:
            if net:assigned[pad['id']].add(net)
        supplier=supplied.get(frozenset(p['id'] for p in pair))
        if supplier:
            details.append({'id':route['id'],'from':pair[0]['ref']+'.'+pair[0]['pin'],
                            'to':pair[1]['ref']+'.'+pair[1]['pin'],'net':net,
                            'kind':'factory','exported':False,'section':'Supplier assembly',
                            'assembly':supplier['assembly'],'part':supplier['part'],
                            'review':'supplier','track_ids':route['track_ids'],
                            'endpoint_pad_ids':[p['id'] for p in pair]})
            continue
        awg=str(next(iter(gauges))) if len(gauges)==1 else ''
        if not awg:
            unknown.add(route['id'])
            warnings.append('AWG '+('conflict '+str(sorted(gauges)) if gauges else 'not specified')+' on '+pair[0]['ref']+'.'+pair[0]['pin']+' -> '+pair[1]['ref']+'.'+pair[1]['pin'])
        cut=math.ceil((route['route_mm']+slack_mm-1e-7)/round_mm)*round_mm
        terms=[termination(p,counts[p['id']],warnings) for p in pair]
        row=[pad_name(pair[0],board),pin_label(pair[0]),pad_name(pair[1],board),pin_label(pair[1]),awg,f'{cut:g}',
             termination_code(terms[0],awg),termination_code(terms[1],awg)]
        rows.append(row)
        details.append({'id':route['id'],'from':pair[0]['ref']+'.'+pair[0]['pin'],
                        'to':pair[1]['ref']+'.'+pair[1]['pin'],'net':net,'kind':'route-section' if boundary else 'wire','exported':True,
                        'row':row,'section':'PCB traces','route_mm':round(route['route_mm'],6),
                        'review':'pending',
                        'cut_mm':cut,'slack_mm':slack_mm,'track_ids':route['track_ids'],
                        'endpoint_pad_ids':[p['id'] for p in pair]})
    if any(len(n)>1 for n in assigned.values()):
        raise ValueError('Different electrical nets are routed into the same terminal clamp.')
    # Factory/common groups constrain electrical consistency, but do not create
    # extra physical wires. Glands are currently routing markers, not wire ends.
    by_endpoint={(p['ref'],p['pin']):p['id'] for p in board['pads']}
    for group in board.get('internal_groups',[]):
        nets={n for endpoint in group for n in assigned.get(by_endpoint.get(tuple(endpoint)),set())}
        if len(nets)>1:
            message=('Electrical net conflict on internally common terminals '+
                     ', '.join('.'.join(p) for p in group)+': '+', '.join(sorted(nets)))
            warnings.append(message)
            affected={by_endpoint.get(tuple(endpoint)) for endpoint in group}
            for detail in details:
                if affected.intersection(detail['endpoint_pad_ids']):
                    detail['review']='net-conflict'
                    detail.setdefault('issues',[]).append(message)
    return rows,details,list(dict.fromkeys(warnings))
