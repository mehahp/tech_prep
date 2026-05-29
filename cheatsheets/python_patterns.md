# Python Patterns Cheatsheet — *re-type from memory daily*

The backup-language for the coding round and the substrate for any
"manipulate this data" question. Drill the data-structure idioms until they're
reflex; that's where time is lost under pressure. Runnable versions live in
`python/patterns.py` (`python3 patterns.py` runs their self-tests).

---

## 1. Collections you must reach for instantly

```python
from collections import Counter, defaultdict, deque

# frequency count
Counter("aabbbc")                  # Counter({'b':3,'a':2,'c':1})
Counter(words).most_common(3)      # top-3 [(item, count), ...]

# group-by without pandas (THE everyday pattern)
groups = defaultdict(list)
for row in rows:
    groups[row["region"]].append(row)      # region -> [rows]

# running totals per key
totals = defaultdict(int)
for r in rows:
    totals[r["region"]] += r["cost"]

# set for O(1) membership / dedup
seen = set()

# deque for O(1) pops from both ends (BFS queue, sliding window)
q = deque([start]); q.popleft(); q.append(x)
```

---

## 2. Sorting (a top source of interview wins/losses)

```python
sorted(xs)                              # new list, ascending
sorted(xs, reverse=True)
sorted(rows, key=lambda r: r["cost"])              # by one field
sorted(rows, key=lambda r: (-r["cost"], r["name"]))# cost desc, then name asc
xs.sort()                               # in place, returns None  (don't assign it!)

# stable sort means you can sort by secondary key first, then primary
```

Idiom: **top-k** → `sorted(...)[:k]` or `heapq.nlargest(k, xs, key=...)`
(`nlargest` is O(n log k), better for large n).

---

## 3. Comprehensions & unpacking

```python
[f(x) for x in xs if cond(x)]                  # list
{k: v for k, v in pairs}                        # dict
{x for x in xs}                                 # set
total = sum(r["cost"] for r in rows)            # generator (no list built)
a, b, *rest = [1, 2, 3, 4]                       # rest == [3,4]
for i, x in enumerate(xs): ...                   # index + value
for a, b in zip(xs, ys): ...                     # pairwise
```

---

## 4. The four algorithm patterns that cover most coding rounds

**(a) Hash map one-pass (lookup complement / seen-before):**
```python
def two_sum(nums, target):
    seen = {}                       # value -> index
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
```

**(b) Two pointers (sorted array / pair from both ends):**
```python
def pair_sum_sorted(a, target):
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target: return (i, j)
        if s < target:  i += 1
        else:           j -= 1
    return None
```

**(c) Sliding window (longest/shortest subarray meeting a condition):**
```python
def longest_unique_substr(s):
    last = {}                       # char -> last index
    start = best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1    # shrink window past the repeat
        last[ch] = i
        best = max(best, i - start + 1)
    return best
```

**(d) Frequency / grouping (anagrams, counts, dedup):**
```python
def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)   # signature as key
    return list(groups.values())
```

Also keep handy: **BFS** on a graph/grid (deque + visited set), and a binary
search (`bisect.bisect_left`).

---

## 5. Reading tabular data (you may get a CSV/list-of-dicts, "no pandas")

```python
import csv
with open("data.csv", newline="") as f:
    rows = list(csv.DictReader(f))        # list of dict, keys = header

# aggregate: total cost per region
agg = defaultdict(float)
for r in rows:
    agg[r["region"]] += float(r["cost"])

# "SQL in Python": join + groupby + filter mentally map to:
#   join    -> build dict keyed by join column, then lookup
#   groupby -> defaultdict
#   filter  -> if-condition in the loop / comprehension
#   order   -> sorted(..., key=...)
```

**Join via dict index:**
```python
dc_region = {d["dc_id"]: d["region"] for d in data_centers}   # build index
for s in servers:
    s["region"] = dc_region.get(s["dc_id"])                    # lookup = the join
```

---

## 6. pandas (if allowed — say "I can do it in SQL, pandas, or plain Python")

```python
import pandas as pd
df = pd.read_csv("data.csv")

df[df.cost > 100]                                   # filter (WHERE)
df.groupby("region")["cost"].sum()                  # GROUP BY + SUM
df.groupby("region").agg(total=("cost","sum"),
                         n=("cost","size"))         # multiple aggs
df.merge(dc, on="dc_id", how="left")                # LEFT JOIN
df.sort_values("cost", ascending=False).head(5)     # ORDER BY ... LIMIT
df["roll7"] = df.sort_values("date").groupby("server")["cpu"] \
               .transform(lambda s: s.rolling(7).mean())   # window / moving avg
df.pivot_table(index="user", columns="month", values="amt", aggfunc="sum")
```
Map each pandas op to its SQL equivalent out loud — interviewers love that you
see the equivalence.

---

## 7. Complexity vocabulary (state it for every solution)
- dict/set lookup & insert: **O(1)** average
- sort: **O(n log n)**
- nested loop over pairs: **O(n²)** — name it, then try to beat it with a hash map
- sliding window / two pointers: **O(n)** time, **O(1)**–O(k) space

## 8. Tiny correctness habits
- Handle empty input and single element first.
- Watch integer vs float division (`/` float, `//` floor).
- Don't mutate a list while iterating it.
- `dict.get(k, default)` instead of `KeyError`.
- Return type matches what's asked (index vs value, list vs set).
