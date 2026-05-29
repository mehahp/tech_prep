# Worked Example: "Design a capacity-monitoring & forecasting system"

A fully narrated answer for the most likely design prompt for this team. Read it,
then **close it and re-deliver it out loud from the 6 headers** in `framework.md`.
Re-doing it verbally 2–3 times this week is the rep that builds confidence.

> Prompt: *"We run tens of thousands of servers across several data centers. Design
> a system to collect their utilization, let engineers query/visualize it, and
> forecast capacity needs so we can plan purchases and avoid both outages and
> waste."*

---

## 1. Requirements & scope
**Clarifying questions I'd ask:**
- How many servers, and how often do they report? (Assume ~50k servers, 1 sample/min.)
- What metrics? (CPU, mem, requests, maybe disk/net.)
- Who queries it and how? (Engineers: dashboards over hours–months; ML jobs: bulk
  historical reads.)
- Forecast horizon & granularity? (Per-DC and per-service, weeks–months ahead.)
- Freshness/latency tolerance for dashboards? (A minute or two is fine — not trading.)

**Functional:** ingest metrics; store time series; query by entity + time range;
forecast future utilization/capacity; alert on anomalies/headroom.
**Non-functional:** very write-heavy, append-mostly; durable; cost-efficient
storage; queries p95 < ~1s for dashboards; high availability for ingestion.
**Out of scope (stated):** auth, the dashboard UI itself, the procurement workflow.

## 2. Estimate
- Writes: 50k servers × ~4 metrics / 60s ≈ **3.3k writes/sec** sustained (bursty).
- Raw volume: 50k × 4 × 1440 samples/day ≈ **288M points/day**. At ~20 bytes
  compressed ≈ **~6 GB/day raw** → tiering/downsampling clearly needed for years
  of retention.
- Reads: modest (engineers + periodic ML jobs) vs writes → **write-optimized** store.

## 3. High-level design
```
 servers/agents ──▶ ingestion gateway ──▶ queue (Kafka) ──▶ stream writer ──▶ time-series store
                                                                │                    │
                                                                ▼                    ▼
                                                         downsampler          query API ──▶ dashboards
                                                         (raw→hourly→daily)    bulk export ──▶ ML pipeline ──▶ forecasts ──▶ planning + alerts
```
- **Agent** on each host buffers and pushes samples (resfilient to brief outages).
- **Queue** decouples ingest spikes from storage (backpressure, replay).
- **Time-series store** (see §4) for the raw + rolled-up data.
- **Query API** serves range queries; **ML pipeline** reads history, writes forecasts.

## 4. Data model & APIs
**Storage choice:** a time-series database / columnar store partitioned by time,
because the access pattern is "append constantly, read by (entity, time range),
aggregate over time." (Plain row-store RDBMS would struggle at this write volume;
relational still fine for the *dimension* data — servers, DCs, services.)

Logical schema (mirrors `sql/prep.db` on purpose):
- `usage_metrics(metric_ts, server_id, cpu_util, mem_util, requests)` — the fact/TS.
- dimensions: `servers`, `data_centers`, `regions`, `services`, `deployments`.
- `forecasts(entity_type, entity_id, target_date, metric, predicted, lower, upper)`.

**Retention/rollups:** raw @ 7–30 days → hourly avg/max @ 1 yr → daily @ multi-yr.
Keep `max` alongside `avg` (peaks drive capacity, not averages).

**APIs:**
- `ingest(server_id, ts, metrics{})`
- `query(entity, metric, start, end, granularity)`
- `get_forecast(entity, metric, horizon)`

## 5. Deep dive — the forecasting part (their wheelhouse)
- **Aggregate** raw → per-(DC|service|region) daily series (a big GROUP BY — same
  shape as the SQL drills).
- **Features**: lags (t-1, t-7), rolling mean/max, day-of-week & month-of-year
  seasonality, holidays/launch calendar, trend.
- **Models**: baseline first (seasonal-naive / linear trend) → then a forecaster
  (e.g., gradient-boosted trees on the features, or a classical seasonal model).
  Always compare against the baseline.
- **Backtesting**: rolling-origin evaluation (train to T, predict T+h, slide
  forward). Split by **time**, never randomly.
- **Metric & the key insight**: don't just minimize RMSE — **errors are
  asymmetric**. Under-forecasting → outages/SLO breaches; over-forecasting →
  wasted spend. So optimize an asymmetric loss or add a demand-aware safety buffer,
  and report headroom (capacity − forecasted peak) per DC.
- **From forecast to decision**: capacity planning is an optimization — minimize
  cost subject to "provisioned ≥ forecasted peak demand × safety factor" and
  reliability/latency constraints, per region. That hands off to the planning team.

## 6. Scale, reliability, wrap-up
- **Scale writes:** partition/shard the TS store by time + entity hash; the queue
  absorbs bursts; batch writes.
- **Scale reads:** pre-aggregate rollups so dashboards hit small tables; cache hot
  dashboard queries.
- **Reliability:** agent-side buffering + queue replay means no data loss on a
  brief store outage; replicate storage; monitor ingestion lag.
- **Cost:** tiered retention + downsampling + compression keeps multi-year history
  affordable — which is itself the team's mandate (efficiency).
- **Monitoring:** ingestion lag, missing-data gaps, forecast error drift,
  capacity-headroom alerts.

**One-paragraph summary (how I'd close):** "Agents push metrics through a queue
into a time-series store with tiered rollups; a query API serves dashboards from
the rollups; an ML pipeline reads history, produces capacity forecasts with an
asymmetric loss that penalizes under-provisioning, and feeds a cost-minimizing
capacity plan. It's write-optimized, tiered for cost, and the forecasting accounts
for the fact that running out of capacity is worse than having a little spare."

---

## Drill it
Set a 12-minute timer and deliver this from just the 6 headers, out loud. Then
have me (or a friend) throw one curveball: *"What if servers report late or
out of order?"* (→ event-time vs processing-time, watermarks, late-arriving
upserts into rollups) or *"How do you attribute shared cost to a service?"*
(→ usage-weighted allocation via the `deployments` join).
