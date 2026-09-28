# Personal Finance / Expense Tracker

An end-to-end mini analyst tool: logs expenses into a SQLite database
via a simple CLI, then produces a spending summary and charts —
demonstrating the full pipeline from data entry → storage → insight.

## Files
- `expense_tracker.py` — CLI: `seed`, `add`, `report`
- `sample_expenses.csv` — sample data (150 transactions across 9 months)
- `chart_spend_by_category.png`, `chart_monthly_spend.png` — example output charts

## How to run
```bash
pip install pandas matplotlib

python expense_tracker.py seed     # loads sample_expenses.csv into expenses.db
python expense_tracker.py add      # interactively log a new expense
python expense_tracker.py report   # prints summary + saves charts
```

## What it does
- Stores each expense (`date`, `category`, `amount`, `note`) in a local
  SQLite database (`expenses.db`, created automatically)
- `report` computes:
  - Total spend
  - Spend by category (pie chart)
  - Spend by month (bar chart)

## Skills demonstrated
SQLite schema design and querying from Python, building a simple CLI
tool with `argparse`, and Pandas-based aggregation/visualization — a
compact demonstration of the full "log → store → analyze" pipeline.

## Possible extensions
- Add a monthly budget per category and flag overspending
- Add a `--month` filter to `report` for month-specific breakdowns
- Build a small Streamlit front end on top of the same database
