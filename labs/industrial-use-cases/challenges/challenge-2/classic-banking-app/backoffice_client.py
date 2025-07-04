#!/usr/bin/env python3

##############################################################################
#                                                                            #
#  ██████  ██████  ███    ███      ██████  ██████  ██████  ██████           #
#     ██   ██   ██ ████  ████     ██      ██    ██ ██   ██ ██   ██          #
#     ██   ██████  ██ ████ ██     ██      ██    ██ ██████  ██████           #
#     ██   ██   ██ ██  ██  ██     ██      ██    ██ ██   ██ ██               #
#  ██████  ██████  ██      ██      ██████  ██████  ██   ██ ██               #
#                                                                            #
##############################################################################
#                                                                            #
#  IBM Corporation @ 2025                                                    #
#  Client Engineering                                                        #
#                                                                            #
#  Author: florin.manaila@de.ibm.com                                         #
#                                                                            #
#  "Code is like humor. When you have to explain it, it's bad." - Cory House #
#                                                                            #
##############################################################################

"""backoffice_client.py – GFM Bank ops-centre CLI (v5)

• Lookup customer by name or IBAN
• Optional fee reversal on an IBAN (custom amount)
• Optional overdraft limit change (0–10 000 EUR)

Environment
-----------
COREBANK_URL   Base URL of demo_api (default http://127.0.0.1:8000)
"""

import argparse
import datetime as dt
import os
import pprint
import sys

import requests

BASE_URL = os.getenv("COREBANK_URL", "http://127.0.0.1:8000")


def login() -> str:
    r = requests.post(
        f"{BASE_URL}/token",
        data={"username": "backoffice", "password": "backoffice123"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def auth_hdr(tok: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {tok}"}


def get(endpoint: str, tok: str):
    r = requests.get(f"{BASE_URL}{endpoint}", headers=auth_hdr(tok), timeout=10)
    r.raise_for_status()
    return r.json()


def post(endpoint: str, tok: str, payload):
    r = requests.post(
        f"{BASE_URL}{endpoint}", headers=auth_hdr(tok), json=payload, timeout=10
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser(description="Back-office demo client")
    ap.add_argument("--customer-name", help="Substring search")
    ap.add_argument("--iban", help="Provide IBAN directly instead of customer name")
    ap.add_argument("--fee-reversal-iban", help="IBAN to credit")
    ap.add_argument("--fee-reversal-amount", type=float, help="Amount to reverse (default 15.00 EUR)")
    ap.add_argument("--set-overdraft", type=float, help="Grant/change overdraft limit (0–10 000 EUR)")
    args = ap.parse_args()

    tok = login()

    # Lookup logic
    if args.iban:
        account = next((a for a in get("/accounts", tok) if a["iban"] == args.iban), None)
        if not account:
            print("IBAN not found.")
            sys.exit(1)
        customer = next((c for c in get("/customers", tok) if c["customer_id"] == account["customer_id"]), None)
        cust_accounts = [account]
    elif args.customer_name:
        customers = get("/customers", tok)
        matches = [c for c in customers if args.customer_name.lower() in c["name"].lower()]
        if not matches:
            print("No customer match.")
            sys.exit(1)
        customer = matches[0]
        accounts = get("/accounts", tok)
        cust_accounts = [a for a in accounts if a["customer_id"] == customer["customer_id"]]
    else:
        print("Error: Provide either --iban or --customer-name.")
        sys.exit(1)

    print("\n== Customer ==")
    pprint.pprint(customer, sort_dicts=False)

    print("\n== Accounts ==")
    pprint.pprint(cust_accounts, sort_dicts=False)

    # Overdraft update
    if args.set_overdraft is not None:
        if not (0 <= args.set_overdraft <= 10_000):
            print("Overdraft must be between 0–10 000 EUR.")
            sys.exit(1)
        target_acct = cust_accounts[0]
        if args.fee_reversal_iban:
            tgt = [a for a in cust_accounts if a["iban"] == args.fee_reversal_iban]
            if tgt:
                target_acct = tgt[0]
        res = requests.patch(
            f"{BASE_URL}/accounts/{target_acct['account_id']}/overdraft",
            headers=auth_hdr(tok),
            params={"limit_eur": args.set_overdraft},
            timeout=10,
        )
        res.raise_for_status()
        print("\nOverdraft updated:", res.json())

    # Fee reversal
    if args.fee_reversal_iban:
        acct = next((a for a in cust_accounts if a["iban"] == args.fee_reversal_iban), None)
        if acct is None:
            print("IBAN not in customer account list.")
            sys.exit(1)
        reversal_amt = args.fee_reversal_amount or 15.00
        res = post(
            f"/transactions/{acct['account_id']}",
            tok,
            {
                "amount_eur": reversal_amt,
                "type": "FEE_REVERSAL",
                "booking_ts": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            },
        )
        print(f"\nFee reversal of €{reversal_amt:,.2f} posted:", res)


if __name__ == "__main__":
    main()
