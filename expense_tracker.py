"""
Personal Finance / Expense Tracker
------------------------------------
A small end-to-end analyst-style tool: logs expenses into a SQLite
database, then visualizes spending by category and over time.

Run:
    python expense_tracker.py seed        # load sample_expenses.csv into the DB (first run)
    python expense_tracker.py add         # interactively add a new expense
    python expense_tracker.py report      # print summary + save charts
"""
import argparse
import sqlite3
import sys
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "expenses.db"
SAMPLE_CSV = "sample_expenses.csv"

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Entertainment",
              "Shopping", "Health", "Education", "Other"]


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT
        )
    """)
    return conn


def cmd_seed(args):
    conn = get_conn()
    df = pd.read_csv(SAMPLE_CSV)
    df.to_sql("expenses", conn, if_exists="append", index=False)
    print(f"Loaded {len(df)} sample expenses into {DB_FILE}.")


def cmd_add(args):
    conn = get_conn()
    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()
    amount = float(input("Amount: ").strip())
    note = input("Note (optional): ").strip()
    today = date.today().isoformat()

    conn.execute(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?,?,?,?)",
        (today, category, amount, note),
    )
    conn.commit()
    print(f"Logged {amount} in {category} on {today}.")


def cmd_report(args):
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM expenses", conn, parse_dates=["date"])

    if df.empty:
        print("No expenses logged yet. Run `seed` or `add` first.")
        sys.exit(0)

    df["month"] = df["date"].dt.to_period("M").astype(str)

    print("=== Total spend ===")
    print(f"{df['amount'].sum():,.2f}\n")

    print("=== Spend by category ===")
    by_cat = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    print(by_cat.round(2))
    print()

    print("=== Spend by month ===")
    by_month = df.groupby("month")["amount"].sum().sort_index()
    print(by_month.round(2))

    # Chart 1: pie chart of spend by category
    plt.figure(figsize=(6, 6))
    by_cat.plot(kind="pie", autopct="%1.0f%%")
    plt.ylabel("")
    plt.title("Spend by Category")
    plt.tight_layout()
    plt.savefig("chart_spend_by_category.png", dpi=150)
    plt.close()

    # Chart 2: monthly spend trend
    plt.figure(figsize=(8, 4))
    by_month.plot(kind="bar", color="#1F4E79")
    plt.title("Monthly Spend")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("chart_monthly_spend.png", dpi=150)
    plt.close()

    print("\nCharts saved: chart_spend_by_category.png, chart_monthly_spend.png")


def main():
    parser = argparse.ArgumentParser(description="Personal expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("seed", help="load sample data into the database").set_defaults(func=cmd_seed)
    sub.add_parser("add", help="interactively add an expense").set_defaults(func=cmd_add)
    sub.add_parser("report", help="print summary and save charts").set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
