import csv
from pathlib import Path
import tempfile
import unittest

from model import change_fields
from source import parse
from terminations import legacy_endpoint, populate, regauge, review
from test_wiring import schematic


class TerminationTests(unittest.TestCase):
    def test_legacy_pin_names_resolve_to_current_pin_ids(self):
        cases = {
            ('Mains Plug', 'PE'): ('J2', 'G'),
            ('Mains Plug', 'L1'): ('J2', 'X'),
            ('Contactor K1', 'COIL A2 BOT'): ('K1', 'A2.BOT'),
            ('Contactor K2', 'L1 TOP (1)'): ('K2', '1'),
            ('Contactor K4', 'NO44 RIGHT BOT'): ('K4', '44'),
            ('Overload OL1', '2 BOT'): ('OL4', '2'),
            ('Overload OL2', '96 BOT'): ('OL6', '96'),
            ('Drum Switch', '1U'): ('S3', '1T'),
            ('Drum Switch', '1.U'): ('S3', '1T'),
            ('Drum Switch', '1L'): ('S3', '1B'),
            ('Drum Switch', '1.L'): ('S3', '1B'),
            ('S3', '1T'): ('S3', '1T'),
            ('S3', '1B'): ('S3', '1B'),
            ('Coil Enable Relay', 'A1+ TOP'): ('K3', 'A1+'),
            ('DC Supply', '3_BOT'): ('PS1', '3_BOT'),
            ('Button Station', 'R5'): ('S2', '5T'),
            ('Button Station', 'L2'): ('S2', '2B'),
            ('S2', '1B'): ('S2', '1B'),
        }
        for args, expected in cases.items():
            with self.subTest(args=args):
                self.assertEqual(legacy_endpoint(*args), expected)

    def test_regauge_preserves_twin_count_length_and_stud_dimensions(self):
        self.assertEqual(regauge('Twin ferrule 2 × 18 AWG; L=TBD mm', 16),
                         'Twin ferrule 2 × 16 AWG; L=TBD mm')
        self.assertEqual(regauge('Ring 16 AWG; ID=M4; OD=TBD mm', 12),
                         'Ring 12 AWG; ID=M4; OD=TBD mm')

    def test_population_covers_every_pin_and_preserves_existing_fields(self):
        text = change_fields(schematic(), {'source': {'Termination.1': 'User-selected termination'}})
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'records.csv'
            with path.open('w', newline='') as stream:
                csv.writer(stream).writerow(['FROM', 'FROM PIN', 'TO', 'TO PIN', 'AWG',
                                            'LENGTH', 'TERM 1', 'TERM 2'])
            candidate, provenance = populate(text, path)
        result = review(candidate)
        self.assertEqual(result['pin_fields'], 4)
        self.assertEqual(next(e['termination'] for e in result['entries']
                              if e['reference'] == 'TB1' and e['pin'] == '1'),
                         'User-selected termination')
        def strip(tree):
            return [[v for v in n if not(isinstance(v, list) and v[0] == 'property'
                        and v[1].startswith('Termination.'))]
                    if isinstance(n, list) and n[0] == 'symbol' else n for n in tree]
        self.assertEqual(strip(parse(text)), strip(parse(candidate)))


if __name__ == '__main__':
    unittest.main()
