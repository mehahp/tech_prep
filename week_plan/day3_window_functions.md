# Day 3 — Window Functions

**The highest-leverage day.** Window functions are explicitly called out and are
what make you look strong for a *time-series/forecasting* team. Invest here.

### Warm-up (10 min)
From blank: re-type the conditional-aggregation pattern and one HAVING query.
Then re-type cheatsheet sections 1–2. Check.

### Learn (25 min)
Read `cheatsheets/sql_patterns.md` section **3 (window functions)** slowly. The
mental model to lock in: *like GROUP BY but keeps every row and annotates it.*
- `OVER (PARTITION BY … ORDER BY … <frame>)`
- `ROW_NUMBER` vs `RANK` vs `DENSE_RANK` (ties: arbitrary / gaps / no gaps).
- `LAG` / `LEAD` for period-over-period.
- Frames: default with ORDER BY = running total; `ROWS BETWEEN n PRECEDING AND
  CURRENT ROW` = moving window. **This is the bit people forget.**
- The **top-N-per-group** recipe — memorize it, it's the most reused pattern.

### Drills (60 min) — `sql/problems.md` Block C, **Q16–Q24**
Priority order (do these even if you don't finish all):
- **Q16** 7-day moving average (the frame syntax — do it twice).
- **Q17 / Q18** ranking + top-1-per-group (ROW_NUMBER in a CTE, filter `=1`).
- **Q19** day-over-day with `LAG`.
- **Q20 / Q21** running total and % of group total.
- **Q22** top-2-per-group with `DENSE_RANK` — the canonical interview question.
- **Q24** gaps-and-islands streak (stretch — great to *talk through* even if hard).

Tip: for each, say which clause does the work and **why you can't filter on the
window result without a CTE** (Q18, Q22 force this).

### Spaced repetition (15 min)
Redo **Q12 (Day 2)** and **Q6 (Day 1)** cold.

### Reflect (5 min)
Can you write the moving-average frame from memory? And the top-N-per-group CTE?
Those two are non-negotiable — flag for tomorrow if shaky.

**Done when:** you can write a moving average, a `LAG` delta, and a
top-N-per-group query from a blank screen, explaining each aloud.
