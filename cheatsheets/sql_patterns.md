# SQL Patterns Cheatsheet — *re-type this from memory daily*

This is your repetition core. Every morning, open a blank file and reproduce as
many of these as you can **without looking**, then diff against this. Muscle
memory of syntax is what frees your brain to think about the actual problem in
the interview.

SQLite and Postgres dialect notes are flagged `[SQLite]` / `[PG]` where they differ.

---

## 0. Query evaluation order (say this in your head)
You *write*: `SELECT … FROM … JOIN … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT`
SQL *executes*: `FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

Consequences to recite:
- You **can't** use a `SELECT` alias in `WHERE` (alias doesn't exist yet) — but
  you usually **can** in `ORDER BY`.
- `WHERE` filters **rows before** grouping. `HAVING` filters **groups after**.
- Window functions run **after** GROUP BY/HAVING, **before** ORDER BY/LIMIT — so
  you can't filter on a window result in `WHERE`; wrap it in a CTE/subquery.

---

## 1. Joins

```sql
-- INNER: only matching rows on both sides
SELECT a.*, b.col
FROM a JOIN b ON b.a_id = a.id;

-- LEFT: all of a, NULLs where b has no match  (use to "keep everything on left")
SELECT a.*, b.col
FROM a LEFT JOIN b ON b.a_id = a.id;

-- Anti-join: rows in a with NO match in b  (two idioms — know both)
SELECT a.* FROM a LEFT JOIN b ON b.a_id = a.id WHERE b.id IS NULL;
SELECT a.* FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.a_id = a.id);

-- Self-join (e.g. employee/manager, or comparing rows in same table)
SELECT e.name, m.name AS manager
FROM emp e LEFT JOIN emp m ON m.id = e.manager_id;
```

**Filter-in-JOIN vs WHERE on a LEFT JOIN (a classic gotcha):**
```sql
-- keeps all a, b.col NULL when status<>'active'
... a LEFT JOIN b ON b.a_id=a.id AND b.status='active'
-- silently turns it into an INNER join (drops a-rows with no active b)
... a LEFT JOIN b ON b.a_id=a.id WHERE b.status='active'
```

**Row-multiplication rule:** a join multiplies rows when the join key is not
unique on the "other" side. If `SUM` looks too big, you probably fanned out —
aggregate the child table in a CTE first, *then* join.

---

## 2. Aggregation

```sql
SELECT grp, COUNT(*) AS n, COUNT(DISTINCT user_id) AS uniq_users,
       SUM(x) AS total, AVG(x) AS mean, MIN(x), MAX(x)
FROM t
WHERE x IS NOT NULL          -- pre-aggregation filter
GROUP BY grp
HAVING COUNT(*) > 5          -- post-aggregation filter
ORDER BY total DESC;
```

**Conditional aggregation (memorize this shape — it shows up constantly):**
```sql
SELECT
  SUM(CASE WHEN status='paid'  THEN amount ELSE 0 END) AS paid_amount,
  SUM(CASE WHEN status='fraud' THEN 1      ELSE 0 END) AS fraud_count,
  AVG(CASE WHEN region='us' THEN latency END)          AS us_avg_latency, -- NULLs ignored by AVG
  COUNT(*) FILTER (WHERE status='paid')                AS paid_count     -- [PG] cleaner form
FROM t
GROUP BY grp;
```
`COUNT(DISTINCT col)`, and `COUNT(col)` ignores NULLs while `COUNT(*)` doesn't.

**Pivot (rows → columns) via conditional agg:**
```sql
SELECT user_id,
  SUM(CASE WHEN month='2025-01' THEN amt END) AS jan,
  SUM(CASE WHEN month='2025-02' THEN amt END) AS feb
FROM t GROUP BY user_id;
```

---

## 3. Window functions  — `func() OVER (PARTITION BY … ORDER BY … [frame])`

The mental model: like GROUP BY, but **keeps every row** and attaches a computed
value. `PARTITION BY` = the group; `ORDER BY` = order within the group;
the frame = which rows feed the calc.

```sql
-- Ranking within a group
ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)  -- 1,2,3,4 (no ties)
RANK()       OVER (PARTITION BY dept ORDER BY salary DESC)  -- 1,2,2,4 (gaps)
DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC)  -- 1,2,2,3 (no gaps)

-- Previous / next row
LAG(x)  OVER (ORDER BY d)          -- value from prior row (NULL on first)
LAG(x, 1, 0) OVER (ORDER BY d)     -- offset 1, default 0
LEAD(x) OVER (ORDER BY d)          -- value from next row

-- Aggregates as windows
SUM(x)  OVER (PARTITION BY id ORDER BY d)                       -- running total
AVG(x)  OVER (PARTITION BY id ORDER BY d
              ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)         -- 7-row moving avg
SUM(x)  OVER (PARTITION BY id)                                  -- group total on every row
ROUND(100.0 * x / SUM(x) OVER (PARTITION BY id), 2)             -- % of group total

-- First/last/nth within partition
FIRST_VALUE(x) OVER (PARTITION BY id ORDER BY d)
NTILE(4)       OVER (ORDER BY x)                                -- quartile buckets
```

**Frames (the part people forget):**
- Default frame *when ORDER BY is present* = `RANGE BETWEEN UNBOUNDED PRECEDING
  AND CURRENT ROW` (running total). For moving averages, specify `ROWS BETWEEN
  N PRECEDING AND CURRENT ROW` explicitly.
- No `ORDER BY` ⇒ frame is the whole partition (use for "group total per row").

**Top-N-per-group recipe (the single most useful window pattern):**
```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY grp ORDER BY metric DESC) AS rn
  FROM t
)
SELECT * FROM ranked WHERE rn <= 3;   -- can't put this filter in WHERE without the CTE
```

---

## 4. CTEs (`WITH`)

Use them to name steps and read top-to-bottom. Prefer over nested subqueries for
anything non-trivial — and say *why* in the interview ("readability + I can test
each stage").

```sql
WITH per_server AS (        -- step 1: aggregate to a clean grain
    SELECT server_id, SUM(cost_usd) AS total FROM cost_records GROUP BY server_id
),
ranked AS (                 -- step 2: build on step 1
    SELECT *, RANK() OVER (ORDER BY total DESC) AS rnk FROM per_server
)
SELECT * FROM ranked WHERE rnk <= 5;   -- step 3: final
```

**Recursive CTE (date spine / hierarchy / sequence):**
```sql
WITH RECURSIVE cal(d) AS (
    SELECT DATE '2025-03-01'                          -- anchor
    UNION ALL
    SELECT d + INTERVAL '1 day' FROM cal WHERE d < DATE '2025-04-29'  -- [PG]
    -- [SQLite]: SELECT date(d,'+1 day') FROM cal WHERE d < '2025-04-29'
)
SELECT * FROM cal;
```
Use a date spine + LEFT JOIN + COALESCE(…,0) to fill **missing days** with zeros
(forecasting/time-series questions love this).

---

## 5. Dates (dialect table — know both, you'll be told which DB)

| task | SQLite | Postgres |
|------|--------|----------|
| add days | `date(d,'+7 days')` | `d + INTERVAL '7 days'` |
| month bucket | `strftime('%Y-%m', d)` | `to_char(d,'YYYY-MM')` or `date_trunc('month', d)` |
| day of week | `strftime('%w', d)` (0=Sun) | `EXTRACT(DOW FROM d)` |
| day diff | `julianday(a)-julianday(b)` | `a::date - b::date` |
| now | `date('now')` | `CURRENT_DATE` |

---

## 6. Other patterns worth one rep each

```sql
-- De-duplicate, keep newest per key
WITH r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) rn FROM t)
SELECT * FROM r WHERE rn = 1;

-- Find duplicates
SELECT key, COUNT(*) FROM t GROUP BY key HAVING COUNT(*) > 1;

-- NULL handling
COALESCE(x, 0)            -- first non-null
NULLIF(a, 0)             -- avoid divide-by-zero: x / NULLIF(denom, 0)

-- Set ops
SELECT … UNION SELECT …       -- dedupes
SELECT … UNION ALL SELECT …   -- keeps dups (faster)
SELECT … EXCEPT SELECT …      -- in first not second

-- Median-ish: PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)  [PG]
```

---

## 7. The 6 "explain it crisply" answers (rehearse aloud)
1. **WHERE vs HAVING**: WHERE filters rows pre-aggregation; HAVING filters groups post-aggregation.
2. **INNER vs LEFT**: INNER drops non-matches on either side; LEFT keeps all left rows.
3. **RANK vs DENSE_RANK vs ROW_NUMBER**: ties get gaps / no gaps / are broken arbitrarily.
4. **Why a CTE before a window**: you must aggregate to the right grain first, and you can't filter on a window result without nesting.
5. **When a JOIN inflates rows**: when the join key isn't unique on the other table; detect with a COUNT before/after.
6. **Window vs GROUP BY**: GROUP BY collapses rows; window keeps them and annotates.
