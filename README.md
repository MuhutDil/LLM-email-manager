# LLM Email Manager

An AI-powered email management agent built with **LangChain**, **LangGraph**, and the **GigaChat** language model. This system automatically processes incoming emails, categorizes them, extracts critical information from regulatory notices, and takes appropriate actions such as forwarding emails or sending escalation notifications.

## 📋 Overview

This project demonstrates how to build intelligent email processing workflows using state-of-the-art LLM orchestration frameworks. The system handles various email types including:

- **Regulatory notices** (OSHA violations, building code violations, etc.)
- **Invoices and billing-related emails**
- **Customer support requests**
- **General inquiries**

## 🏗️ Architecture

The system consists of two main workflow graphs:

### 1. Email Agent Graph (`graphs/email_agent.py`)

The primary entry point that routes emails to appropriate handlers:

```
START → email_agent → [tool execution] → email_agent → END
                         ↓
                    email_tools
```

**Available Tools:**
- `forward_email` - Forwards emails to internal departments
- `send_wrong_email_notification_to_sender` - Notifies senders of misdirected emails
- `extract_notice_data` - Extracts structured data from regulatory notices
- `determine_email_action` - Decides routing for invoices, customer emails, and general inquiries

### 2. Notice Extraction Graph (`graphs/notice_extraction.py`)

A specialized sub-graph for processing regulatory compliance notices:

```
START → parse_notice_message → check_escalation_status → [escalation needed?]
                                                      ↓
                                          send_escalation_email OR create_legal_ticket
                                                      ↓
                                           answer_follow_up_question → END
```

**Key Features:**
- Extracts structured fields (violations, fines, deadlines, contact info)
- Evaluates escalation criteria (text-based and dollar thresholds)
- Sends escalation emails to executives for urgent matters
- Creates legal tickets for tracking
- Answers follow-up questions about notice details

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- GigaChat API credentials

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LLM-email-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
```bash
# Create a .env file with your GigaChat credentials
echo "GIGACHAT_API_KEY=your_api_key_here" > .env
```

### Running the Example Workflow

Execute the example workflow to see the email agent in action:

```bash
python example_workflow.py
```

This processes several example emails including:
- OSHA safety violation notices
- Invoice emails
- Customer maintenance requests
- Building code violations

### Visualizing the Graphs

Generate visual representations of the workflow graphs:

```bash
python utils/visualize_graph.py
```

This creates PNG diagrams showing the flow of each graph:
- `main_graph.png` - Email Agent workflow
- `notice_extraction_graph.png` - Notice Extraction workflow

## 📁 Project Structure

```
LLM-email-manager/
├── chains/                 # LLM chains for specific tasks
│   ├── binary_questions.py      # Yes/no question answering
│   ├── escalation_check.py      # Escalation decision logic
│   └── notice_extraction.py     # Notice field extraction
├── graphs/                 # LangGraph workflow definitions
│   ├── email_agent.py           # Main email routing graph
│   └── notice_extraction.py     # Regulatory notice processing
├── utils/                  # Utility functions
│   ├── gigachat_settings.py     # LLM configuration
│   ├── graph_utils.py           # Graph helper functions
│   ├── logging_config.py        # Logging setup
│   └── visualize_graph.py       # Graph visualization
├── tests/                  # Comprehensive test suite
│   ├── test_binary_questions.py
│   ├── test_email_agent.py
│   ├── test_escalation_check.py
│   ├── test_gigachat_settings.py
│   ├── test_graph_utils.py
│   ├── test_logging_config.py
│   ├── test_notice_extraction.py
│   └── test_notice_extraction_graph.py
├── example_emails.py       # Sample emails for testing
├── example_workflow.py     # Demo workflow execution
├── requirements.txt        # Python dependencies
├── main_graph.png          # Email Agent visualization
└── notice_extraction_graph.png  # Notice Extraction visualization
```

## 🔧 Configuration

### Escalation Criteria

You can customize escalation rules in `example_workflow.py`:

```python
escalation_criteria = """
There's an immediate risk of electrical, water, or fire damage
"""
```

The system escalates when:
- Text criteria match the notice content, OR
- Potential fines exceed the dollar threshold (default: $100,000)

### Email Routing Rules

Default routing in `graphs/email_agent.py`:
- **Invoices/Billing** → `billing@company.com`
- **Customer Support** → `support@company.com`, `cdetuma@company.com`, `ctu@abc.com`
- **Other** → Attempts to infer correct department

## 🧪 Testing

Run the comprehensive test suite:

```bash
pytest tests/ -v
```

Tests cover:
- Binary question answering chains
- Email agent tool execution
- Escalation checking logic
- GigaChat settings configuration
- Graph utility functions
- Logging configuration
- Notice extraction parsing
- Full notice extraction graph workflows

## 📊 Example Workflows

### Scenario 1: OSHA Violation Notice
1. Email received from OSHA regarding safety violations
2. Agent identifies it as a regulatory notice
3. Calls `extract_notice_data` tool
4. Notice Extraction Graph:
   - Parses violations, fines ($25,000 per violation), deadlines
   - Checks escalation criteria
   - If urgent (e.g., electrical/fire risk) → sends escalation email
   - Creates legal ticket for tracking
   - Answers follow-up questions about compliance requirements

### Scenario 2: Invoice Email
1. Invoice email received from vendor
2. Agent calls `determine_email_action`
3. Forwards to billing department
4. Sends notification to sender with correct contact info

### Scenario 3: Customer Complaint
1. Customer reports HVAC issue
2. Agent routes to support team
3. Forwards to all three support contacts
4. Notifies customer of correct department

## 🔍 Key Components

### Chains (`chains/`)
- **Binary Questions Chain**: Answers yes/no questions about notice content
- **Escalation Check Chain**: Determines if notice requires immediate attention
- **Notice Parser Chain**: Extracts structured data from regulatory notices

### Graphs (`graphs/`)
- **Email Agent**: Main orchestrator using LLM tool calling
- **Notice Extraction**: Specialized workflow for compliance notices

### Utilities (`utils/`)
- **GigaChat Settings**: Configures the LLM model and parameters
- **Graph Utils**: Helper functions for email escalation and ticket creation
- **Logging Config**: Centralized logging for debugging and monitoring
- **Visualize Graph**: Generates Mermaid diagrams of workflow graphs

## 📝 License

This project is based on examples from [Real Python's LangGraph tutorial](https://realpython.com/langgraph-python/).

```

## 📞 Support

For questions or issues, please refer to the LangChain and LangGraph documentation or open an issue in the repository.

