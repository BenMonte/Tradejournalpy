A CLI tool that analyzes historical trade data from an Excel journal and generates performance reports with optional LLM-powered strategy diagnostics.

## Features

- Reads trade data from `.xlsx` files (Entry Date, P&L, Return %, R-Multiple)
- Computes 12 performance metrics: win rate, expectancy, profit factor, drawdown, and more
- Generates JSON and Markdown reports
- Optional GPT-powered strategy diagnostics via the OpenAI API

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py --file TradeDatabase.xlsx
```

### Options

| Flag | Description | Default |
|---|---|---|
| `--file <path>` | Path to the Excel trade journal | `TradeDatabase.xlsx` |
| `--capital <amount>` | Initial capital in dollars | `10000` |
| `--skip-llm` | Skip LLM narrative generation | disabled |

### Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your own is required for diagnostics |
| `OPENAI_MODEL` | Override the default model |

## Output

Reports are written to the `output/` directory:
- `report.json` — machine-readable performance metrics
- `report.md` — formatted Markdown report with optional LLM analysis

## Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
main.py            CLI entry point
models.py          Trade and PerformanceSummary dataclasses
ingest.py          Excel file reader (openpyxl)
calculator.py      Performance metric calculations
llm.py             OpenAI API integration
reporting.py       JSON and Markdown report writers
tests/
  test_calculator.py   Unit tests for all metrics
```
