# Day 4 — CTEs & Combining Everything

**Goal:** use `WITH` to structure multi-step queries readably, and combine
joins + aggregation + windows into one coherent answer. CTEs were called out
explicitly. This is also the day your SQL starts to *look senior*.

### Warm-up (10 min)
From blank: the moving-average window, the `LAG` delta, and the top-N-per-group
CTE from Day 3. Check against solutions.

### Learn (20 min)
Read `cheatsheets/sql_patterns.md` sections **4 (CTEs)**, **5 (dates)**, **6 (other
patterns)**. Internalize:
- CTEs = named steps; build each on the last; reads top-to-bottom.
- **Why aggregate in a CTE before a window** (right grain first; can't filter on a
  window result without nesting).
- Recursive CTE = anchor `UNION ALL` recursive-step; used for a **date spine** to
  fill missing days with `COALESCE(…,0)`.
- De-dup / find-duplicates idioms.

### Drills (60 min) — `sql/problems.md` Block D, **Q25–Q30**
- **Q25** CTE + compare to an aggregate-of-aggregates (above-average DCs).
- **Q26** efficiency metric (cost per million requests) — role-relevant phrasing.
- **Q27** week-over-week growth: bucket → aggregate → `LAG` % change. The full stack.
- **Q28** MTTR: conditional agg + date math + open-count in one query.
- **Q29** "current run-rate": join chain + filter to latest date. Real analyst work.
- **Q30** recursive CTE date spine + LEFT JOIN + COALESCE. Do this one slowly; it's
  the time-series-completeness trick forecasting teams care about.

### Spaced repetition (15 min)
Redo **Q22 (Day 3)** and **Q14 (Day 2)** cold.

### Reflect (5 min)
Pick the single hardest query you wrote today and explain, out loud, what each CTE
does and why it's ordered that way. That narration *is* the interview skill.

**Done when:** you can decompose a gnarly request into 2–3 CTEs on the fly and say
why each stage exists.
