# SQL Problems (30) — graded by topic

Work against `prep.db`. Attempt each **before** opening `solutions.sql`.
Run with: `python3 query.py "<your query>"` or put it in a file and pass the path.

**Process for every problem (say it out loud):**
1. What tables do I need, and how do they join?
2. What's the grain (one row per ___) of my result?
3. Filter before or after aggregation?
4. Run it. Sanity-check row counts and a couple of values.

Difficulty: ⭐ easy · ⭐⭐ medium · ⭐⭐⭐ harder

---

## Block A — Foundations & Joins (Day 1)

**Q1 ⭐** List all servers (`server_id`, `server_type`, `cores`) in data center
`iad1`. (Hint: join `servers` → `data_centers`.)

**Q2 ⭐** For every server, show its `server_id`, its DC `name`, and its region
`name`. (Three-table join.)

**Q3 ⭐** Count how many servers each data center has. Show DC name and the count,
ordered by count descending.

**Q4 ⭐⭐** List each service `name` and the `name` of every server it is currently
deployed on (i.e., `end_date IS NULL`).

**Q5 ⭐⭐** Find services that have **no current deployments**. (Think: LEFT JOIN +
`IS NULL`, or `NOT IN` / `NOT EXISTS`.)

**Q6 ⭐⭐** Show every region and its number of servers, **including regions with
zero servers**. (Why does an INNER JOIN give the wrong answer here?)

**Q7 ⭐⭐** List all `gpu` servers that are `active`, with their DC name and hourly
cost, most expensive first.

**Q8 ⭐⭐** For each `tier`, how many distinct servers run at least one service of
that tier (current deployments)? (Join `services`→`deployments`→`servers`,
`COUNT(DISTINCT ...)`.)

---

## Block B — Aggregations: GROUP BY / HAVING / conditional (Day 2)

**Q9 ⭐** Total realized cost (`cost_usd`) across the whole 60-day window.

**Q10 ⭐** Total cost per server. Show `server_id` and total, top 5 by cost.

**Q11 ⭐⭐** Average daily `cpu_util` per data center over the window. Show DC name,
rounded to 3 decimals, highest first.

**Q12 ⭐⭐** For each region, total cost and average cpu_util. (Join the time-series
facts up through servers → data_centers → regions.)

**Q13 ⭐⭐** Which data centers have an **average cpu_util below 0.35**? (This is a
post-aggregation filter — `HAVING`.) Show DC name + avg.

**Q14 ⭐⭐** Per server, count how many days it was "hot" (cpu_util > 0.8) vs "cold"
(cpu_util < 0.2) using **conditional aggregation** (`SUM(CASE WHEN ...)`). Show
only servers with at least 1 hot day, hot days descending.

**Q15 ⭐⭐⭐** Monthly total cost per region. Bucket `cost_date` into `YYYY-MM` and
group by region + month. (Use `strftime('%Y-%m', cost_date)`.)

---

## Block C — Window Functions (Day 3)

**Q16 ⭐⭐** For each server, show `metric_date`, `cpu_util`, and a **7-day moving
average** of cpu_util (current row + previous 6 days), ordered by date.

**Q17 ⭐⭐** Rank servers within each data center by total cost (highest = rank 1).
Use `RANK()` (or `ROW_NUMBER`). Show dc name, server_id, total cost, rank.

**Q18 ⭐⭐** For each data center, return the **single most expensive server**
(top-1-per-group). (ROW_NUMBER in a subquery/CTE, filter `= 1`.)

**Q19 ⭐⭐** For server `1000`, show `metric_date`, `requests`, and the
**day-over-day change** in requests using `LAG`.

**Q20 ⭐⭐** Running (cumulative) total of daily cost for the whole fleet, by date.
(Aggregate per day first, then a window running sum.)

**Q21 ⭐⭐⭐** For each server, the **% of its total 60-day cost** incurred on each
day = daily cost / `SUM(cost) OVER (PARTITION BY server)`. Show one server's rows.

**Q22 ⭐⭐⭐** Top-2 most-utilized servers (by avg cpu_util) **per region**. (Avg
per server in a CTE, then `DENSE_RANK() OVER (PARTITION BY region ...)`.)

**Q23 ⭐⭐⭐** For each region and date, the daily total cost **and** that region's
**7-day trailing average** of daily total cost. (Aggregate to region/day, then
window over the partition.)

**Q24 ⭐⭐⭐** Find each server's **longest streak of consecutive days** with
cpu_util > 0.7. (Classic "gaps and islands": `ROW_NUMBER` trick — date minus a
row counter is constant within a streak.)

---

## Block D — CTEs & Putting It Together (Day 4)

**Q25 ⭐⭐** Using CTEs, list data centers whose total cost is **above the fleet
average** data-center cost. (CTE 1: cost per DC. CTE 2: avg of those. Join/compare.)

**Q26 ⭐⭐⭐** "Utilization efficiency": for each region, cost **per million
requests** = total cost / (total requests / 1e6). Lowest (most efficient) first.

**Q27 ⭐⭐⭐** Week-over-week fleet cost growth. Bucket dates into ISO week (or just
sequential 7-day buckets from the start), sum cost per week, then show each week's
cost and the **% change vs the prior week** (`LAG`).

**Q28 ⭐⭐⭐** Mean time to resolve (MTTR) incidents per service: average of
`resolved_date - opened_date` in days, only for resolved incidents. Also show
count of still-open incidents per service. (Conditional agg + date math.)

**Q29 ⭐⭐⭐** For each service, its current monthly run-rate cost: sum the most
recent day's `cost_usd` across all servers it is **currently** deployed on
(`end_date IS NULL`), × 30. (Join chain + filter to the max date.)

**Q30 ⭐⭐⭐ (recursive)** Generate a calendar of all 60 dates in the window using a
**recursive CTE** (no calendar table), then LEFT JOIN fleet daily cost so that any
missing day would show as 0. (Demonstrates recursive CTE + outer join + COALESCE.)

---

## Stretch / "explain this" prompts (great for talking out loud)
- When does a JOIN multiply your rows, and how would you detect it?
- `WHERE` vs `HAVING` — give a one-line rule.
- `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` — when does the choice matter?
- Why put aggregation in a CTE before applying a window function?
- How would you find duplicates on `(metric_date, server_id)` if the PK weren't there?
