"""Stage the owner-requested panel datums and 1 mm wiring-target grid."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import sys, re, json, math, hashlib, shutil

PROJECT = Path('/Users/evanthayer/Projects/_hardware/powermatic_1200')
PARTS = Path('/Users/evanthayer/Projects/_parts')
WORK = Path('/private/tmp/powermatic-panel-datums')
sys.path.insert(0, str(PROJECT / 'tools/wiring'))
from source import parse, nodes, one, prop, children, key, replace, FOOTPRINT_BLOCK

# Point in the original footprint that becomes the new origin.
SPECS = {
    'BNSPDX-23-W_BottomWall': (0, 0, 'Y=0 is the outer panel face; X=0 is the gland axis'),
    'BNSPDX-23-W_MainsPlug_BottomWall': (0, 0, 'Y=0 is the outer panel face; X=0 is the gland axis'),
    'BSPDX-23-W_BottomWall': (0, 0, 'Y=0 is the outer panel face; X=0 is the gland axis'),
    'BSPBX-22-W_BottomWall': (0, 0, 'Y=0 is the outer panel face; X=0 is the gland axis'),
    '222102_LeftWall': (0, 0, 'X=0 is the outer panel face; Y=0 is the shaft axis'),
    'XB4BVB1_LeftWall': (-16.82571, 0, 'X=0 is the outer panel face at the bezel underside; Y=0 is the operating axis'),
    'XB4BVB4_LeftWall': (-16.82571, 0, 'X=0 is the outer panel face at the bezel underside; Y=0 is the operating axis'),
    'T4171310004-001_LeftWall': (3, 0, 'X=0 is the outer panel face at the modeled sealing-ring rear tangent; Y=0 is the connector axis'),
}
XY = re.compile(r'\((at|start|end|mid|center|xy)\s+(-?[\d.]+)\s+(-?[\d.]+)')

def fmt(x):
    return format(Decimal(str(x)).quantize(Decimal('.000001')).normalize(), 'f')

def translate(raw, dx, dy):
    if dx == 0 and dy == 0:
        return raw
    return XY.sub(lambda m: '(' + m[1] + ' ' + fmt(Decimal(m[2])+Decimal(str(dx))) + ' ' + fmt(Decimal(m[3])+Decimal(str(dy))), raw)

def whole(x):
    return int(Decimal(str(x)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def change(raw, spec, board=False):
    ox, oy, datum = spec
    dx, dy = -ox, -oy
    edits, pads = [], []
    for a,b,child in children(raw):
        kind = key(child)
        new = child
        if kind == 'pad':
            p = parse(child); at = one(p, 'at')
            before = list(map(float, at[1:3]))
            shifted = [before[0]+dx, before[1]+dy]
            target = list(map(whole, shifted))
            new = re.sub(r'\(at\s+-?[\d.]+\s+-?[\d.]+', '(at %d %d' % tuple(target), child, count=1)
            pads.append({'number':p[1], 'before':before, 'datum_relative':shifted, 'after':target,
                         'rounding_delta':[target[i]-shifted[i] for i in (0,1)]})
        elif kind.startswith('fp_') or kind == 'property':
            new = translate(child, dx, dy)
        elif kind == 'model':
            # KiCad PCB +Y is opposite the model's +Y.
            m = re.search(r'\(offset\s+\(xyz\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\)', child)
            assert m, 'Missing model translation'
            # Both lamp models share the same original axes. Match the saved
            # white lamp's height; its operating axis is 14.95 mm above model Z=0.
            root = parse(raw) if ('XB4BVB' in raw[:120]) else None
            lamp = root is not None
            height = '60.05' if lamp else m[3]
            value = '(offset (xyz %s %s %s)' % (fmt(Decimal(m[1])+Decimal(str(dx))), fmt(Decimal(m[2])-Decimal(str(dy))),height)
            new = child[:m.start()] + value + child[m.end():]
        elif kind == 'descr':
            n=parse(child)
            new='(descr '+json.dumps(n[1]+'. Panel datum: '+datum+'. Numbered wiring-target centers use the nearest integer millimetre X/Y; physical geometry is retained.')+')'
        elif board and kind == 'at':
            n=parse(child); x,y=map(float,n[1:3]); angle=float(n[3]) if len(n)>3 else 0
            assert angle == 0, 'Review rotated placement before applying'
            new='(at '+fmt(x+ox)+' '+fmt(y+oy)+(' '+n[3] if len(n)>3 else '')+')'
        if new != child: edits.append((a,b,new))
    return replace(raw, edits), pads

manifest={'library':[], 'placements':[], 'schematic':'Existing placed-symbol footprint IDs already select these same updated library files; J4 and J5 are board-only mechanical glands.'}
manifest['lamp_height']={'white_and_red_model_z_offset_mm':60.05,'operating_axis_height_above_component_plane_mm':75,'red_previous_offset_mm':0,'white_source_axis_height_mm':14.95}
lib=PARTS/'footprints/Controls.pretty'
stage=WORK/'footprints/Controls.pretty'
for name,spec in SPECS.items():
    source=(WORK/'library-before'/(name+'.kicad_mod')).read_text()
    candidate,pads=change(source,spec)
    (stage/(name+'.kicad_mod')).write_text(candidate)
    manifest['library'].append({'name':name,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
        'candidate_sha256':hashlib.sha256(candidate.encode()).hexdigest(),'old_datum_xy':spec[:2],
        'datum':spec[2],'pads':pads})

source=(WORK/'before/powermatic_1200.kicad_pcb').read_text()
edits=[]
for m in FOOTPRINT_BLOCK.finditer(source):
    raw=m[0]
    name=re.match(r'\t\(footprint "Controls:([^"]+)"',raw)
    if not name or name[1] not in SPECS:continue
    n=parse(raw);new,pads=change(raw,SPECS[name[1]],True)
    manifest['placements'].append({'reference':prop(n,'Reference'),'name':name[1],
        'before_origin':one(n,'at')[1:],'after_origin':one(parse(new),'at')[1:],'pads':pads})
    edits.append((m.start(),m.end(),new))
assert {p['reference'] for p in manifest['placements']}=={'J1','J2','J4','J5','H1','H2','SW1'}
(WORK/'after/powermatic_1200.kicad_pcb').write_text(replace(source,edits))
for ext in ('kicad_sch','kicad_pro'):
    shutil.copy2(WORK/('before/powermatic_1200.'+ext),WORK/('after/powermatic_1200.'+ext))
(WORK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Staged eight library footprints and seven board instances; %d placed wiring targets.' % sum(len(p['pads']) for p in manifest['placements']))
