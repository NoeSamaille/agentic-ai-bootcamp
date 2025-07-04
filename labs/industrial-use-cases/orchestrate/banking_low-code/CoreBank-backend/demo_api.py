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

import sqlite3, hashlib, uuid
# from datetime import datetime as dt, UTC
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, condecimal
from typing import Optional, List, Dict, Any
from datetime import datetime as dt, timezone 

DB_PATH='corebank.db'
oauth=OAuth2PasswordBearer(tokenUrl='token')
app=FastAPI(title='Corebank Demo API v5 + ManualTx')

def get_db():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def verify(tok:str, db):
    row=db.execute('SELECT username,role FROM users WHERE username=?',(tok,)).fetchone()
    if not row:
        raise HTTPException(status_code=401, detail='Invalid token')
    return row

def require_role(row, allowed:set[str]):
    if row['role'] not in allowed:
        raise HTTPException(status_code=403, detail='Forbidden')
    return row

@app.post('/token')
def login(form:OAuth2PasswordRequestForm=Depends(), db=Depends(get_db)):
    row=db.execute('SELECT hashed_password FROM users WHERE username=?',(form.username,)).fetchone()
    if not row or hashlib.sha256(form.password.encode()).hexdigest()!=row['hashed_password']:
        raise HTTPException(status_code=401, detail='Bad credentials')
    return {'access_token':form.username,'token_type':'bearer'}

@app.get('/accounts')
def list_accounts(db=Depends(get_db), token:str=Depends(oauth)):
    user=verify(token, db)
    rows=db.execute('SELECT * FROM accounts').fetchall()
    if user['role']=='BACKOFFICE':
        return [dict(r) for r in rows]
    return [{k:r[k] for k in ('account_id','iban','customer_id')} for r in rows]

@app.get('/customers')
def customers(db=Depends(get_db), token:str=Depends(oauth)):
    require_role(verify(token, db), {'BACKOFFICE'})
    return [dict(r) for r in db.execute('SELECT * FROM customers')]

@app.get('/transactions/{account_id}')
def tx_list(account_id:str, db=Depends(get_db), token:str=Depends(oauth)):
    verify(token, db)
    return [dict(r) for r in db.execute('SELECT * FROM transactions WHERE account_id=?',(account_id,))]

class Transfer(BaseModel):
    source_account_id:str
    destination_account_id:str
    amount_eur:condecimal(gt=0,max_digits=14,decimal_places=2)

@app.post('/transfer')
def make_transfer(body:Transfer, db=Depends(get_db), token:str=Depends(oauth)):
    verify(token, db)
    bal=db.execute('SELECT COALESCE(SUM(amount_eur),0) AS bal FROM transactions WHERE account_id=?',(body.source_account_id,)).fetchone()['bal']
    od=db.execute('SELECT overdraft_limit_eur FROM accounts WHERE account_id=?',(body.source_account_id,)).fetchone()['overdraft_limit_eur']
    if bal - float(body.amount_eur) < -od:
        raise HTTPException(status_code=403, detail=f'Insufficient funds. Balance {bal:.2f}, overdraft {od:.2f}')
    now=dt.now(UTC).isoformat(timespec='seconds')
    debit, credit=str(uuid.uuid4()), str(uuid.uuid4())
    try:
        db.execute('BEGIN')
        db.execute('INSERT INTO transactions VALUES (?,?,?,?,?)',(debit, body.source_account_id, now, -float(body.amount_eur), 'TRANSFER_OUT'))
        db.execute('INSERT INTO transactions VALUES (?,?,?,?,?)',(credit, body.destination_account_id, now, float(body.amount_eur), 'TRANSFER_IN'))
        db.commit()
    except:
        db.rollback()
        raise
    return {'status':'POSTED','debit_tx':debit,'credit_tx':credit,'timestamp':now}

@app.patch('/accounts/{account_id}/overdraft')
def set_overdraft(account_id:str, limit_eur:float, db=Depends(get_db), token:str=Depends(oauth)):
    require_role(verify(token, db), {'BACKOFFICE'})
    if not (0<=limit_eur<=10_000):
        raise HTTPException(status_code=400, detail='Limit must be 0-10 000')
    db.execute('UPDATE accounts SET overdraft_limit_eur=? WHERE account_id=?',(limit_eur, account_id))
    db.commit()
    return {'account_id':account_id,'overdraft_limit_eur':limit_eur}

class ManualTx(BaseModel):
    amount_eur: float
    type: str
    booking_ts: str

@app.post("/transactions/{account_id}")
def manual_post(account_id: str, tx: ManualTx, db=Depends(get_db), token: str = Depends(oauth)):
    require_role(verify(token, db), {"BACKOFFICE"})
    if tx.type not in ("FEE_REVERSAL", "MANUAL_ADJ"):
        raise HTTPException(400, detail="Only FEE_REVERSAL or MANUAL_ADJ allowed")
    tx_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO transactions VALUES (?,?,?,?,?)",
        (tx_id, account_id, tx.booking_ts, tx.amount_eur, tx.type),
    )
    db.commit()
    return {"status": "POSTED", "tx_id": tx_id}

# New models for wrapper endpoints
class BalanceInquiry(BaseModel):
    iban: str
    username: str = "teller"
    password: str = "teller123"

class IbanTransfer(BaseModel):
    source_iban: str
    destination_iban: str
    amount_eur: float
    username: str = "teller"
    password: str = "teller123"

class OverdraftApproval(BaseModel):
    iban: str
    overdraft_limit_eur: float
    username: str = "backoffice"
    password: str = "backoffice123"

class FeeReversal(BaseModel):
    iban: str
    amount_eur: float
    username: str = "backoffice"
    password: str = "backoffice123"

# New wrapper endpoints for simplified API access
@app.post("/balance-inquiry")
def balance_inquiry(body: BalanceInquiry, db=Depends(get_db)):
    # Create a Form with the credentials
    form_data = OAuth2PasswordRequestForm(username=body.username, password=body.password)
    
    # Authenticate
    login_result = login(form_data, db)
    token = login_result["access_token"]
    
    # Get accounts to find the account_id for the given IBAN
    accounts = [dict(r) for r in db.execute('SELECT * FROM accounts').fetchall()]
    account = next((a for a in accounts if a["iban"] == body.iban), None)
    
    if not account:
        raise HTTPException(status_code=404, detail="IBAN not found")
    
    # Get transactions for the account
    transactions = [dict(r) for r in db.execute('SELECT * FROM transactions WHERE account_id=?', (account["account_id"],))]
    
    # Calculate current balance
    current_balance = sum(tx["amount_eur"] for tx in transactions)
    
    # Get recent transactions (sorted by timestamp, latest first)
    recent_transactions = sorted(transactions, key=lambda x: x["booking_ts"], reverse=True)[:5]
    
    return {
        "iban": body.iban,
        "account_id": account["account_id"],
        "current_balance_eur": current_balance,
        "overdraft_limit_eur": account["overdraft_limit_eur"],
        "available_balance_eur": current_balance + account["overdraft_limit_eur"],
        "recent_transactions": recent_transactions
    }

@app.post("/iban-transfer")
def iban_transfer(body: IbanTransfer, db=Depends(get_db)):
    try:
        # Ensure timezone is imported
        from datetime import timezone  # Add this import at the top of the function
        
        # Manual authentication instead of using OAuth2PasswordRequestForm directly
        row = db.execute('SELECT hashed_password FROM users WHERE username=?', (body.username,)).fetchone()
        if not row or hashlib.sha256(body.password.encode()).hexdigest() != row['hashed_password']:
            raise HTTPException(status_code=401, detail='Bad credentials')
        
        token = body.username  # Set token to username after successful auth
        
        # Get accounts to find the account_ids for the given IBANs
        accounts = [dict(r) for r in db.execute('SELECT * FROM accounts').fetchall()]
        
        # Find source and destination accounts
        source_account = next((a for a in accounts if a["iban"] == body.source_iban), None)
        destination_account = next((a for a in accounts if a["iban"] == body.destination_iban), None)
        
        if not source_account:
            raise HTTPException(status_code=404, detail="Source IBAN not found")
        if not destination_account:
            raise HTTPException(status_code=404, detail="Destination IBAN not found")
        
        # Get initial balance for logging
        initial_bal = db.execute('SELECT COALESCE(SUM(amount_eur),0) AS bal FROM transactions WHERE account_id=?', 
                               (source_account["account_id"],)).fetchone()['bal']
        
        # Create transfer request - convert amount_eur to proper decimal
        transfer_body = Transfer(
            source_account_id=source_account["account_id"],
            destination_account_id=destination_account["account_id"],
            amount_eur=float(body.amount_eur)
        )
        
        # Execute transfer
        bal = db.execute('SELECT COALESCE(SUM(amount_eur),0) AS bal FROM transactions WHERE account_id=?',
                       (transfer_body.source_account_id,)).fetchone()['bal']
        od = db.execute('SELECT overdraft_limit_eur FROM accounts WHERE account_id=?',
                      (transfer_body.source_account_id,)).fetchone()['overdraft_limit_eur']
        
        if bal - float(transfer_body.amount_eur) < -od:
            raise HTTPException(status_code=403, 
                              detail=f'Insufficient funds. Balance {bal:.2f}, overdraft {od:.2f}')
        
        now = dt.now(timezone.utc).isoformat(timespec='seconds')
        debit, credit = str(uuid.uuid4()), str(uuid.uuid4())
        
        try:
            db.execute('BEGIN')
            db.execute('INSERT INTO transactions VALUES (?,?,?,?,?)',
                     (debit, transfer_body.source_account_id, now, -float(transfer_body.amount_eur), 'TRANSFER_OUT'))
            db.execute('INSERT INTO transactions VALUES (?,?,?,?,?)',
                     (credit, transfer_body.destination_account_id, now, float(transfer_body.amount_eur), 'TRANSFER_IN'))
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
        # Get updated balance after transfer
        new_bal = db.execute('SELECT COALESCE(SUM(amount_eur),0) AS bal FROM transactions WHERE account_id=?',
                           (source_account["account_id"],)).fetchone()['bal']
        
        # Return combined result
        return {
            "status": "POSTED",
            "source_iban": body.source_iban,
            "destination_iban": body.destination_iban,
            "amount_eur": float(body.amount_eur),
            "debit_tx": debit,
            "credit_tx": credit,
            "timestamp": now,
            "new_balance_eur": new_bal
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch all other exceptions and return a 500 error
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Endpoints for the backoffice operations

# Model for overdraft approval (without credentials)
class OverdraftApproval(BaseModel):
    iban: str
    overdraft_limit_eur: float

@app.post("/approve-overdraft")
def approve_overdraft(body: OverdraftApproval, db=Depends(get_db)):
    try:
        # Hardcoded backoffice credentials
        username = "backoffice"
        password = "backoffice123"
        
        # Authenticate with hardcoded credentials
        row = db.execute('SELECT hashed_password FROM users WHERE username=?', (username,)).fetchone()
        if not row or hashlib.sha256(password.encode()).hexdigest() != row['hashed_password']:
            raise HTTPException(status_code=401, detail='Bad credentials')
        
        # Verify backoffice role
        user_role = db.execute('SELECT role FROM users WHERE username=?', (username,)).fetchone()['role']
        if user_role != 'BACKOFFICE':
            raise HTTPException(status_code=403, detail='Forbidden - backoffice role required')
        
        # Validate overdraft amount
        if not (0 <= body.overdraft_limit_eur <= 10_000):
            raise HTTPException(status_code=400, detail='Overdraft limit must be between 0 and 10,000 EUR')
        
        # Find account by IBAN
        accounts = [dict(r) for r in db.execute('SELECT * FROM accounts').fetchall()]
        account = next((a for a in accounts if a["iban"] == body.iban), None)
        if not account:
            raise HTTPException(status_code=404, detail='IBAN not found')
        
        # Get customer info
        customers = [dict(r) for r in db.execute('SELECT * FROM customers').fetchall()]
        customer = next((c for c in customers if c["customer_id"] == account["customer_id"]), None)
        
        # Update overdraft limit
        db.execute('UPDATE accounts SET overdraft_limit_eur=? WHERE account_id=?', 
                 (body.overdraft_limit_eur, account["account_id"]))
        db.commit()
        
        # Return success response
        return {
            "account_id": account["account_id"],
            "iban": body.iban,
            "customer_name": customer["name"] if customer else "Unknown",
            "overdraft_limit_eur": body.overdraft_limit_eur,
            "message": f"Overdraft limit updated successfully to {body.overdraft_limit_eur} EUR"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Model for fee reversal (without credentials)
class FeeReversal(BaseModel):
    iban: str
    amount_eur: float

@app.post("/fee-reversal")
def process_fee_reversal(body: FeeReversal, db=Depends(get_db)):
    try:
        # Hardcoded backoffice credentials
        username = "backoffice"
        password = "backoffice123"
        
        # Authenticate with hardcoded credentials
        row = db.execute('SELECT hashed_password FROM users WHERE username=?', (username,)).fetchone()
        if not row or hashlib.sha256(password.encode()).hexdigest() != row['hashed_password']:
            raise HTTPException(status_code=401, detail='Bad credentials')
        
        # Verify backoffice role
        user_role = db.execute('SELECT role FROM users WHERE username=?', (username,)).fetchone()['role']
        if user_role != 'BACKOFFICE':
            raise HTTPException(status_code=403, detail='Forbidden - backoffice role required')
        
        # Find account by IBAN
        accounts = [dict(r) for r in db.execute('SELECT * FROM accounts').fetchall()]
        account = next((a for a in accounts if a["iban"] == body.iban), None)
        if not account:
            raise HTTPException(status_code=404, detail='IBAN not found')
        
        # Get customer info
        customers = [dict(r) for r in db.execute('SELECT * FROM customers').fetchall()]
        customer = next((c for c in customers if c["customer_id"] == account["customer_id"]), None)
        
        # Create fee reversal transaction
        from datetime import timezone  # Ensure timezone is imported
        booking_ts = dt.now(timezone.utc).isoformat(timespec='seconds')
        tx_id = str(uuid.uuid4())
        
        db.execute(
            "INSERT INTO transactions VALUES (?,?,?,?,?)",
            (tx_id, account["account_id"], booking_ts, body.amount_eur, "FEE_REVERSAL")
        )
        db.commit()
        
        # Get updated balance
        transactions = [dict(r) for r in db.execute('SELECT * FROM transactions WHERE account_id=?', 
                                                  (account["account_id"],))]
        new_balance = sum(tx["amount_eur"] for tx in transactions)
        
        # Return success response
        return {
            "status": "POSTED",
            "iban": body.iban,
            "customer_name": customer["name"] if customer else "Unknown",
            "amount_eur": body.amount_eur,
            "transaction_id": tx_id,
            "booking_ts": booking_ts,
            "new_balance_eur": new_balance,
            "message": f"Fee reversal of {body.amount_eur} EUR processed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
