# Practice data model (`prep.db`)

A miniature iCloud-style capacity/cost dataset. 60 days of daily metrics
(2025-03-01 .. 2025-04-29). Built deterministically by `build_db.py`, so your
answers will match `solutions.sql`.

Learn this model cold — knowing the tables by heart removes friction in the
interview (even though the real one will use a different schema, the *shapes*
recur: a dimension table, a fact table, a time series).

## Tables

### `regions` — geographic regions
| col | type | notes |
|-----|------|-------|
| region_id | INT PK | |
| name | TEXT | e.g. `us-east` |
| country | TEXT | |

### `data_centers` — DCs belong to a region
| col | type | notes |
|-----|------|-------|
| dc_id | INT PK | |
| region_id | INT FK→regions | |
| name | TEXT | e.g. `iad1` |
| capacity_cores | INT | total cores the DC can host |
| opened_date | TEXT (date) | |

### `services` — logical services
| col | type | notes |
|-----|------|-------|
| service_id | INT PK | |
| name | TEXT | e.g. `photos-sync` |
| team | TEXT | owning team |
| tier | TEXT | `critical` / `standard` / `batch` |

### `servers` — physical/virtual hosts in a DC
| col | type | notes |
|-----|------|-------|
| server_id | INT PK | |
| dc_id | INT FK→data_centers | |
| server_type | TEXT | `compute` / `storage` / `gpu` |
| cores | INT | |
| memory_gb | INT | |
| hourly_cost_usd | REAL | |
| commissioned_date | TEXT (date) | |
| status | TEXT | `active` / `idle` / `retired` |

### `deployments` — a service running on a server over an interval
| col | type | notes |
|-----|------|-------|
| deployment_id | INT PK | |
| service_id | INT FK→services | |
| server_id | INT FK→servers | |
| start_date | TEXT (date) | |
| end_date | TEXT (date) | **NULL = still active** |

### `usage_metrics` — daily time series per server
| col | type | notes |
|-----|------|-------|
| metric_date | TEXT (date) | |
| server_id | INT FK→servers | |
| cpu_util | REAL | 0..1 |
| mem_util | REAL | 0..1 |
| requests | INT | requests served that day |
| | | PK = (metric_date, server_id) |

### `cost_records` — realized daily cost per server
| col | type | notes |
|-----|------|-------|
| cost_date | TEXT (date) | |
| server_id | INT FK→servers | |
| cost_usd | REAL | |
| | | PK = (cost_date, server_id) |

### `incidents` — service incidents
| col | type | notes |
|-----|------|-------|
| incident_id | INT PK | |
| service_id | INT FK→services | |
| severity | INT | 1 (worst) .. 4 |
| opened_date | TEXT (date) | |
| resolved_date | TEXT (date) | **NULL = still open** |

## Relationships (the join map)

```
regions 1───* data_centers 1───* servers 1───* usage_metrics
                                   │   *└─────* cost_records
                                   │
services 1───* deployments *───────┘
services 1───* incidents
```

## Date notes (matters in the interview)
On **Postgres** (primary), the date columns are real `DATE` types:
- Add days: `d + 7` or `d + INTERVAL '7 days'`. Month bucket: `to_char(d,'YYYY-MM')`
  or `date_trunc('month', d)`. Day-of-week: `EXTRACT(DOW FROM d)`.
- Day difference is plain subtraction: `dateA - dateB` → integer days.
- Gotcha: `ROUND(x, n)` needs `x` to be `numeric`. `cpu_util`/`mem_util` are
  `double precision`, so write `ROUND(AVG(cpu_util)::numeric, 3)`.

On **SQLite** (fallback) dates are ISO text `'YYYY-MM-DD'` (sorts/compares as text):
`date('2025-03-01','+7 days')`, `strftime('%Y-%m', d)`, `strftime('%w', d)`
(0=Sunday), `julianday(a) - julianday(b)` for day diffs.

`cheatsheets/sql_patterns.md` lists both dialects side by side.
