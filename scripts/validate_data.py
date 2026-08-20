from datetime import date
def validate(rows):
    if not rows:raise ValueError("empty")
    seen=set()
    for r in rows:
        if r["draw"] in seen:raise ValueError("duplicate draw")
        seen.add(r["draw"]);n=r["numbers"]
        if len(n)!=6 or len(set(n))!=6 or n!=sorted(n) or not all(1<=x<=43 for x in n):raise ValueError(f"bad numbers {r['draw']}")
        if not 1<=r["bonus"]<=43 or r["bonus"] in n:raise ValueError(f"bad bonus {r['draw']}")
        date.fromisoformat(r["date"])
    miss=[x for x in range(min(seen),max(seen)+1) if x not in seen]
    if miss:raise ValueError(f"missing draws {miss[:20]}")
