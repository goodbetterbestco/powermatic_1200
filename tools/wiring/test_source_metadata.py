import unittest
from source import footprint_metadata,parse,nodes


class FootprintMetadataTests(unittest.TestCase):
    def check_metadata(self,text):
        expected=nodes(parse(text),'footprint');actual=footprint_metadata(text)
        self.assertEqual(len(actual),len(expected))
        for a,b in zip(actual,expected):
            for key in ['uuid','property','jumper_pad_groups']:
                self.assertEqual(nodes(a,key),nodes(b,key))
        return actual

    def test_native_serialization_ignores_dense_artwork_and_preserves_fields(self):
        text='''(kicad_pcb
\t(footprint "F"
\t\t(property "Reference" "TB1"
\t\t\t(effects (font (size 1 1)))
\t\t)
\t\t(uuid "fp")
\t\t(jumper_pad_groups ("1" "2"))
\t\t(fp_line
\t\t\t(start 0 0) (end 10 10)
\t\t\t(uuid "drawing")
\t\t)
\t)
)'''
        actual=self.check_metadata(text)
        self.assertEqual(nodes(actual[0],'fp_line'),[])

    def test_non_native_formatting_falls_back_to_full_parser(self):
        self.check_metadata('(kicad_pcb (footprint "F" (uuid "fp") (property "Reference" "TB1") (jumper_pad_groups ("1" "2"))))')

    def test_quoted_parentheses_in_metadata_are_preserved(self):
        self.check_metadata('(kicad_pcb\n\t(footprint "F"\n\t\t(uuid "fp")\n\t\t(property "Description" "(quoted) text")\n\t)\n)')
