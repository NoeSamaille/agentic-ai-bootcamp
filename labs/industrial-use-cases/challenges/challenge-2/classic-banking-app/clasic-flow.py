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
GFM Bank Direct Operations Solution

This solution uses direct command execution without the agent framework
for guaranteed reliable operation.
"""

import os
import sys
import re
import subprocess
from typing import Dict, Any, List

# Script paths - using values that we know work
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_PATH = sys.executable
TELLER_SCRIPT = os.path.join(CURRENT_DIR, "teller_client.py")
BACKOFFICE_SCRIPT = os.path.join(CURRENT_DIR, "backoffice_client.py")

print(f"Current directory: {CURRENT_DIR}")
print(f"Python path: {PYTHON_PATH}")
print(f"Teller script: {TELLER_SCRIPT}")
print(f"Backoffice script: {BACKOFFICE_SCRIPT}")

# ----- Direct Banking Operations -----

def check_balance(iban):
    """Check the balance of an account."""
    print(f"\n--- Checking Balance for {iban} ---")
    cmd = [PYTHON_PATH, TELLER_SCRIPT, "--src-iban", iban]
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"Error (code {result.returncode}): {result.stderr}")
            return f"Error checking balance: {result.stderr or 'Unknown error'}"
        
        return result.stdout
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error: {str(e)}"

def transfer_money(src_iban, dst_iban, amount):
    """Transfer money between accounts."""
    print(f"\n--- Transferring {amount} from {src_iban} to {dst_iban} ---")
    cmd = [PYTHON_PATH, TELLER_SCRIPT, "--src-iban", src_iban, 
           "--dst-iban", dst_iban, "--amount", str(amount)]
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"Error (code {result.returncode}): {result.stderr}")
            return f"Error executing transfer: {result.stderr or 'Unknown error'}"
        
        return result.stdout
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error: {str(e)}"

def set_overdraft(iban, amount):
    """Set overdraft limit for an account."""
    print(f"\n--- Setting Overdraft of {amount} for {iban} ---")
    cmd = [PYTHON_PATH, BACKOFFICE_SCRIPT, "--iban", iban, 
           "--set-overdraft", str(amount)]
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"Error (code {result.returncode}): {result.stderr}")
            return f"Error setting overdraft: {result.stderr or 'Unknown error'}"
        
        return result.stdout
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error: {str(e)}"

def reverse_payment(iban, amount):
    """Reverse a payment."""
    print(f"\n--- Reversing Payment of {amount} for {iban} ---")
    cmd = [PYTHON_PATH, BACKOFFICE_SCRIPT, "--iban", iban, 
           "--fee-reversal-iban", iban, "--fee-reversal-amount", str(amount)]
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"Error (code {result.returncode}): {result.stderr}")
            return f"Error reversing payment: {result.stderr or 'Unknown error'}"
        
        return result.stdout
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error: {str(e)}"

# ----- Banking System -----

class BankingSystem:
    def __init__(self):
        """Initialize the banking system."""
        # Run a test to verify connectivity
        test_result = check_balance("DE89320895326389021994")
        if "Current balance:" in test_result:
            print("✅ Banking system initialized successfully!")
        else:
            print("⚠️ Banking system initialization warning - balance check failed!")
    
    def extract_client_info(self, message):
        """Extract client information from the message."""
        info = {
            "client_iban": None,
            "destination_iban": None,
            "amount": None,
            "overdraft_requested": False,
            "reversal_requested": False
        }
        
        # Extract IBAN(s)
        iban_pattern = r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}"
        ibans = re.findall(iban_pattern, message)
        
        if ibans:
            info["client_iban"] = ibans[0]
            if len(ibans) > 1:
                info["destination_iban"] = ibans[1]
        
        # Extract amount
        amount_pattern = r"(\d+(?:,\d+)?(?:\.\d+)?)(?:\s*(?:eur|euro|€))"
        amounts = re.findall(amount_pattern, message.lower())
        
        if amounts:
            try:
                info["amount"] = float(amounts[0].replace(',', ''))
            except ValueError:
                pass
        
        # Check for operation types
        if any(term in message.lower() for term in ["balance", "how much", "account info"]):
            info["operation"] = "balance"
        elif any(term in message.lower() for term in ["transfer", "send money", "pay"]):
            info["operation"] = "transfer"
        elif any(term in message.lower() for term in ["overdraft", "credit line", "credit request"]):
            info["operation"] = "overdraft"
            info["overdraft_requested"] = True
        elif any(term in message.lower() for term in ["reverse", "reversal", "revert", "cancel payment"]):
            info["operation"] = "reversal"
            info["reversal_requested"] = True
        else:
            info["operation"] = "unknown"
        
        print("\nExtracted information:")
        for key, value in info.items():
            print(f"{key}: {value}")
            
        return info
    
    def format_balance_response(self, balance_output):
        """Format balance information into a nice response."""
        # Extract current balance
        balance_match = re.search(r'Current balance: (€[-\d,.]+)', balance_output)
        balance = balance_match.group(1) if balance_match else "Unknown"
        
        # Extract transactions
        transactions = []
        tx_match = re.findall(r"'amount_eur': ([-\d.]+)[^}]*'type': '([^']+)'", balance_output)
        
        for amount, tx_type in tx_match[:5]:  # Show top 5 transactions
            amount_float = float(amount)
            amount_str = f"{amount_float:,.2f}"
            symbol = "+" if amount_float > 0 else ""
            transactions.append(f"{symbol}€{amount_str} - {tx_type}")
        
        # Build nice formatted response
        response = f"🏦 **GFM Bank Account Information** 🏦\n\n"
        response += f"Your current account balance is **{balance}**.\n\n"
        
        if transactions:
            response += "**Recent Transactions:**\n"
            for i, tx in enumerate(transactions, 1):
                response += f"{i}. {tx}\n"
        
        return response
    
    def format_transfer_response(self, transfer_output, src_iban, dst_iban, amount):
        """Format transfer information into a nice response."""
        # Check for success indicators
        success = "POSTED" in transfer_output
        
        # Build nice formatted response
        response = f"🏦 **GFM Bank Transfer Service** 🏦\n\n"
        
        if success:
            response += f"✅ Your transfer of **€{amount:,.2f}** has been successfully processed!\n\n"
            response += f"**Details:**\n"
            response += f"• From: {src_iban}\n"
            response += f"• To: {dst_iban}\n"
            
            # Try to extract new balance
            balance_match = re.search(r'Current balance: (€[-\d,.]+)', transfer_output)
            if balance_match:
                response += f"• New Balance: **{balance_match.group(1)}**\n"
        else:
            response += f"❌ We could not process your transfer of **€{amount:,.2f}**.\n\n"
            response += "Please check your account information and try again.\n"
        
        return response
    
    def format_overdraft_response(self, overdraft_output, iban, amount):
        """Format overdraft information into a nice response."""
        # Check for success indicators
        success = "Overdraft updated" in overdraft_output
        
        # Build nice formatted response
        response = f"🏦 **GFM Bank Overdraft Service** 🏦\n\n"
        
        if success:
            response += f"✅ Your overdraft request of **€{amount:,.2f}** has been approved!\n\n"
            response += f"**Details:**\n"
            response += f"• Account: {iban}\n"
            response += f"• Overdraft Limit: **€{amount:,.2f}**\n"
            
            # Try to extract customer name
            name_match = re.search(r"'name': '([^']+)'", overdraft_output)
            if name_match:
                response += f"• Account Holder: {name_match.group(1)}\n"
        else:
            response += f"❌ We could not process your overdraft request of **€{amount:,.2f}**.\n\n"
            response += "Please check your account information and try again.\n"
        
        return response
    
    def format_reversal_response(self, reversal_output, iban, amount):
        """Format reversal information into a nice response."""
        # Check for success indicators
        success = "Fee reversal" in reversal_output and "POSTED" in reversal_output
        
        # Build nice formatted response
        response = f"🏦 **GFM Bank Payment Reversal Service** 🏦\n\n"
        
        if success:
            response += f"✅ Your payment reversal of **€{amount:,.2f}** has been processed!\n\n"
            response += f"**Details:**\n"
            response += f"• Account: {iban}\n"
            response += f"• Reversed Amount: **€{amount:,.2f}**\n"
            
            # Try to extract transaction ID
            tx_id_match = re.search(r"'tx_id': '([^']+)'", reversal_output)
            if tx_id_match:
                response += f"• Transaction ID: {tx_id_match.group(1)}\n"
        else:
            response += f"❌ We could not process your reversal request of **€{amount:,.2f}**.\n\n"
            response += "Please check your account information and try again.\n"
        
        return response
    
    def generate_generic_response(self, user_message):
        """Generate a generic response when the operation is unknown."""
        response = f"🏦 **GFM Bank** 🏦\n\n"
        response += "I'm here to help you with your banking needs! I can:\n\n"
        response += "• Check your account balance\n"
        response += "• Transfer money between accounts\n"
        response += "• Set up overdraft facilities\n"
        response += "• Process payment reversals\n\n"
        
        response += "Please provide your account IBAN and let me know what you'd like to do."
        
        return response
    
    def process_message(self, user_message):
        """Process a user message and perform the appropriate banking operation."""
        # Extract information from the message
        info = self.extract_client_info(user_message)
        
        # Handle different operations
        if info["operation"] == "balance" and info["client_iban"]:
            # Get account balance
            balance_output = check_balance(info["client_iban"])
            
            if "Current balance:" in balance_output:
                return self.format_balance_response(balance_output)
            else:
                return f"🏦 **GFM Bank** 🏦\n\nI'm sorry, but I couldn't retrieve the balance for account {info['client_iban']}. Please try again later."
                
        elif info["operation"] == "transfer" and info["client_iban"] and info["destination_iban"] and info["amount"]:
            # Transfer money
            transfer_output = transfer_money(info["client_iban"], info["destination_iban"], info["amount"])
            
            return self.format_transfer_response(transfer_output, info["client_iban"], info["destination_iban"], info["amount"])
            
        elif info["operation"] == "overdraft" and info["client_iban"] and info["amount"]:
            # Validate overdraft amount
            if info["amount"] < 1000 or info["amount"] > 10000:
                return f"🏦 **GFM Bank Overdraft Service** 🏦\n\nℹ️ Overdraft amounts must be between €1,000 and €10,000. Your requested amount of €{info['amount']:,.2f} is {'too low' if info['amount'] < 1000 else 'too high'}. Please submit a new request with an amount within the acceptable range."
            
            # Set overdraft
            overdraft_output = set_overdraft(info["client_iban"], info["amount"])
            
            return self.format_overdraft_response(overdraft_output, info["client_iban"], info["amount"])
            
        elif info["operation"] == "reversal" and info["client_iban"] and info["amount"]:
            # Reverse payment
            reversal_output = reverse_payment(info["client_iban"], info["amount"])
            
            return self.format_reversal_response(reversal_output, info["client_iban"], info["amount"])
            
        elif info["client_iban"] and not info["operation"] == "unknown":
            # We have an IBAN but not enough information
            if info["operation"] == "transfer":
                return f"🏦 **GFM Bank** 🏦\n\nTo process a transfer, I need to know the destination IBAN and the amount. Please provide this information."
            elif info["operation"] == "overdraft":
                return f"🏦 **GFM Bank** 🏦\n\nTo process an overdraft request, I need to know the amount (between €1,000 and €10,000). Please specify the amount you need."
            elif info["operation"] == "reversal":
                return f"🏦 **GFM Bank** 🏦\n\nTo process a payment reversal, I need to know the amount. Please specify the amount you want to reverse."
            else:
                # Default to checking balance
                balance_output = check_balance(info["client_iban"])
                
                if "Current balance:" in balance_output:
                    return self.format_balance_response(balance_output)
                else:
                    return f"🏦 **GFM Bank** 🏦\n\nI'm sorry, but I couldn't retrieve the balance for account {info['client_iban']}. Please try again later."
        else:
            # Not enough information to determine what the user wants
            return self.generate_generic_response(user_message)

# ----- Main Function -----

def main():
    """Run the banking system."""
    print("\n🏦 Welcome to GFM Bank! 🏦")
    print("How can we assist you today?")
    print("(Type 'exit' to end the conversation)")
    
    banking_system = BankingSystem()
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            print("\n🏦 Thank you for banking with GFM Bank! Have a great day! 🏦")
            break
        
        response = banking_system.process_message(user_input)
        print(f"\nGFM Bank: {response}")

if __name__ == "__main__":
    main()
