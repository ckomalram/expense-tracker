import argparse
import json
from datetime import datetime

EXPENSE_FILE = "expenses.json"

# Utils Methods
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

# Crud Methods
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

def update_expense(expense_id , description=None, amount=None):
    expenses = load_expenses()
    for expense in expenses:
        if(expense['id'] == expense_id):
            if description:
                expense['description'] = description
            if amount:
                expense['amount'] = amount
            save_expenses(expenses)
            print(f'Expense updated successfully (ID: {expense_id})')
            return
    print(f'Not found expense (ID: {expense_id})')

def delete_expense(expense_id):
    expenses = load_expenses()
    refresh_expenses = [expense for expense in expenses if expense['id']!= expense_id]
    if len(expenses) == len(refresh_expenses):
        print(f'Not found expense (ID: {expense_id})')
    else:
        save_expenses(refresh_expenses)
        print(f'Expense delete successfully (ID: {expense_id})')  

def summary_expenses(month= None):
    expenses = load_expenses()
    print(type(month))


    if month:
        totalAmountList = [expense['amount'] for expense in expenses if get_expense_month(expense) == month]
        totalSum = sum(totalAmountList)
        print(f'Total Expenses for Month:  {totalSum}')
    else:
        totalAmountList = [expense['amount'] for expense in expenses]
        totalSum = sum(totalAmountList)
        print(f'Total Expenses:  {totalSum}')

def get_expense_month(expense):
    expenseDate = expense['date']
    formatDate = datetime.strptime(expenseDate, '%Y-%m-%d')
    return formatDate.month

def run():
    parser = argparse.ArgumentParser(description='Expense Tracker Project')
    subparsers = parser.add_subparsers(dest='command')

    # Subacommands to add an new expense
    add_parser = subparsers.add_parser('add', help="Add an new expense")
    add_parser.add_argument('-d', '--description', required=True, help="Description of the expense")
    add_parser.add_argument('-a','--amount', required=True,type=float, help="Amount of the expense" )

    # Subcmd to list expenses
    subparsers.add_parser('list', help="List all expenses")

    # Subcmd to update an expense
    update_parser = subparsers.add_parser('update', help="Update an expense")
    update_parser.add_argument('--id',required=True, type=int, help="Id of expense")
    update_parser.add_argument('--description',help="Description of the expense")
    update_parser.add_argument('--amount', type=float, help="Amount of the expense" )

    # Subcmd to delete an expense
    delete_parser = subparsers.add_parser('delete', help="delete an expense")
    delete_parser.add_argument('--id',required=True, type=int, help="Id of expense")

    # Subcmd to summary general and by month
    summary_parser = subparsers.add_parser('summary', help="show summary of expenses")
    summary_parser.add_argument('-m', '--month',type=int,help='argument to show summary by month')

    args = parser.parse_args()

    if args.command == 'add':
        print(args.description)
        print(args.amount)
        add_expense(args.description, args.amount)
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'update':
        update_expense(args.id, args.description, args.amount)        
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'summary':
        summary_expenses(args.month)
# Resumen de gastos 
# Resumen de gastos por mes

if __name__ == '__main__':
    run()