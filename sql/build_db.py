#!/usr/bin/env python3
"""
Build prep.db: a small, deterministic, cloud-infrastructure-themed dataset for
SQL practice. The theme (regions, data centers, servers, services, daily usage
metrics, cost records, incidents) mirrors the iCloud capacity/cost/forecasting
domain you're interviewing for, so the drills double as light domain prep.

Run once:   python3 build_db.py
Re-run any time to reset the database to a clean state (it drops + recreates).

Deterministic: a fixed RNG seed means everyone gets identical data, so the
solutions in solutions.sql produce the same answers you will.
"""
import os
import random
import sqlite3
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "prep.db")

SCHEMA = """
DROP TABLE IF EXISTS usage_metrics;
DROP TABLE IF EXISTS cost_records;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS deployments;
DROP TABLE IF EXISTS servers;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS data_centers;
DROP TABLE IF EXISTS regions;

CREATE TABLE regions (
    region_id   INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    country     TEXT NOT NULL
);

CREATE TABLE data_centers (
    dc_id            INTEGER PRIMARY KEY,
    region_id        INTEGER NOT NULL REFERENCES regions(region_id),
    name             TEXT NOT NULL,
    capacity_cores   INTEGER NOT NULL,   -- total cores the DC can host
    opened_date      TEXT NOT NULL
);

CREATE TABLE services (
    service_id   INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    team         TEXT NOT NULL,          -- owning team
    tier         TEXT NOT NULL           -- 'critical' | 'standard' | 'batch'
);

CREATE TABLE servers (
    server_id          INTEGER PRIMARY KEY,
    dc_id              INTEGER NOT NULL REFERENCES data_centers(dc_id),
    server_type        TEXT NOT NULL,    -- e.g. 'compute', 'storage', 'gpu'
    cores              INTEGER NOT NULL,
    memory_gb          INTEGER NOT NULL,
    hourly_cost_usd    REAL NOT NULL,
    commissioned_date  TEXT NOT NULL,
    status             TEXT NOT NULL     -- 'active' | 'idle' | 'retired'
);

-- which service runs on which server, over a time interval (end_date NULL = current)
CREATE TABLE deployments (
    deployment_id  INTEGER PRIMARY KEY,
    service_id     INTEGER NOT NULL REFERENCES services(service_id),
    server_id      INTEGER NOT NULL REFERENCES servers(server_id),
    start_date     TEXT NOT NULL,
    end_date       TEXT            -- NULL means still active
);

-- daily time series per server
CREATE TABLE usage_metrics (
    metric_date  TEXT NOT NULL,
    server_id    INTEGER NOT NULL REFERENCES servers(server_id),
    cpu_util     REAL NOT NULL,     -- 0..1 average utilization that day
    mem_util     REAL NOT NULL,     -- 0..1
    requests     INTEGER NOT NULL,  -- total requests served
    PRIMARY KEY (metric_date, server_id)
);

CREATE TABLE cost_records (
    cost_date    TEXT NOT NULL,
    server_id    INTEGER NOT NULL REFERENCES servers(server_id),
    cost_usd     REAL NOT NULL,     -- realized cost that day
    PRIMARY KEY (cost_date, server_id)
);

CREATE TABLE incidents (
    incident_id  INTEGER PRIMARY KEY,
    service_id   INTEGER NOT NULL REFERENCES services(service_id),
    severity     INTEGER NOT NULL,  -- 1 (worst) .. 4
    opened_date  TEXT NOT NULL,
    resolved_date TEXT              -- NULL means still open
);
"""


def main():
    rng = random.Random(42)  # deterministic
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    cur = conn.cursor()

    # --- regions ---
    regions = [
        (1, "us-east", "USA"),
        (2, "us-west", "USA"),
        (3, "eu-central", "Germany"),
        (4, "ap-southeast", "Singapore"),
    ]
    cur.executemany("INSERT INTO regions VALUES (?,?,?)", regions)

    # --- data centers ---
    data_centers = [
        (10, 1, "iad1", 20000, "2018-03-01"),
        (11, 1, "iad2", 16000, "2020-06-15"),
        (12, 2, "sjc1", 24000, "2017-09-10"),
        (13, 3, "fra1", 18000, "2019-01-20"),
        (14, 4, "sin1", 12000, "2021-11-05"),
    ]
    cur.executemany("INSERT INTO data_centers VALUES (?,?,?,?,?)", data_centers)

    # --- services ---
    services = [
        (100, "photos-sync",   "media",    "critical"),
        (101, "backup-store",  "storage",  "critical"),
        (102, "mail-relay",    "comms",    "standard"),
        (103, "notes-sync",    "media",    "standard"),
        (104, "ml-forecast",   "capacity", "batch"),
        (105, "keychain",      "security", "critical"),
        (106, "analytics-etl", "capacity", "batch"),
    ]
    cur.executemany("INSERT INTO services VALUES (?,?,?,?)", services)

    # --- servers ---
    server_types = ["compute", "compute", "storage", "gpu"]
    statuses_pool = ["active"] * 8 + ["idle", "retired"]
    servers = []
    sid = 1000
    for dc_id, *_ in data_centers:
        n = rng.randint(6, 10)
        for _ in range(n):
            stype = rng.choice(server_types)
            cores = rng.choice([16, 32, 64, 96])
            mem = cores * rng.choice([4, 8])
            base = 0.04 * cores + (0.5 if stype == "gpu" else 0.0)
            hourly = round(base * rng.uniform(0.9, 1.2), 3)
            year = rng.choice([2019, 2020, 2021, 2022, 2023])
            month = rng.randint(1, 12)
            comm = f"{year}-{month:02d}-01"
            status = rng.choice(statuses_pool)
            servers.append((sid, dc_id, stype, cores, mem, hourly, comm, status))
            sid += 1
    cur.executemany(
        "INSERT INTO servers VALUES (?,?,?,?,?,?,?,?)", servers
    )
    active_servers = [s for s in servers if s[7] != "retired"]

    # --- deployments: assign 1-2 services per non-retired server ---
    deployments = []
    did = 5000
    for s in active_servers:
        k = rng.randint(1, 2)
        chosen = rng.sample([sv[0] for sv in services], k)
        for svc in chosen:
            start_year = rng.choice([2022, 2023, 2024])
            start = f"{start_year}-{rng.randint(1,12):02d}-01"
            # ~30% have an end_date (rotated off)
            end = None
            if rng.random() < 0.3:
                end = "2025-0%d-01" % rng.randint(1, 3)
            deployments.append((did, svc, s[0], start, end))
            did += 1
    cur.executemany("INSERT INTO deployments VALUES (?,?,?,?,?)", deployments)

    # --- daily usage_metrics + cost_records for 60 days ---
    start_day = date(2025, 3, 1)
    days = [start_day + timedelta(days=i) for i in range(60)]
    usage_rows = []
    cost_rows = []
    for s in active_servers:
        server_id = s[0]
        cores = s[3]
        hourly = s[5]
        # each server has a baseline utilization + weekly seasonality + drift + noise
        base_cpu = rng.uniform(0.2, 0.7)
        drift = rng.uniform(-0.002, 0.004)  # slow trend
        for i, d in enumerate(days):
            dow = d.weekday()  # 0=Mon
            weekend_dip = -0.12 if dow >= 5 else 0.0
            seasonal = 0.06 * ((i % 7) / 6.0)
            noise = rng.uniform(-0.05, 0.05)
            cpu = base_cpu + drift * i + weekend_dip + seasonal + noise
            cpu = min(0.99, max(0.02, cpu))
            mem = min(0.99, max(0.05, cpu * rng.uniform(0.7, 1.1)))
            requests = int(max(0, cpu * cores * rng.uniform(800, 1200)))
            usage_rows.append(
                (d.isoformat(), server_id, round(cpu, 3), round(mem, 3), requests)
            )
            # cost = 24h * hourly, scaled a bit by utilization (variable + fixed)
            daily_cost = 24 * hourly * (0.6 + 0.4 * cpu)
            cost_rows.append((d.isoformat(), server_id, round(daily_cost, 2)))
    cur.executemany(
        "INSERT INTO usage_metrics VALUES (?,?,?,?,?)", usage_rows
    )
    cur.executemany("INSERT INTO cost_records VALUES (?,?,?)", cost_rows)

    # --- incidents ---
    incidents = []
    iid = 9000
    for _ in range(40):
        svc = rng.choice([sv[0] for sv in services])
        sev = rng.choice([1, 2, 2, 3, 3, 3, 4, 4])
        opened = start_day + timedelta(days=rng.randint(0, 59))
        resolved = None
        if rng.random() < 0.8:
            resolved = opened + timedelta(days=rng.randint(0, 6))
            resolved = resolved.isoformat()
        incidents.append((iid, svc, sev, opened.isoformat(), resolved))
        iid += 1
    cur.executemany("INSERT INTO incidents VALUES (?,?,?,?,?)", incidents)

    conn.commit()

    # summary
    print(f"Built {DB_PATH}")
    for tbl in [
        "regions", "data_centers", "services", "servers",
        "deployments", "usage_metrics", "cost_records", "incidents",
    ]:
        n = cur.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl:15s} {n:6d} rows")
    conn.close()


if __name__ == "__main__":
    main()
