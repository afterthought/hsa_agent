"""
Healthcare Bill Processing Agent

This agent scans for PDF healthcare bills, extracts key information,
and maintains spreadsheets for HSA reconciliation and tax auditing.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import anyio

from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
)
from pdf_utils import extract_pdf_text, scan_for_pdfs
from spreadsheet_manager import SpreadsheetManager


# Optional: Load environment variables if you haven't authenticated Claude Code
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required if Claude Code is already authenticated


# Custom Tools
@tool(
    "scan_pdfs",
    "Scan a directory for PDF files and return their paths",
    {
        "directory": str,
        "recursive": bool,
    }
)
async def scan_pdfs_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """Scan a directory for PDF files."""
    directory = args.get("directory", ".")
    recursive = args.get("recursive", True)

    try:
        pdf_files = scan_for_pdfs(directory, recursive)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "found": len(pdf_files),
                        "files": pdf_files
                    }, indent=2)
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error scanning directory: {str(e)}"
                }
            ],
            "isError": True
        }


@tool(
    "extract_pdf_content",
    "Extract text content from a PDF file",
    {
        "pdf_path": str,
    }
)
async def extract_pdf_content_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """Extract text content from a PDF file."""
    pdf_path = args.get("pdf_path")

    if not pdf_path:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "Error: pdf_path is required"
                }
            ],
            "isError": True
        }

    try:
        text = extract_pdf_text(pdf_path)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Extracted content from {pdf_path}:\n\n{text}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error extracting PDF content: {str(e)}"
                }
            ],
            "isError": True
        }


@tool(
    "add_bill_to_spreadsheet",
    "Add a healthcare bill record to the tracking spreadsheet",
    {
        "provider": str,
        "date": str,
        "amount": float,
        "pdf_path": str,
        "description": str,
        "category": str,
    }
)
async def add_bill_to_spreadsheet_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """Add a healthcare bill to the tracking spreadsheet."""
    try:
        manager = SpreadsheetManager()

        record = {
            "provider": args.get("provider", ""),
            "date": args.get("date", ""),
            "amount": args.get("amount", 0.0),
            "pdf_path": args.get("pdf_path", ""),
            "description": args.get("description", ""),
            "category": args.get("category", "medical"),
        }

        manager.add_record(record)
        manager.save()

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Successfully added bill record:\n{json.dumps(record, indent=2)}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error adding record to spreadsheet: {str(e)}"
                }
            ],
            "isError": True
        }


@tool(
    "get_spreadsheet_summary",
    "Get a summary of all tracked healthcare bills",
    {}
)
async def get_spreadsheet_summary_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get a summary of all tracked bills."""
    try:
        manager = SpreadsheetManager()
        summary = manager.get_summary()

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Healthcare Bills Summary:\n{json.dumps(summary, indent=2)}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error getting summary: {str(e)}"
                }
            ],
            "isError": True
        }


@tool(
    "export_for_taxes",
    "Export healthcare bills in a format suitable for tax filing",
    {
        "year": int,
        "output_path": str,
    }
)
async def export_for_taxes_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """Export bills for tax purposes."""
    try:
        manager = SpreadsheetManager()
        year = args.get("year")
        output_path = args.get("output_path", f"tax_export_{year}.xlsx")

        manager.export_for_taxes(year, output_path)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Successfully exported tax records for {year} to {output_path}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error exporting tax records: {str(e)}"
                }
            ],
            "isError": True
        }


# Create the MCP server with all tools
healthcare_server = create_sdk_mcp_server(
    name="healthcare-tools",
    version="1.0.0",
    tools=[
        scan_pdfs_tool,
        extract_pdf_content_tool,
        add_bill_to_spreadsheet_tool,
        get_spreadsheet_summary_tool,
        export_for_taxes_tool,
    ]
)


async def run_agent(initial_prompt: str = None):
    """Run the healthcare bill processing agent."""

    # Configure agent options
    options = ClaudeAgentOptions(
        mcp_servers={"healthcare": healthcare_server},
        allowed_tools=[
            "mcp__healthcare__scan_pdfs",
            "mcp__healthcare__extract_pdf_content",
            "mcp__healthcare__add_bill_to_spreadsheet",
            "mcp__healthcare__get_spreadsheet_summary",
            "mcp__healthcare__export_for_taxes",
        ],
        system_prompt="""You are a healthcare bill processing assistant. Your job is to:
1. Scan directories for PDF healthcare bills
2. Extract key information: provider name, date, and amount
3. Add records to the tracking spreadsheet
4. Help with HSA reconciliation and tax preparation

When processing bills:
- Look for provider/facility names
- Extract dates in various formats
- Find amounts (look for "Amount Due", "Total", "Balance", etc.)
- Categorize as medical, dental, vision, pharmacy, etc.

Be thorough and ask for clarification if information is unclear.""",
        max_turns=50,
    )

    # Run the agent
    async with ClaudeSDKClient(options=options) as client:
        if initial_prompt:
            print(f"User: {initial_prompt}\n")
            await client.query(initial_prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Agent: {block.text}\n")

        # Interactive loop
        print("Healthcare Bill Processing Agent is ready!")
        print("Type 'exit' or 'quit' to stop.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                await client.query(user_input)

                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                print(f"\nAgent: {block.text}\n")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")


def main():
    """Main entry point for CLI."""
    import sys

    initial_prompt = None
    if len(sys.argv) > 1:
        initial_prompt = " ".join(sys.argv[1:])

    anyio.run(run_agent, initial_prompt)


if __name__ == "__main__":
    main()
