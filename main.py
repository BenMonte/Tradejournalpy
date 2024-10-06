import argparse
import os
import sys

from ingest import read_trades
from calculator import calculate
from llm import generate_narrative
from reporting import write_json, write_markdown


DEFAULT_FILE = "TradeDatabase.xlsx"
DEFAULT_CAPITAL = 10_000
OUTPUT_DIR = "output"


def main() -> None:
    parser = argparse.ArgumentParser(description="Trade Journal Analyzer")
    parser.add_argument("--file", default=DEFAULT_FILE, help="Path to the Excel trade journal")
    parser.add_argument("--capital", type=float, default=DEFAULT_CAPITAL, help="Initial capital in dollars")
    parser.add_argument("--skip-llm", action="store_true", help="Skip LLM narrative even if API key is set")
    args = parser.parse_args()

    print("Trade Journal Analyzer\n")

    # 1. Ingest
    try:
        trades = read_trades(args.file)
        print(f"Loaded {len(trades)} trades from {args.file}\n")
    except Exception as e:
        print(f"Failed to load trades: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Compute metrics
    summary = calculate(trades, args.capital)
    _print_summary(summary)

    # 3. LLM diagnostics
    narrative = None
    if not args.skip_llm:
        print("\nGenerating LLM diagnostics...")
        narrative = generate_narrative(summary)
        if narrative:
            print("\n=== Strategy Diagnostics ===")
            print(narrative)

    # 4. Write reports
    try:
        json_path = os.path.join(OUTPUT_DIR, "report.json")
        write_json(summary, json_path)
        print(f"\nJSON report:     {json_path}")

        md_path = os.path.join(OUTPUT_DIR, "report.md")
        write_markdown(summary, args.file, narrative, md_path)
        print(f"Markdown report: {md_path}")
    except Exception as e:
        print(f"Failed to write reports: {e}", file=sys.stderr)
        sys.exit(1)


def _print_summary(s) -> None:
    print("=== Performance Summary ===")
    print(f"  Total Trades:          {s.total_trades}")
    print(f"  Win Rate:              {s.win_rate * 100:.2f}%")
    print(f"  Expectancy (R):        {s.expectancy_r:.2f}")
    print(f"  Average R:             {s.average_r:.2f}")
    print(f"  Avg Win R:             {s.average_win_r:.2f}")
    print(f"  Avg Loss R:            {s.average_loss_r:.2f}")
    print(f"  Profit Factor:         {s.profit_factor:.2f}")
    print(f"  Largest Win R:         {s.largest_win_r:.2f}")
    print(f"  Largest Loss R:        {s.largest_loss_r:.2f}")
    print(f"  Std Dev R:             {s.std_dev_r:.2f}")
    print(f"  Max Consec. Losses:    {s.max_consecutive_losses}")
    print(f"  Max Drawdown:          {s.max_drawdown_percent * 100:.2f}%")


if __name__ == "__main__":
    main()
