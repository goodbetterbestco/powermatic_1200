import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
from model import Schematic, Panel, atomic_write, change_fields, digest, make_rows
from source import parse, nodes, children, key


def schematic():
    return '''(kicad_sch (version 20250114)
      (lib_symbols (symbol "Test:Pair" (symbol "Pair_1_1"
        (pin passive line (at 0 10.16 270) (length 0) (name "TERM") (number "1"))
        (pin passive line (at 0 -10.16 90) (length 0) (name "TERM") (number "2")))))
      (wire (pts (xy 20 0) (xy 40 0)) (stroke (width 0) (type default)) (uuid "wire"))
      (symbol (lib_id "Test:Pair") (at 100 130 0) (unit 1)
        (property "Reference" "TB1") (property "Value" "KN-T12GRY-25") (uuid "source"))
      (symbol (lib_id "Test:Pair") (at 200 307 0) (unit 1)
        (property "Reference" "F1") (property "Value" "Fuse") (uuid "target")))'''


def board():
    devices = '''(footprint "Test:Pair" (at 100 130) (property "Reference" "TB1")
                   (pad "1" thru_hole circle (at 0 -7.65)) (pad "2" thru_hole circle (at 0 7.65)))
                 (footprint "Test:Pair" (at 200 307) (property "Reference" "F1")
                   (pad "1" thru_hole circle (at 0 -20)) (pad "2" thru_hole circle (at 0 20)))'''
    def duct(at):
        return f'''(footprint "Controls:T1-1530G1-1_400mm_Front" (at {at})
            (property "Reference" "REF**")
            (fp_line (start 0 -20) (end 400 -20))
            (fp_line (start 0 20) (end 400 20)))'''
    return '(kicad_pcb ' + devices + ''.join(duct(at) for at in ['10 52', '10 207', '10 412', '430 432 90']) + ')'


def record(**changes):
    r = {'id': 'W001', 'schema': 1, 'section': 'Test', 'kind': 'wire', 'review': 'pending',
         'from_endpoint': {'symbol_uuid': 'source', 'pin': '1'},
         'to': {'symbol_uuid': 'target', 'pin': '1'}, 'awg': '18', 'term1': 'ferrule', 'term2': 'ring',
         'length': {'mode': 'manual', 'mm': '00450'}}
    r.update(changes)
    return r


class WiringTests(unittest.TestCase):
    def setUp(self):
        self.sch = Schematic(schematic())
        self.panel = Panel(board())
        self.nets = {('TB1', '1'): 'NET', ('F1', '1'): 'NET'}

    def test_persistent_endpoint_follows_renumbering(self):
        renamed = Schematic(schematic().replace('"F1"', '"F9"'))
        self.assertEqual(renamed.resolve(record()['to'])[1:], ('F9', '1'))

    def test_copied_symbol_does_not_duplicate_original_wire_records(self):
        payload = dict(record(), from_pin='1', from_symbol_uuid='source')
        payload.pop('id'); payload.pop('from_endpoint')
        text = change_fields(schematic(), {'source': {'Wire.W001': json.dumps(payload)}})
        original = next(raw for _, _, raw in children(text) if key(raw) == 'symbol' and '"source"' in raw)
        copied = original.replace('"TB1"', '"TB9"').replace('"source"', '"copy"', 1)
        sc = Schematic(text[:-1] + copied + ')')
        self.assertEqual(len(sc.records()), 1)
        self.assertEqual(sc.copied_wire_fields[0]['id'], 'W001')

    def test_unfinished_symbol_export_uses_temporary_name_only(self):
        text = schematic().replace('"F1"', '"F?"')
        sc = Schematic(text, allow_in_progress=True)
        snapshot, aliases = sc.export_snapshot()
        self.assertIn('"F?"', sc.text)
        self.assertNotIn('"F?"', snapshot)
        self.assertEqual(len(aliases), 1)

    def test_deleted_symbol_and_renumbered_pin_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'deleted/replaced'):
            self.sch.resolve({'symbol_uuid': 'missing', 'pin': '1'})
        with self.assertRaisesRegex(ValueError, 'has no pin'):
            self.sch.resolve({'symbol_uuid': 'target', 'pin': '999'})

    def test_wrong_net_cannot_generate_a_wire(self):
        with self.assertRaisesRegex(ValueError, 'not on one connected net'):
            make_rows(self.sch, self.panel, [record()], {('TB1', '1'): 'A', ('F1', '1'): 'B'})

    def test_wrong_terminal_clamp_is_rejected_even_on_same_net(self):
        wire = '(wire (pts (xy 100 140.16) (xy 200 296.84)) (stroke (width 0) (type default)) (uuid "other-port"))'
        sch = Schematic(schematic()[:-1] + wire + ')')
        with self.assertRaisesRegex(ValueError, 'drawn wire'):
            make_rows(sch, self.panel, [record()], {('TB1', '1'): 'NET', ('TB1', '2'): 'NET', ('F1', '1'): 'NET'})

    def test_duplicate_wire_pairs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate wire'):
            make_rows(self.sch, self.panel, [record(), record(id='W002')], self.nets)

    def test_factory_bridge_and_plug_cable_are_not_assembly_rows(self):
        for kind in ['factory', 'bridge', 'internal', 'plug_cable']:
            rows, details = make_rows(self.sch, self.panel, [record(kind=kind)], self.nets)
            self.assertEqual(rows, [])
            self.assertFalse(details[0]['exported'])

    def test_manual_length_preserves_user_text(self):
        rows, _ = make_rows(self.sch, self.panel, [record()], self.nets)
        self.assertEqual(rows[0][5], '00450')

    def test_nan_manual_length_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'manual length'):
            make_rows(self.sch, self.panel, [record(length={'mode': 'manual', 'mm': 'nan'})], self.nets)

    def test_auto_route_uses_whole_centers_between_different_ducts(self):
        rows, details = make_rows(self.sch, self.panel, [record(length={'mode': 'auto'})], self.nets)
        points = details[0]['route_points']
        self.assertIn([430.0, 52.0], points)
        self.assertIn([430.0, 207.0], points)
        self.assertEqual(float(rows[0][5]) % 50, 0)
        self.assertGreaterEqual(float(rows[0][5]), details[0]['route_mm'] + 200)

    def test_same_duct_avoids_vertical_trunk(self):
        source = self.panel.endpoint('TB1', '2')
        target = self.panel.endpoint('F1', '1')
        _, points = self.panel.route(source, target)
        self.assertFalse(any(p[0] == 430 for p in points))

    def test_missing_footprint_pad_is_not_silently_aliased(self):
        with self.assertRaisesRegex(ValueError, 'pad .* missing'):
            self.panel.endpoint('F1', '3_BOT')

    def test_bottom_gland_uses_closest_vertical_open_end(self):
        gland = '(footprint "Controls:Controls_BottomWall" (at 435 485) (property "Reference" "J5") (pad "1" thru_hole circle (at 0 -8)))'
        panel = Panel(board()[:-1] + gland + ')')
        source = panel.endpoint('J5', '1')
        self.assertFalse(source['duct']['horizontal'])
        self.assertEqual(source['approach'][-1], (430.0, 432.0))
        length, points = panel.route(source, panel.endpoint('F1', '1'))
        self.assertGreater(length, 0)
        self.assertIn((430.0, 207.0), points)

    def test_property_update_preserves_wiring_and_all_other_properties(self):
        text = schematic()
        payload = dict(record())
        payload.pop('id'); payload.pop('from_endpoint')
        payload['from_pin'] = '1'
        changed = change_fields(text, {'source': {'Wire.W001': json.dumps(payload)}})
        self.assertEqual(nodes(parse(changed), 'wire'), nodes(parse(text), 'wire'))
        self.assertEqual(Schematic(changed).records()[0]['to'], payload['to'])
        clean = parse(changed)
        for s in nodes(clean, 'symbol'):
            s[:] = [v for v in s if not (isinstance(v, list) and v[:2] == ['property', 'Wire.W001'])]
        self.assertEqual(clean, parse(text))

    def test_external_save_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as work:
            p = Path(work) / 'test.sch'
            p.write_bytes(b'user changes')
            with self.assertRaisesRegex(ValueError, 'changed'):
                atomic_write(p, b'replacement', expected=digest(b'older file'))
            self.assertEqual(p.read_bytes(), b'user changes')


if __name__ == '__main__':
    unittest.main()
