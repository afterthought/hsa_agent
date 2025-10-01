"""
Example Usage Script for Healthcare Bill Processing Agent

This script demonstrates various ways to use the healthcare agent.
"""

import anyio
from healthcare_agent import run_agent


async def example_1_scan_and_process():
    """Example 1: Scan a directory and process all bills."""
    print("=== Example 1: Scan and Process ===\n")
    await run_agent("Scan ./sample_bills for PDFs and extract information from all of them")


async def example_2_get_summary():
    """Example 2: Get a summary of tracked bills."""
    print("\n=== Example 2: Get Summary ===\n")
    await run_agent("Show me a summary of all tracked healthcare bills")


async def example_3_export_taxes():
    """Example 3: Export bills for tax year."""
    print("\n=== Example 3: Export for Taxes ===\n")
    await run_agent("Export all healthcare bills from 2024 for tax filing")


async def example_4_interactive():
    """Example 4: Start interactive session."""
    print("\n=== Example 4: Interactive Mode ===\n")
    await run_agent()


async def main():
    """Run examples."""
    import sys

    examples = {
        "1": ("Scan and Process", example_1_scan_and_process),
        "2": ("Get Summary", example_2_get_summary),
        "3": ("Export for Taxes", example_3_export_taxes),
        "4": ("Interactive Mode", example_4_interactive),
    }

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("Healthcare Bill Processing Agent - Examples\n")
        print("Available examples:")
        for key, (name, _) in examples.items():
            print(f"  {key}. {name}")
        print("\nUsage: uv run python example_usage.py [1-4]")
        print("Or run without arguments for interactive mode\n")

        choice = input("Select an example (1-4) or press Enter for interactive: ").strip()

    if not choice:
        choice = "4"

    if choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}\n")
        await func()
    else:
        print(f"Invalid choice: {choice}")
        print("Please select 1-4")


if __name__ == "__main__":
    anyio.run(main)
