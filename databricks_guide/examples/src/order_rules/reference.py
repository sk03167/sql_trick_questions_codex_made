"""Independent local oracle, not an implementation of Spark/Delta execution."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import re

def normalize(e):
    for key in ("event_id", "order_id", "sequence", "op", "event_time"):
        if e.get(key) is None or str(e[key]) == "":
            raise ValueError(f"Missing {key}")
    if not re.fullmatch(r"[0-9]+", str(e["sequence"])):
        raise ValueError("Invalid sequence")
    seq = int(e["sequence"])
    if seq > 9223372036854775807:
        raise ValueError("Sequence exceeds BIGINT")
    if e["op"] not in {"I", "U", "D"}:
        raise ValueError("Invalid op")
    ts = datetime.fromisoformat(str(e["event_time"]).replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise ValueError("Oracle requires explicit event timezone")
    ts = ts.astimezone(timezone.utc)
    amount, region = None, None
    if e["op"] != "D":
        if not re.fullmatch(r"[0-9]{1,16}(\.[0-9]{1,2})?", str(e.get("amount"))):
            raise ValueError("Amount must fit decimal(18,2) without rounding")
        try:
            amount = Decimal(str(e.get("amount")))
        except InvalidOperation as ex:
            raise ValueError("Invalid amount") from ex
        if not amount.is_finite() or amount < 0 or amount != amount.quantize(Decimal("0.01")):
            raise ValueError("Amount must be nonnegative decimal cents")
        region = e.get("region")
        if not isinstance(region, str) or not region:
            raise ValueError("Missing region")
    if e.get("_rescued_data") is not None:
        raise ValueError("Unexpected rescued data")
    return dict(event_id=str(e["event_id"]), order_id=str(e["order_id"]),
                sequence=seq, op=e["op"], event_time=ts,
                amount=amount, region=region)

def replay(events):
    ids, positions, state = {}, {}, {}
    for raw in events:
        e = normalize(raw)
        payload = tuple((k, e[k]) for k in sorted(e) if k != "event_id")
        eid, pos = e["event_id"], (e["order_id"], e["sequence"])
        if eid in ids and ids[eid] != payload:
            raise ValueError("Conflicting event ID")
        if pos in positions and positions[pos] != payload:
            raise ValueError("Conflicting per-order sequence")
        ids[eid], positions[pos] = payload, payload
        previous = state.get(e["order_id"])
        if previous is None or e["sequence"] > previous["sequence"] or (
            e["sequence"] == previous["sequence"] and e["event_id"] > previous["event_id"]):
            state[e["order_id"]] = e
    return state

def current(state):
    return {k: v for k, v in state.items() if v["op"] != "D"}

def revenue(state):
    result = {}
    for e in current(state).values():
        key = (e["event_time"].date().isoformat(), e["region"])
        count, total = result.get(key, (0, Decimal("0.00")))
        result[key] = count + 1, total + e["amount"]
    return result
