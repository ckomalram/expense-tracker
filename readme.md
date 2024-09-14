# Expense Tracker
 A simple expense tracker application to manage your finances. The application should allow users to add, delete, and view their expenses. The application should also provide a summary of the expenses.

## Requirements:
- Python 3.x
- Basic knowledge of running scripts from the command line.

## Installation:
    ```sh   
    git clone
    python3 -m venv env    
    source env/bin/activate
    cd expense-tracker
    pip3 install -r requirements.txt
    ``` 
## Features
- Add expenses with description, amount, and category.
- Update or delete existing expenses.
- View all expenses or filter by category.
- View a summary of total expenses.
- View a summary of expenses for a specific month.
- Set a monthly budget and receive a warning when the budget is exceeded.
- Export expenses to a CSV file.

## Usage

To use the Expense Tracker, run the `main.py` script from the command line with the following commands.

### Add an Expense
```bash
python main.py add --description "Lunch" --amount 15.50 --category "Food"
```
This command adds an expense with the given description, amount, and optional category.

### List All Expenses
```bash
python main.py list
```
Lists all recorded expenses.

### List Expenses by Category
```bash
python main.py list --category "Food"
```
Lists all expenses for a specific category.

### View Summary of Total Expenses
```bash
python main.py summary
```
Displays the total expenses recorded.

### View Monthly Summary
```bash
python main.py summary --month 8
```
Displays the total expenses for a specific month (e.g., for August).

### Set a Monthly Budget
```bash
python main.py budget --month 8 --amount 500
```
Sets a budget for a specific month (e.g., August). The system will alert you when you exceed this budget.

### Delete an Expense
```bash
python main.py delete --id 1
```
Deletes the expense with the specified ID.

### Export Expenses to CSV
```bash
python main.py export --filename "expenses.csv"
```
Exports all expenses to a CSV file with the specified filename.
    ```

## Data Storage

Expenses are stored in a JSON file (`expenses.json`). Budgets are stored in a separate file (`budget.json`). You can back up or modify these files as needed.

## Project url
- [expense-tracker](https://roadmap.sh/projects/expense-tracker)

## Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/new-feature).
3. Make your changes and commit them (git commit -am 'Add new feature').
4. Push the branch to your fork (git push origin feature/new-feature).
5. Open a new Pull Request.


## License
This project is licensed under the MIT License. 

## Acknowledgements

Special thanks to the Python community for providing libraries and inspiration to build this project.
