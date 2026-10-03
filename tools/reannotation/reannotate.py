#!/usr/bin/env python3
"""Stage functional annotation without changing wires or physical placements.

Terminal identities follow the existing panel clusters via schematic UUIDs.
Their schematic instances are reordered into existing logical-group slots.
"""
from pathlib import Path
import json,sys,re,hashlib,uuid,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/cable_glands'));from sexpr import parse,one,nodes,prop
sys.path.insert(0,str(ROOT/'tools/controls_footprints/left_wall'));from install import children,key,replace
WORK=Path(sys.argv[1]);WORK.mkdir(parents=True,exist_ok=True)
PROJECT=ROOT/'kicad/powermatic_1200';SCH=PROJECT/'powermatic_1200.kicad_sch';PCB=PROJECT/'powermatic_1200.kicad_pcb'
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def fmt(v):return f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v)>1e-7 else '0'
def q(s):return json.dumps(s)
def ref_edit(n,new):
    ed=[]
    for a,b,c in children(n):
        if key(c)=='property' and parse(c)[1]=='Reference':
            ed.append((a,b,re.sub(r'^(\(property "Reference" )"[^"\n]*"',lambda m:m[1]+q(new),c,count=1)))
        elif key(c)=='instances':
            ed.append((a,b,re.sub(r'\(reference "[^"\n]*"\)','(reference '+q(new)+')',c)))
    return replace(n,ed)
def move(n,x,y):
    old=one(parse(n),'at');dx=x-float(old[1]);dy=y-float(old[2]);ed=[]
    for a,b,c in children(n):
        if key(c)=='at':ed.append((a,b,f'(at {fmt(x)} {fmt(y)} {old[3]})'))
        elif key(c)=='property':
            inner=[]
            for aa,bb,cc in children(c):
                if key(cc)=='at':
                    p=parse(cc);inner.append((aa,bb,f'(at {fmt(float(p[1])+dx)} {fmt(float(p[2])+dy)} {p[3]})'))
            ed.append((a,b,replace(c,inner)))
    return replace(n,ed)
def stage_schematic():
    source=SCH.read_text();board=PCB.read_text();s=parse(source);b=parse(board)
    instances=nodes(s,'symbol');byid={one(n,'uuid')[1]:n for n in instances};byref={prop(n,'Reference'):n for n in instances}
    tf=[f for f in nodes(b,'footprint') if (prop(f,'Reference') or '').startswith('TB')]
    upper=sorted([f for f in tf if prop(f,'Value')=='KN-T12GRY-25' and float(one(f,'at')[2])<200],key=lambda f:float(one(f,'at')[1]))
    lower=sorted([f for f in tf if prop(f,'Value')=='KN-T12GRY-25' and float(one(f,'at')[2])>200],key=lambda f:float(one(f,'at')[1]))
    grounds=sorted([f for f in tf if prop(f,'Value')=='KN-G12SP-10'],key=lambda f:float(one(f,'at')[1]))
    assert (len(upper),len(lower),len(grounds))==(18,11,6)
    netlist=ET.parse(WORK/'before.xml').getroot()
    for net in netlist.findall('nets/net'):
        if any(n.attrib['ref'].startswith('TB') for n in net.findall('node')):assert net.attrib['name'].startswith('unconnected-'), 'A terminal is already wired; move its attached wiring explicitly.'
    target_byid={};planned={};groups=[]
    allocations=[(upper[:5],range(1,6),'24V distribution',['+24V']*5),
                 (upper[5:10],range(6,11),'0V distribution',['0V']*5),
                 (upper[10:15],range(11,16),'Pendant commands',['FWD_CMD','REV_CMD','STOP_CHAIN','LOW_CMD','HIGH_CMD']),
                 (upper[15:18],range(16,19),'M12 E-stop',['+24V','J1 pins 2-3 series link','J1 pin 4 coil-enable return']),
                 (lower[5:],range(19,25),'Motor leads',[f'M1_T{i}' for i in range(1,7)]),
                 (lower[:3],range(25,28),'Incoming phases',['L1_IN','L2_IN','L3_IN']),
                 (lower[3:5],range(28,30),'Pendant supply feeds',['+24V_CTRL','+24V_RUN']),
                 (grounds,range(50,56),'Protective earth',['PE']*6)]
    for fps,seq,group,signals in allocations:
        assert len(fps)==len(seq)==len(signals)
        refs=[]
        for f,num,signal in zip(fps,seq,signals):
            sid=one(f,'path')[1].split('/')[-1];assert sid in byid;new='TB'+str(num)
            target_byid[sid]=new;planned[new]=dict(group=group,planned_net=signal);refs.append(new)
        groups.append(dict(group=group,references=refs))
    # Existing non-terminal groups are retained; the direction pair becomes K1/K2
    # and the distinct enable relay K3. All units share the physical device ref.
    device_mapping={'K2':'K3','K3':'K2'}
    mapping={};rows=[]
    for n in instances:
        sid=one(n,'uuid')[1];old=prop(n,'Reference');new=target_byid.get(sid,device_mapping.get(old,old))
        if old in mapping:assert mapping[old]==new
        mapping[old]=new
        rows.append(dict(symbol_uuid=sid,old_reference=old,new_reference=new,unit=int(one(n,'unit')[1]),value=prop(n,'Value'),**planned.get(new,{})))
    assert len(set(mapping.values()))==len(mapping),'Duplicate reference'
    ed=[]
    for a,b,n in children(source):
        if key(n)!='symbol':continue
        sid=one(parse(n),'uuid')[1];old=prop(parse(n),'Reference');new=mapping[old]
        out=ref_edit(n,new) if new!=old else n
        if sid in target_byid:
            slot=byref[new];x,y=map(float,one(slot,'at')[1:3]);out=move(out,x,y)
        if out!=n:ed.append((a,b,out))
    result=replace(source,ed)
    # Add non-electrical captions identifying the terminal groups; the user wires.
    captions=[('+24 V',193.04,95.25),('0 V',215.9,95.25),('Commands',238.76,95.25),
              ('M12 E-stop',257.81,95.25),('PE',288.29,95.25),
              ('Motor T1-T6',195.58,123.19),('Incoming phases',217.17,123.19),('CTRL / RUN',232.41,123.19)]
    text=[f'(text {q(t)} (at {fmt(x)} {fmt(y)} 0) (effects (font (size 1.27 1.27))) (uuid "{uuid.uuid4()}"))' for t,x,y in captions]
    result=result[:result.rfind(')')]+'\n'+'\n'.join(text)+'\n)\n'
    for k in ['wire','label','global_label','junction','no_connect','lib_symbols']:
        assert nodes(parse(source),k)==nodes(parse(result),k),k
    (WORK/'schematic.before.kicad_sch').write_text(source);(WORK/'board.before.kicad_pcb').write_text(board)
    (WORK/SCH.name).write_text(result)
    report=dict(schematic_before_sha256=digest(source),schematic_after_sha256=digest(result),board_before_sha256=digest(board),reference_mapping=mapping,symbols=rows,terminal_groups=groups,wires_labels_and_cached_symbols_preserved=True,terminal_wiring_added=False)
    (WORK/'annotation.json').write_text(json.dumps(report,indent=2)+'\n');print('Staged logical schematic annotation; wires and labels unchanged.')
def stage_board():
    report=json.loads((WORK/'annotation.json').read_text());source=(WORK/'board.before.kicad_pcb').read_text()
    s=parse((WORK/SCH.name).read_text());byid={one(n,'uuid')[1]:n for n in nodes(s,'symbol')}
    netlist=ET.parse(WORK/'after.xml').getroot();pin_nets={(p.attrib['ref'],p.attrib['pin']):n.attrib['name'] for n in netlist.findall('nets/net') for p in n.findall('node')}
    ed=[];names={};links=[];board_only=0
    for a,b,n in children(source):
        if key(n)!='footprint':continue
        d=parse(n);path=one(d,'path')
        if not path:board_only+=1;continue
        sid=path[1].split('/')[-1];assert sid in byid,(prop(d,'Reference'),sid)
        new=prop(byid[sid],'Reference');out=ref_edit(n,new)
        for p in nodes(d,'pad'):
            net=one(p,'net')
            if not net or net[1]=='0':continue
            expect=pin_nets.get((new,p[1]));assert expect is not None,(new,p[1])
            code=int(net[1]);assert code not in names or names[code]==expect,('Net collision',code,names.get(code),expect)
            names[code]=expect
        if out!=n:ed.append((a,b,out))
        links.append(dict(footprint_uuid=one(d,'uuid')[1],symbol_uuid=sid,old_reference=prop(d,'Reference'),new_reference=new))
    result=replace(source,ed);old=parse(source);net_ed=[]
    for a,b,n in children(result):
        if key(n)=='net':
            p=parse(n);code=int(p[1])
            if code in names and p[2]!=names[code]:net_ed.append((a,b,f'(net {code} {q(names[code])})'))
        elif key(n)=='footprint':
            pe=[]
            for aa,bb,p in children(n):
                if key(p)=='pad':
                    nn=[]
                    for aaa,bbb,nt in children(p):
                        if key(nt)=='net':
                            v=parse(nt);code=int(v[1])
                            if code in names and v[2]!=names[code]:nn.append((aaa,bbb,f'(net {code} {q(names[code])})'))
                    if nn:pe.append((aa,bb,replace(p,nn)))
            if pe:net_ed.append((a,b,replace(n,pe)))
    result=replace(result,net_ed);new=parse(result)
    oldfp={one(f,'uuid')[1]:f for f in nodes(old,'footprint')};newfp={one(f,'uuid')[1]:f for f in nodes(new,'footprint')};assert oldfp.keys()==newfp.keys()
    for uid,o in oldfp.items():
        n=newfp[uid]
        for k in ['at','path','model','fp_line','fp_poly','fp_arc','fp_rect','fp_circle','attr']:assert nodes(o,k)==nodes(n,k),(uid,k)
        op=nodes(o,'pad');np=nodes(n,'pad');assert len(op)==len(np)
        for a,b in zip(op,np):
            assert [x for x in a if not isinstance(x,list) or x[0]!='net']==[x for x in b if not isinstance(x,list) or x[0]!='net']
            if one(a,'net'):assert one(a,'net')[1]==one(b,'net')[1]
    for k in ['segment','via','zone','gr_line','gr_arc','gr_poly','gr_rect','gr_text','group']:assert nodes(old,k)==nodes(new,k),k
    (WORK/PCB.name).write_text(result);report.update(board_after_sha256=digest(result),pcb_associations=links,pcb_geometry_and_pad_net_codes_preserved=True,board_only_footprints_preserved=board_only)
    (WORK/'annotation.json').write_text(json.dumps(report,indent=2)+'\n');print('Staged matching panel references and net names; all placements and pad net codes preserved.')
if sys.argv[2]=='schematic':stage_schematic()
elif sys.argv[2]=='board':stage_board()
else:raise ValueError('Use schematic or board mode')
