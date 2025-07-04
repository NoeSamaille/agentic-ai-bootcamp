# Agentic AI Challenge #2: 
# Branch Banking — Overdraft & Transfer Reversal

![Bank teller counter](https://thumbs.dreamstime.com/b/motion-people-talking-to-teller-service-counter-inside-td-bank-coquitlam-bc-canada-may-motion-people-talking-to-125479505.jpg)

## Overview

Refactor the classic **GFM Bank** branch‑office application into an **Agentic AI system** powered by **watsonx**. Participants will build cooperating **Teller** and **Back‑office** agents that use the live Core‑Banking API to grant temporary overdrafts, execute payments and perform same‑day reversals, all while enforcing the business rules defined below.

> **Important** — The agent clients **must** call the production Core‑Banking System deployed at:
>
> ```text
> https://gfm-corebanking-backend.1944johjccn7.eu-de.codeengine.appdomain.cloud
> ```
>
> Obtain an access‑token via `POST /token` (password grant) and send it as `Authorization: Bearer <token>` on every subsequent request. See the Swagger specification for field names and response schemas. citeturn2file0

---

## Core‑Banking API Cheat‑Sheet

| Purpose              | Method & Path                                                  | Mandatory Fields                                            | Notes                                                                                                                  |
| -------------------- | -------------------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Login**            | `POST /token`                                                  | `username`, `password`, `grant_type="password"`             | Returns `{access_token, token_type}`.                                                                                  |
| **List accounts**    | `GET /accounts`                                                | –                                                           | Returns array of accounts belonging to the logged‑in customer.                                                         |
| **Account details**  | `GET /accounts/{account_id}`                                   | –                                                           | Includes `balance_eur` and `overdraft_limit_eur`.                                                                      |
| **Transactions**     | `GET /transactions/{account_id}`                               | –                                                           | Ordered latest‑first.                                                                                                  |
| **Money transfer**   | `POST /transfer`                                               | `source_account_id`, `destination_account_id`, `amount_eur` | Amount > 0 €. Returns `tx_id`.                                                                                         |
| **Set overdraft**    | `PATCH /accounts/{account_id}/overdraft?limit_eur={new_limit}` | Path & query params                                         | Must be **1 000 – 10 000** €.                                                                                          |
| **(Bonus) Reversal** | *Not in core API*                                              | –                                                           | Implement by posting a compensating transfer **back** to the source IBAN and linking the original `tx_id` in metadata. |

> **Hint:** you may wrap the above endpoints with LangChain `RequestsTool` or build thin python SDKs `teller_client.py` and `backoffice_client.py` that expose functions such as `get_balance()`, `transfer()`, `set_overdraft()`, and `reverse()`. Register these functions as **tool‑calls** in your agent framework so the LLM can invoke them autonomously.

---

## Challenge Objective

Create an autonomous assistant that can guide a retail customer through the following conversation **without human intervention**:

1. "Transfer **€8 000** from my IBAN **DE71 … 890** to **DE55 … 123**."
2. "Insufficient funds? OK, grant me an overdraft of **€5 000**."
3. "Great – now retry the transfer."
4. "Oops, I sent too much — please reverse that transfer."

The system must carry out the operations through the API, return concise status messages and keep the ledger consistent.

---

### Functional Requirements

1. **Conversation & Reasoning**

   * Accept free‑text input for balance, transfer, overdraft and reversal requests.
   * Decide when the Teller agent may act locally and when it must escalate to Back‑office.

2. **API Integration**

   * All database actions **must** go through the hosted Core‑Banking API (no direct SQLite access).
   * Store the base URL and credentials in environment variables (`BANK_API_URL`, `BANK_USER`, `BANK_PASS`).
   * Implement automatic token refresh on HTTP 401.

3. **Business‑Rule Enforcement**

   * Overdraft amount must be **€1 000 – 10 000**.
   * No automatic overdraft suggestions — only on explicit customer request.
   * Reversals must reference the original `tx_id` (e.g. via a `metadata.ref_tx_id` field) and occur on the same business date.

4. **watsonx & Agentic Frameworks**

   * Orchestrate the flow with **Watsonx Orchestrate**, **watsonx.ai function calling**, **LangGraph**, **CrewAI**, **Autogen**, etc.
   * Register each endpoint wrapper as a tool so the LLM can plan ➜ call ➜ observe.

---

## User Story

> **Title:** AI‑powered Teller & Back‑office Assistant for Retail Overdrafts
>
> **As a** retail customer at GFM Bank,
> **I want** to chat with an AI assistant to request overdrafts, send payments and undo mistakes,
> **So that** I can manage my account quickly without waiting in line.

---

## Expected Solution Workflow

1. **Transfer Attempt**
   *Teller Agent* checks balance via `GET /accounts/{id}`.
   If funds are insufficient it informs the user and shows the available amount.

2. **Explicit Overdraft Request**
   Upon "Grant me an overdraft of €X", Teller forwards a `PATCH /accounts/{id}/overdraft` call to *Back‑office Agent*.

3. **Overdraft Approval Logic**
   Back‑office verifies `1 000 ≤ X ≤ 10 000`.

   * If valid: approves and returns new limit.
   * Else: rejects with reason.

4. **Transfer Execution**
   Teller retries the original `POST /transfer`.

5. **Transfer Reversal**
   Teller routes to Back‑office; Back‑office posts a compensating transfer and stores `metadata.ref_tx_id`.

6. **Conversation Closure**
   Teller summarises all actions and shows the final balance via `GET /accounts/{id}`.

Add a state‑machine or agent‑graph diagram (`docs/architecture.png`) to illustrate the control flow.

---

## Evaluation Criteria

| Weight | Criterion                 | What we look for                                                                               |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------------- |
| 35 %   | **Accuracy & Compliance** | Correct enforcement of overdraft range, proper reversal referencing `tx_id`, ledger integrity. |
| 25 %   | **Agentic Design**        | Clear Teller vs Back‑office separation, autonomous decision‑making, watsonx tool‑usage.        |
| 20 %   | **Integration Quality**   | Robust HTTP calls, JWT refresh, error handling, idempotency, `.env` secrets.                   |
| 10 %   | **User Experience**       | Natural language, helpful confirmations, optional DE/EN localisation.                          |
| 10 %   | **Documentation**         | Setup guide, test script, architecture diagram.                                                |

### Bonus Points

* Nightly job (agent) that resets expired overdrafts.
* PSD2‑style audit log + Retriever to answer "Why was my overdraft approved?".
* watsonx Prompt Lab to fine‑tune policy checks.

---

## Getting Started

1. Clone this repo and create a virtual‑env.
2. Copy `.env.example` ➜ `.env` and fill in `BANK_USER/BANK_PASS` (use the demo customer from your instructor).
3. Implement JSON tools with thin wrappers around the endpoints above.
4. Build agents with watsonx that will use the logic from `teller_agent.py` and `backoffice_agent.py`.
5. Test your solution by executing the scripted dialogue.

Good luck building the next‑generation **branch‑banking AI assistant**! 🚀

