#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

# -------------------- Helper Functions --------------------
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def generate_id(expenses):
    if not expenses:
        return 1
    return max(exp['id'] for exp in expenses) + 1

def find_expense(expenses, expense_id):
    for exp in expenses:
        if exp['id'] == expense_id:
            return exp
    return None

# -------------------- Commands --------------------
def add_expense(args):
    expenses = load_expenses()
    if args.amount < 0:
        print("Amount cannot be negative!")
        return
    new_expense = {
        "id": generate_id(expenses),
        "description": args.description,
        "amount": args.amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_expense['id']})")

def update_expense(args):
    expenses = load_expenses()
    expense = find_expense(expenses, args.id)
    if not expense:
        print("Expense not found!")
        return
    if args.description:
        expense["description"] = args.description
    if args.amount is not None:
        if args.amount < 0:
            print("Amount cannot be negative!")
            return
        expense["amount"] = args.amount
    save_expenses(expenses)
    print(f"Expense ID {args.id} updated successfully")

def delete_expense(args):
    expenses = load_expenses()
    expense = find_expense(expenses, args.id)
    if not expense:
        print("Expense not found!")
        return
    expenses.remove(expense)
    save_expenses(expenses)
    print("Expense deleted successfully")

def list_expenses(args):
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<5} {'Date':<12} {'Description':<20} {'Amount':<10}")
    for exp in expenses:
        print(f"{exp['id']:<5} {exp['date']:<12} {exp['description']:<20} ${exp['amount']:<10}")

def summary_expenses(args):
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    if args.month:
        month_expenses = [e for e in expenses if datetime.strptime(e['date'], "%Y-%m-%d").month == args.month]
        total = sum(e['amount'] for e in month_expenses)
        print(f"Total expenses for month {args.month}: ${total}")
    else:
        total = sum(e['amount'] for e in expenses)
        print(f"Total expenses: ${total}")

# -------------------- CLI Setup --------------------
def main():
    parser = argparse.ArgumentParser(description="Simple Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("--description", required=True, type=str)
    parser_add.add_argument("--amount", required=True, type=float)
    parser_add.set_defaults(func=add_expense)

    # Update
    parser_update = subparsers.add_parser("update")
    parser_update.add_argument("--id", required=True, type=int)
    parser_update.add_argument("--description", type=str)
    parser_update.add_argument("--amount", type=float)
    parser_update.set_defaults(func=update_expense)

    # Delete
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("--id", required=True, type=int)
    parser_delete.set_defaults(func=delete_expense)

    # List
    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=list_expenses)

    # Summary
    parser_summary = subparsers.add_parser("summary")
    parser_summary.add_argument("--month", type=int, help="Month number (1-12)")
    parser_summary.set_defaults(func=summary_expenses)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
