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

## SQLite date notes (matters in the interview)
- Dates are stored as ISO text `'YYYY-MM-DD'`, which **sorts and compares
  correctly as text** (`WHERE metric_date >= '2025-04-01'` works).
- Useful functions: `date('2025-03-01','+7 days')`, `strftime('%Y-%m', d)` for
  month bucketing, `strftime('%w', d)` for day-of-week (0=Sunday),
  `julianday(a) - julianday(b)` for day differences.
- These differ slightly from Postgres (`date_trunc`, `EXTRACT`, `a::date - b::date`).
  `cheatsheets/sql_patterns.md` lists both dialects side by side.
