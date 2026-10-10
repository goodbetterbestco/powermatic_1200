import copy,json,unittest
from assemblies import supplied_assemblies
from model import Schematic
from source import parse
from traces import rows_from_traces
from test_traces import route_board
from test_wiring import schematic

class AssemblyTests(unittest.TestCase):
    def fixture(self):
        board=route_board();board['internal_groups']=[]
        for p in board['pads']:p['footprint_id']=p['id']
        m={'schema':1,'pads':{'A':['A','1'],'B':['B','1']}}
        fields={'Wire.SuppliedAssembly':'busbar'}
        for pin,host in [('A',board['pads'][0]),('B',board['pads'][1])]:
            board['pads'].append({'id':'supplier-'+pin,'footprint_id':'supplier','ref':'BB1','pin':pin,
                'net':'NET','at':host['at'][:],'fields':fields.copy(),
                'termination':'Supplied assembly connection (retained)'})
            board['contacts'].append({'track':'s','pad':'supplier-'+pin,'point':host['at'][:]})
        footprint=parse('(footprint (uuid "supplier") (property "Reference" "BB1") '
            '(property "MPN" "HMX1-BBREV") (property "Wire.SuppliedAssembly" "busbar") '
            '(property "Wire.Host.A" "A") (property "Wire.Host.B" "B") '
            '(property "Wire.MatingPads" '+json.dumps(json.dumps(m))+') (jumper_pad_groups (A B)))')
        return board,footprint,{('TB1','1'):'NET',('F1','1'):'NET'}
    def test_native_jumper_bridges_omit_loose_wire_and_keep_coverage(self):
        board,fp,nets=self.fixture();assemblies=supplied_assemblies(board,[fp],nets)
        self.assertEqual(board['internal_groups'],[[['TB1','1'],['F1','1']]])
        self.assertEqual(len(assemblies),1)
        rows,details,warnings=rows_from_traces(board,Schematic(schematic()),nets)
        self.assertEqual(rows,[]);self.assertFalse(details[0]['exported']);self.assertEqual(details[0]['kind'],'factory')
        self.assertEqual(warnings,[])
    def test_stale_host_identity_and_net_are_rejected(self):
        for change in ['host','net','position']:
            board,fp,nets=self.fixture()
            if change=='host':next(x for x in fp if isinstance(x,list) and x[:2]==['property','Wire.Host.A'])[2]='missing'
            elif change=='net':board['pads'][2]['net']='OTHER'
            else:board['pads'][2]['at']=[.1,0]
            with self.assertRaises(ValueError):supplied_assemblies(board,[fp],nets)
    def test_different_net_native_group_is_rejected_even_with_matching_contacts(self):
        board,fp,nets=self.fixture();board['pads'][1]['net']=board['pads'][3]['net']='OTHER';nets['F1','1']='OTHER'
        with self.assertRaisesRegex(ValueError,'joins different'):supplied_assemblies(board,[fp],nets)
    def test_incomplete_native_jumper_group_is_rejected(self):
        board,fp,nets=self.fixture();fp[-1]=['jumper_pad_groups',['A']]
        with self.assertRaisesRegex(ValueError,'cover each'):supplied_assemblies(board,[fp],nets)
    def test_separate_kit_piece_can_have_zero_additional_purchase_quantity(self):
        board,fp,nets=self.fixture()
        fp.append(['property','Wire.PurchaseQuantity','0'])
        fp.append(['property','Wire.KitID','HMX1-BBREV_K1_K2'])
        fp.append(['property','PartID','HMX1-BBREV_BOT'])
        result=supplied_assemblies(board,[fp],nets)[0]
        self.assertEqual(result['quantity'],0)
        self.assertEqual(result['kit_id'],'HMX1-BBREV_K1_K2')
        self.assertEqual(result['piece'],'HMX1-BBREV_BOT')
        self.assertEqual(len(result['connections']),1)
    def test_supplier_bridge_does_not_make_an_external_wire_a_twin_ferrule(self):
        board,fp,nets=self.fixture()
        board['pads'].append({'id':'external','footprint_id':'external','ref':'TB2','pin':'1',
            'at':[0,10],'fields':{},'net':'NET','termination':'Ferrule 18 AWG; L=10 mm'})
        board['tracks'].append({'id':'external-wire','kind':'segment','start':[0,0],'end':[0,10],
            'layer':'F.Cu','net':'NET','length_mm':10})
        board['contacts'] += [{'track':'external-wire','pad':'A','point':[0,0]},
            {'track':'external-wire','pad':'supplier-A','point':[0,0]},
            {'track':'external-wire','pad':'external','point':[0,10]}]
        supplied_assemblies(board,[fp],nets)
        rows,details,warnings=rows_from_traces(board,Schematic(schematic()),nets)
        self.assertEqual(len(rows),1)
        self.assertIn('F18_TBDmm',rows[0][6:])
        self.assertFalse(any(term.startswith('F2x') for term in rows[0][6:]))
        self.assertEqual(warnings,[])
