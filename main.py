import argparse
import json
from datetime import datetime
import csv

EXPENSE_FILE = "expenses.json"
EXPORT_FILE = "expenses.csv"
BUDGET_FILE = "budget.json"
FIELD_NAMES = ['id','description','amount','category','date']

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

def print_expenses(expenses):
        print("#ID  \tDate       \tDescription   \t\t\t\tCategory  \t\t\t\tAmount")
        for expense in expenses:
            print(f" {expense['id']}   \t{expense['date']}  \t{expense['description']}       \t\t\t\t{expense['category']}       \t\t\t\t${expense['amount']}")

def get_expense_month(expense):
    expenseDate = expense['date']
    formatDate = datetime.strptime(expenseDate, '%Y-%m-%d')
    return formatDate.month


# Crud Methods
def add_expense(description, amount, category= "general"):
    expenses = load_expenses()
    new_expense = {
        'id': len(expenses) + 1,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'description': description,
        'amount': amount,
        'category': category
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Created! (ID: {new_expense['id']})")

def list_expenses(category= None):
    expenses = load_expenses()
    if category:
        filtered_expenses = [expense for expense in expenses if expense['category'] == category]
        print_expenses(filtered_expenses)
    else:
        print_expenses(expenses)

def update_expense(expense_id , description=None, amount=None, category=None):
    expenses = load_expenses()
    for expense in expenses:
        if(expense['id'] == expense_id):
            if description:
                expense['description'] = description
            if amount:
                expense['amount'] = amount
            if category:
                expense['category'] = category                
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

    if month:
        totalAmountList = [expense['amount'] for expense in expenses if get_expense_month(expense) == month]
        totalSum = sum(totalAmountList)
        print(f'Total Expenses for Month:  {totalSum}')
    else:
        totalAmountList = [expense['amount'] for expense in expenses]
        totalSum = sum(totalAmountList)
        print(f'Total Expenses:  {totalSum}')

# Budget Methods
def load_budget():
    try:
        with open(BUDGET_FILE, 'r') as file:
            budget = json.load(file)
    except FileNotFoundError:
        budget = []
    return budget

def save_budget(budget):
    with open(BUDGET_FILE, 'w') as file:
        json.dump(budget, file, indent=4)

def set_budget(month, amount):
    budgets = load_budget()
    budget = [budget for budget in budgets if budget['month'] == month]
    if budget:
        budget[0]['amount'] = amount
    else:
        new_budget = {
            'month': month,
            'amount': amount
        }
        budgets.append(new_budget)

    save_budget(budgets)
    print(f"Budget set for month {month}: ${amount}")

def check_budget(month):
    budgets = load_budget()
    expenses = load_expenses() 
    budget = [budget for budget in budgets if budget['month'] == month]   
    total_expenses = sum(expense['amount'] for expense in expenses if datetime.strptime(expense['date'], '%Y-%m-%d').month == month)
    
    if  not budget:
        print(f"Budget for month {month} not found. please set.")
        return
    elif  total_expenses > budget[0]['month']:
        print(f"Warning: You have exceeded your budget for month {month}!")
        print(f"Total expenses: ${total_expenses}, Budget: ${budget[0]['month']}")
    else:
        print(f"Total expenses for month {month}: ${total_expenses}")


# export methods
def export_file(filename):
    expenses = load_expenses()
    with open(filename, 'w', newline='') as csvile:       
        writter = csv.DictWriter(csvile, fieldnames=FIELD_NAMES)
        writter.writeheader()
        for expense in expenses:
            writter.writerow(expense)

    print(f"Expenses exported to {filename} successfully!")


def run():
    parser = argparse.ArgumentParser(description='Expense Tracker Project')
    subparsers = parser.add_subparsers(dest='command')

    # Subacommands to add an new expense
    add_parser = subparsers.add_parser('add', help="Add an new expense")
    add_parser.add_argument('-d', '--description', required=True, help="Description of the expense")
    add_parser.add_argument('-a','--amount', required=True,type=float, help="Amount of the expense" )
    add_parser.add_argument('-c','--category',default="general",help="category of the expense" )

    # Subcmd to list expenses
    list_parser = subparsers.add_parser('list', help="List all expenses")
    list_parser.add_argument('-c','--category',help="filter by category of the expense" )

    # Subcmd to update an expense
    update_parser = subparsers.add_parser('update', help="Update an expense")
    update_parser.add_argument('--id',required=True, type=int, help="Id of expense")
    update_parser.add_argument('--description',help="Description of the expense")
    update_parser.add_argument('--amount', type=float, help="Amount of the expense" )
    update_parser.add_argument('--category',help="category of the expense" )


    # Subcmd to delete an expense
    delete_parser = subparsers.add_parser('delete', help="delete an expense")
    delete_parser.add_argument('--id',required=True, type=int, help="Id of expense")

    # Subcmd to summary general and by month
    summary_parser = subparsers.add_parser('summary', help="show summary of expenses")
    summary_parser.add_argument('-m', '--month',type=int,help='argument to show summary by month')

    # Subcmd to initialize budget
    check_budget_parser= subparsers.add_parser('check-budget', help="check monthly budget")
    check_budget_parser.add_argument('--month', required=True, type=int, help="month for the budget")

    budget_parser = subparsers.add_parser('budget', help="Set monthly budget")
    budget_parser.add_argument('--month', required=True, type=int, help="month for the budget")
    budget_parser.add_argument('--amount', required=True, type=float, help="budget amount for the month")

    # Subcmd for export in csv
    csv_parser = subparsers.add_parser('export', help="to export expenses in csv")
    csv_parser.add_argument('-f','--filename', default=EXPORT_FILE, help="name of file to export data") 

    args = parser.parse_args()

    if args.command == 'add':
        add_expense(args.description, args.amount, args.category)
    elif args.command == 'list':
        list_expenses(args.category)
    elif args.command == 'update':
        update_expense(args.id, args.description, args.amount, args.category)        
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'summary':
        summary_expenses(args.month)
    elif args.command == 'budget':
        set_budget(args.month,args.amount)       
    elif args.command == 'check-budget':
        check_budget(args.month)     
    elif args.command == 'export':
        export_file(args.filename)              


if __name__ == '__main__':
    run()