#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Spin up a local PostgreSQL with the practice dataset loaded.
# Postgres is the most common interview SQL, so this is the recommended path.
#
# Usage:
#   ./setup_pg.sh            # uses Docker (no local Postgres install needed)
#   ./setup_pg.sh --local    # loads into an already-running local Postgres
#
# After it finishes it prints a connection string. Practice with:
#   psql "$PREP_URL" -c "SELECT * FROM servers LIMIT 5;"
#   psql "$PREP_URL" -f myscratch.sql
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

# 1. Make sure the data file exists (idempotent, deterministic).
python3 build_db.py >/dev/null
echo "✔ generated seed.sql"

MODE="${1:-docker}"

if [ "$MODE" = "--local" ]; then
  # Load into an existing local server. Override host/user/db via env if needed.
  : "${PGHOST:=localhost}"; : "${PGPORT:=5432}"; : "${PGUSER:=$USER}"; : "${PGDATABASE:=prep}"
  createdb "$PGDATABASE" 2>/dev/null || true
  psql -d "$PGDATABASE" -q -f schema.sql -f seed.sql
  echo "✔ loaded into local Postgres db '$PGDATABASE'"
  echo
  echo "export PREP_URL=postgresql://${PGUSER}@${PGHOST}:${PGPORT}/${PGDATABASE}"
  exit 0
fi

# Docker path -------------------------------------------------------------
if ! command -v docker >/dev/null; then
  echo "Docker not found. Either install Docker, or run:  ./setup_pg.sh --local"
  echo "(or use the zero-install SQLite fallback — see HOW_TO_PRACTICE.md)"
  exit 1
fi

NAME=prep-pg
PORT=5433
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" \
  -e POSTGRES_PASSWORD=prep -e POSTGRES_DB=prep \
  -p ${PORT}:5432 postgres:16 >/dev/null
echo "✔ started Postgres 16 container '$NAME' on localhost:${PORT}"

echo -n "waiting for Postgres to accept connections"
for _ in $(seq 1 30); do
  if docker exec "$NAME" pg_isready -U postgres >/dev/null 2>&1; then break; fi
  echo -n "."; sleep 1
done
echo " ready"

# Load using the CONTAINER's own psql (so no host psql install is required).
cat schema.sql seed.sql | docker exec -i "$NAME" psql -U postgres -d prep -q
echo "✔ loaded schema + data"
echo
if command -v psql >/dev/null; then
  echo "Practice from your terminal (psql client detected):"
  echo "  export PREP_URL=postgresql://postgres:prep@localhost:${PORT}/prep"
  echo "  psql \"\$PREP_URL\" -c \"SELECT * FROM servers LIMIT 5;\""
  echo "  psql \"\$PREP_URL\" -f myscratch.sql"
else
  echo "No psql client on this machine — use the container's psql instead:"
  echo "  docker exec -it $NAME psql -U postgres -d prep        # interactive shell"
  echo "  docker exec -i  $NAME psql -U postgres -d prep < myscratch.sql"
  echo
  echo "(Optional, for a nicer workflow:  brew install libpq && brew link --force libpq"
  echo " then: export PREP_URL=postgresql://postgres:prep@localhost:${PORT}/prep )"
fi
echo
echo "Stop/remove the container later with:  docker rm -f $NAME"
