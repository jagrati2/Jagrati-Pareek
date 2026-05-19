import json

def add(amount, category, description):

    expense = {"amount": amount, "category": category.lower(), "description": description}

    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
            expenses.append(expense)
    except FileNotFoundError:
        expenses = [expense]

    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("Expense added successfully!")

    

def view():

    with open("expenses.json", "r") as file:
        expenses=json.load(file)

    for expense in expenses:
        print(f"Amount: {expense['amount']} - Category: {expense['category']}")

def filter_by_category(category):

    with open('expenses.json', 'r') as file:
        expenses = json.load(file)

    filtered_expenses = [expense for expense in expenses if expense['category'] == category]
    if not filtered_expenses:
        print(f"No expenses found for category: {category}")
        return
    for expense in filtered_expenses:
        print(f"Amount: {expense['amount']} - Category: {expense['category']}")

def total_expenses():

    with open('expenses.json', 'r') as file:
        expenses = json.load(file)

    total = sum(expense['amount'] for expense in expenses)
    print(f"Total Expenses: {total}")

    

              

