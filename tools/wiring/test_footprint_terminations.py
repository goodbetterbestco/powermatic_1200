import csv
import json
from pathlib import Path
import tempfile
import unittest

from footprint_terminations import stage, review
from model import change_fields, Panel, Schematic
from source import parse, nodes, one, prop
from test_wiring import schematic, board


def linked_board():
    return (board().replace('(property "Reference" "TB1")',
                            '(uuid "source-fp") (path "/source") (property "Reference" "TB1")')
            .replace('(property "Reference" "F1")',
                     '(uuid "target-fp") (path "/target") (property "Reference" "F1")')
            .replace('(property "Reference" "REF**")',
                     '(uuid "duct") (property "Reference" "REF**")'))


class FootprintTerminationTests(unittest.TestCase):
    def run_stage(self, sch, pcb):
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'legacy.csv'
            with path.open('w', newline='') as stream:
                csv.writer(stream).writerow(['FROM', 'FROM PIN', 'TO', 'TO PIN',
                                            'AWG', 'LENGTH', 'TERM 1', 'TERM 2'])
            return stage(sch, pcb, path)

    def test_moves_fields_to_footprints_and_preserves_physical_objects(self):
        pcb = linked_board().replace('(property "Termination.1" "ferrule")', '')
        sch = change_fields(schematic(), {'source': {'Termination.1': 'Owner selection'}})
        new_sch, new_pcb, _ = self.run_stage(sch, pcb)
        self.assertIsNone(prop(Schematic(new_sch).by_uuid['source'], 'Termination.1'))
        self.assertEqual(Panel(new_pcb).termination('TB1', '1'), 'Owner selection')
        def geometry(text):
            return [[v for v in f if not (isinstance(v, list) and v[0] == 'property'
                         and (v[1].startswith('Termination.') or v[1] == 'Wire.TerminationPolicy'))]
                    for f in nodes(parse(text), 'footprint')]
        self.assertEqual(geometry(pcb), geometry(new_pcb))

    def test_conflicting_owner_fields_stop_migration(self):
        sch = change_fields(schematic(), {'source': {'Termination.1': 'Different selection'}})
        with self.assertRaisesRegex(ValueError, 'selections conflict'):
            self.run_stage(sch, linked_board())

    def test_external_metadata_owner_has_no_geometry_and_is_excluded(self):
        sch = schematic().replace('"TB1"', '"M1"')
        sch = change_fields(sch, {'source': {'Termination.1': 'Motor splice'}})
        pcb = linked_board()
        root = parse(pcb)
        # Remove the source footprint using its source span, preserving duct routing.
        from source import children, key, replace
        pcb = replace(pcb, [(a,b,'') for a,b,raw in children(pcb)
                            if key(raw)=='footprint' and prop(parse(raw),'Reference')=='TB1'])
        new_sch, new_pcb, _ = self.run_stage(sch, pcb)
        f = next(f for f in nodes(parse(new_pcb), 'footprint') if prop(f, 'Reference') == 'M1')
        self.assertEqual(nodes(f, 'pad') + nodes(f, 'model') + nodes(f, 'fp_line'), [])
        self.assertTrue({'board_only','exclude_from_pos_files','exclude_from_bom'} <= set(one(f,'attr')))
        self.assertEqual(Panel(new_pcb).termination('M1','1'), 'Motor splice')
        self.assertEqual(json.loads(prop(f,'Wire.TerminalPins')), ['1','2'])
        self.assertGreater(review(new_pcb)['pin_fields'], 0)

    def test_wire_termination_copies_are_removed_without_changing_endpoints(self):
        payload = {'schema':1, 'from_symbol_uuid':'source', 'from_pin':'1',
                   'to':{'symbol_uuid':'target','pin':'1'}, 'term1':'ferrule', 'term2':'ring'}
        sch = change_fields(schematic(), {'source': {'Wire.W001':json.dumps(payload)}})
        new_sch, _, _ = self.run_stage(sch, linked_board())
        record = Schematic(new_sch).records()[0]
        self.assertNotIn('term1', record)
        self.assertNotIn('term2', record)
        self.assertEqual(record['to'], payload['to'])


if __name__ == '__main__':
    unittest.main()
