# TransactionShield

![License](https://img.shields.io/badge/license-MIT-blue)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

## AI-Powered Fraud Detection with Human Oversight

TransactionShield detects potentially fraudulent financial transactions by analyzing risk factors and automatically pausing suspicious activities until a human security analyst reviews and approves them.

![TransactionShield Overview](assets/transactionshield-overview.png)

## 🔍 Overview

TransactionShield is an intelligent fraud detection system designed to protect financial institutions and their customers from fraudulent transactions. The system leverages AI to analyze each transaction's risk profile based on multiple factors including unusual amounts, locations, recipient patterns, and timing.

### Key Features

- 🧠 **AI-powered analysis** of transactions against account history and patterns
- ⚖️ **Automatic risk assessment** categorization (low, medium, high, critical)
- ⚡ **Streamlined approval workflow** that minimizes disruption to legitimate activities
- ✅ **Automatic approval** for low and medium risk transactions
- 👨‍💼 **Human confirmation** for high-risk and critical transactions
- 📋 **Comprehensive documentation** and transaction audit trail
- 🔄 Built on **LlamaIndex's agent workflow technology** for reliable human-AI interaction

## 💻 Installation

### Prerequisites

- Python 3.9+
- OpenAI API key or compatible LLM service

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/transactionshield.git
cd transactionshield
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Usage

Run the main script:

```bash
python transaction_security.py
```

This will:
1. Initialize the system with mock transaction and account data
2. Analyze each transaction for risk factors
3. Process low-risk transactions automatically
4. Request human confirmation for high-risk transactions
5. Generate a transaction summary report

## 📊 Example Output

```
Processing 2 transactions...

Analyzing transaction: TRX-001
Type: transfer
Amount: 1200.0 USD
Recipient: Jane Smith

Analyzing risk...
Risk level: LOW

Low/medium risk transaction. Auto-approving...
Transaction TRX-001 has been automatically approved.

Analyzing transaction: TRX-002
Type: wire
Amount: 25000.0 USD
Recipient: Acme Corp

Analyzing risk...
Risk level: HIGH
Risk factors: Unusual destination country, Amount exceeds typical transaction, First-time recipient, Unusual time of day

High-risk transaction detected. Requesting human confirmation...

TRANSACTION SECURITY ALERT

Transaction ID: TRX-002
Type: wire
Amount: 25000.0 USD
Recipient: Acme Corp

RISK ASSESSMENT: HIGH

RISK FACTORS:
Unusual destination country, Amount exceeds typical transaction, First-time recipient, Unusual time of day

THIS TRANSACTION HAS BEEN AUTOMATICALLY PAUSED DUE TO ITS HIGH RISK LEVEL.

Security Analyst Smith, do you authorize this transaction to proceed? (yes/no/investigate): yes

Result: Transaction TRX-002 for 25000.0 USD has been approved by Security Analyst Smith.

===== TRANSACTION SUMMARY =====
- TRX-001 (transfer): APPROVED
  Amount: 1200.0 USD
  Risk Level: LOW
  Approved by: Auto-approval System
  Approval date: 2025-04-23T15:30:45.123456

- TRX-002 (wire): APPROVED
  Amount: 25000.0 USD
  Risk Level: HIGH
  Approved by: Security Analyst Smith
  Approval date: 2025-04-23T15:31:12.654321
```

## 🏗️ Project Structure

```
transactionshield/
├── transaction_security.py    # Main application file
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables (not in repo)
├── LICENSE                    # License file
├── README.md                  # This file
└── assets/                    # Images and other assets
    └── transactionshield-overview.png
```

## 🔮 Future Work

- Integration with banking systems and payment gateways
- Advanced anomaly detection using machine learning
- Support for cryptocurrency transaction monitoring
- Real-time alert systems for security teams
- Mobile notification for customer verification of suspicious transactions
- Behavioral biometrics integration for additional security layers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LlamaIndex](https://www.llamaindex.ai/) for AI agent workflows
- Transaction data and account examples are fictional and for demonstration purposes only
- This project is a proof-of-concept and should be appropriately tested and adapted before use in production financial systems
