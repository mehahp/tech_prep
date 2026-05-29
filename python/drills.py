#!/usr/bin/env python3
"""
DRILLS — implement each function so the tests at the bottom pass.

This is the repetition engine for the Python round. Workflow:
  1. Delete a function body, replace with `pass`, and re-implement it from scratch.
  2. Run `python3 drills.py`. Red -> fix. Green -> next.
  3. Tomorrow, do it again from a blank function. Speed + fluency is the goal.

Reference solutions are filled in so the file runs out of the box; the point is
to keep blanking them out and rebuilding until it's automatic. Problems are
framed in the capacity/cost/forecasting domain you're interviewing for.
"""
from collections import defaultdict, Counter


# 1. Total cost per region.  rows: [{"region","cost"}]  -> {region: total}
def cost_per_region(rows):
    agg = defaultdict(float)
    for r in rows:
        agg[r["region"]] += r["cost"]
    return dict(agg)


# 2. Average cpu_util per server.  rows: [{"server","cpu"}] -> {server: avg}
def avg_cpu_per_server(rows):
    total = defaultdict(float)
    count = defaultdict(int)
    for r in rows:
        total[r["server"]] += r["cpu"]
        count[r["server"]] += 1
    return {s: round(total[s] / count[s], 3) for s in total}


# 3. Underutilized servers: avg cpu below threshold. Return sorted list of ids.
def underutilized(rows, threshold):
    avg = avg_cpu_per_server(rows)
    return sorted(s for s, c in avg.items() if c < threshold)


# 4. Day-over-day change. series: list of (date, value) sorted by date.
#    Return list of (date, delta) where delta vs previous day (first -> None).
def day_over_day(series):
    out = []
    prev = None
    for d, v in sorted(series):
        out.append((d, None if prev is None else round(v - prev, 3)))
        prev = v
    return out


# 5. Top-N most expensive servers. rows: [{"server","cost"}] aggregated already.
#    Return list of server ids, highest cost first, length n.
def top_n_expensive(rows, n):
    return [r["server"] for r in sorted(rows, key=lambda r: r["cost"], reverse=True)[:n]]


# 6. Detect anomalies: days where value > mean + k*std (simple z-score gate).
#    Return list of (date, value). values is list of (date, value).
def anomalies(series, k=2.0):
    vals = [v for _, v in series]
    n = len(vals)
    if n == 0:
        return []
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / n
    std = var ** 0.5
    if std == 0:
        return []
    return [(d, v) for d, v in series if v > mean + k * std]


# 7. Forecast next value via simple moving average of the last `window` points.
def sma_forecast(values, window):
    if not values:
        return None
    w = values[-window:]
    return round(sum(w) / len(w), 3)


# 8. Bin servers into utilization buckets: 'idle'<0.2, 'normal'<0.8, else 'hot'.
#    rows: [{"server","cpu"}] (already averaged). Return {bucket: count}.
def utilization_buckets(rows):
    counts = Counter()
    for r in rows:
        c = r["cpu"]
        bucket = "idle" if c < 0.2 else ("hot" if c >= 0.8 else "normal")
        counts[bucket] += 1
    return dict(counts)


# 9. Join usage to cost by (server, date); return total cost per server but only
#    counting days where cpu < 0.2 (wasted spend).
#    usage:[{"server","date","cpu"}] cost:[{"server","date","cost"}]
def wasted_spend(usage, cost):
    cost_idx = {(c["server"], c["date"]): c["cost"] for c in cost}
    waste = defaultdict(float)
    for u in usage:
        if u["cpu"] < 0.2:
            waste[u["server"]] += cost_idx.get((u["server"], u["date"]), 0.0)
    return dict(waste)


# 10. Longest streak of consecutive days a server was 'hot' (cpu>0.7).
#     series: list of (date_index_int, cpu) sorted by date_index. Return int.
def longest_hot_streak(series, threshold=0.7):
    best = cur = 0
    prev_idx = None
    for idx, cpu in sorted(series):
        if cpu > threshold:
            if prev_idx is not None and idx == prev_idx + 1:
                cur += 1
            else:
                cur = 1
            best = max(best, cur)
            prev_idx = idx
        else:
            cur = 0
            prev_idx = idx
    return best


# ---------------------------------------------------------------- tests ------
def _test():
    rows = [{"region": "us", "cost": 10.0}, {"region": "us", "cost": 5.0},
            {"region": "eu", "cost": 7.0}]
    assert cost_per_region(rows) == {"us": 15.0, "eu": 7.0}

    u = [{"server": 1, "cpu": 0.4}, {"server": 1, "cpu": 0.6},
         {"server": 2, "cpu": 0.1}]
    assert avg_cpu_per_server(u) == {1: 0.5, 2: 0.1}
    assert underutilized(u, 0.2) == [2]

    s = [("2025-01-01", 100), ("2025-01-02", 130), ("2025-01-03", 120)]
    assert day_over_day(s) == [("2025-01-01", None), ("2025-01-02", 30),
                               ("2025-01-03", -10)]

    cr = [{"server": 1, "cost": 50}, {"server": 2, "cost": 90},
          {"server": 3, "cost": 10}]
    assert top_n_expensive(cr, 2) == [2, 1]

    a = [("d1", 10), ("d2", 11), ("d3", 9), ("d4", 50)]
    assert anomalies(a, k=1.5) == [("d4", 50)]

    assert sma_forecast([2, 4, 6, 8], 2) == 7.0
    assert sma_forecast([], 3) is None

    bk = [{"server": 1, "cpu": 0.1}, {"server": 2, "cpu": 0.5},
          {"server": 3, "cpu": 0.9}]
    assert utilization_buckets(bk) == {"idle": 1, "normal": 1, "hot": 1}

    usage = [{"server": 1, "date": "d1", "cpu": 0.1},
             {"server": 1, "date": "d2", "cpu": 0.5}]
    cost = [{"server": 1, "date": "d1", "cost": 20.0},
            {"server": 1, "date": "d2", "cost": 25.0}]
    assert wasted_spend(usage, cost) == {1: 20.0}

    hot = [(1, 0.8), (2, 0.9), (3, 0.5), (4, 0.8), (5, 0.85), (6, 0.9)]
    assert longest_hot_streak(hot) == 3

    print("drills.py: all tests passed ✔")


if __name__ == "__main__":
    _test()
