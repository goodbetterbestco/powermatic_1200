import unittest
from presentation import pin_label,termination_code


class SchedulePresentationTests(unittest.TestCase):
    def test_pin_aliases_and_compound_numbers_preserve_identity(self):
        self.assertEqual(pin_label({'ref':'PS1','pin':'1_BOT','fields':{'Wire.PinLabel.1_BOT':'PE'}}),'PS1_PE')
        self.assertEqual(pin_label({'ref':'FH1','pin':'P2.A','fields':{'Wire.PinLabel.P2.A':'P2A'}}),'FH1_P2A')
        self.assertEqual(pin_label({'ref':'K1','pin':'A1.TOP','fields':{}}),'K1_A1_TOP')
        self.assertEqual(pin_label({'ref':'TB43','pin':'2','fields':{}}),'TB43_2')

    def test_compact_codes_preserve_type_size_length_and_twin_count(self):
        cases=[('Ferrule; L=10 mm','18','F18_10mm'),
               ('Twin ferrule 2 × 18 AWG; L=TBD mm','18','F2x18_TBDmm'),
               ('Ring terminal, 14 AWG; stud=#10-32; OD<=9 mm','14','R14_1032_9mm'),
               ('Bare stranded copper, 18 AWG; strip=5 mm','18','B18_5mm'),
               ('Plug clamp, 12 AWG','12','B12'),
               ('Factory pigtail, 22 AWG (retained)','22','supplier'),
               ('Single ferrule; L=10 mm','','FTBD_10mm')]
        for text,awg,expected in cases:
            with self.subTest(text=text):self.assertEqual(termination_code(text,awg),expected)

    def test_nonwire_endpoint_is_not_falsely_assigned_a_termination(self):
        self.assertEqual(termination_code('Supplied fork-ended lead (retained)','18'),'supplier')
        self.assertEqual(termination_code('N/A — cable pass-through; no electrical termination','14'),'')
        with self.assertRaisesRegex(ValueError,'Assign an F/R/B termination'):
            termination_code('Unassigned termination with a note','18')
