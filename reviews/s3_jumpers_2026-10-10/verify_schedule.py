"""Native routing fixture: saved S3 plus its three external conductors.

Run with KiCad's bundled Python and the snapshot directory as the argument.
This exercises actual pad geometry and the existing schedule/coverage code.
"""
from pathlib import Path
import csv
import json
import sys
import xml.etree.ElementTree as E

import pcbnew

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'tools/wiring'))
sys.path.insert(0, str(PROJECT.parents[1] / 'bom_review'))
from source import footprint_metadata, one, prop
from model import Schematic
from traces import rows_from_traces
from generate import coverage
from native_kicad_tracks import read

WORK = Path(sys.argv[1])
netlist = E.parse(WORK / 'before/netlist.xml')
pin_nets = {(v.attrib['ref'], v.attrib['pin']):n.attrib['name']
            for n in netlist.findall('./nets/net') for v in n.findall('node')}
schematic = Schematic((WORK/'before/powermatic_1200.kicad_sch').read_text(), allow_in_progress=True)
results = {}

for state in ('before','after'):
    source = pcbnew.LoadBoard(str(WORK/state/'powermatic_1200.kicad_pcb'))
    saved = next(f for f in source.GetFootprints() if f.GetReference() == 'S3')
    board = pcbnew.BOARD()
    fp = pcbnew.Cast_to_FOOTPRINT(saved.Duplicate(False))
    board.Add(fp)
    fp.SetOrientationDegrees(0)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(90), pcbnew.FromMM(95)))
    nets = {}
    pads = {p.GetNumber():p for p in fp.Pads()}
    for p in pads.values():
        name = pin_nets['S3',p.GetNumber()]
        if name not in nets:
            nets[name] = pcbnew.NETINFO_ITEM(board, name)
            board.Add(nets[name])
        p.SetNet(nets[name])
    test_pin_nets = dict(pin_nets)
    for i,pin in enumerate(('1B','1T','2T'),1):
        source_pad = pads[pin]
        ref = 'EXT'+str(i)
        target = pcbnew.FOOTPRINT(board)
        board.Add(target)
        target.SetReference(ref)
        target.SetValue('External control conductor')
        target.SetField('Part Name','Control wire destination')
        target.SetField('Termination.1','Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm')
        target.SetField('Wire.AWG.1','16')
        position = source_pad.GetPosition() + pcbnew.VECTOR2I(pcbnew.FromMM(60),0)
        target.SetPosition(position)
        p = pcbnew.PAD(target)
        p.SetNumber('1')
        p.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        p.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(3),pcbnew.FromMM(3)))
        p.SetDrillSize(pcbnew.VECTOR2I(pcbnew.FromMM(2),pcbnew.FromMM(2)))
        p.SetLayerSet(pcbnew.LSET.AllCuMask())
        p.SetPosition(position)
        p.SetNet(nets[source_pad.GetNetname()])
        target.Add(p)
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(source_pad.GetPosition())
        track.SetEnd(position)
        track.SetLayer(pcbnew.F_Cu)
        track.SetWidth(pcbnew.FromMM(1.29))
        track.SetNet(nets[source_pad.GetNetname()])
        board.Add(track)
        test_pin_nets[ref,'1'] = source_pad.GetNetname()
    path = WORK/state/'s3-routing-fixture.kicad_pcb'
    pcbnew.SaveBoard(str(path), board)
    geometry = read(path)
    geometry['internal_groups'] = []
    for footprint in footprint_metadata(path.read_text()):
        if prop(footprint,'Reference') != 'S3': continue
        groups = one(footprint,'jumper_pad_groups')
        for group in groups[1:] if groups else []:
            geometry['internal_groups'].append([['S3',pin] for pin in group])
    rows,details,warnings = rows_from_traces(geometry,schematic,test_pin_nets)
    assert len(rows) == 3, (state,rows,warnings)
    assert not warnings, warnings
    assert all(row[4] == '16' for row in rows)
    assert all(detail['from'].split('.')[0] != detail['to'].split('.')[0] for detail in details)
    fixture_nets = {}
    for pad in geometry['pads']:
        fixture_nets.setdefault(pad['net'],[]).append((pad['ref'],pad['pin']))
    audit = coverage(schematic,fixture_nets,details,geometry['internal_groups'])
    with (WORK/state/'s3-fixture-wires.csv').open('w',newline='') as f:
        csv.writer(f).writerows(rows)
    results[state] = {'wire_rows':rows,'row_count':len(rows),'warnings':warnings,
                      'jumper_groups':geometry['internal_groups'],'coverage':audit}

assert results['before']['wire_rows'] == results['after']['wire_rows']
assert all(n['covered'] for n in results['after']['coverage'])
assert sum(not n['covered'] for n in results['before']['coverage']) == 6
(WORK/'schedule_fixture_validation.json').write_text(json.dumps(results,indent=2)+'\n')
print('Native S3 fixture: three external wire rows unchanged; seven straps add zero rows; every connected S3 net covered after grouping.')
