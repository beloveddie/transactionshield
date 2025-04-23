"""
Financial Transaction Security System

A system that helps financial institutions detect potentially fraudulent transactions,
automatically flagging suspicious activities and requiring human confirmation before proceeding.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.core.workflow import (
    InputRequiredEvent,
    HumanResponseEvent
)

# Define risk levels for transactions
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Define transaction types
class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    CURRENCY_EXCHANGE = "currency_exchange"
    WIRE = "wire"

# Transaction model for schema compatibility
class TransactionModel(BaseModel):
    transaction_id: str
    account_id: str
    transaction_type: TransactionType
    amount: float
    currency: str
    recipient: Optional[str] = None
    recipient_account: Optional[str] = None
    timestamp: datetime
    location: Optional[str] = None
    ip_address: Optional[str] = None
    device_id: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    risk_factors: Optional[List[str]] = None
    approved: bool = False
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None

# Account model for context
class AccountModel(BaseModel):
    account_id: str
    customer_name: str
    account_type: str
    balance: float
    currency: str
    daily_limit: float
    country: str
    usual_countries: List[str]
    usual_transaction_amounts: List[float]
    usual_recipients: List[str]
    transaction_history_summary: str

# Initialize the LLM
def init_llm():
    """Initialize the LLM with appropriate parameters"""
    llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    return llm

# Function to generate mock transaction data
def get_mock_transactions():
    """Generate mock transaction data for testing"""
    transactions = [
        {
            "transaction_id": "TRX-001",
            "account_id": "ACC-12345",
            "transaction_type": "transfer",
            "amount": 1200.00,
            "currency": "USD",
            "recipient": "Jane Smith",
            "recipient_account": "ACC-67890",
            "timestamp": datetime.now().isoformat(),
            "location": "New York, USA",
            "ip_address": "192.168.1.1",
            "device_id": "DEVICE-001",
            "risk_level": "low",
            "risk_factors": [],
            "approved": False,
            "approved_by": None,
            "approval_date": None
        },
        {
            "transaction_id": "TRX-002",
            "account_id": "ACC-12345",
            "transaction_type": "wire",
            "amount": 25000.00,
            "currency": "USD",
            "recipient": "Acme Corp",
            "recipient_account": "ACC-99999",
            "timestamp": datetime.now().isoformat(),
            "location": "Lagos, Nigeria",
            "ip_address": "203.0.113.42",
            "device_id": "DEVICE-002",
            "risk_level": "high",
            "risk_factors": [
                "Unusual destination country",
                "Amount exceeds typical transaction",
                "First-time recipient",
                "Unusual time of day"
            ],
            "approved": False,
            "approved_by": None,
            "approval_date": None
        }
    ]
    return transactions

# Function to get mock account data
def get_mock_account():
    """Generate mock account data"""
    account = {
        "account_id": "ACC-12345",
        "customer_name": "John Doe",
        "account_type": "Checking",
        "balance": 35000.00,
        "currency": "USD",
        "daily_limit": 10000.00,
        "country": "United States",
        "usual_countries": ["United States", "Canada"],
        "usual_transaction_amounts": [100.00, 500.00, 1000.00],
        "usual_recipients": ["Jane Smith", "Bob Johnson", "Local Utility Co"],
        "transaction_history_summary": "Regular payroll deposits. Typical transfers to family members. Regular payments for utilities and subscriptions. No international transfers in the past 6 months."
    }
    return account

# Function to analyze risk for a transaction
async def analyze_transaction_risk(llm, transaction, account):
    """Analyze transaction risk using the LLM"""
    
    # Create prompt for the LLM
    prompt = f"""
    As a financial security AI, please analyze the following transaction for potential fraud risk:
    
    TRANSACTION DETAILS:
    - Transaction ID: {transaction['transaction_id']}
    - Type: {transaction['transaction_type']}
    - Amount: {transaction['amount']} {transaction['currency']}
    - Recipient: {transaction.get('recipient', 'N/A')}
    - Recipient Account: {transaction.get('recipient_account', 'N/A')}
    - Location: {transaction.get('location', 'N/A')}
    - IP Address: {transaction.get('ip_address', 'N/A')}
    - Device ID: {transaction.get('device_id', 'N/A')}
    - Time: {transaction['timestamp']}
    
    ACCOUNT CONTEXT:
    - Account ID: {account['account_id']}
    - Customer: {account['customer_name']}
    - Account Type: {account['account_type']}
    - Balance: {account['balance']} {account['currency']}
    - Daily Limit: {account['daily_limit']} {account['currency']}
    - Country: {account['country']}
    - Usual Countries: {', '.join(account['usual_countries'])}
    - Usual Transaction Amounts: {', '.join([str(amount) for amount in account['usual_transaction_amounts']])}
    - Usual Recipients: {', '.join(account['usual_recipients'])}
    - Transaction History: {account['transaction_history_summary']}
    
    Evaluate this transaction for fraud risk. Consider factors such as:
    1. Transaction amount relative to usual behavior
    2. Transaction location compared to account holder's usual countries
    3. First-time recipients vs known recipients
    4. Time of transaction relative to normal patterns
    5. Transaction type relative to account history
    
    Return a JSON object with the following fields:
    - risk_level: ("low", "medium", "high", "critical")
    - risk_factors: [list of risk factors identified]
    - risk_explanation: detailed explanation of the risk assessment
    """
    
    # For a real implementation, we would call the LLM here
    # response = await llm.acomplete(prompt)
    
    # For this example, we'll use the mock data
    if transaction['risk_level'] == 'high':
        return {
            "risk_level": "high",
            "risk_factors": transaction['risk_factors'],
            "risk_explanation": "This transaction shows multiple risk factors including an unusual destination country (Nigeria), an amount significantly higher than typical transactions, and a first-time recipient. The transaction amount of $25,000 exceeds the usual transaction pattern and is being sent to a country not in the list of usual countries for this account."
        }
    else:
        return {
            "risk_level": "low",
            "risk_factors": [],
            "risk_explanation": "This transaction appears to be normal based on the account history and transaction patterns. The amount is within typical ranges, the recipient is known, and the location matches the account holder's usual activity area."
        }

# Tool function to confirm high-risk transactions
async def confirm_transaction(ctx: Context, 
                             transaction_id: str, 
                             amount: float, 
                             currency: str,
                             transaction_type: str,
                             recipient: str, 
                             risk_level: str,
                             risk_factors: List[str],
                             reviewer_name: str) -> str:
    """Request human confirmation for a suspicious transaction"""
    
    # Prepare the confirmation message
    confirmation_text = f"""
    TRANSACTION SECURITY ALERT
    
    Transaction ID: {transaction_id}
    Type: {transaction_type}
    Amount: {amount} {currency}
    Recipient: {recipient}
    
    RISK ASSESSMENT: {risk_level.upper()}
    
    RISK FACTORS:
    {', '.join(risk_factors) if risk_factors else 'None identified'}
    
    THIS TRANSACTION HAS BEEN AUTOMATICALLY PAUSED DUE TO ITS {risk_level.upper()} RISK LEVEL.
    """
    
    # Emit an event to the external stream to be captured
    ctx.write_event_to_stream(
        InputRequiredEvent(
            prefix=confirmation_text + f"\n\n{reviewer_name}, do you authorize this transaction to proceed? (yes/no/investigate):",
            user_name=reviewer_name,
        )
    )
    
    # Wait until we see a HumanResponseEvent
    response = await ctx.wait_for_event(
        HumanResponseEvent, requirements={"user_name": reviewer_name}
    )
    
    # Act on the input from the event
    user_response = response.response.strip().lower()
    
    if user_response == "yes":
        return f"Transaction {transaction_id} for {amount} {currency} has been approved by {reviewer_name}."
    elif user_response == "investigate":
        return f"Transaction {transaction_id} has been marked for further investigation."
    else:
        return f"Transaction {transaction_id} has been rejected by {reviewer_name}."

# Create the transaction security workflow
def create_workflow(llm):
    """Create the agent workflow for transaction security review"""
    
    workflow = AgentWorkflow.from_tools_or_functions(
        [confirm_transaction],
        llm=llm,
        system_prompt="""
        You are a Financial Security Assistant AI.
        Your role is to review transactions and identify potential fraud.
        For any transaction with "high" or "critical" risk level, you MUST use the confirm_transaction function.
        Low and medium risk transactions can be approved automatically.
        Always prioritize security while minimizing disruption to legitimate customer activity.
        """
    )
    
    return workflow

# Main function to run the transaction security system
async def main():
    # Initialize LLM
    llm = init_llm()
    
    # Create workflow
    workflow = create_workflow(llm)
    
    # Get mock data
    transactions = get_mock_transactions()
    account = get_mock_account()
    reviewer_name = "Security Analyst Smith"
    
    print(f"Processing {len(transactions)} transactions...\n")
    
    # Process each transaction
    for transaction in transactions:
        print(f"Analyzing transaction: {transaction['transaction_id']}")
        print(f"Type: {transaction['transaction_type']}")
        print(f"Amount: {transaction['amount']} {transaction['currency']}")
        print(f"Recipient: {transaction.get('recipient', 'N/A')}")
        
        # Analyze risk
        print("\nAnalyzing risk...")
        risk_analysis = await analyze_transaction_risk(llm, transaction, account)
        transaction['risk_level'] = risk_analysis['risk_level']
        transaction['risk_factors'] = risk_analysis['risk_factors']
        
        print(f"Risk level: {transaction['risk_level'].upper()}")
        if transaction['risk_factors']:
            print(f"Risk factors: {', '.join(transaction['risk_factors'])}")
        
        # For low/medium risk transactions, auto-approve
        if transaction['risk_level'] in ['low', 'medium']:
            print(f"\nLow/medium risk transaction. Auto-approving...")
            transaction["approved"] = True
            transaction["approved_by"] = "Auto-approval System"
            transaction["approval_date"] = datetime.now().isoformat()
            print(f"Transaction {transaction['transaction_id']} has been automatically approved.")
            continue
        
        # For high/critical risk transactions, require human confirmation
        print(f"\nHigh-risk transaction detected. Requesting human confirmation...")
        
        # Run the workflow
        handler = workflow.run(
            user_msg=f"Review this high-risk {transaction['transaction_type']} transaction for {transaction['amount']} {transaction['currency']} to {transaction.get('recipient', 'unknown recipient')}",
            context_dict={
                "transaction_id": transaction['transaction_id'],
                "amount": transaction['amount'],
                "currency": transaction['currency'],
                "transaction_type": transaction['transaction_type'],
                "recipient": transaction.get('recipient', 'Unknown'),
                "risk_level": transaction['risk_level'],
                "risk_factors": transaction['risk_factors'],
                "reviewer_name": reviewer_name
            }
        )
        
        # Process events from the agent
        async for event in handler.stream_events():
            # Handle InputRequiredEvent events (security analyst confirmation)
            if isinstance(event, InputRequiredEvent):
                print("\n" + event.prefix)
                response = input()
                handler.ctx.send_event(
                    HumanResponseEvent(
                        response=response,
                        user_name=event.user_name,
                    )
                )
        
        # Get and print the response
        response = await handler
        print(f"\nResult: {response}")
        
        # Update transaction approval status based on response
        if "approved" in str(response).lower():
            transaction["approved"] = True
            transaction["approved_by"] = reviewer_name
            transaction["approval_date"] = datetime.now().isoformat()
    
    # Generate transaction report
    print("\n===== TRANSACTION SUMMARY =====")
    for transaction in transactions:
        status = "APPROVED" if transaction.get('approved', False) else "REJECTED"
        print(f"- {transaction['transaction_id']} ({transaction['transaction_type']}): {status}")
        print(f"  Amount: {transaction['amount']} {transaction['currency']}")
        print(f"  Risk Level: {transaction['risk_level'].upper()}")
        if transaction.get('approved', False):
            print(f"  Approved by: {transaction.get('approved_by', 'Unknown')}")
            print(f"  Approval date: {transaction.get('approval_date', 'Unknown')}")
        print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
