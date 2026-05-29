# tech_prep — 7-Day Interview Curriculum

Prep for a **45-minute full-stack technical interview** (coding + data + systems
design) for a **Sr. ML Optimization Engineer (iCloud capacity/cost/forecasting)**
role at Apple. The role is open to strong junior candidates who show potential.

A previous employee hinted the test will lean on **SQL** (most likely) or Python,
specifically: **joins, aggregations, window functions, and CTEs**. This curriculum
is weighted accordingly.

> Your stated goal: *enough fluency and confidence to think out loud and
> communicate clearly under time pressure.* That is a **repetition** goal, not a
> "solve 300 problems" goal. This plan is built around drilling a small set of
> patterns until they are automatic.

---

## How this repo is organized

```
tech_prep/
├── README.md                  ← you are here (master plan)
├── cheatsheets/
│   ├── sql_patterns.md        ← THE daily-repeat file (SQL syntax + patterns)
│   ├── python_patterns.md     ← daily-repeat file (Python syntax + patterns)
│   └── communication.md       ← how to talk through a problem in 45 min
├── sql/
│   ├── build_db.py            ← builds prep.db (run once)
│   ├── query.py               ← run ad-hoc SQL:  python3 query.py "SELECT ..."
│   ├── schema.md              ← the data model you'll practice against
│   ├── problems.md            ← 30 graded SQL problems
│   └── solutions.sql          ← solutions (peek only after attempting)
├── python/
│   ├── patterns.py            ← runnable reference implementations
│   ├── problems.md            ← coding problems w/ test cases
│   └── drills.py              ← runnable drills + assert-based tests
├── systems_design/
│   ├── framework.md           ← a repeatable 45-min design framework
│   └── worked_example.md      ← capacity-planning system, fully worked
└── week_plan/
    ├── day1_sql_foundations.md
    ├── day2_aggregations.md
    ├── day3_window_functions.md
    ├── day4_ctes_and_combos.md
    ├── day5_python_coding.md
    ├── day6_systems_design.md
    └── day7_mock_and_review.md
```

---

## Setup (do this first, ~1 minute)

```bash
cd sql
python3 build_db.py          # creates sql/prep.db with a cloud-infra dataset
python3 query.py "SELECT name FROM sqlite_master WHERE type='table';"
```

Then run any query two ways:

```bash
# one-off:
python3 query.py "SELECT * FROM servers LIMIT 5;"

# from a file:
python3 query.py myscratch.sql
```

No external services needed — it's local SQLite, which supports CTEs and window
functions just like Postgres for everything you'll be drilling.

---

## The week at a glance

| Day | Focus | Why |
|-----|-------|-----|
| 1 | **SQL foundations**: SELECT/WHERE/JOIN | Joins are explicitly called out; everything builds on these |
| 2 | **Aggregations**: GROUP BY / HAVING / conditional agg | Called out; the bread and butter of data questions |
| 3 | **Window functions**: rank, lag/lead, running totals, moving avg | Called out; separates strong candidates from average ones |
| 4 | **CTEs + combining everything** | Called out; how you structure a hard query readably |
| 5 | **Python coding** | The "or Python" backup; also the algorithmic-thinking signal |
| 6 | **Systems design** | The "systems" leg; framed around forecasting/capacity |
| 7 | **Timed mock + spaced review** | Consolidate; rehearse the 45-min format |

---

## Daily rhythm (≈90–120 min/day)

Repetition is the whole point. Every day, regardless of the topic:

1. **Warm-up (10 min)** — re-type yesterday's cheatsheet patterns *from memory*,
   then check. Typing the syntax beats reading it.
2. **New material (20 min)** — read that day's `week_plan/dayN_*.md`.
3. **Drills (45–60 min)** — solve the day's problems *out loud*, narrating as if
   an interviewer is watching. Write the query/code, run it, check it.
4. **Spaced repetition (15 min)** — redo **2 problems from a previous day** with
   no notes. If you can't, that pattern goes on tomorrow's warm-up.
5. **Reflect (5 min)** — note the one pattern that tripped you up.

Mantra: **don't move on until you can write the pattern from a blank screen.**

---

## What to actually master (the short list)

If you only internalize these, you'll be in good shape:

**SQL**
- The 4 join types and when each changes row counts
- `GROUP BY` + `HAVING` vs `WHERE` (pre- vs post-aggregation)
- Conditional aggregation: `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`
- Window basics: `OVER (PARTITION BY ... ORDER BY ...)`
- `ROW_NUMBER / RANK / DENSE_RANK` for "top-N-per-group"
- `LAG / LEAD` for period-over-period change
- Running totals & moving averages via window frames
- CTEs (`WITH`) to break a problem into named steps; recursive CTE basics

**Python**
- Dict / `Counter` / `defaultdict` for grouping & frequency
- Two-pointer & sliding window
- Hash-map lookups (the "one-pass" trick)
- Sorting with `key=` and the difference vs `sorted`
- Reading/grouping tabular data without pandas, and with pandas `groupby`

**Communication**
- Restate → clarify → examples/edge cases → approach → code → test → complexity
- Think out loud; narrate tradeoffs even when you pick the obvious option

See `cheatsheets/communication.md` for the script.

---

## Start here

Run setup above, then open `week_plan/day1_sql_foundations.md`.
