# GFM Bank – Branch Transfer Amount Correction  
**Process Code:** `GFM‑BR‑TFR‑013`  
**Applies to:** All branches using teller system **“GFM Core 7.2”**  
**Maximum duration:** **25 minutes**

---

## 1. Objectives
1. Restore customer funds when an internal transfer is posted with the wrong amount.  
2. Preserve dual (four‑eyes) control between front office and back office.  
3. Provide a clear audit trail and daily reconciliation entry.

## 2. Roles
| Role | Responsibility |
|------|----------------|
| **Teller** (branch) | Posts transfers, detects errors, communicates with customer and back office. |
| **Back‑office clerk** (Ops Centre) | Posts reversing credit, logs exception, reconciles at end of day. |

## 3. Time‑boxed Workflow <sub>(24 min target &le; 25 min SLA)</sub>

| Step | Actor | Action | Target time |
|------|-------|--------|-------------|
| 1 | Teller | Verify customer identity and display balance. | 2 min |
| 2 | Teller | Capture transfer details, read back amount aloud. | 2 min |
| 3 | Teller | Post transaction and hand receipt to customer. | 1 min |
| 4 | Teller | Detect the wrong amount (self‑check or customer alert). | 1 min |
| 5 | Teller | Call back‑office hotline, quote original Tx‑ID. | 2 min |
| 6 | Back‑office | Locate transaction in system. | 3 min |
| 7 | Back‑office | Post reversing **credit** (same amount). | 3 min |
| 8 | Back‑office | Confirm reversal Tx‑ID to teller. | 1 min |
| 9 | Teller | Refresh ledger, confirm funds restored. | 2 min |
| 10 | Teller | Post **correct** transfer amount. | 2 min |
| 11 | Teller | Print final receipt, obtain customer signature. | 2 min |
| 12 | Teller | File signed receipt in daily batch envelope. | 2 min |
| 13 | Back‑office | Log exception for end‑of‑day report. | 2 min |

> **Total expected time:** **24 minutes**

## 4. System Procedures
* The reversal is a separate **credit** entry that references the original Tx‑ID in the narrative.  
* Reversal **must occur on the same business date (T + 0)**.  
* After 18:00 CET cutoff, teller opens a Help‑Desk ticket instead of phone reversal.

## 5. Audit & Reconciliation
* Daily *“Wrong Amount Transfers”* report lists every Step‑7 reversal for supervisor review.  
* Branch manager signs the report by **T + 1 12:00 CET**.

---

_Last updated: 2025‑05‑16_
