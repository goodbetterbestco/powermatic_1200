import json
from unittest.mock import patch
import unittest

from model import change_fields
from sizes import FIELD, color_for, inspect
from test_wiring import schematic


class SizeValidationTests(unittest.TestCase):
    def candidate(self, source_awg=18, source_scope='panel_control', source_net='NET', owner='source'):
        updates = {}
        for sid, awg, scope, net in [
            ('source', source_awg, source_scope, source_net),
            ('target', 16, 'controls_conduit', 'NET'),
        ]:
            updates[sid] = {FIELD: json.dumps({
                'schema': 1, 'owner_uuid': owner if sid == 'source' else sid,
                'entries': [{'pin': '1', 'net': net, 'scope': scope, 'awg': awg}],
            })}
        return change_fields(schematic(), updates)

    def inspect(self, text):
        with patch('sizes.export_netlist', return_value=(
            {'NET': {('TB1', '1'), ('F1', '1')}},
            {('TB1', '1'): 'NET', ('F1', '1'): 'NET'},
        )):
            return inspect(text)

    def test_same_net_can_have_different_panel_and_external_sizes(self):
        report = self.inspect(self.candidate())
        self.assertTrue(report['complete_connection_sizing'])
        self.assertEqual({r['awg'] for r in report['entries']}, {16, 18})
        self.assertFalse(report['physical_wire_schedule_complete'])

    def test_missing_assignment_is_reported_without_inventing_a_default(self):
        text = change_fields(self.candidate(), {'target': {FIELD: None}})
        report = self.inspect(text)
        self.assertFalse(report['complete_connection_sizing'])
        self.assertEqual(report['missing'], ['F1.1'])

    def test_copied_fields_cannot_attach_to_another_symbol(self):
        with self.assertRaisesRegex(ValueError, 'copied'):
            self.inspect(self.candidate(owner='original-other-symbol'))

    def test_stale_net_declaration_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'differs from native'):
            self.inspect(self.candidate(source_net='OLD_NET'))

    def test_fixed_connections_do_not_get_a_guessed_awg(self):
        with self.assertRaisesRegex(ValueError, 'invented gauge'):
            self.inspect(self.candidate(source_scope='suppressor_lead'))
        report = self.inspect(self.candidate(source_scope='suppressor_lead', source_awg=None))
        self.assertTrue(report['complete_connection_sizing'])

    def test_invalid_awg_is_rejected(self):
        for awg in [0, 41, '18', None]:
            with self.subTest(awg=awg), self.assertRaisesRegex(ValueError, 'integer AWG'):
                self.inspect(self.candidate(source_awg=awg))

    def test_motor_pe_keeps_pe_color_in_motor_run(self):
        self.assertEqual(color_for('motor_conduit', 'PE'), 'Green/Yellow')
        self.assertEqual(color_for('motor_conduit', 'T1'), 'Black')

    def test_factory_leads_keep_pin_specific_colors(self):
        self.assertEqual([color_for('factory_pigtail', str(p)) for p in range(1, 5)],
                         ['Brown', 'White', 'Blue', 'Black'])
        self.assertIsNone(color_for('incoming_cable', 'X'))


if __name__ == '__main__':
    unittest.main()
