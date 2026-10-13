import json, random, sys, unittest
from decimal import Decimal
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "src"))
from order_rules.reference import replay, current, revenue

def fixture(name):
    return [json.loads(s) for s in (BASE / "fixtures" / name).read_text().splitlines()]

class OrderContractTests(unittest.TestCase):
    def setUp(self): self.events = fixture("orders_001.json")
    def test_initial_expected_state(self):
        s=replay(self.events)
        self.assertEqual(set(current(s)), {"O100", "O300"})
        self.assertEqual(s["O200"]["sequence"], 3)
        self.assertEqual(s["O999"]["op"], "D")
        self.assertEqual(revenue(s), {("2026-10-12", "IN"): (1,Decimal("120.00")), ("2026-10-12", "US"): (1,Decimal("50.00"))})
    def test_replay_idempotency(self):
        self.assertEqual(replay(self.events), replay(self.events * 3))
    def test_arrival_order_independence(self):
        expected=replay(self.events); rng=random.Random(317)
        for _ in range(200):
            rows=list(self.events);rng.shuffle(rows)
            self.assertEqual(replay(rows), expected)
    def test_corrections_remove_old_group(self):
        s=replay(self.events+fixture("orders_002.json"))
        self.assertEqual(set(current(s)), {"O100"})
        self.assertEqual(revenue(s), {("2026-10-12", "IN"): (1,Decimal("130.00"))})
    def test_event_identity_conflict(self):
        bad=dict(self.events[0],amount="999.00")
        with self.assertRaises(ValueError): replay(self.events+[bad])
    def test_sequence_conflict(self):
        bad=dict(self.events[0],event_id="OTHER",amount="999.00")
        with self.assertRaises(ValueError): replay(self.events+[bad])
    def test_delete_does_not_need_amount(self):
        self.assertEqual(replay([self.events[-1]])["O999"]["op"], "D")
    def test_delete_then_late_update(self):
        rows=[e for e in self.events if e["order_id"]=="O200"]
        self.assertNotIn("O200",current(replay(list(reversed(rows)))))
    def test_all_deleted(self):
        deletes=[dict(e,event_id="D"+e["event_id"],sequence=str(int(e["sequence"])+100),op="D") for e in self.events]
        self.assertEqual(revenue(replay(self.events+deletes)), {})
    def test_invalid_records(self):
        for change in ({"amount":"-1"},{"amount":"NaN"},{"amount":"1.005"},{"amount":"1e2"},{"sequence":"9223372036854775808"},{"event_time":"2026-10-12T01:00:00"},{"event_id":""},{"sequence":"bad"},{"op":"X"},{"event_time":"bad"},{"region":None},{"_rescued_data":"{}"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                replay([dict(self.events[0],**change)])
    def test_empty_source(self): self.assertEqual(replay([]), {})
    def test_utc_group_boundary(self):
        e=dict(self.events[0],event_time="2026-10-12T00:15:00+05:30")
        self.assertEqual(list(revenue(replay([e])))[0][0],"2026-10-11")
if __name__=="__main__": unittest.main()
