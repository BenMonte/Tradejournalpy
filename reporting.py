import json
import os
from dataclasses import asdict
from datetime import datetime
from models import PerformanceSummary


def write_json(summary: PerformanceSummary, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(asdict(summary), f, indent=2)


def write_markdown(
    summary: PerformanceSummary,
    input_file_name: str,
    llm_narrative: str | None,
    output_path: str,
) -> None:
    s = summary
    lines = [
        "# Trade Journal Analyzer — Performance Report\n",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"**Input file:** {input_file_name}\n",
        "## Performance Metrics\n",
        "| Metric | Value |",
        "|---|---|",
        _row("Total Trades", str(s.total_trades)),
        _row("Win Rate", f"{s.win_rate * 100:.2f}%"),
        _row("Expectancy (R)", f"{s.expectancy_r:.2f}"),
        _row("Average R", f"{s.average_r:.2f}"),
        _row("Avg Win R", f"{s.average_win_r:.2f}"),
        _row("Avg Loss R", f"{s.average_loss_r:.2f}"),
        _row("Profit Factor", f"{s.profit_factor:.2f}"),
        _row("Largest Win R", f"{s.largest_win_r:.2f}"),
        _row("Largest Loss R", f"{s.largest_loss_r:.2f}"),
        _row("Std Dev R", f"{s.std_dev_r:.2f}"),
        _row("Max Consecutive Losses", str(s.max_consecutive_losses)),
        _row("Max Drawdown", f"{s.max_drawdown_percent * 100:.2f}%"),
        "",
        "## Strategy Diagnostics (LLM)\n",
    ]

    if llm_narrative and llm_narrative.strip():
        lines.append(llm_narrative)
    else:
        lines.append("*LLM diagnostics were not generated for this report.*")

    lines.append("")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def _row(label: str, value: str) -> str:
    return f"| {label} | {value} |"
