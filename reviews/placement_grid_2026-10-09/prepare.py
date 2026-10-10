"""Stage a 462 mm backplate and whole-mm enclosure/device placement."""
from pathlib import Path
from decimal import Decimal
import sys,re,json,hashlib,shutil

PROJECT=Path('/Users/evanthayer/Projects/_hardware/powermatic_1200')
PARTS=Path('/Users/evanthayer/Projects/_parts')
WORK=Path('/private/tmp/powermatic-placement-grid')
sys.path.insert(0,str(PROJECT/'tools/wiring'))
from source import parse,nodes,one,prop,children,key,replace,FOOTPRINT_BLOCK

BASE='EN4SD20208GY_Open_Front'
VARIANT=BASE+'_Grid1mm'
XY=re.compile(r'\((at|start|end|mid|center|xy)\s+(-?[\d.]+)\s+(-?[\d.]+)')
def fmt(v):return format(Decimal(str(v)).quantize(Decimal('.000001')).normalize(),'f')
def shift(raw,dx,dy):
    return XY.sub(lambda m:'('+m[1]+' '+fmt(Decimal(m[2])+Decimal(str(dx)))+' '+fmt(Decimal(m[3])+Decimal(str(dy))),raw)

def enclosure(raw):
    edits=[]
    for a,b,c in children(raw):
        kind=key(c);new=c
        if kind.startswith('fp_') or kind=='property':new=shift(c,.241,-.241)
        elif kind=='model':
            assert re.search(r'\(offset\s+\(xyz\s+0\s+0\s+0\)',c)
            new=re.sub(r'\(offset\s+\(xyz\s+0\s+0\s+0\)','(offset (xyz 0.241 0.241 0)',c)
        elif kind=='descr':
            new='(descr '+json.dumps('Hammond EN4SD20208GY 508 x 508 mm enclosure routing view; centered around a 462 x 462 mm backplate. Origin at backplate lower-left, enclosure faces at local X=-23/485 and Y=-485/23. Source STEP dimensions unchanged; translated 0.241 mm in model X/Y for grid alignment.')+')'
        if new!=c:edits.append((a,b,new))
    raw=replace(raw,edits)
    return raw.replace('"'+BASE+'"','"'+VARIANT+'"',1) if raw.lstrip().startswith('(footprint "'+BASE+'"') else raw.replace('"Controls:'+BASE+'"','"Controls:'+VARIANT+'"',1)

source=(WORK/'before/powermatic_1200.kicad_pcb').read_text()
edits=[];placements=[];edge_changes=[]
positions={'J2':(57,485),'J4':(385,485),'J5':(435,485),'SW1':(-23,130),'H1':(-23,52),'H2':(-23,207),'J1':(-23,308)}
for m in FOOTPRINT_BLOCK.finditer(source):
    n=parse(m[0]);ref=prop(n,'Reference');new=m[0]
    if n[1]=='Controls:'+BASE:
        assert one(n,'at')[1:]==['0','462']
        new=enclosure(m[0])
        placements.append({'ref':'enclosure','old_id':n[1],'new_id':'Controls:'+VARIANT,'origin':[0,462],'drawing_delta':[.241,-.241]})
    elif ref in positions:
        changes=[]
        for a,b,c in children(m[0]):
            if key(c)=='at':changes.append((a,b,'(at %d %d)' % positions[ref]))
        assert len(changes)==1
        new=replace(m[0],changes)
        placements.append({'ref':ref,'before':one(n,'at')[1:],'after':positions[ref]})
    if new!=m[0]:edits.append((m.start(),m.end(),new))

for a,b,c in children(source):
    kind=key(c)
    if not kind.startswith('gr_'):continue
    n=parse(c)
    if one(n,'layer')[1]!='Edge.Cuts':continue
    # Grow the long spans; translate corner features as rigid groups so their
    # hole radii, notch shape and distances from the nearest edges are retained.
    def expand(m):
        x,y=Decimal(m[2]),Decimal(m[3])
        if x>Decimal('230.759'):x+=Decimal('.482')
        if y<Decimal('231.241'):y-=Decimal('.482')
        return '('+m[1]+' '+fmt(x)+' '+fmt(y)
    new=XY.sub(expand,c)
    if new!=c:edits.append((a,b,new));edge_changes.append(one(n,'uuid')[1])

assert len(placements)==8
assert 0 < len(edge_changes) <= 32
(WORK/'after/powermatic_1200.kicad_pcb').write_text(replace(source,edits))
for ext in ('kicad_sch','kicad_pro'):shutil.copy2(WORK/('before/powermatic_1200.'+ext),WORK/('after/powermatic_1200.'+ext))
lib=PARTS/'footprints/Controls.pretty'/(BASE+'.kicad_mod')
raw=lib.read_text();candidate=enclosure(raw)
(WORK/'footprints/Controls.pretty'/(VARIANT+'.kicad_mod')).write_text(candidate)
manifest={'backplate_mm':[462,462],'enclosure_mm':[508,508],'enclosure_corners':[[-23,-23],[485,-23],[485,485],[-23,485]],'border_mm':23,'placements':placements,'edge_cuts_modified_uuids':edge_changes,'library_source':str(lib),'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'variant':VARIANT,'candidate_sha256':hashlib.sha256(candidate.encode()).hexdigest(),'notes':'Existing fuse-insert and cover mating origins retained; their mating offsets are outside the seven wall-device placement changes.'}
(WORK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared 462 mm backplate, grid enclosure variant and seven integral-origin wall devices.')
