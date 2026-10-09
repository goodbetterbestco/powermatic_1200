import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).parent))
from extract import bom_rows,merge_rows,tag_rows

SCH='''(kicad_sch (lib_symbols)
(symbol (lib_id "Test:Part") (at 0 0 0) (unit 1) (uuid "s1") (in_bom yes)
 (property "Reference" "K1") (property "MPN" "0123") (property "Part Name" "Contactor")
 (property "Category" "Control") (property "BOM.COST" "2.50"))
(symbol (lib_id "Test:Part") (at 0 0 0) (unit 1) (uuid "s2") (in_bom yes)
 (property "Reference" "K2") (property "MPN" "0123") (property "Part Name" "Contactor")
 (property "Category" "Control") (property "BOM.COST" "2.50"))
(symbol (lib_id "Test:Part") (at 0 0 0) (unit 1) (uuid "s3") (in_bom no)
 (property "Reference" "J1") (property "MPN" "EXCLUDED")))'''
PCB='''(kicad_pcb
(footprint "Test:Part" (uuid "p1") (property "Reference" "K1") (property "MPN" "0123"))
(footprint "Test:Part" (uuid "p2") (property "Reference" "K2") (property "MPN" "0123"))
(footprint "Test:Block" (uuid "p3") (attr board_only) (property "Reference" "TB1")
 (property "MPN" "TB") (property "Part Name" "Block"))
(footprint "Metadata" (uuid "p4") (attr board_only exclude_from_bom)
 (property "Reference" "J1") (property "Wire.MetadataOnly" "yes"))
(footprint "Rail" (uuid "p5") (attr board_only exclude_from_bom) (property "MPN" "RAIL")))'''


class ExtractTests(unittest.TestCase):
    def test_counts_physical_parts_once_and_respects_exclusions(self):
        rows,report=bom_rows(SCH,PCB)
        self.assertEqual(len(rows),2)
        row=next(r for r in rows if 'Contactor' in r[1])
        self.assertEqual(row[2],'2');self.assertEqual(row[5:7],['2.50','5.00'])
        self.assertIn('0123',row[1])
        self.assertEqual(report['component_instances'],3)

    def test_saved_kicad_changes_flow_to_bom_and_missing_fields_stay_blank(self):
        rows,_=bom_rows(SCH.replace('Contactor','New name'),PCB)
        row=next(r for r in rows if 'New name' in r[1]);self.assertEqual(row[3:5],['',''])
        self.assertEqual(row[7:],['',''])

    def test_conflicting_linked_part_numbers_stop_extraction(self):
        with self.assertRaisesRegex(ValueError,'MPN differ'):
            bom_rows(SCH,PCB.replace('"0123"','"OTHER"',1))


class MergeTests(unittest.TestCase):
    def test_linked_rows_preserve_purchasing_quantity_and_local_rows(self):
        _,report=bom_rows(SCH,PCB)
        original=[{'TYPE':'Purchase','NAME':'Existing item','QUA':'2','PACK':'25','UNIT':'PACK',
                   'COST':'9.75','LINE':'19.50','SUPPLIER':'Chosen','SPN':'0123'},
                  {'TYPE':'Wire','NAME':'Wire spool','QUA':'1','COST':'3','SPN':'SPOOL'}]
        tagged=tag_rows(original,report['groups'])
        self.assertEqual(tagged[0]['SOURCE'],'KiCad');self.assertEqual(tagged[1]['SOURCE'],'Local')
        self.assertEqual({k:tagged[0][k] for k in original[0]},original[0])
        group=report['groups'][0];group['quantity']=29;group['explicit_bom_fields']={}
        merged,_=merge_rows(tagged,report['groups'])
        self.assertEqual(merged[0]['QUA'],'2');self.assertEqual(merged[0]['KICAD QTY'],'29')
        self.assertEqual(merged[0]['COST'],'9.75');self.assertEqual(merged[0]['LINE'],'19.50')
        self.assertEqual(merged[1],tagged[1])

    def test_removed_source_rows_are_removed_but_local_data_survives(self):
        rows=[{'SOURCE':'KiCad','SOURCE KEY':'old','NAME':'Old part'},
              {'SOURCE':'Local','NAME':'Conduit','QUA':'10'}]
        merged,removed=merge_rows(rows,[])
        self.assertEqual(merged,[rows[1]]);self.assertEqual(removed,['Old part'])

    def test_ambiguous_initial_matches_stay_local(self):
        groups=[{'key':'a','identifiers':['PN'],'names':[],'quantity':1},
                {'key':'b','identifiers':['PN'],'names':[],'quantity':1}]
        self.assertEqual(tag_rows([{'SPN':'PN','NAME':'Unclear'}],groups)[0]['SOURCE'],'Local')


if __name__=='__main__':unittest.main()
