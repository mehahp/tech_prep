# Day 5 — Python Coding

**Goal:** be fluent enough in Python that if they say "do it in Python instead of
SQL," you're comfortable. Don't over-invest — SQL is the likely focus — but a
confident Python round is a strong signal.

### Warm-up (10 min)
From blank: re-type the four algorithm patterns from
`cheatsheets/python_patterns.md` section 4 (hash-map one-pass, two-pointer,
sliding window, group-by). Run `python3 python/patterns.py` to confirm.

### Learn (20 min)
Read `cheatsheets/python_patterns.md` sections 1–6. Especially:
- `Counter` / `defaultdict` for grouping & counting.
- Sorting with `key=` and tuple keys for multi-sort.
- "SQL in Python": join via dict index, groupby via defaultdict.
- The pandas ↔ SQL mapping (say each equivalence aloud).

### Drills (60 min) — `python/problems.md`
- **Tier 1 (P1–P5)**: the data-wrangling set. These mirror your SQL drills — do
  them first; they're the most role-relevant. Use `python/drills.py` as the test
  harness (functions 1–10 there cover this ground).
- **Tier 2 (P6–P8, P10)**: classic algorithms. Narrate brute force → optimized.
- Practice method: blank out a function body in `drills.py`, reimplement, run
  `python3 drills.py` until green. Repeat the ones you fumble.

### Spaced repetition (15 min)
Switch back to SQL so you don't lose it: redo **Q16 (moving avg)** and **Q22
(top-2 per region)** cold in `query.py`.

### Reflect (5 min)
For each Python solution, did you state time + space complexity unprompted? Make
that a reflex.

**Done when:** you can write `group_by_sum`, a dict-index join, a moving average,
and `two_sum` from a blank file, stating complexity for each.
