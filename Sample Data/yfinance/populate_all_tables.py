#!/usr/bin/env python3
"""
Master script to populate all database tables in the correct order.
Runs all data population scripts sequentially.
"""

import subprocess
import sys
import os
from datetime import datetime

# Scripts to run in order
SCRIPTS = [
    {
        "name": "Tickers",
        "script": "insert_tickers.py",
        "description": "Fetching S&P 500 ticker symbols",
        "estimated_time": "~30 seconds"
    },
    {
        "name": "Price History",
        "script": "insert_price_history.py",
        "description": "Downloading 1 year of hourly price data",
        "estimated_time": "~5-15 minutes (depending on network speed)"
    },
    {
        "name": "Users",
        "script": "insert_users.py",
        "description": "Generating fake user accounts",
        "estimated_time": "~5 seconds"
    },
    {
        "name": "Portfolios",
        "script": "insert_portfolios.py",
        "description": "Creating portfolios for users",
        "estimated_time": "~5 seconds"
    },
    {
        "name": "Holdings",
        "script": "insert_holdings.py",
        "description": "Adding stock holdings to portfolios",
        "estimated_time": "~30 seconds"
    },
    {
        "name": "Alerts",
        "script": "insert_alerts.py",
        "description": "Creating price alerts for users",
        "estimated_time": "~10 seconds"
    }
]


def print_header():
    """Print script header"""
    print("=" * 70)
    print(" MarketWatch Database - Complete Data Population")
    print("=" * 70)
    print(f" Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()


def print_step(step_num, total_steps, script_info):
    """Print step information"""
    print(f"\n{'─' * 70}")
    print(f"Step {step_num}/{total_steps}: {script_info['name']}")
    print(f"{'─' * 70}")
    print(f"Description: {script_info['description']}")
    print(f"Estimated time: {script_info['estimated_time']}")
    print(f"Running: {script_info['script']}")
    print()


def run_script(script_path):
    """Run a Python script and return success status"""
    try:
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            text=True,
            capture_output=False  # Show output in real-time
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running {script_path}")
        print(f"  Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


def print_summary(results, start_time):
    """Print execution summary"""
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 70)
    print(" Execution Summary")
    print("=" * 70)

    for i, (script_info, success) in enumerate(results, 1):
        status = "✓ Success" if success else "✗ Failed"
        print(f"{i}. {script_info['name']}: {status}")

    print("=" * 70)
    print(f"Total time: {duration}")
    print(f"Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Overall success
    if all(success for _, success in results):
        print("\n✓ All tables populated successfully!")
        print("\nYou can now:")
        print("  - Access the API at http://localhost:8000")
        print("  - View API docs at http://localhost:8000/docs")
        print("  - Run queries using the Sample Queries/ directory")
        return 0
    else:
        print("\n✗ Some scripts failed. Please check the errors above.")
        return 1


def main():
    """Main execution function"""
    start_time = datetime.now()
    print_header()

    # Check if .env file exists
    if not os.path.exists("../../.env"):
        print("✗ Error: .env file not found!")
        print("  Please create a .env file with your database credentials.")
        print("  See .env.example for reference.")
        return 1

    print(f"Total steps: {len(SCRIPTS)}")
    print("This will take approximately 10-20 minutes to complete.")
    print()

    # Ask for confirmation
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Aborted by user.")
        return 0

    # Run each script in sequence
    results = []
    for i, script_info in enumerate(SCRIPTS, 1):
        print_step(i, len(SCRIPTS), script_info)

        success = run_script(script_info['script'])
        results.append((script_info, success))

        if not success:
            print(f"\n✗ Failed at step {i}: {script_info['name']}")
            print("Stopping execution. Please fix the error and try again.")
            break

        print(f"\n✓ Step {i} completed successfully!")

    # Print summary
    return print_summary(results, start_time)


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user (Ctrl+C)")
        sys.exit(1)
