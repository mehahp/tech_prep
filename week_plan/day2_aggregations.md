# Day 2 — Aggregations: GROUP BY / HAVING / Conditional

**Goal:** fluent GROUP BY, crisp on WHERE-vs-HAVING, and automatic with the
`SUM(CASE WHEN …)` conditional-aggregation pattern. All called out by your referrer.

### Warm-up (10 min)
From a blank screen, re-type Day 1's join examples + whatever you flagged. Then
re-type cheatsheet section 1. Check against the file.

### Learn (20 min)
Read `cheatsheets/sql_patterns.md` section **2 (aggregation)**. Internalize:
- `WHERE` (pre-agg, on rows) vs `HAVING` (post-agg, on groups).
- `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`.
- Conditional aggregation shape — say it like a chant:
  `SUM(CASE WHEN <cond> THEN 1 ELSE 0 END)`.
- Pivot via conditional agg.

### Drills (60 min) — `sql/problems.md` Block B, **Q9–Q15**
Focus:
- **Q12** — aggregating facts up a 3-table chain to region grain. Watch the grain!
- **Q13** — `HAVING` (post-aggregation filter). Try writing it with `WHERE` first
  and see the error; that mistake cements the rule.
- **Q14** — the conditional-aggregation rep. Do it twice.
- **Q15** — date bucketing with `strftime('%Y-%m', …)`. Note the Postgres
  equivalent (`to_char` / `date_trunc`) — you may be on Postgres.

### Spaced repetition (15 min)
Redo **Q5 and Q6** from Day 1, no notes.

### Reflect (5 min)
Could you state the WHERE-vs-HAVING rule in one sentence without thinking? If not,
it's tomorrow's warm-up.

**Done when:** you can write a grouped query with conditional aggregation and a
HAVING filter, cold, and explain WHERE vs HAVING in one breath.
