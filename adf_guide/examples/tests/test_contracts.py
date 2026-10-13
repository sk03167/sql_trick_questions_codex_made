import json,random,shutil,sys,tempfile,unittest
from pathlib import Path
from decimal import Decimal
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B))
from reference_rules import batch_prefix,summarize_csv,verify_copy,commit_changes,live_keys
class FileAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.source=Path(self.tmp.name)/'source';self.sink=Path(self.tmp.name)/'sink'
        self.source.mkdir();self.sink.mkdir();self.names=['orders_001.csv','orders_002.csv']
        for name in self.names:
            shutil.copy(B/'fixtures'/name,self.source/name);shutil.copy(self.source/name,self.sink/name)
    def test_expected_fixture(self):
        self.assertEqual(verify_copy(self.source,self.sink,self.names),{'records':3,'revenue':{'IN':Decimal('145.00'),'US':Decimal('50.00')}})
    def test_same_batch_path(self):
        self.assertEqual(batch_prefix('landing/orders','orders-20261012-001'),'landing/orders/batch=orders-20261012-001')
        self.assertEqual(batch_prefix('landing/orders','orders-20261012-001'),batch_prefix('landing/orders','orders-20261012-001'))
    def test_batch_path_injection(self):
        for root,batch in [('landing/orders','../bad'),('../private','ok'),('/absolute','ok'),('landing','')]:
            with self.subTest(root=root,batch=batch),self.assertRaises(ValueError):batch_prefix(root,batch)
    def test_missing_copy_file(self):
        (self.sink/self.names[1]).unlink()
        with self.assertRaises(ValueError):verify_copy(self.source,self.sink,self.names)
    def test_extra_partial_file(self):
        (self.sink/'partial.tmp').write_text('partial')
        with self.assertRaises(ValueError):verify_copy(self.source,self.sink,self.names)
    def test_corruption(self):
        (self.sink/self.names[0]).write_text('damaged')
        with self.assertRaises(ValueError):verify_copy(self.source,self.sink,self.names)
    def test_duplicate_expected_file(self):
        with self.assertRaises(ValueError):verify_copy(self.source,self.sink,self.names+self.names[:1])
    def test_nested_path_escape(self):
        with self.assertRaises(ValueError):verify_copy(self.source,self.sink,['../secret'])
    def test_duplicate_business_id(self):
        p=self.sink/'duplicates.csv';p.write_text('order_id,amount,region\nO100,1.00,IN\nO100,1.00,IN\n')
        with self.assertRaises(ValueError):summarize_csv([p])
    def test_fractional_cents(self):
        p=self.sink/'bad.csv';p.write_text('order_id,amount,region\nO100,1.005,IN\n')
        with self.assertRaises(ValueError):summarize_csv([p])
    def test_wrong_schema(self):
        p=self.sink/'bad.csv';p.write_text('amount,order_id,region\n1.00,O100,IN\n')
        with self.assertRaises(ValueError):summarize_csv([p])
class BoundaryAcceptance(unittest.TestCase):
    def setUp(self):self.events=[{'order_id':'A','version':1,'op':'I','amount':'100.00'},{'order_id':'A','version':3,'op':'D'},{'order_id':'A','version':2,'op':'U','amount':'120.00'},{'order_id':'B','version':4,'op':'I','amount':'50.00'}]
    def test_delete_ordering(self):
        s,w=commit_changes({},0,0,4,self.events);self.assertEqual(live_keys(s),{'B'});self.assertEqual(w,4)
    def test_arrival_order_independent(self):
        expected=commit_changes({},0,0,4,self.events);rng=random.Random(317)
        for _ in range(150):
            e=list(self.events);rng.shuffle(e);self.assertEqual(commit_changes({},0,0,4,e),expected)
    def test_duplicate_event_no_extra_effect(self):
        self.assertEqual(commit_changes({},0,0,4,self.events*3),commit_changes({},0,0,4,self.events))
    def test_stale_watermark_rejected(self):
        with self.assertRaises(ValueError):commit_changes({},4,0,4,self.events)
    def test_outside_interval(self):
        with self.assertRaises(ValueError):commit_changes({},0,0,3,self.events)
    def test_conflicting_sequence(self):
        with self.assertRaises(ValueError):commit_changes({},0,0,4,self.events+[dict(self.events[0],amount='999.00')])
    def test_failure_keeps_input_state(self):
        state={'Z':{'order_id':'Z','version':0,'op':'I','amount':'1.00'}};before=json.dumps(state,sort_keys=True)
        with self.assertRaises(ValueError):commit_changes(state,0,0,4,self.events+[{'order_id':'X','version':9,'op':'I'}])
        self.assertEqual(json.dumps(state,sort_keys=True),before)
    def test_empty_interval(self):self.assertEqual(commit_changes({},4,4,4,[]),({},4))
    def test_unseen_delete_retained(self):
        s,w=commit_changes({},0,0,1,[{'order_id':'X','version':1,'op':'D'}]);self.assertEqual(live_keys(s),set());self.assertEqual(s['X']['version'],1)
    def test_late_update_cannot_resurrect(self):
        state={'A':{'order_id':'A','version':3,'op':'D'}}
        s,w=commit_changes(state,0,0,2,[{'order_id':'A','version':2,'op':'U','amount':'10.00'}]);self.assertEqual(live_keys(s),set())
if __name__=='__main__':unittest.main()
