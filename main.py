import argparse
import json
from datetime import datetime

EXPENSE_FILE = "expenses.json"

def load_expenses():
    try:
        with open(EXPENSE_FILE, 'r') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []
    except json.JSONDecodeError:
        expenses = []
    return expenses

def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as file:
        json.dump(expenses, file)

def add_expense(description, amount):
    expenses = load_expenses()
    new_expense = {
        'id': len(expenses) + 1,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'description': description,
        'amount': amount
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Created! (ID: {new_expense['id']})")

def list_expenses():
    expenses = load_expenses()
    print("#ID  \tDate       \tDescription  \t\t\t\tAmount")
    for expense in expenses:
        print(f" {expense['id']}   \t{expense['date']}  \t{expense['description']}       \t\t\t\t${expense['amount']}")

def run():
    parser = argparse.ArgumentParser(description='Expense Tracker Project')
    subparsers = parser.add_subparsers(dest='command')

    # Subacommands to add an new expense
    add_parser = subparsers.add_parser('add', help="Add an new expense")
    add_parser.add_argument('-d', '--description', required=True, help="Description of the expense")
    add_parser.add_argument('-a','--amount', required=True, help="Amount of the expense" )

    list_parser = subparsers.add_parser('list', help="List all expenses")


    args = parser.parse_args()

    if args.command == 'add':
        print('We need to add an expense')
        print(args.description)
        print(args.amount)
        add_expense(args.description, args.amount)
    elif args.command == 'list':
        print('We need to list all expenses')
        list_expenses()


if __name__ == '__main__':
    run()