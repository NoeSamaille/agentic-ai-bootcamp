"""backend_client.py – Quick tester for the Merck Supply Mock API
================================================================
Fixed: removed Python 3.12 *global-before-use* SyntaxError.

Usage examples:
    python backend_client.py events --limit 5
    python backend_client.py inventory MAT-123
    python backend_client.py performance SUP-001
    python backend_client.py route-risk "Hamburg Port"
    python backend_client.py risk SUP-001
    python backend_client.py add-event '{"supplier_id":"SUP-001", ...}'
"""
from __future__ import annotations

import os
import sys
import json
import argparse
from typing import Optional

import requests
from rich import print  # rich pretty-print
from rich.console import Console
from rich.table import Table

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_BASE_URL = os.getenv("SUPPLY_BASE_URL", "http://localhost:8000")
console = Console()

def _full(path: str, base_url: str) -> str:
    return f"{base_url.rstrip('/')}{path}"

# ---------------------------------------------------------------------------
# API wrappers
# ---------------------------------------------------------------------------

def fetch_events(base_url: str, since: Optional[str], limit: int):
    params = {"limit": str(limit)}
    if since:
        params["since"] = since
    r = requests.get(_full("/events", base_url), params=params, timeout=15)
    r.raise_for_status()
    events = r.json()
    table = Table(title=f"Events (showing {len(events)})")
    table.add_column("id", style="cyan")
    table.add_column("stamp")
    table.add_column("supplier", style="magenta")
    table.add_column("type")
    table.add_column("delay h")
    for ev in events:
        table.add_row(
            ev["event_id"],
            ev["timestamp"].split("T")[0],
            ev["supplier_id"],
            ev["event_type"],
            str(ev.get("delay_hours") or "-"),
        )
    console.print(table)


def fetch_inventory(base_url: str, material_id: str):
    r = requests.get(_full(f"/materials/{material_id}/inventory", base_url), timeout=10)
    r.raise_for_status()
    console.print_json(data=r.json())


def fetch_performance(base_url: str, supplier_id: str):
    r = requests.get(_full(f"/suppliers/{supplier_id}/performance", base_url), timeout=10)
    r.raise_for_status()
    console.print_json(data=r.json())


def fetch_route_risk(base_url: str, location: str):
    r = requests.get(_full(f"/route-risk/{location}", base_url), timeout=10)
    r.raise_for_status()
    console.print_json(data=r.json())


def fetch_supplier_risk(base_url: str, supplier_id: str):
    r = requests.get(_full(f"/suppliers/{supplier_id}/risk", base_url), timeout=10)
    r.raise_for_status()
    console.print_json(data=r.json())


def add_event_from_json(base_url: str, json_str: str):
    try:
        payload = json.loads(json_str)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Invalid JSON:[/red] {exc}")
        sys.exit(1)
    r = requests.post(_full("/events", base_url), json=payload, timeout=10)
    r.raise_for_status()
    console.print("[green]Event created:[/green]")
    console.print_json(data=r.json())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Merck Supply Mock API client")
    ap.add_argument("command", choices=[
        "events", "inventory", "performance", "route-risk", "risk", "add-event"
    ])
    ap.add_argument("param1", nargs="?", help="ID or JSON depending on command")
    ap.add_argument("--limit", type=int, default=10, help="events limit (for events cmd)")
    ap.add_argument("--since", help="ISO timestamp filter (for events cmd)")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base url (default env SUPPLY_BASE_URL or localhost:8000)")

    args = ap.parse_args()
    base_url = args.base_url.rstrip("/")

    try:
        if args.command == "events":
            fetch_events(base_url, args.since, args.limit)
        elif args.command == "inventory":
            if not args.param1:
                ap.error("material_id required for inventory command")
            fetch_inventory(base_url, args.param1)
        elif args.command == "performance":
            if not args.param1:
                ap.error("supplier_id required for performance command")
            fetch_performance(base_url, args.param1)
        elif args.command == "route-risk":
            if not args.param1:
                ap.error("location required for route-risk command")
            fetch_route_risk(base_url, args.param1)
        elif args.command == "risk":
            if not args.param1:
                ap.error("supplier_id required for risk command")
            fetch_supplier_risk(base_url, args.param1)
        elif args.command == "add-event":
            if not args.param1:
                ap.error("JSON payload required for add-event command")
            add_event_from_json(base_url, args.param1)
    except requests.HTTPError as exc:
        console.print(f"[red]HTTP error {exc.response.status_code}[/red] – {exc.response.text}")
    except requests.RequestException as exc:
        console.print(f"[red]Request failed:[/red] {exc}")


if __name__ == "__main__":
    main()

