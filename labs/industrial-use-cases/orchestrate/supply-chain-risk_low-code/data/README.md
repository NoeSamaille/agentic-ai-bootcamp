# 📦 Supply Chain Operational Database

This database powers a **Supply Chain Control Tower** by aggregating key operational data—such as inventory levels, supplier performance, transportation risks, and disruption events—into a centralized schema.

---

## 🧱 Database Overview

| Table Name            | Description |
|-----------------------|-------------|
| `inventory_levels`    | Tracks material stock levels and their current status (e.g., low, medium, high). |
| `supplier_performance`| Stores performance ratings of suppliers, essential for procurement and risk assessment. |
| `route_risk`          | Contains risk scores for transportation routes (e.g., ports, terminals), used for logistics planning. |
| `events`              | Logs supply chain disruptions such as customs holds, shipment delays, or material shortages. |

---

## 📊 Schema Details

### `inventory_levels`
| Column         | Type     | Description                         |
|----------------|----------|-------------------------------------|
| `material_id`  | TEXT     | Unique identifier of the material   |
| `description`  | TEXT     | Name/description of the material    |
| `status`       | TEXT     | Risk status: `low`, `medium`, `high`|
| `quantity`     | INTEGER  | Quantity currently in inventory     |

### `supplier_performance`
| Column             | Type     | Description                          |
|--------------------|----------|--------------------------------------|
| `supplier_id`      | TEXT     | Unique supplier identifier           |
| `supplier_name`    | TEXT     | Name of the supplier                 |
| `performance_score`| FLOAT    | Score (0–100) indicating supplier reliability |

### `route_risk`
| Column        | Type     | Description                           |
|---------------|----------|---------------------------------------|
| `location`    | TEXT     | Name of the route or terminal         |
| `risk_score`  | FLOAT    | Risk level on a scale from 0 to 1     |
| `risk_type`   | TEXT     | Type of risk modeling used (e.g., `multi-factor`) |

### `events`
| Column             | Type     | Description                                  |
|--------------------|----------|----------------------------------------------|
| `event_id`         | TEXT     | Unique identifier for the event              |
| `timestamp`        | TEXT     | ISO timestamp of the event                   |
| `supplier_id`      | TEXT     | Related supplier ID                          |
| `supplier_name`    | TEXT     | Related supplier name                        |
| `material_id`      | TEXT     | Material impacted                            |
| `material_description` | TEXT | Description of the impacted material         |
| `event_type`       | TEXT     | Type of disruption (e.g., `customs_hold`)    |
| `delay_hours`      | INTEGER  | Duration of delay (if applicable)            |
| `eta_original`     | TEXT     | Original ETA (nullable)                      |
| `eta_new`          | TEXT     | New ETA (nullable)                           |
| `location`         | TEXT     | Disruption location                          |
| `disruption_reason`| TEXT     | Cause or system reason (e.g., auto-generated)|

---

## 🧠 Use Cases

- Real-time supply chain **monitoring**
- **Risk scoring** of suppliers and logistics nodes
- **Delay forecasting** and **inventory alerting**
- Data source for **AI-based supply chain assistants**

---

## 📌 Notes

- All data are examples
- Ideal for simulation of AI planning agents or orchestration platforms like **IBM watsonx Orchestrate**.
