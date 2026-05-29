# How to actually practice (start here)

This answers two things: **how to run the practice problems**, and **the loop you
repeat to build fluency**. Postgres is the primary target (it's the most common
interview SQL); a zero-install SQLite fallback is included.

---

## Part 1 — Get a database running

Pick ONE. If you're not sure, pick A.

### Option A — Postgres via Docker (recommended, closest to a real interview)
You need Docker installed (no separate Postgres install required). One command:
```bash
cd sql
./setup_pg.sh
```
The script loads the data using the **container's own** `psql`, so it works even
if you don't have a `psql` client on your Mac. When it finishes it prints how to
connect, based on what you have:

- **If you have a `psql` client** (`brew install libpq && brew link --force libpq`):
  ```bash
  export PREP_URL=postgresql://postgres:prep@localhost:5433/prep
  psql "$PREP_URL" -c "SELECT * FROM servers LIMIT 5;"
  ```
- **If you don't** — just use the container's psql:
  ```bash
  docker exec -it prep-pg psql -U postgres -d prep          # interactive shell
  docker exec -i  prep-pg psql -U postgres -d prep < myscratch.sql   # run a file
  ```

Stop it later with `docker rm -f prep-pg`. Re-run `./setup_pg.sh` any time to reset.

### Option B — Postgres you already have installed
```bash
cd sql
./setup_pg.sh --local          # creates a 'prep' db and loads it
export PREP_URL=postgresql://$USER@localhost:5432/prep
```
(If your server uses different host/user, set `PGHOST`/`PGUSER`/`PGPORT` first.)

### Option C — SQLite, zero install (works fully offline)
No server needed; Python's built-in SQLite supports CTEs and window functions.
```bash
cd sql
python3 build_db.py            # creates prep.db
```
Use `solutions_sqlite.sql` instead of `solutions.sql` for the few queries that
differ (dates/rounding). Everything else is identical.

> The dataset is **identical** across all three — same numbers, same answers.

---

## Part 2 — Run a query (three equivalent ways)

**Postgres with a host `psql` client (Options A/B):**
```bash
# one-off query inline:
psql "$PREP_URL" -c "SELECT * FROM servers LIMIT 5;"

# run a file of SQL you wrote:
psql "$PREP_URL" -f myscratch.sql

# interactive shell (type queries, end with ; , quit with \q):
psql "$PREP_URL"
```

**Postgres via Docker without a host `psql` (most common on a fresh Mac):**
```bash
docker exec -it prep-pg psql -U postgres -d prep            # interactive shell
docker exec -i  prep-pg psql -U postgres -d prep -c "SELECT * FROM servers LIMIT 5;"
docker exec -i  prep-pg psql -U postgres -d prep < myscratch.sql   # run a file
```
Handy psql tips inside the shell: `\dt` lists tables, `\d servers` describes a
table, `\x` toggles expanded (vertical) output for wide rows.

**SQLite (Option C):** use the included runner.
```bash
python3 query.py "SELECT * FROM servers LIMIT 5;"   # inline
python3 query.py myscratch.sql                       # from a file
python3 query.py                                     # interactive REPL
```

---

## Part 3 — The loop for SOLVING a problem (do this every time)

Problems live in `sql/problems.md` (30 of them, grouped by topic). For each:

1. **Read the problem.** Note the expected output columns.
2. **Open a scratch file** to write your attempt:
   ```bash
   cd sql
   $EDITOR myscratch.sql        # or just use the interactive shell
   ```
   (Files matching `*scratch*` are git-ignored, so write freely.)
3. **Say the plan out loud** before typing (tables? join keys? grain? filter
   before or after aggregation?). This rehearses the interview narration.
4. **Write and run it:**
   ```bash
   psql "$PREP_URL" -f myscratch.sql        # Postgres
   # or
   python3 query.py myscratch.sql           # SQLite
   ```
5. **Sanity-check** the output: right number of rows? values plausible?
6. **Only now** open the solution and compare:
   - Postgres: `sql/solutions.sql`   ·   SQLite: `sql/solutions_sqlite.sql`
   - Find a specific answer, e.g. Q16:
     ```bash
     grep -n "Q16" sql/solutions.sql      # find the line, then read that block
     ```
7. **If you got it wrong or peeked → mark it.** Redo it from a blank screen later
   the same day, and again tomorrow. That re-doing is the whole point.

### Concrete first run (copy/paste to confirm everything works)
```bash
cd sql
# Q1: servers in data center iad1
psql "$PREP_URL" -c "
  SELECT s.server_id, s.server_type, s.cores
  FROM servers s JOIN data_centers d ON d.dc_id = s.dc_id
  WHERE d.name = 'iad1';"
```
Compare with the Q1 block in `solutions.sql`. That's the entire workflow.

---

## Part 4 — Python practice

```bash
cd python
python3 patterns.py     # reference implementations + self-tests (should print ✔)
python3 drills.py        # 10 role-flavored drills + tests (should print ✔)
```
To practice a drill: open `drills.py`, **replace one function body with `pass`**,
re-implement it from scratch, then run `python3 drills.py` until it's green again.
Repeat tomorrow from blank. `python/problems.md` lists the problems + test cases.

---

## Part 5 — The weekly rhythm

Follow `week_plan/day1…day7`. Each day = warm-up (re-type yesterday's patterns
from memory) → new drills → redo 2 old problems cold → note what was shaky.
Cheatsheets in `cheatsheets/` are meant to be **re-typed from a blank screen
daily** — that repetition is what makes the syntax automatic under pressure.

Daily checklist:
- [ ] Re-typed yesterday's patterns from memory
- [ ] Did today's new problems, narrating out loud
- [ ] Redid 2 earlier problems cold
- [ ] Wrote down the one thing that tripped me up (→ tomorrow's warm-up)

---

## Troubleshooting
- `psql: command not found` → you don't have a host Postgres client. Either use
  the container's psql (`docker exec -it prep-pg psql -U postgres -d prep`),
  install one (`brew install libpq && brew link --force libpq`), or use the
  SQLite fallback (Option C).
- `PREP_URL` empty → re-run the `export PREP_URL=...` line from setup output.
- Docker port in use → edit `PORT` in `setup_pg.sh` (default 5433).
- Want to reset data → re-run `./setup_pg.sh` (Postgres) or `python3 build_db.py` (SQLite).
- `ROUND(...)` errors on Postgres → cast doubles to numeric: `ROUND(x::numeric, 2)`
  (this is why the Postgres solutions cast `cpu_util` — a classic gotcha worth knowing).
