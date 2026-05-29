#!/usr/bin/env python3
"""
Tiny SQL runner for prep.db so you can practice without installing a DB client.

Usage:
    python3 query.py "SELECT * FROM servers LIMIT 5;"   # inline SQL
    python3 query.py path/to/file.sql                    # SQL from a file
    python3 query.py                                     # interactive REPL

Prints results as an aligned table. Multiple statements in a file are run in
order; the last statement that returns rows is displayed.
"""
import os
import sys
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "prep.db")


def render(cols, rows, max_rows=50):
    if not cols:
        return "(no result set)"
    rows = list(rows)
    shown = rows[:max_rows]
    widths = [len(c) for c in cols]
    for r in shown:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(str(v)))
    line = "  ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
    sep = "  ".join("-" * widths[i] for i in range(len(cols)))
    out = [line, sep]
    for r in shown:
        out.append("  ".join(str(v).ljust(widths[i]) for i, v in enumerate(r)))
    if len(rows) > max_rows:
        out.append(f"... ({len(rows)} rows total, showing {max_rows})")
    else:
        out.append(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
    return "\n".join(out)


def run(conn, sql):
    cur = conn.cursor()
    last = None
    for stmt in [s for s in sql.split(";") if s.strip()]:
        cur.execute(stmt)
        if cur.description:
            cols = [d[0] for d in cur.description]
            last = (cols, cur.fetchall())
    conn.commit()
    if last:
        print(render(*last))
    else:
        print("OK (no rows returned)")


def main():
    if not os.path.exists(DB_PATH):
        sys.exit("prep.db not found. Run:  python3 build_db.py")
    conn = sqlite3.connect(DB_PATH)

    if len(sys.argv) >= 2:
        arg = " ".join(sys.argv[1:])
        if os.path.isfile(arg):
            with open(arg) as f:
                sql = f.read()
        else:
            sql = arg
        try:
            run(conn, sql)
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
        return

    # interactive REPL
    print("prep.db REPL — end statements with ';', Ctrl-D to quit.")
    buf = ""
    try:
        while True:
            line = input("sql> " if not buf else "...> ")
            buf += " " + line
            if ";" in line:
                try:
                    run(conn, buf)
                except sqlite3.Error as e:
                    print(f"SQL error: {e}")
                buf = ""
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
