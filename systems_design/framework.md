# Systems Design — a repeatable framework (junior-friendly)

For a junior/early role they're testing **structured thinking and communication**,
not whether you can design Google from scratch. Have a framework you can run on
*any* prompt so you never freeze. Practice narrating it out loud.

A 45-min interview rarely spends more than ~15–20 min on design (the rest is
coding/SQL), so aim for a clear, complete-at-a-high-level answer over deep rabbit
holes.

---

## The 6-step framework (memorize the headers)

### 1. Requirements & scope (~3 min) — *ask, don't assume*
- **Functional**: what must it do? (the 2–3 core features)
- **Non-functional**: scale (QPS, data volume), latency, availability, consistency,
  cost. **Get numbers** — "how many servers/metrics/users?"
- **Explicitly out of scope**: name what you're *not* designing. Shows judgment.

### 2. Estimate (~2 min) — back-of-envelope
- Traffic: reads/sec, writes/sec. Data: bytes/record × records/day → storage/yr.
- This sizes your storage and tells you read- vs write-heavy. Even rough is fine;
  show the *method*.

### 3. High-level design (~5 min) — boxes and arrows
- Clients → API/ingestion → processing → storage → serving/consumers.
- Draw it (or describe it linearly). Name each component's one job.

### 4. Data model & APIs (~3 min)
- Key tables/schemas, the main read & write access patterns.
- 2–3 API signatures (`ingest(metric)`, `query(range)`).
- Storage choice + *why* (relational vs time-series vs object vs cache).

### 5. Deep dive (~4 min) — pick the interesting bottleneck
- Let the interviewer steer, or pick the hardest part. Discuss the key tradeoff
  (e.g., batch vs streaming, precompute vs query-time, consistency vs latency).

### 6. Scale, reliability, wrap-up (~3 min)
- Bottlenecks → fixes: partitioning/sharding, caching, read replicas, queues,
  batching, downsampling/retention.
- Failure modes & monitoring. Then summarize the design in 3 sentences.

---

## The tradeoff vocabulary (sprinkle these, honestly)
- **Batch vs streaming**: latency vs simplicity/cost.
- **Precompute (materialize) vs query-time**: fast reads + storage/staleness vs
  flexibility + slow reads.
- **SQL/relational vs NoSQL vs time-series DB vs object store**: pick per access
  pattern; justify it.
- **Caching**: what to cache, TTL, invalidation ("the two hard problems").
- **Sharding/partitioning**: by what key? hot partitions?
- **CAP / consistency**: strong vs eventual — what does *this* use case tolerate?
- **Horizontal vs vertical scaling**, queues for backpressure, idempotency.

---

## Topics tailored to THIS role (capacity / cost / forecasting)
Because this is an ML Optimization / capacity-planning team, expect data- and
ML-flavored design prompts. Be ready to discuss:

- **Metrics ingestion pipeline**: collect CPU/mem/requests from thousands of
  servers → store as a time series → serve dashboards + feed models. (Worked
  example in `worked_example.md`.)
- **Time-series storage**: high write volume, append-mostly, queried by
  (entity, time range). Downsampling + retention tiers (raw → hourly → daily).
- **Forecasting pipeline**: features (lags, rolling stats, seasonality, calendar) →
  train → backtest → serve predictions → monitor drift. Offline vs online.
- **Capacity / resource-allocation as optimization**: decision variables (how much
  capacity per region), objective (minimize cost), constraints (meet demand at
  p95, reliability/latency SLOs, physical limits). You don't need to solve an LP
  live, but framing a problem as objective + constraints + variables is exactly
  what this team does — say it that way.
- **Cost model**: fixed + variable cost, $/core-hour, unit cost ($/request),
  attributing shared cost to services, over/under-provisioning tradeoff.

---

## ML-specific mini-framework (if they go there)
1. **Frame it**: regression/forecast/classification? What's predicted, at what
   horizon, how is it used downstream?
2. **Data & features**: sources, granularity, leakage risks, lag/rolling/seasonal
   features, train/val/test split **by time** (never random for time series).
3. **Model**: start simple (baseline: last value / seasonal naive / linear),
   justify before reaching for anything fancy.
4. **Evaluation**: pick a metric tied to the business (MAPE/RMSE; or cost of
   over- vs under-forecast — they're asymmetric here!). **Backtest** on rolling
   windows.
5. **Serving & monitoring**: batch vs real-time, retraining cadence, drift/alerting.

> Senior signal: "Under-forecasting capacity risks an outage; over-forecasting
> wastes money. Those errors aren't symmetric, so I'd optimize an asymmetric loss
> / add a safety buffer, not just minimize RMSE." Say something like that.

---

## Anti-patterns to avoid
- Jumping to a solution before clarifying requirements.
- Naming technologies without justifying them ("I'd use Kafka" — *why?*).
- Designing for Google scale when they said 100 servers.
- Going silent. Keep narrating; the framework is your safety rail.
