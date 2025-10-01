# Healthcare Bill Processing Agent

An AI-powered agent built with the Claude Agent SDK that automatically processes healthcare bills from PDFs, extracts key information, and maintains organized spreadsheets for HSA reconciliation and tax auditing.

## Features

- 🔍 **Automatic PDF Scanning**: Recursively scans directories for healthcare bill PDFs
- 📄 **Intelligent Extraction**: Uses Claude AI to extract provider, date, amount, and categorize bills
- 📊 **Spreadsheet Management**: Automatically maintains organized Excel spreadsheets
- 💰 **HSA Reconciliation**: Tracks HSA-eligible expenses separately
- 📈 **Tax Preparation**: Exports tax-ready summaries by year
- 🤖 **Interactive Agent**: Natural language interface for queries and operations

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)**: Fast Python package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Node.js** (for Claude Code)
- **Claude Code CLI**: Install with `npm install -g @anthropic-ai/claude-code`
- **Claude Code Authentication**: You need Claude Code authenticated with an API key

## Installation

### Option 1: Install as CLI Tool (Recommended)

```bash
# Navigate to the project directory
cd agent_demo

# Install with uv (creates virtual environment and installs as CLI)
uv sync

# The CLI is now available as 'healthcare-agent'
uv run healthcare-agent
```

### Option 2: Install in Development Mode

```bash
# Install in editable mode for development
uv pip install -e .

# Now you can use 'healthcare-agent' command directly
healthcare-agent
```

### Authentication Setup

If you haven't already authenticated Claude Code, you have two options:

**Option A - Use Claude Code's built-in authentication (recommended):**
```bash
# The SDK will use Claude Code's existing credentials
# No additional setup needed if you're already using Claude Code
```

**Option B - Set API key via environment variable:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your API key from [Anthropic Console](https://console.anthropic.com/)

## Quick Start

### Run the Agent Interactively

```bash
# Using uv run
uv run healthcare-agent

# Or if installed globally
healthcare-agent
```

This starts an interactive session where you can ask the agent to:
- Scan for PDFs
- Process specific bills
- View summaries
- Export reports

### Run with Initial Command

```bash
# Process bills immediately
uv run healthcare-agent "Scan ~/Documents/Medical for PDFs and process all bills"

# Or if installed globally
healthcare-agent "Scan ~/Documents/Medical for PDFs and process all bills"
```

## Usage Examples

### Example 1: Process Bills from a Directory

```bash
healthcare-agent "Scan ~/Documents/Healthcare for PDFs and extract information from all bills"
```

The agent will:
1. Find all PDF files in the directory
2. Extract text from each PDF
3. Identify provider, date, and amount
4. Add records to the tracking spreadsheet

### Example 2: Interactive Session

```
You: Scan ./medical_bills for PDFs

Agent: I found 5 PDF files. Would you like me to process them?

You: Yes, process all of them

Agent: Processing bill 1 of 5...
Extracted:
- Provider: City Hospital
- Date: 2024-03-15
- Amount: $450.00
- Category: medical

Added to spreadsheet.
...

You: Show me a summary

Agent: Healthcare Bills Summary:
- Total Records: 5
- Total Amount: $2,340.50
- By Category:
  - Medical: $1,890.00
  - Dental: $450.50
...

You: Export tax records for 2024

Agent: Successfully exported tax records for 2024 to tax_export_2024.xlsx
```

### Example 3: HSA Reconciliation

```python
# In Python script or interactive session
You: Show me all HSA-eligible expenses and export them for reconciliation

Agent: Found 12 HSA-eligible expenses totaling $3,450.00
Exported to hsa_reconciliation.xlsx
```

## Custom Tools

The agent provides these custom tools:

### 1. `scan_pdfs`
Scans a directory for PDF files.
- **Parameters:**
  - `directory`: Path to scan
  - `recursive`: Scan subdirectories (default: true)

### 2. `extract_pdf_content`
Extracts text from a PDF file.
- **Parameters:**
  - `pdf_path`: Path to the PDF file

### 3. `add_bill_to_spreadsheet`
Adds a healthcare bill record to the tracking spreadsheet.
- **Parameters:**
  - `provider`: Provider/facility name
  - `date`: Bill date (various formats accepted)
  - `amount`: Bill amount
  - `category`: medical, dental, vision, pharmacy, etc.
  - `description`: Additional details
  - `pdf_path`: Path to source PDF

### 4. `get_spreadsheet_summary`
Returns a summary of all tracked bills with breakdowns by year, category, and provider.

### 5. `export_for_taxes`
Exports bills for a specific tax year.
- **Parameters:**
  - `year`: Tax year
  - `output_path`: Output file path

## Spreadsheet Structure

### Main Workbook: `healthcare_bills.xlsx`

**Bills Sheet:**
- date: Bill date
- provider: Provider/facility name
- amount: Bill amount
- category: Bill category
- description: Additional details
- pdf_path: Path to source PDF
- year: Extracted year
- month: Extracted month
- added_on: When the record was added

**Summary Sheets:**
- By Year: Annual totals
- By Category: Totals by category
- By Provider: Totals by provider

### Tax Export: `tax_export_{year}.xlsx`

- Details: All bills for the year
- Category Summary: Totals by category
- Monthly Summary: Month-by-month breakdown
- Summary: Overall statistics

### HSA Reconciliation: `hsa_reconciliation.xlsx`

- HSA Expenses: All HSA-eligible expenses
- Yearly Totals: HSA totals by year

## Project Structure

```
agent_demo/
├── pyproject.toml           # Project metadata and dependencies
├── healthcare_agent.py      # Main agent script (CLI entry point)
├── pdf_utils.py             # PDF scanning and extraction
├── spreadsheet_manager.py   # Spreadsheet management
├── example_usage.py         # Example usage demonstrations
├── .python-version          # Python version for uv
├── .gitignore              # Git ignore patterns
├── README.md               # This file
└── healthcare_bills.xlsx   # Generated spreadsheet (created at runtime)
```

## Development

### Working with uv

```bash
# Install dependencies
uv sync

# Run the CLI in development
uv run healthcare-agent

# Run tests (if you add them)
uv run pytest

# Add a new dependency
uv add package-name

# Update dependencies
uv lock --upgrade

# Format code with ruff
uv run ruff format .

# Lint code
uv run ruff check .
```

### Building and Publishing

```bash
# Build the package
uv build

# The package will be in dist/
# You can install it with: pip install dist/healthcare_bill_agent-0.1.0-py3-none-any.whl
```

## Advanced Configuration

### Customizing the Agent

Edit `healthcare_agent.py` to modify:

- **System prompt**: Adjust how the agent interprets bills
- **Categories**: Add custom bill categories
- **Extraction logic**: Modify what information to extract
- **Tool permissions**: Control which tools are available

### Adding Custom Tools

```python
from claude_agent_sdk import tool

@tool(
    "my_custom_tool",
    "Description of what it does",
    {"param1": str, "param2": int}
)
async def my_custom_tool(args):
    # Your logic here
    return {
        "content": [
            {"type": "text", "text": "Result"}
        ]
    }

# Add to healthcare_server tools list
```

## Troubleshooting

### "Claude Code not installed"
```bash
npm install -g @anthropic-ai/claude-code
```

### "No text could be extracted from the PDF"
Some PDFs are image-based. Consider using OCR:
```bash
pip install pytesseract
```

### "API key not found"
Ensure your `.env` file exists and contains:
```
ANTHROPIC_API_KEY=your-actual-api-key
```

### Permission Errors
Ensure the agent has read permissions for PDF directories and write permissions for the output directory.

## Best Practices

1. **Organize PDFs**: Keep bills in a dedicated directory
2. **Consistent Naming**: Use descriptive filenames (e.g., `2024-03-15_CityHospital.pdf`)
3. **Regular Processing**: Process bills regularly to avoid backlog
4. **Verify Extraction**: Review extracted information for accuracy
5. **Backup Spreadsheets**: Keep backups of your tracking spreadsheets
6. **OCR for Scans**: If bills are scanned images, use OCR preprocessing

## Security & Privacy

- All processing happens locally
- PDFs are not uploaded anywhere
- API calls only contain extracted text snippets
- Spreadsheets remain on your system
- Keep your API key secure in `.env` file

## Contributing

To extend functionality:
1. Add new tools in `healthcare_agent.py`
2. Enhance PDF extraction in `pdf_utils.py`
3. Add export formats in `spreadsheet_manager.py`

## License

This project is provided as-is for educational and personal use.

## Support

For issues related to:
- **Claude Agent SDK**: [GitHub Issues](https://github.com/anthropics/claude-agent-sdk-python/issues)
- **Claude API**: [Anthropic Support](https://support.anthropic.com/)
- **This Agent**: Open an issue in your repository

## Future Enhancements

Potential improvements:
- [ ] OCR support for image-based PDFs
- [ ] Multiple spreadsheet formats (CSV, Google Sheets)
- [ ] Duplicate detection
- [ ] Receipt photo processing
- [ ] Insurance claim tracking
- [ ] Automated categorization rules
- [ ] Email integration for e-bills
- [ ] Budget alerts and notifications
# hsa_agent
