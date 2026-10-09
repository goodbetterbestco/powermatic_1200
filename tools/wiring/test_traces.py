import json
import unittest
from model import Schematic,change_fields
from traces import rows_from_traces
from test_wiring import schematic


def route_board(awg='18'):
    fields={'Part Name':'Block','Wire.AWG.1':awg}
    pads=[{'id':'A','ref':'TB1','pin':'1','at':[0,0],'fields':fields.copy(),
           'net':'NET','termination':'Ferrule or twin ferrule as required'},
          {'id':'B','ref':'F1','pin':'1','at':[10,0],'fields':{'Part Name':'Fuse'},
           'net':'NET','termination':'Ferrule 18 AWG; L=TBD mm'}]
    return {'pads':pads,'tracks':[{'id':'s','kind':'segment','start':[0,0],'end':[10,0],
                                 'layer':'F.Cu','net':'NET','length_mm':10}],
            'contacts':[{'track':'s','pad':'A','point':[0,0]}, {'track':'s','pad':'B','point':[10,0]}]}


class TraceAdapterTests(unittest.TestCase):
    def setUp(self):
        self.sch=Schematic(schematic());self.nets={('TB1','1'):'NET',('F1','1'):'NET'}

    def test_complete_trace_adds_a_wire_without_any_wire_record(self):
        rows,details,warnings=rows_from_traces(route_board(),self.sch,self.nets)
        self.assertEqual(len(rows),1);self.assertEqual(rows[0][4:6],['18','110'])
        self.assertIn('Ferrule',rows[0][6:]);self.assertEqual(details[0]['route_mm'],10)
        self.assertEqual(warnings,[])

    def test_route_disappears_when_trace_is_removed(self):
        b=route_board();b['tracks']=[];b['contacts']=[]
        self.assertEqual(rows_from_traces(b,self.sch,self.nets)[0],[])

    def test_wrong_schematic_net_rejects_schedule(self):
        with self.assertRaisesRegex(ValueError,'endpoints/net disagree'):
            rows_from_traces(route_board(),self.sch,{('TB1','1'):'NET',('F1','1'):'OTHER'})

    def test_unassigned_board_only_block_inherits_the_connected_circuit(self):
        b=route_board();b['pads'][0]['ref']='TB40';b['pads'][0]['net']='';
        rows,_,_=rows_from_traces(b,self.sch,{('F1','1'):'NET'})
        self.assertIn(['TB40','1'],[rows[0][:2],rows[0][2:4]])

    def test_unknown_or_conflicting_gauges_remain_blank_and_are_reported(self):
        b=route_board('14')
        rows,_,warnings=rows_from_traces(b,self.sch,self.nets)
        self.assertEqual(rows[0][4],'');self.assertTrue(any('AWG conflict' in w for w in warnings))
        b=route_board();b['pads'][0]['fields'].pop('Wire.AWG.1');b['pads'][1]['termination']='Ferrule'
        rows,_,warnings=rows_from_traces(b,self.sch,self.nets)
        self.assertEqual(rows[0][4],'');self.assertTrue(any('not specified' in w for w in warnings))

    def test_unused_schematic_pin_cannot_become_a_valid_wire_silently(self):
        with self.assertRaisesRegex(ValueError,'marks this terminal unconnected'):
            rows_from_traces(route_board(),self.sch,{('TB1','1'):'NET',('F1','1'):'unconnected-X'})

    def test_legacy_stale_records_do_not_block_trace_export(self):
        payload={'schema':1,'from_pin':'1','to':{'symbol_uuid':'deleted','pin':'1'}}
        sch=Schematic(change_fields(schematic(),{'source':{'Wire.W001':json.dumps(payload)}}))
        self.assertEqual(len(rows_from_traces(route_board(),sch,self.nets)[0]),1)

    def test_length_scope_is_reported_for_a_routing_proxy(self):
        b=route_board();b['pads'][0]['fields']['Wire.LengthScope']='Panel tail only'
        rows,_,warnings=rows_from_traces(b,self.sch,self.nets)
        self.assertEqual(len(rows),1)
        self.assertIn('TB1: Panel tail only',warnings)

    def test_stale_sizing_does_not_block_wires_or_supply_an_outdated_gauge(self):
        payload={'schema':1,'owner_uuid':'source','entries':[{'pin':'1','net':'OLD','awg':14}]}
        sch=Schematic(change_fields(schematic(),{'source':{'Wire.Sizes':json.dumps(payload)}}))
        b=route_board();b['pads'][0]['fields'].pop('Wire.AWG.1');b['pads'][1]['termination']='Ferrule'
        rows,_,warnings=rows_from_traces(b,sch,self.nets)
        self.assertEqual(len(rows),1);self.assertEqual(rows[0][4],'')
        self.assertTrue(any('stale sizing net' in w for w in warnings))

    def test_current_endpoint_gauge_survives_an_unrelated_stale_sizing_field(self):
        payload={'schema':1,'owner_uuid':'target','entries':[{'pin':'2','net':'OLD','awg':14}]}
        sch=Schematic(change_fields(schematic(),{'target':{'Wire.Sizes':json.dumps(payload)}}))
        rows,_,warnings=rows_from_traces(route_board(),sch,self.nets)
        self.assertEqual(rows[0][4],'18')
        self.assertTrue(any('stale sizing net' in w for w in warnings))

    def test_gland_boundary_is_exported_with_its_actual_nontermination(self):
        b=route_board();b['pads'][0]['pass_through']=True
        b['pads'][0]['termination']='N/A — cable pass-through; no electrical termination'
        rows,details,warnings=rows_from_traces(b,self.sch,self.nets)
        self.assertEqual(len(rows),1);self.assertEqual(details[0]['kind'],'route-section')
        self.assertIn(b['pads'][0]['termination'],rows[0][6:])
        self.assertTrue(any('external run' in w for w in warnings))

    def test_common_block_net_conflicts_are_visible_without_hiding_recorded_wires(self):
        b=route_board()
        b['pads'] += [
            {'id':'C','ref':'TB1','pin':'2','at':[0,10],
             'fields':{'Wire.AWG.2':'18'},'net':'OTHER','termination':'Ferrule'},
            {'id':'D','ref':'F2','pin':'1','at':[10,10],
             'fields':{},'net':'OTHER','termination':'Ferrule'}]
        b['tracks'].append({'id':'s2','kind':'segment','start':[0,10],'end':[10,10],
                            'layer':'F.Cu','net':'OTHER','length_mm':10})
        b['contacts'] += [{'track':'s2','pad':'C','point':[0,10]},
                          {'track':'s2','pad':'D','point':[10,10]}]
        b['internal_groups']=[[['TB1','1'],['TB1','2']]]
        rows,details,warnings=rows_from_traces(b,self.sch,{**self.nets,('TB1','2'):'OTHER'})
        self.assertEqual(len(rows),2)
        self.assertTrue(any('Electrical net conflict' in w for w in warnings))
        self.assertTrue(all(d['review']=='net-conflict' for d in details))

    def test_two_routed_wires_on_one_block_clamp_use_twin_ferrules(self):
        b=route_board()
        b['pads'].append({'id':'C','ref':'TB2','pin':'TOP','at':[0,10],
                         'fields':{'Wire.AWG.TOP':'18'},'net':'NET','termination':'Ferrule or twin ferrule as required'})
        b['tracks'].append({'id':'s2','kind':'segment','start':[0,0],'end':[0,10],
                            'layer':'F.Cu','net':'NET','length_mm':10})
        b['contacts'] += [{'track':'s2','pad':'A','point':[0,0]},{'track':'s2','pad':'C','point':[0,10]}]
        rows,_,warnings=rows_from_traces(b,self.sch,self.nets)
        self.assertEqual(len(rows),2);self.assertEqual(warnings,[])
        self.assertTrue(all('Twin ferrule' in row[6:] for row in rows))


if __name__=='__main__':unittest.main()
