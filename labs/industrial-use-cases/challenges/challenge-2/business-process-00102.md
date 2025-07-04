
# GFM Bank – Granting a Temporary Overdraft to a Retail Customer  
**Process Code:** `GFM‑BR‑ODR‑001`  
**Maximum duration:** 20 minutes  
**Applies to:** Current‑account overdraft up to €10 000

| Role | Responsibility |
|------|----------------|
| **Teller** | Receives customer request, launches balance enquiry, raises overdraft request to Ops. |
| **Back‑office Clerk** | Verifies request, sets `overdraft_limit_eur`, confirms to teller. |

---

## Step‑by‑Step Workflow (time‑boxed)

| Step | Actor | Action | Target time |
|------|-------|--------|-------------|
| 1 | Teller | Identify customer; show current balance. | 2 min |
| 2 | Teller | Capture overdraft amount ≤ €10 000; phone Ops hotline. | 2 min |
| 3 | Back‑office | Verify customer standing & KYC; locate account. | 4 min |
| 4 | Back‑office | Update `overdraft_limit_eur` = requested amount (UI or API). | 2 min |
| 5 | Back‑office | Read back new limit & Tx‑ref to teller. | 1 min |
| 6 | Teller | Refresh ledger; confirm overdraft now available. | 2 min |
| 7 | Teller | Execute requested payment or advise customer. | 3 min |
| 8 | Teller | Print overdraft confirmation letter; customer signs. | 3 min |
| 9 | Teller | File signed letter in daily batch envelope. | 1 min |

**Total expected time:** **20 minutes**

---

## System Rules

1. Overdraft limit hard‑capped at **€10 000** for retail segment.  
2. Limit is stored in `accounts.overdraft_limit_eur`.  
3. Reversion to 0 occurs automatically 30 days after grant (batch job T + 30).  
4. If request occurs after 18:00 CET, teller files Help‑Desk ticket; Ops processes next business morning.

---

## Audit & Compliance

* “Temporary Overdrafts” report lists every change to `overdraft_limit_eur` > 0.  
* Branch supervisor reviews and signs report by **T + 1 12:00 CET**.  
* Signed customer letter retained per PSD2 record‑keeping (10 years).  

_Last updated: 2025‑05‑16_
