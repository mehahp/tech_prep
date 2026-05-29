# Python Coding Problems + Test Cases

The interview is "most likely SQL," so Python is your backup and your
algorithmic-thinking signal. Don't over-invest — get fluent with the patterns in
`patterns.py`/`drills.py`, then do these. Narrate every solution (see
`cheatsheets/communication.md`).

For each: write the function, then run the listed test cases. `drills.py` already
has an assert harness you can extend.

---

## Tier 1 — must be automatic (data wrangling, role-relevant)

**P1. group_by_sum(rows, key, value)** — GROUP BY + SUM over list-of-dicts.
- `[{"r":"us","c":10},{"r":"us","c":5},{"r":"eu","c":7}], "r","c"` → `{"us":15,"eu":7}`
- `[]` → `{}`
- Edge: missing key should error clearly (or you decide to skip — state it).

**P2. left_join(left, right, on)** — enrich left rows with right's columns.
- left has a key with no match → keep the row, no extra fields.
- right has duplicate keys → which wins? (Decide + say it. Last-wins is simplest.)

**P3. moving_average(series, window)** — trailing average of (date, value).
- `[("d1",2),("d2",4),("d3",6)], 2` → `[("d1",2.0),("d2",3.0),("d3",5.0)]`
- `window=1` → unchanged values. Empty → `[]`.

**P4. top_n_per_group(rows, group_key, metric_key, n)** — the window pattern.
- Ties at the boundary: keep first-encountered (stable) or all? State it.
- `n` larger than a group → return whole group.

**P5. day_over_day(series)** — delta vs previous day.
- First element delta is `None`. Single element → `[(d, None)]`. Empty → `[]`.

---

## Tier 2 — classic algorithms (the "can you think" check)

**P6. two_sum(nums, target)** → indices. Test: `[2,7,11,15],9`→`[0,1]`;
`[3,3],6`→`[0,1]`; no solution → `None`. State O(n) hash-map approach vs O(n²).

**P7. longest_unique_substr(s)** → length. `"abcabcbb"`→3, `"bbbb"`→1, `""`→0,
`"pwwkew"`→3. Explain the sliding window + why `start` only moves forward.

**P8. group_anagrams(words)**. `["eat","tea","tan","nat","bat"]` →
`[["eat","tea"],["tan","nat"],["bat"]]` (order-independent). Key = sorted chars.

**P9. merge_intervals(intervals)** — merge overlapping `[start,end]`.
- `[[1,3],[2,6],[8,10]]` → `[[1,6],[8,10]]`. Sort by start first.
- Useful framing: "consolidating overlapping maintenance windows."

**P10. binary_search(a, target)** → index or -1. Test boundaries: first, last,
absent, empty. Be careful with `lo<=hi` and `mid` update (off-by-one is the trap).

---

## Tier 3 — light data-science flavor (fits the role; optional)

**P11. sma_forecast(values, window)** — predict next point as mean of last
`window`. Then discuss: how would you weight recent points more? (→ EWMA.)

**P12. anomalies(series, k)** — flag points above mean + k·std. Discuss why a
rolling/robust stat (median, MAD) is better for trending/seasonal data.

**P13. detect_seasonality_naive(series, period)** — average value per position in
the cycle (e.g., per weekday). Returns `{position: avg}`. Test on a 14-day
series with a clear weekday pattern.

**P14. cumulative(values)** — running total list. `[1,2,3]`→`[1,3,6]`. (`itertools.accumulate` exists — mention it, but also code it by hand.)

---

## How to practice these for *retention*
- Day 5: do P1–P8 once with notes, then P1–P5 again from a blank function.
- Day 7: redo P1–P5 + P6–P7 cold, timed (≤8 min each, narrating).
- Any you fail twice → add to tomorrow's warm-up. That's the whole repetition loop.

## Talking points to drop while coding
- Always state complexity (time + space) unprompted.
- Call out the edge cases you're handling *before* the interviewer asks.
- Map the problem to its SQL twin when relevant ("this is a GROUP BY", "this is
  top-N-per-group", "this is a LEFT JOIN") — shows transferable thinking.
