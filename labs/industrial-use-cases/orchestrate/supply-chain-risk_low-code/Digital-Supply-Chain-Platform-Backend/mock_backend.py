"""Mock Supply-Chain Backend – SQLite Big Dataset Edition
=======================================================
Merck *Disruption-Response* demo with:
  • **SQLite** persistent store (`merck_supply.db` by default)
  • **10 000+ synthetic events** auto-generated into **data.sql** the first time you run
  • **Extra tables** for richer prompts:
        – `inventory_levels`  (criticality & days of supply)
        – `supplier_performance` (on-time % over last 90 days)
        – `route_risk` (risk score + factors)
  • FastAPI endpoints:
        GET  /events?since=ISO
        POST /events
        GET  /suppliers/{id}/risk              (combined risk index)
        GET  /suppliers/{id}/performance       (on-time metric)
        GET  /materials/{id}/inventory         (stock & criticality)
        GET  /route-risk/{location}

Run locally
-----------
    pip install fastapi uvicorn pydantic faker
    uvicorn mock_backend:app --reload --port 8000
(The first start takes ~5 s while it fabricates the dataset.)
"""
from __future__ import annotations

import os
import uuid
import random
import sqlite3
import datetime as _dt
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

try:
    from faker import Faker  # used *only* for initial data synthesis
except ImportError:  # pragma: no cover
    Faker = None  # type: ignore

# ---------------------------------------------------------------------------
# 1.  Configuration & helpers
# ---------------------------------------------------------------------------
DB_PATH = os.getenv("SUPPLY_DB_PATH", "merck_supply.db")
DATASET_SQL_PATH = Path(os.getenv("SUPPLY_DATASET_SQL", "data.sql"))
EVENT_COUNT = int(os.getenv("SUPPLY_EVENT_COUNT", "10000"))

_SUPPLIERS = [
    ("SUP-001", "Acme PharmaChem"),
    ("SUP-002", "Globex Logistics"),
    ("SUP-003", "OmniRaw Materials"),
    ("SUP-004", "Northwind Bio"),
    ("SUP-005", "Pinnacle MedTrans"),
]
_MATERIALS = [
    ("MAT-123", "Active Ingredient X"),
    ("MAT-456", "Packaging Material B"),
    ("MAT-789", "Buffer Solution C"),
    ("MAT-321", "Excipient Y"),
    ("MAT-654", "Filler Z"),
]
_EVENT_TYPES = [
    "shipment_delay",
    "quality_issue",
    "customs_hold",
    "raw_material_shortage",
    "transport_strike",
]
_LOCATIONS = [
    "Hamburg Port",
    "Frankfurt Airport",
    "Munich Rail Terminal",
    "Rotterdam Port",
    "Berlin Warehouse",
]

# ---------------------------------------------------------------------------
# 2.  Database bootstrap
# ---------------------------------------------------------------------------

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
CREATE TABLE IF NOT EXISTS events (
    event_id            TEXT PRIMARY KEY,
    timestamp           TEXT,
    supplier_id         TEXT,
    supplier_name       TEXT,
    material_id         TEXT,
    material_description TEXT,
    event_type          TEXT,
    delay_hours         INTEGER,
    eta_original        TEXT,
    eta_new             TEXT,
    location            TEXT,
    disruption_reason   TEXT
);

CREATE TABLE IF NOT EXISTS inventory_levels (
    material_id          TEXT PRIMARY KEY,
    material_description TEXT,
    criticality          TEXT,
    on_hand_days         INTEGER
);

CREATE TABLE IF NOT EXISTS supplier_performance (
    supplier_id   TEXT PRIMARY KEY,
    supplier_name TEXT,
    on_time_percent_90d REAL
);

CREATE TABLE IF NOT EXISTS route_risk (
    location     TEXT PRIMARY KEY,
    risk_score   REAL,
    risk_factors TEXT
);
        """
    )
    conn.commit()


def _rowcount(conn: sqlite3.Connection, table: str) -> int:
    cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
    return cur.fetchone()[0]


# ---------------------------------------------------------------------------
# 3.  Synthetic dataset fabrication (only on first launch)
# ---------------------------------------------------------------------------

def _rand_dt(within_days: int = 90) -> _dt.datetime:
    now = _dt.datetime.utcnow()
    delta = _dt.timedelta(days=random.randint(0, within_days), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return now - delta


def _gen_event_sql(fake) -> str:  # type: ignore[override]
    supplier_id, supplier_name = random.choice(_SUPPLIERS)
    material_id, material_description = random.choice(_MATERIALS)
    event_type = random.choice(_EVENT_TYPES)
    delay_hours = None
    eta_orig = eta_new = None

    if event_type in {"shipment_delay", "customs_hold", "transport_strike"}:
        delay_hours = random.choice([6, 12, 24, 36, 48])
        eta_orig_dt = _rand_dt()
        eta_new_dt = eta_orig_dt + _dt.timedelta(hours=delay_hours)
        eta_orig = eta_orig_dt.isoformat()
        eta_new = eta_new_dt.isoformat()

    disruption_reason = fake.sentence(nb_words=4) if fake else "autogen disruption"
    location = random.choice(_LOCATIONS)

    return (
        "INSERT INTO events VALUES ('EVT-{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}');".format(
            uuid.uuid4().hex[:8],
            _rand_dt().isoformat(),
            supplier_id,
            supplier_name,
            material_id,
            material_description,
            event_type,
            delay_hours if delay_hours is not None else "NULL",
            f"'{eta_orig}'" if eta_orig else "NULL",
            f"'{eta_new}'" if eta_new else "NULL",
            location,
            disruption_reason.replace("'", "''"),
        )
    )


def _build_dataset_sql() -> str:
    fake = Faker() if Faker else None

    sql_lines: List[str] = []

    # inventory_levels
    for material_id, material_description in _MATERIALS:
        criticality = random.choice(["low", "medium", "high"])
        on_hand = random.randint(2, 30)
        sql_lines.append(
            "INSERT INTO inventory_levels VALUES ('{}', '{}', '{}', {});".format(
                material_id, material_description, criticality, on_hand
            )
        )

    # supplier_performance
    for supplier_id, supplier_name in _SUPPLIERS:
        on_time = round(random.uniform(75, 99), 2)
        sql_lines.append(
            "INSERT INTO supplier_performance VALUES ('{}', '{}', {});".format(
                supplier_id, supplier_name, on_time
            )
        )

    # route_risk
    for loc in _LOCATIONS:
        risk = round(random.uniform(0, 1), 2)
        factors = (fake.sentence(nb_words=6) if fake else "multi-factor")
        sql_lines.append(
            "INSERT INTO route_risk VALUES ('{}', {}, '{}');".format(
                loc, risk, factors.replace("'", "''")
            )
        )

    # events (many!)
    sql_lines.append("-- 10k+ events")
    for _ in range(EVENT_COUNT):
        sql_lines.append(_gen_event_sql(fake))

    return "\n".join(sql_lines)


def _populate_if_empty(conn: sqlite3.Connection) -> None:
    if _rowcount(conn, "events") > 0:
        return  # already populated

    print("[bootstrap] generating synthetic dataset ({} events)…".format(EVENT_COUNT))
    sql_blob = _build_dataset_sql()
    # write to file so the user has a standalone dataset snapshot
    DATASET_SQL_PATH.write_text(sql_blob, encoding="utf-8")
    conn.executescript(sql_blob)
    conn.commit()


# initialise database (runs once at module import)
conn0 = _connect()
_create_schema(conn0)
_populate_if_empty(conn0)
conn0.close()

# ---------------------------------------------------------------------------
# 4.  Pydantic view models
# ---------------------------------------------------------------------------
class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8]}")
    timestamp: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
    supplier_id: str
    supplier_name: str
    material_id: str
    material_description: str
    event_type: str
    delay_hours: Optional[int] = None
    eta_original: Optional[_dt.datetime] = None
    eta_new: Optional[_dt.datetime] = None
    location: Optional[str] = None
    disruption_reason: Optional[str] = None

class InventoryLevel(BaseModel):
    material_id: str
    material_description: str
    criticality: str
    on_hand_days: int

class SupplierPerformance(BaseModel):
    supplier_id: str
    supplier_name: str
    on_time_percent_90d: float

class RouteRisk(BaseModel):
    location: str
    risk_score: float
    risk_factors: str

# ---------------------------------------------------------------------------
# 5.  FastAPI endpoints
# ---------------------------------------------------------------------------
app = FastAPI(title="Merck Supply Events API (SQLite)", version="0.3.0")

# helper – convert sqlite Row → Event

def _row_to_event(r: sqlite3.Row) -> Event:
    return Event(
        event_id=r["event_id"],
        timestamp=_dt.datetime.fromisoformat(r["timestamp"]),
        supplier_id=r["supplier_id"],
        supplier_name=r["supplier_name"],
        material_id=r["material_id"],
        material_description=r["material_description"],
        event_type=r["event_type"],
        delay_hours=r["delay_hours"],
        eta_original=_dt.datetime.fromisoformat(r["eta_original"]) if r["eta_original"] else None,
        eta_new=_dt.datetime.fromisoformat(r["eta_new"]) if r["eta_new"] else None,
        location=r["location"],
        disruption_reason=r["disruption_reason"],
    )


@app.get("/events", response_model=List[Event])
def get_events(
    since: Optional[_dt.datetime] = Query(None, description="Return events after this UTC timestamp"),
    limit: int = Query(1000, ge=1, le=10000, description="Max rows to return (default 1000)"),
):
    conn = _connect()
    if since:
        rows = conn.execute(
            "SELECT * FROM events WHERE timestamp > ? ORDER BY timestamp DESC LIMIT ?",
            (since.isoformat(), limit),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [_row_to_event(r) for r in rows]


@app.post("/events", response_model=Event, status_code=201)
def add_event(event: Event):
    conn = _connect()
    conn.execute(
        "INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            event.event_id,
            event.timestamp.isoformat(),
            event.supplier_id,
            event.supplier_name,
            event.material_id,
            event.material_description,
            event.event_type,
            event.delay_hours,
            event.eta_original.isoformat() if event.eta_original else None,
            event.eta_new.isoformat() if event.eta_new else None,
            event.location,
            event.disruption_reason,
        ),
    )
    conn.commit()
    conn.close()
    return event


@app.get("/suppliers/{supplier_id}/performance", response_model=SupplierPerformance)
def get_performance(supplier_id: str):
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM supplier_performance WHERE supplier_id=?", (supplier_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return SupplierPerformance(
        supplier_id=row["supplier_id"],
        supplier_name=row["supplier_name"],
        on_time_percent_90d=row["on_time_percent_90d"],
    )


@app.get("/materials/{material_id}/inventory", response_model=InventoryLevel)
def get_inventory(material_id: str):
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM inventory_levels WHERE material_id=?", (material_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Material not found")
    return InventoryLevel(
        material_id=row["material_id"],
        material_description=row["material_description"],
        criticality=row["criticality"],
        on_hand_days=row["on_hand_days"],
    )


@app.get("/route-risk/{location}", response_model=RouteRisk)
def get_route_risk(location: str):
    conn = _connect()
    row = conn.execute("SELECT * FROM route_risk WHERE location=?", (location,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Location not found")
    return RouteRisk(
        location=row["location"], risk_score=row["risk_score"], risk_factors=row["risk_factors"]
    )


@app.get("/suppliers/{supplier_id}/risk")
def supplier_risk(supplier_id: str):
    """Aggregate delay frequency & on-time %, return 0-1 risk index."""
    conn = _connect()
    perf = conn.execute(
        "SELECT on_time_percent_90d FROM supplier_performance WHERE supplier_id=?",
        (supplier_id,),
    ).fetchone()
    events = conn.execute(
        "SELECT delay_hours FROM events WHERE supplier_id=?", (supplier_id,)
    ).fetchall()
    conn.close()

    if not perf or not events:
        raise HTTPException(status_code=404, detail="Supplier not found")

    high_delay = [e["delay_hours"] for e in events if e["delay_hours"] and e["delay_hours"] >= 24]
    delay_ratio = len(high_delay) / len(events)
    on_time_metric = perf["on_time_percent_90d"] / 100.0
    risk_index = round(min(1.0, 0.7 * delay_ratio + 0.3 * (1 - on_time_metric)), 2)

    return {"supplier_id": supplier_id, "risk_index": risk_index}


# ---------------------------------------------------------------------------
# 6.  Dev entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mock_backend:app", host="0.0.0.0", port=8000, reload=True)

