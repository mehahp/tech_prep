-- ============================================================================
-- SQL SOLUTIONS (SQLite dialect) for problems.md  -- run against prep.db
-- This is the FALLBACK file. If you're practicing on Postgres (recommended),
-- use solutions.sql instead. Only Q11,Q13,Q15,Q16,Q22,Q24,Q27,Q28,Q30 differ.
-- Peek only AFTER you've attempted a problem.
-- Run one with:  python3 query.py "<paste query body>"
-- ============================================================================

-- ---------------------------------------------------------------- Block A ----

-- Q1: servers in iad1
SELECT s.server_id, s.server_type, s.cores
FROM servers s
JOIN data_centers d ON d.dc_id = s.dc_id
WHERE d.name = 'iad1';

-- Q2: server + dc name + region name (3-table join)
SELECT s.server_id, d.name AS dc_name, r.name AS region_name
FROM servers s
JOIN data_centers d ON d.dc_id = s.dc_id
JOIN regions r ON r.region_id = d.region_id;

-- Q3: server count per DC
SELECT d.name AS dc_name, COUNT(*) AS server_count
FROM data_centers d
JOIN servers s ON s.dc_id = d.dc_id
GROUP BY d.dc_id, d.name
ORDER BY server_count DESC;

-- Q4: service -> currently deployed server names
SELECT sv.name AS service, s.server_id, s.server_type
FROM services sv
JOIN deployments dp ON dp.service_id = sv.service_id
JOIN servers s ON s.server_id = dp.server_id
WHERE dp.end_date IS NULL
ORDER BY sv.name;

-- Q5: services with NO current deployments (anti-join)
SELECT sv.service_id, sv.name
FROM services sv
WHERE NOT EXISTS (
    SELECT 1 FROM deployments dp
    WHERE dp.service_id = sv.service_id AND dp.end_date IS NULL
);
-- equivalent LEFT JOIN form:
-- SELECT sv.service_id, sv.name
-- FROM services sv
-- LEFT JOIN deployments dp
--   ON dp.service_id = sv.service_id AND dp.end_date IS NULL
-- WHERE dp.deployment_id IS NULL;

-- Q6: every region + server count INCLUDING zero (LEFT JOIN; INNER drops empties)
SELECT r.name AS region, COUNT(s.server_id) AS server_count
FROM regions r
LEFT JOIN data_centers d ON d.region_id = r.region_id
LEFT JOIN servers s ON s.dc_id = d.dc_id
GROUP BY r.region_id, r.name
ORDER BY server_count DESC;

-- Q7: active gpu servers with DC name + hourly cost
SELECT s.server_id, d.name AS dc_name, s.hourly_cost_usd
FROM servers s
JOIN data_centers d ON d.dc_id = s.dc_id
WHERE s.server_type = 'gpu' AND s.status = 'active'
ORDER BY s.hourly_cost_usd DESC;

-- Q8: distinct servers per tier (current deployments)
SELECT sv.tier, COUNT(DISTINCT dp.server_id) AS server_count
FROM services sv
JOIN deployments dp ON dp.service_id = sv.service_id
WHERE dp.end_date IS NULL
GROUP BY sv.tier
ORDER BY server_count DESC;

-- ---------------------------------------------------------------- Block B ----

-- Q9: total fleet cost
SELECT ROUND(SUM(cost_usd), 2) AS total_cost
FROM cost_records;

-- Q10: total cost per server, top 5
SELECT server_id, ROUND(SUM(cost_usd), 2) AS total_cost
FROM cost_records
GROUP BY server_id
ORDER BY total_cost DESC
LIMIT 5;

-- Q11: avg daily cpu_util per DC
SELECT d.name AS dc_name, ROUND(AVG(u.cpu_util), 3) AS avg_cpu
FROM usage_metrics u
JOIN servers s ON s.server_id = u.server_id
JOIN data_centers d ON d.dc_id = s.dc_id
GROUP BY d.dc_id, d.name
ORDER BY avg_cpu DESC;

-- Q12: per region: total cost + avg cpu_util
SELECT r.name AS region,
       ROUND(SUM(c.cost_usd), 2) AS total_cost,
       ROUND(AVG(u.cpu_util), 3) AS avg_cpu
FROM regions r
JOIN data_centers d ON d.region_id = r.region_id
JOIN servers s ON s.dc_id = d.dc_id
JOIN cost_records c ON c.server_id = s.server_id
JOIN usage_metrics u ON u.server_id = s.server_id AND u.metric_date = c.cost_date
GROUP BY r.region_id, r.name
ORDER BY total_cost DESC;

-- Q13: DCs with avg cpu_util < 0.35  (HAVING = post-aggregation filter)
SELECT d.name AS dc_name, ROUND(AVG(u.cpu_util), 3) AS avg_cpu
FROM usage_metrics u
JOIN servers s ON s.server_id = u.server_id
JOIN data_centers d ON d.dc_id = s.dc_id
GROUP BY d.dc_id, d.name
HAVING AVG(u.cpu_util) < 0.35
ORDER BY avg_cpu;

-- Q14: conditional aggregation -> hot/cold day counts per server
SELECT server_id,
       SUM(CASE WHEN cpu_util > 0.8 THEN 1 ELSE 0 END) AS hot_days,
       SUM(CASE WHEN cpu_util < 0.2 THEN 1 ELSE 0 END) AS cold_days
FROM usage_metrics
GROUP BY server_id
HAVING SUM(CASE WHEN cpu_util > 0.8 THEN 1 ELSE 0 END) >= 1
ORDER BY hot_days DESC;

-- Q15: monthly cost per region (strftime is SQLite; Postgres: to_char(cost_date,'YYYY-MM'))
SELECT r.name AS region,
       strftime('%Y-%m', c.cost_date) AS month,
       ROUND(SUM(c.cost_usd), 2) AS total_cost
FROM cost_records c
JOIN servers s ON s.server_id = c.server_id
JOIN data_centers d ON d.dc_id = s.dc_id
JOIN regions r ON r.region_id = d.region_id
GROUP BY r.name, month
ORDER BY r.name, month;

-- ---------------------------------------------------------------- Block C ----

-- Q16: 7-day moving average of cpu_util per server
SELECT server_id, metric_date, cpu_util,
       ROUND(AVG(cpu_util) OVER (
           PARTITION BY server_id ORDER BY metric_date
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ), 3) AS moving_avg_7d
FROM usage_metrics
ORDER BY server_id, metric_date;

-- Q17: rank servers within DC by total cost
SELECT d.name AS dc_name, t.server_id, ROUND(t.total_cost, 2) AS total_cost,
       RANK() OVER (PARTITION BY d.dc_id ORDER BY t.total_cost DESC) AS cost_rank
FROM (
    SELECT server_id, SUM(cost_usd) AS total_cost
    FROM cost_records GROUP BY server_id
) t
JOIN servers s ON s.server_id = t.server_id
JOIN data_centers d ON d.dc_id = s.dc_id
ORDER BY d.name, cost_rank;

-- Q18: top-1 most expensive server per DC
WITH per_server AS (
    SELECT s.dc_id, c.server_id, SUM(c.cost_usd) AS total_cost
    FROM cost_records c
    JOIN servers s ON s.server_id = c.server_id
    GROUP BY s.dc_id, c.server_id
),
ranked AS (
    SELECT dc_id, server_id, total_cost,
           ROW_NUMBER() OVER (PARTITION BY dc_id ORDER BY total_cost DESC) AS rn
    FROM per_server
)
SELECT d.name AS dc_name, r.server_id, ROUND(r.total_cost, 2) AS total_cost
FROM ranked r
JOIN data_centers d ON d.dc_id = r.dc_id
WHERE r.rn = 1
ORDER BY d.name;

-- Q19: day-over-day change in requests for server 1000 (LAG)
SELECT metric_date, requests,
       requests - LAG(requests) OVER (ORDER BY metric_date) AS dod_change
FROM usage_metrics
WHERE server_id = 1000
ORDER BY metric_date;

-- Q20: fleet daily cost running total
WITH daily AS (
    SELECT cost_date, SUM(cost_usd) AS day_cost
    FROM cost_records GROUP BY cost_date
)
SELECT cost_date,
       ROUND(day_cost, 2) AS day_cost,
       ROUND(SUM(day_cost) OVER (ORDER BY cost_date), 2) AS running_total
FROM daily
ORDER BY cost_date;

-- Q21: each day's % of a server's total cost (server 1000 shown)
SELECT cost_date, ROUND(cost_usd, 2) AS cost_usd,
       ROUND(100.0 * cost_usd / SUM(cost_usd) OVER (PARTITION BY server_id), 3)
         AS pct_of_server_total
FROM cost_records
WHERE server_id = 1000
ORDER BY cost_date;

-- Q22: top-2 most-utilized servers per region (DENSE_RANK)
WITH per_server AS (
    SELECT d.region_id, u.server_id, AVG(u.cpu_util) AS avg_cpu
    FROM usage_metrics u
    JOIN servers s ON s.server_id = u.server_id
    JOIN data_centers d ON d.dc_id = s.dc_id
    GROUP BY d.region_id, u.server_id
),
ranked AS (
    SELECT region_id, server_id, avg_cpu,
           DENSE_RANK() OVER (PARTITION BY region_id ORDER BY avg_cpu DESC) AS rnk
    FROM per_server
)
SELECT r.name AS region, k.server_id, ROUND(k.avg_cpu, 3) AS avg_cpu, k.rnk
FROM ranked k
JOIN regions r ON r.region_id = k.region_id
WHERE k.rnk <= 2
ORDER BY r.name, k.rnk;

-- Q23: region daily cost + region 7-day trailing avg
WITH region_daily AS (
    SELECT d.region_id, c.cost_date, SUM(c.cost_usd) AS day_cost
    FROM cost_records c
    JOIN servers s ON s.server_id = c.server_id
    JOIN data_centers d ON d.dc_id = s.dc_id
    GROUP BY d.region_id, c.cost_date
)
SELECT r.name AS region, rd.cost_date,
       ROUND(rd.day_cost, 2) AS day_cost,
       ROUND(AVG(rd.day_cost) OVER (
           PARTITION BY rd.region_id ORDER BY rd.cost_date
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ), 2) AS trailing_7d_avg
FROM region_daily rd
JOIN regions r ON r.region_id = rd.region_id
ORDER BY r.name, rd.cost_date;

-- Q24: longest streak of consecutive days with cpu_util > 0.7 per server
--      gaps-and-islands: within a streak, (date - row_number) is constant.
WITH hot AS (
    SELECT server_id, metric_date,
           ROW_NUMBER() OVER (PARTITION BY server_id ORDER BY metric_date) AS rn
    FROM usage_metrics
    WHERE cpu_util > 0.7
),
grp AS (
    SELECT server_id, metric_date,
           date(metric_date, '-' || rn || ' days') AS grp_key
    FROM hot
),
streaks AS (
    SELECT server_id, grp_key, COUNT(*) AS streak_len
    FROM grp
    GROUP BY server_id, grp_key
)
SELECT server_id, MAX(streak_len) AS longest_streak
FROM streaks
GROUP BY server_id
ORDER BY longest_streak DESC;

-- ---------------------------------------------------------------- Block D ----

-- Q25: DCs above the average per-DC cost (CTEs)
WITH dc_cost AS (
    SELECT s.dc_id, SUM(c.cost_usd) AS total_cost
    FROM cost_records c
    JOIN servers s ON s.server_id = c.server_id
    GROUP BY s.dc_id
),
avg_cost AS (
    SELECT AVG(total_cost) AS mean_dc_cost FROM dc_cost
)
SELECT d.name AS dc_name, ROUND(dc.total_cost, 2) AS total_cost
FROM dc_cost dc
JOIN data_centers d ON d.dc_id = dc.dc_id
CROSS JOIN avg_cost a
WHERE dc.total_cost > a.mean_dc_cost
ORDER BY total_cost DESC;

-- Q26: cost per million requests, per region (efficiency)
WITH agg AS (
    SELECT d.region_id,
           SUM(c.cost_usd) AS total_cost,
           SUM(u.requests) AS total_requests
    FROM cost_records c
    JOIN usage_metrics u
      ON u.server_id = c.server_id AND u.metric_date = c.cost_date
    JOIN servers s ON s.server_id = c.server_id
    JOIN data_centers d ON d.dc_id = s.dc_id
    GROUP BY d.region_id
)
SELECT r.name AS region,
       ROUND(total_cost, 2) AS total_cost,
       total_requests,
       ROUND(total_cost / (total_requests / 1000000.0), 2) AS cost_per_million_req
FROM agg
JOIN regions r ON r.region_id = agg.region_id
ORDER BY cost_per_million_req ASC;

-- Q27: week-over-week fleet cost growth (sequential 7-day buckets from start)
WITH daily AS (
    SELECT cost_date, SUM(cost_usd) AS day_cost
    FROM cost_records GROUP BY cost_date
),
weekly AS (
    SELECT CAST(julianday(cost_date) - julianday('2025-03-01') AS INTEGER) / 7
             AS week_idx,
           SUM(day_cost) AS week_cost
    FROM daily
    GROUP BY week_idx
)
SELECT week_idx,
       ROUND(week_cost, 2) AS week_cost,
       ROUND(week_cost - LAG(week_cost) OVER (ORDER BY week_idx), 2) AS abs_change,
       ROUND(100.0 * (week_cost - LAG(week_cost) OVER (ORDER BY week_idx))
             / LAG(week_cost) OVER (ORDER BY week_idx), 2) AS pct_change
FROM weekly
ORDER BY week_idx;

-- Q28: MTTR (days) per service + open incident count (conditional agg + date math)
SELECT sv.name AS service,
       ROUND(AVG(CASE WHEN i.resolved_date IS NOT NULL
                      THEN julianday(i.resolved_date) - julianday(i.opened_date)
                 END), 2) AS mttr_days,
       SUM(CASE WHEN i.resolved_date IS NULL THEN 1 ELSE 0 END) AS open_incidents,
       COUNT(*) AS total_incidents
FROM services sv
LEFT JOIN incidents i ON i.service_id = sv.service_id
GROUP BY sv.service_id, sv.name
ORDER BY mttr_days DESC NULLS LAST;
-- (SQLite tolerates NULLS LAST; Postgres supports it natively too.)

-- Q29: current monthly run-rate cost per service (latest day's cost * 30)
WITH latest AS (SELECT MAX(cost_date) AS d FROM cost_records),
last_day_cost AS (
    SELECT c.server_id, c.cost_usd
    FROM cost_records c, latest
    WHERE c.cost_date = latest.d
)
SELECT sv.name AS service,
       ROUND(SUM(ldc.cost_usd) * 30, 2) AS monthly_run_rate
FROM services sv
JOIN deployments dp
  ON dp.service_id = sv.service_id AND dp.end_date IS NULL
JOIN last_day_cost ldc ON ldc.server_id = dp.server_id
GROUP BY sv.service_id, sv.name
ORDER BY monthly_run_rate DESC;

-- Q30: recursive CTE calendar LEFT JOIN fleet daily cost (missing days -> 0)
WITH RECURSIVE cal(d) AS (
    SELECT '2025-03-01'
    UNION ALL
    SELECT date(d, '+1 day') FROM cal WHERE d < '2025-04-29'
),
daily AS (
    SELECT cost_date, SUM(cost_usd) AS day_cost
    FROM cost_records GROUP BY cost_date
)
SELECT cal.d AS metric_date,
       ROUND(COALESCE(daily.day_cost, 0), 2) AS fleet_cost
FROM cal
LEFT JOIN daily ON daily.cost_date = cal.d
ORDER BY cal.d;
