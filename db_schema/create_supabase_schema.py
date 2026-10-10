"""Create the full schema in a Supabase project without the database password.

The service key cannot run DDL (it only talks to PostgREST). This script uses
the Supabase Management API instead, which accepts arbitrary SQL, authenticated
with a personal access token (PAT):

    Dashboard -> Account settings -> Access Tokens -> New token

Usage:
    1. Put the token in .env as SUPABASE_ACCESS_TOKEN (never commit it).
    2. python -m db_schema.create_supabase_schema
    3. Revoke the token in the dashboard.

Idempotent: rerunning skips existing tables/constraints/indexes
(same SQL as db_schema/supabase_schema.sql).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SQL_FILE = Path(__file__).parent / "supabase_schema.sql"
API_BASE = "https://api.supabase.com/v1"


def project_ref() -> str:
    url = os.environ.get("SUPABASE_URL", "")
    host = urllib.parse.urlsplit(url).hostname or ""
    ref = host.split(".")[0] if host else ""
    if not ref:
        sys.exit("SUPABASE_URL is not set or does not look like https://<ref>.supabase.co")
    return ref


def run_sql(ref: str, token: str, sql: str) -> None:
    req = urllib.request.Request(
        f"{API_BASE}/projects/{ref}/database/query",
        data=json.dumps({"query": sql}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        sys.exit(f"Management API error {exc.code}: {detail}")
    print(f"SQL executed against project {ref}.")
    for item in body if isinstance(body, list) else [body]:
        if isinstance(item, dict) and item.get("success") is False:
            sys.exit(f"Statement failed: {item}")
        if isinstance(item, dict) and "error" in item and item["error"]:
            sys.exit(f"Statement failed: {item['error']}")


def main() -> None:
    token = os.environ.get("SUPABASE_ACCESS_TOKEN", "").strip()
    if not token:
        sys.exit(
            "SUPABASE_ACCESS_TOKEN is not set.\n"
            "Create a personal access token:\n"
            "  Dashboard -> Account settings -> Access Tokens -> New token\n"
            "then add it to .env as SUPABASE_ACCESS_TOKEN=...\n"
            "(or run db_schema/supabase_schema.sql in the SQL Editor instead)."
        )
    sql = SQL_FILE.read_text(encoding="utf-8")
    run_sql(project_ref(), token, sql)


if __name__ == "__main__":
    main()
