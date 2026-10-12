"""Generate the owner-requested illustrative 150 mm motor routing footprint.

The supplied stock illustration governs the outline, not a mounting pattern.
Run with an output directory; shared-library and project edits are staged there.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import math
import re
import shutil
import sys
import uuid

PROJECT = Path(__file__).resolve().parents[2]
PARTS = PROJECT.parents[1] / '_parts'
WORK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/private/tmp/powermatic-motor-150')
sys.path.insert(0, str(PROJECT / 'tools/wiring'))
from source import children, key, nodes, one, parse, prop, replace, FOOTPRINT_BLOCK

NAME = 'PWRM1200-MOTOR_Top_150mm'
LIBID = 'Controls:' + NAME
PACKAGE = 'Machine motor (150 mm illustrative top view)'
MOTOR_UUID = 'f758497e-4710-4fd6-9851-f0e206557c67'
SCALE = 150 / (1460 - 140)
ORIGIN = (800, 528)
POSITION = (290, 630)
SOURCE_IMAGE = Path('/Users/evanthayer/Downloads/depositphotos_650674342-stock-photo-electric-motor-top-view-illustration.jpg')
PADS = [(f'T{i+1}', x, y) for i, (x, y) in enumerate([(-10, -24), (0, -24), (10, -24), (-10, -14), (0, -14), (10, -14)])]


def fmt(v):
    return f'{v:.6f}'.rstrip('0').rstrip('.') if v else '0'


def uid(label):
    return str(uuid.uuid5(uuid.UUID(MOTOR_UUID), label))


def xy(p):
    return ' '.join(fmt((p[i] - ORIGIN[i]) * SCALE) for i in range(2))


def property_text(name, value, at=(0, 0), layer='F.Fab', hidden=True):
    return f'(property {json.dumps(name)} {json.dumps(value)} (at {fmt(at[0])} {fmt(at[1])}) (layer "{layer}")' + (' (hide yes)' if hidden else '') + f' (uuid "{uid("field:" + name)}") (effects (font (size 2.5 2.5) (thickness 0.15))))'


graphics = []


def line(a, b, layer, width):
    graphics.append(f'(fp_line (start {xy(a)}) (end {xy(b)}) (stroke (width {width}) (type default)) (layer "{layer}") (uuid "{uid("graphic:" + str(len(graphics)))}"))')


def polyline(points, layer, width):
    for a, b in zip(points, points[1:]):
        line(a, b, layer, width)


def arc(a, mid, b, layer, width):
    graphics.append(f'(fp_arc (start {xy(a)}) (mid {xy(mid)}) (end {xy(b)}) (stroke (width {width}) (type default)) (layer "{layer}") (uuid "{uid("graphic:" + str(len(graphics)))}"))')


def rect(a, b, layer, width):
    graphics.append(f'(fp_rect (start {xy(a)}) (end {xy(b)}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}") (uuid "{uid("graphic:" + str(len(graphics)))}"))')


def circle(c, radius, layer, width):
    graphics.append(f'(fp_circle (center {xy(c)}) (end {xy((c[0]+radius,c[1]))}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}") (uuid "{uid("graphic:" + str(len(graphics)))}"))')


def filled(points):
    graphics.append('(fp_poly (pts ' + ' '.join(f'(xy {xy(p)})' for p in points) + ') (stroke (width 0) (type default)) (fill solid) (layer "F.Adhes")' + f' (uuid "{uid("graphic:" + str(len(graphics)))}"))')


# Opaque motor silhouette, with the fan-cover rounded end sampled from quarter circles.
body = [(395, 288), (411, 243), (438, 226), (450, 186), (500, 160), (540, 160), (540, 145), (549, 122), (575, 110), (1100, 110), (1100, 97), (1292, 97)]
body += [(1292 + 168*math.cos(t), 265 + 168*math.sin(t)) for t in [(-math.pi/2 + i*math.pi/24) for i in range(1, 13)]]
body += [(1460, 792)]
body += [(1292 + 168*math.cos(t), 792 + 168*math.sin(t)) for t in [(i*math.pi/24) for i in range(1, 13)]]
body += [(1100, 960), (1100, 946), (575, 946), (550, 935), (540, 910), (540, 896), (500, 896), (450, 870), (438, 830), (411, 813), (395, 768)]
filled(body)
filled([(140,483),(347,483),(347,438),(395,438),(395,618),(347,618),(347,573),(140,573)])
filled([(732,928),(988,928),(988,1034),(732,1034)])

for layer, width in [('F.SilkS', .25), ('F.Fab', .1)]:
    # Shaft, drive-end bearing housing and front face.
    rect((140,483),(347,573),layer,width)
    rect((347,438),(395,618),layer,width)
    polyline([(395,438),(395,288),(411,243),(438,226),(450,186),(500,160),(540,160)],layer,width)
    polyline([(395,618),(395,768),(411,813),(438,830),(450,870),(500,896),(540,896)],layer,width)
    line((500,160),(500,896),layer,width)
    line((540,160),(540,896),layer,width)
    # Main finned body and rear fan cover, retaining the 150 mm shaft-tip/rear-cover span.
    arc((540,145),(550,120),(575,110),layer,width)
    line((575,110),(1100,110),layer,width)
    arc((540,910),(550,936),(575,946),layer,width)
    line((575,946),(1100,946),layer,width)
    polyline([(1100,110),(1100,97),(1292,97)],layer,width)
    arc((1292,97),(1410.793939,146.206061),(1460,265),layer,width)
    line((1460,265),(1460,792),layer,width)
    arc((1460,792),(1410.793939,910.793939),(1292,960),layer,width)
    polyline([(1292,960),(1100,960),(1100,110)],layer,width)
    line((1292,97),(1292,960),layer,width)
    # Cooling ribs: leave a clear upper-half reference field and logical terminal area.
    for y in [132,156,190,335,398,462,528,594,658,720,826,866,902,928]:
        if y in [156,190]:
            line((575,y),(700,y),layer,width)
            line((900,y),(1100,y),layer,width)
        elif y in [335,398]:
            line((575,y),(645,y),layer,width)
            line((955,y),(1100,y),layer,width)
        else:
            line((575,y),(1100,y),layer,width)
        sign = 1 if y < 528 else -1
        arc((540,y+sign*28),(550,y+sign*8),(575,y),layer,width)
    # End-cover screw rims and mounting foot.
    for c in [(1140,248),(1140,808)]:
        circle(c,18,layer,width)
    rect((732,928),(988,1010),layer,width)
    rect((716,1010),(1004,1025),layer,width)
    polyline([(732,1025),(732,1034),(988,1034),(988,1025)],layer,width)
    circle((860,969),25,layer,width)
    # Schematic T1-T6 targets sit inside this illustrative junction area.
    rect((645,273),(955,454),layer,width)
    if layer == 'F.Fab':
        # Fine source features remain on fabrication artwork only.
        for x in [409,419,429,438,450,460]:
            line((x,250),(x,806),layer,width)
        rect((500,242),(620,332),layer,width)
        rect((500,724),(620,814),layer,width)
        # Shaft keyway, detailed bearing and foot screw.
        line((175,516),(271,516),layer,width)
        arc((271,516),(284,528),(271,541),layer,width)
        line((271,541),(175,541),layer,width)
        arc((175,541),(162,528),(175,516),layer,width)
        circle((860,969),18,layer,width)
        for c in [(1140,248),(1140,808)]:
            circle(c,12,layer,width)

props = [property_text('Reference','REF**',(0,-33),'F.SilkS',False),property_text('Value',NAME),property_text('Description','Illustrative machine motor top elevation, 150 mm shaft tip to rear cover; six logical wiring targets T1-T6.'),property_text('Part Name','Two-Speed\nMotor'),property_text('Package',PACKAGE)]
for pin, _, _ in PADS:
    props.append(property_text('Termination.'+pin,'Bare stranded copper, 14 AWG; strip=11 mm'))
pads = [f'(pad "{pin}" thru_hole circle (at {x} {y}) (size 3 3) (drill 2) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (uuid "{uid("pad:"+pin)}"))' for pin,x,y in PADS]
raw = f'(footprint "{NAME}"\n (version 20260206) (generator "pcbnew") (generator_version "10.0") (layer "F.Cu")\n (descr "Illustrative 150 mm machine motor top elevation from the owner supplied image. Six logical T1-T6 wiring targets; not a physical PCB mounting pattern. No 3D model.")\n (tags "Controls motor machine top 150mm logical terminals")\n' + '\n'.join(' '+p for p in props+graphics+pads) + '\n (attr exclude_from_pos_files allow_missing_courtyard)\n (embedded_fonts no)\n)\n'
outlib = WORK/'footprints/Controls.pretty'
outlib.mkdir(parents=True,exist_ok=True)
(outlib/(NAME+'.kicad_mod')).write_text(raw)


def associate(raw):
    edits=[]
    for a,b,c in children(raw):
        kind=key(c)
        if kind=='on_board':
            edits.append((a,b,'(on_board yes)'))
        elif kind=='in_pos_files':
            edits.append((a,b,'(in_pos_files no)'))
        elif kind=='property' and prop(['x',parse(c)],'Footprint') is not None:
            edits.append((a,b,c.replace('(property "Footprint" ""',f'(property "Footprint" "{LIBID}"',1)))
        elif kind=='property' and prop(['x',parse(c)],'Package') is not None:
            edits.append((a,b,c.replace('(property "Package" ""',f'(property "Package" "{PACKAGE}"',1)))
    return replace(raw,edits)


symbols = (WORK/'before/Controls.kicad_sym').read_text()
edits=[]
for a,b,c in children(symbols):
    if key(c)=='symbol' and parse(c)[1]=='PWRM1200-MOTOR':
        edits.append((a,b,associate(c)))
assert len(edits)==1
(WORK/'after/Controls.kicad_sym').write_text(replace(symbols,edits))

sch = (WORK/'before/powermatic_1200.kicad_sch').read_text()
edits=[]
for a,b,c in children(sch):
    kind=key(c)
    if kind=='symbol' and one(parse(c),'uuid')==['uuid',MOTOR_UUID]:
        edits.append((a,b,associate(c)))
    elif kind=='lib_symbols':
        subedits=[]
        for sa,sb,sc in children(c):
            if parse(sc)[1] in ('Controls:PWRM1200-MOTOR', 'Controls:PWRM1200-MOTOR_1', 'PWRM1200-MOTOR_1'):
                subedits.append((sa,sb,associate(sc)))
        assert len(subedits)==1
        edits.append((a,b,replace(c,subedits)))
assert len(edits)==2
(WORK/'after/powermatic_1200.kicad_sch').write_text(replace(sch,edits))

csvtext=(WORK/'before/non_lcsc_parts.csv').read_text()
lines=csvtext.splitlines(keepends=True)
reader=csv.DictReader(io.StringIO(csvtext))
last=reader.line_num
matches=[]
for row in reader:
    if row['PartID']=='PWRM1200-MOTOR':
        original=''.join(lines[last:reader.line_num])
        assert ',Controls:PWRM1200-MOTOR,,' in original
        replacement=original.replace(',Controls:PWRM1200-MOTOR,,',',Controls:PWRM1200-MOTOR,'+LIBID+',',1)
        assert ',Motor,motor,,' in replacement
        replacement=replacement.replace(',Motor,motor,,',',Motor,motor,'+PACKAGE+',',1)
        matches.append((sum(map(len,lines[:last])),sum(map(len,lines[:reader.line_num])),replacement))
    last=reader.line_num
assert len(matches)==1
(WORK/'after/non_lcsc_parts.csv').write_text(replace(csvtext,matches))

# Preserve the metadata footprint UUID and every termination/connector field.
board=(WORK/'before/powermatic_1200.kicad_pcb').read_text()
matches=[]
candidate=parse(raw)
for m in FOOTPRINT_BLOCK.finditer(board):
    if '\n\t\t(property "Reference" "M1"' not in m[0]:
        continue
    old=m[0]
    n=parse(old)
    assert n[1]=='M1_Termination_Metadata' and not nodes(n,'pad')
    changed=old.replace('"M1_Termination_Metadata"',json.dumps(LIBID),1)
    edits=[]
    for a,b,c in children(changed):
        kind=key(c)
        if kind=='at': edits.append((a,b,f'(at {POSITION[0]} {POSITION[1]})'))
        elif kind=='locked': edits.append((a,b,''))
        elif kind=='property':
            pn=parse(c)
            if pn[1]=='Reference':
                edits.append((a,b,property_text('Reference','M1',(0,-33),'F.SilkS',False).replace(uid('field:Reference'),one(pn,'uuid')[1])))
            elif pn[1]=='Wire.MetadataOnly': edits.append((a,b,''))
            elif pn[1]=='Datasheet': edits.append((a,b,c.replace('(property "Datasheet" ""','(property "Datasheet" "${PARTS_LIB}/reviews/Controls/evidence/motor_six_lead_map_2026-09-23.md"')))
            elif pn[1]=='Description': edits.append((a,b,c.replace('(property "Description" ""','(property "Description" "Marathon Electric six-lead motor; 220 V, 60 Hz, 1710/875 RPM, 4.4/4.0 A; leads T1-T6."')))
        elif kind=='attr': edits.append((a,b,'(attr exclude_from_pos_files allow_missing_courtyard)'))
    changed=replace(changed,edits)
    additions=[f'(path "/{MOTOR_UUID}")','(sheetname "/")','(sheetfile "powermatic_1200.kicad_sch")']
    # Preserve symbol fields for native schematic parity.
    placed=next(s for s in nodes(parse((WORK/'after/powermatic_1200.kicad_sch').read_text()),'symbol') if one(s,'uuid')==['uuid',MOTOR_UUID])
    oldnames={p[1] for p in nodes(n,'property')}
    for p in nodes(placed,'property'):
        if p[1] not in oldnames and p[1]!='Footprint':
            additions.append(property_text(p[1],p[2]))
    additions+=graphics
    for pin,x,y in PADS:
        additions.append(f'(pad "{pin}" thru_hole circle (at {x} {y}) (size 3 3) (drill 2) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "M1_{pin}") (pinfunction "{pin}") (pintype "passive") (uuid "{uid("pad:"+pin)}"))')
    changed=changed.rstrip()[:-1]+'\n\t\t'+'\n\t\t'.join(additions)+'\n\t)'
    changed=re.sub(r'(?m)^[ \t]+$', '', changed)
    matches.append((m.start(),m.end(),changed))
assert len(matches)==1
(WORK/'after/powermatic_1200.kicad_pcb').write_text(replace(board,matches))
for p in (WORK/'before').iterdir():
    if p.suffix in ('.kicad_pro', '.kicad_dru') or p.name == 'fp-lib-table':
        shutil.copy2(p, WORK/'after'/p.name)

manifest={'footprint':LIBID,'source_image':str(SOURCE_IMAGE),'image_sha256':hashlib.sha256(SOURCE_IMAGE.read_bytes()).hexdigest(),'image_reference_pixels':{'shaft_tip_x':140,'rear_cover_x':1460,'top_y':97,'foot_bottom_y':1034},'scale_mm_per_pixel':SCALE,'geometric_long_dimension_mm':150,'illustrated_height_mm':(1034-97)*SCALE,'origin_image_pixels':ORIGIN,'pcb_position_mm':POSITION,'terminal_targets':[{'pin':p,'net':'M1_'+p,'local_mm':[x,y],'pcb_mm':[POSITION[0]+x,POSITION[1]+y]} for p,x,y in PADS],'notes':['Owner-requested illustrative outline; motor maximum envelope, mounting holes and real terminal positions are not qualified by this stock image.','Exactly six numbered logical pads T1-T6; PE remains in the saved symbol and existing footprint metadata, without an extra PE pad.','No model, paste apertures or courtyard; panel-elevation exceptions apply. Existing tracks and all other footprints are preserved byte-for-byte.']}
(WORK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Staged {LIBID}: 150 mm long, {manifest["illustrated_height_mm"]:.3f} mm tall; six T1-T6 targets at {POSITION}.')
