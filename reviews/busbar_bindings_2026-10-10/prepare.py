"""Repair placed busbar metadata/contact targets and stage a schedule refresh."""
from collections import Counter
from decimal import Decimal
from pathlib import Path
import json
import re
import sys

PROJECT = Path(__file__).resolve().parents[2]
WORK = Path('/private/tmp/powermatic-busbar-bindings-20261010')
sys.path.insert(0,str(PROJECT/'tools/wiring'))
from source import children,key,nodes,one,parse,prop,replace,FOOTPRINT_BLOCK

board = (WORK/'before/powermatic_1200.kicad_pcb').read_text()
refs = {'BB1','BB2','K1','K2','K4','K5','K6','S2'}
blocks = {}
for m in FOOTPRINT_BLOCK.finditer(board):
    if any('\n\t\t(property "Reference" "'+ref+'"' in m[0] for ref in refs):
        n=parse(m[0]);blocks[prop(n,'Reference')]=(m,n)
assert set(blocks)==refs
host_refs={'A':'K1','B':'K2'}
hosts={role:blocks[ref][1] for role,ref in host_refs.items()}
assert all(len(one(h,'at'))==3 for h in hosts.values())


def fmt(n):
    return format(n.normalize(),'f') if n else '0'


def set_field(raw,name,value):
    found=[]
    for a,b,c in children(raw):
        if key(c)=='property' and parse(c)[1]==name:
            p=parse(c)
            found.append((a,b,c.replace(json.dumps(p[2]),json.dumps(value),1)))
    assert len(found)==1,name
    return replace(raw,found)


pad_changes=[]
removed=[]


def contacts(raw,board_instance):
    fp=parse(raw)
    mapping=json.loads(prop(fp,'Wire.MatingPads'))['pads']
    counts=Counter(p[1] for p in nodes(fp,'pad'))
    assert set(counts)==set(mapping)
    is_bottom='HMX1-BBREV_BOT' in fp[1]
    old_origin=one(fp,'at')[1:3] if board_instance else ['0','0']
    # Normalize BOT's origin to its host datum while preserving the saved
    # global artwork: translate all local graphics/field positions by the
    # opposite 0.0625 mm. Logical pads then use the reusable library positions.
    bottom_origin=one(blocks['BB2'][1],'at')[1:3]
    host_origin=one(hosts['A'],'at')[1:3]
    body_delta_y=Decimal(bottom_origin[1])-Decimal(host_origin[1]) if is_bottom else Decimal(0)
    origin=host_origin if board_instance and is_bottom else old_origin
    coords=re.compile(r'\((at|start|end|mid|center|xy)\s+(-?[\d.]+)\s+(-?[\d.]+)')
    def shift_graphic(c):
        return coords.sub(lambda m:'('+m[1]+' '+m[2]+' '+fmt(Decimal(m[3])+body_delta_y),c)
    edits=[]
    for a,b,c in children(raw):
        kind=key(c)
        if body_delta_y and (kind.startswith('fp_') or kind=='property'):
            edits.append((a,b,shift_graphic(c)))
        elif body_delta_y and board_instance and kind=='at':
            edits.append((a,b,'(at '+' '.join(origin)+')'))
        if key(c)=='descr':
            text=one(fp,'descr')[1]
            new=text.replace('57 mm host spacing','58 mm logical host spacing')
            if new!=text:edits.append((a,b,'(descr '+json.dumps(new)+')'))
        if key(c)!='pad':continue
        p=parse(c);pin=p[1];at=one(p,'at')
        # These three second A-side pads duplicate the proper B contacts.
        # Preserve the left A contacts and their UUIDs; each electrical contact
        # has exactly one logical target after repair.
        if pin.startswith('A') and counts[pin]==2 and Decimal(at[1])>20:
            edits.append((a,b,''));removed.append({'footprint':prop(fp,'Reference') if board_instance else fp[1],'pin':pin,'at':at[1:],'uuid':one(p,'uuid')[1]})
            continue
        role,host_pin=mapping[pin]
        h=hosts[role]
        hp=next(p for p in nodes(h,'pad') if p[1]==host_pin)
        if board_instance:
            hpos=one(h,'at')[1:3]
        else:
            # Reusable library origin is host A's datum. Existing host/grid
            # separation is 58 mm; no component bodies are moved or rescaled.
            hpos=['0','0'] if role=='A' else ['58','0']
        desired=[Decimal(hpos[i])+Decimal(one(hp,'at')[i+1])-Decimal(origin[i]) for i in range(2)]
        net=one(hp,'net')[1]
        sub=[]
        for sa,sb,sc in children(c):
            if key(sc)=='at':
                suffix=' '+str(at[3]) if len(at)>3 else ''
                sub.append((sa,sb,'(at '+' '.join(fmt(v) for v in desired)+suffix+')'))
            elif board_instance and key(sc)=='net':
                sub.append((sa,sb,'(net '+json.dumps(net)+')'))
        changed=replace(c,sub)
        if board_instance and one(p,'net') is None:
            end=changed.rfind(')')
            changed=changed[:end]+'\t(net '+json.dumps(net)+')\n\t\t'+changed[end:]
        if changed!=c:
            pad_changes.append({'footprint':prop(fp,'Reference') if board_instance else fp[1],'pin':pin,'before':at[1:3],'after':[fmt(v) for v in desired],'net':net if board_instance else None})
            edits.append((a,b,changed))
    result=replace(raw,edits)
    result=re.sub(r'(?m)^[ \t]+$','',result)
    pads=nodes(parse(result),'pad')
    assert len(pads)==6 and Counter(p[1] for p in pads)==Counter(mapping.keys())
    return result


edits=[]
for ref in ('BB1','BB2'):
    m,n=blocks[ref]
    raw=contacts(m[0],True)
    for role,host in hosts.items():raw=set_field(raw,'Wire.Host.'+role,one(host,'uuid')[1])
    edits.append((m.start(),m.end(),raw))

# Restore only missing project-owned termination selections from the prior
# recorded migration, after checking UUID, terminal ID and current AWG.
provenance=json.loads((PROJECT/'reviews/footprint_terminations_2026-10-08/provenance.json').read_text())
sch=parse((WORK/'before/powermatic_1200.kicad_sch').read_text())
symbols={prop(s,'Reference'):s for s in nodes(sch,'symbol')}
restored=[]
for ref in ('K1','K2','K4','K5','K6'):
    m,n=blocks[ref]
    pad_ids={p[1] for p in nodes(n,'pad')}
    sizes={e['pin']:e for e in json.loads(prop(symbols[ref],'Wire.Sizes'))['entries']}
    additions=[]
    for row in provenance:
        if row['reference']!=ref:continue
        assert row['footprint_uuid']==one(n,'uuid')[1]
        assert row['pin'] in pad_ids
        field='Termination.'+row['pin']
        if prop(n,field) is not None:continue
        gauge=re.search(r'\b(\d+)\s*AWG\b',row['termination'])
        if gauge:
            assert int(gauge[1])==sizes[row['pin']]['awg'],(ref,row)
        else:
            assert sizes[row['pin']]['scope']=='direct_mount',row
        value=row['termination']
        additions.append('\t\t(property '+json.dumps(field)+' '+json.dumps(value,ensure_ascii=False)+' (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))')
        restored.append({**row,'checked_current_AWG':sizes[row['pin']].get('awg')})
    assert len(additions)==len(pad_ids)
    raw=m[0]
    end=raw.rfind('\t)')
    assert end>0
    raw=raw[:end]+'\n'.join(additions)+'\n'+raw[end:]
    edits.append((m.start(),m.end(),raw))

s2m,s2=blocks['S2']
assert prop(s2,'Wire.RetainedLinks') is None
retained={'schema':1,'pairs':[['1T','3T'],['3T','5T']]}
for pin in ['1T','3T']:
    assert prop(s2,'Termination.'+pin)=='Retained jumper'
    entry=next(e for e in json.loads(prop(s2,'Wire.Sizes'))['entries'] if e['pin']==pin)
    assert entry['scope']=='retained_link' and '1T-3T and 3T-5T' in entry['note']
retained_raw=s2m[0]
end=retained_raw.rfind('\t)')
retained_field='\t\t(property "Wire.RetainedLinks" '+json.dumps(json.dumps(retained,separators=(',',':')))+' (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))\n'
edits.append((s2m.start(),s2m.end(),retained_raw[:end]+retained_field+retained_raw[end:]))
result=replace(board,edits)
# The existing three-arm S2 traces describe a feed/jumper join off the actual
# screw. Terminate both wires at the already-connected nearest screw, removing
# the short shared spur. No electrical endpoints, nets, widths or layers change.
route_fixes=[{'net':'DIRECTION_ENABLE','point':['384','607'],'target':['391.25','607.035141'],'terminal':'S2.2B','remove':'69f785cf-adf9-4426-9f73-41cf1151ef5b','redirect':['435b4950-5220-4897-8d1e-c80b495a4f26','f7d91ee3-8082-44a2-9134-0b447bc5b6f9']},
             {'net':'CONTROL_OVERLOAD_ENABLE','point':['442.483245','648.516755'],'target':['434.75','648.516755'],'terminal':'S2.3T','remove':'20b775d2-4793-4149-a3d6-b96b88f8cb61','redirect':['36ef7de5-331d-4a2e-a734-ad2723e28778','433063e8-743b-47ad-a681-48d9269170d4']}]
route_edits=[]
seen=set()
for a,b,c in children(result):
    if key(c)!='segment':continue
    n=parse(c);ident=one(n,'uuid')[1]
    for fix in route_fixes:
        if ident==fix['remove']:
            assert result[a-1]=='\t' and result[b]=='\n'
            route_edits.append((a-1,b+1,''));seen.add(ident)
        elif ident in fix['redirect']:
            assert one(n,'net')[1]==fix['net']
            sub=[]
            for sa,sb,sc in children(c):
                if key(sc) not in ('start','end'):continue
                value=parse(sc)
                if [Decimal(v) for v in value[1:]]==[Decimal(v) for v in fix['point']]:
                    sub.append((sa,sb,'('+value[0]+' '+' '.join(fix['target'])+')'))
            assert len(sub)==1,(ident,sub)
            route_edits.append((a,b,replace(c,sub)));seen.add(ident)
assert len(seen)==6
(WORK/'after/powermatic_1200.kicad_pcb').write_text(replace(result,route_edits))
for piece in ('TOP','BOT'):
    name='HMX1-BBREV_'+piece+'.kicad_mod'
    (WORK/'after'/name).write_text(contacts((WORK/'before'/name).read_text(),False))
manifest={'bindings':{ref:{role:{'reference':host_refs[role],'uuid':one(host,'uuid')[1]} for role,host in hosts.items()} for ref in ('BB1','BB2')},'removed_duplicate_targets':removed,'logical_pad_changes':pad_changes,'termination_fields_restored':restored,'contactor_placements_changed':False,'busbar_global_artwork_changed':False,'S2_terminal_join_repairs':route_fixes,'S2_retained_links':retained,'other_tracks_changed':False,'existing_host_origin_spacing_mm':58,'notes':['Logical contact targets match the saved HMC grid pads; physical busbar fit is not newly qualified.','BB2 origin changes from Y=130.0625 to the host datum Y=130. Its graphics and fields translate +0.0625 mm locally, preserving their global board positions. The six logical pads move down 0.0625 mm to the host terminals.','Current shared footprints and descriptions are made consistent with the existing 58 mm logical routing target span.','Missing contactor terminations restored from recorded selections after matching the current footprint UUIDs, pad IDs and Wire.Sizes AWG.','Two existing S2 off-terminal branches are moved onto S2.2B and S2.3T, preserving their nets and terminal endpoint relationships.','The installed S2 links 1T-3T and 3T-5T are explicitly retained hardware; the required 2B-4B jumper remains a scheduled new wire.']}
(WORK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Staged BB1/BB2 bindings to K1/K2, six unique contacts per half, exact host-pad targets, and',len(restored),'verified missing contactor termination fields.')
