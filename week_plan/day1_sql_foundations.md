# Day 1 — SQL Foundations: SELECT / WHERE / JOIN

**Goal:** be able to write any join from a blank screen and reason about how it
changes row counts. Joins were *explicitly* called out by your referrer.

### Setup (once)
See `HOW_TO_PRACTICE.md` for full options. Quick version:
```bash
# Postgres (recommended):
cd sql && ./setup_pg.sh
export PREP_URL=postgresql://postgres:prep@localhost:5433/prep
psql "$PREP_URL" -c "SELECT * FROM servers LIMIT 3;"

# or SQLite fallback (no install):
cd sql && python3 build_db.py
python3 query.py "SELECT * FROM servers LIMIT 3;"
```
Throughout the week, "run it" means `psql "$PREP_URL" -f myscratch.sql` (Postgres)
or `python3 query.py myscratch.sql` (SQLite).

### Warm-up (10 min)
Open `sql/schema.md`. Without looking again, draw the join map (which table
connects to which, on what key) on paper. Check it.

### Learn (20 min)
Read `cheatsheets/sql_patterns.md` sections **0 (eval order)** and **1 (joins)**.
Type each join example into your DB and watch the output. Pay attention to:
- INNER vs LEFT and what disappears.
- The two anti-join idioms (`LEFT JOIN ... IS NULL` and `NOT EXISTS`).
- The filter-in-ON vs filter-in-WHERE gotcha on a LEFT JOIN.

### Drills (60 min) — `sql/problems.md` Block A, **Q1–Q8**
Rules:
- Write each query yourself first; run it; check the row count makes sense.
- Narrate out loud: "I need servers + their DC, so I join on dc_id…"
- Only after attempting, compare with `sql/solutions.sql`.

Must-get-right concepts today:
- **Q5** (anti-join) and **Q6** (LEFT JOIN to keep zero-rows) — these separate
  people who *get* joins from people who memorized INNER.
- **Q8** — `COUNT(DISTINCT ...)` across a 3-table join.

### Spaced repetition (none yet — Day 1)
Instead: redo **Q2, Q5, Q6 from a blank screen**. If you can't, that's tomorrow's
warm-up.

### Reflect (5 min)
Write the one join idea that felt shaky. Tomorrow's warm-up starts there.

**Done when:** you can write a 3-table join and an anti-join with no reference.
