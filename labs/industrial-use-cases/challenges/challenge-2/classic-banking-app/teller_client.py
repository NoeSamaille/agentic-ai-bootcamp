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

"""
teller_client.py – GFM Bank teller CLI (v5)

Features
--------
• Balance inquiry (no destination IBAN needed)
• Shows current balance at top
• Internal transfer when --amount > 0 (requires --dst-iban)
• Optional --request-overdraft flag prints a request for ops

Environment
-----------
COREBANK_URL   Base URL of demo_api (default http://127.0.0.1:8000)
"""

import argparse
import os
import pprint
import sys
import requests

BASE_URL = os.getenv("COREBANK_URL", "http://127.0.0.1:8000")


def login() -> str:
    r = requests.post(
        f"{BASE_URL}/token",
        data={"username": "teller", "password": "teller123"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def get_accounts(token: str):
    r = requests.get(f"{BASE_URL}/accounts", headers=auth(token), timeout=10)
    r.raise_for_status()
    return r.json()


def get_ledger(token: str, account_id: str):
    r = requests.get(
        f"{BASE_URL}/transactions/{account_id}", headers=auth(token), timeout=10
    )
    r.raise_for_status()
    return r.json()


def post_transfer(token: str, src_id: str, dst_id: str, amount: float):
    r = requests.post(
        f"{BASE_URL}/transfer",
        headers=auth(token),
        json={
            "source_account_id": src_id,
            "destination_account_id": dst_id,
            "amount_eur": amount,
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser(description="GFM Bank teller CLI")
    ap.add_argument("--src-iban", required=True, help="IBAN to debit / inspect")
    ap.add_argument("--dst-iban", help="IBAN to credit (for transfer)")
    ap.add_argument(
        "--amount",
        type=float,
        default=0,
        help="Amount in EUR; 0 means balance inquiry only",
    )
    ap.add_argument(
        "--request-overdraft",
        type=float,
        help="Ask back office to grant this overdraft (0–10 000 EUR)",
    )
    args = ap.parse_args()

    if args.amount > 0 and not args.dst_iban:
        ap.error("--dst-iban is required when --amount is positive")

    token = login()
    accounts = get_accounts(token)

    # resolve source
    src = next((a for a in accounts if a["iban"] == args.src_iban), None)
    if not src:
        print("Source IBAN not found.")
        sys.exit(1)
    src_id = src["account_id"]

    # optional destination
    if args.amount > 0:
        dst = next((a for a in accounts if a["iban"] == args.dst_iban), None)
        if not dst:
            print("Destination IBAN not found.")
            sys.exit(1)
        dst_id = dst["account_id"]

    # balance and ledger
    full_ledger = get_ledger(token, src_id)
    balance = sum(tx["amount_eur"] for tx in full_ledger)
    print(f"\n== Current balance: €{balance:,.2f} ==")
    print("\n== Current ledger (latest 5 rows) ==")
    latest = sorted(full_ledger, key=lambda x: x["booking_ts"], reverse=True)[:5]
    pprint.pprint(latest, sort_dicts=False)

    # overdraft request message
    if args.request_overdraft is not None:
        print(
            f"\n*** OVERDRAFT REQUEST ***\n"
            f"Please grant €{args.request_overdraft:,.2f} overdraft on {args.src_iban}"
        )

    # transfer execution
    if args.amount > 0:
        print(f"\nPosting transfer of €{args.amount:,.2f} …")
        res = post_transfer(token, src_id, dst_id, args.amount)
        pprint.pprint(res, sort_dicts=False)

        print("\n== Ledger after transfer (latest 5 rows) ==")
        updated = sorted(get_ledger(token, src_id), key=lambda x: x["booking_ts"], reverse=True)[:5]
        pprint.pprint(updated, sort_dicts=False)


if __name__ == "__main__":
    main()
