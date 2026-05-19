import json
from storage import *

print("Welcome to the Expense Tracker!")
print("1. Add Expense")
print("2. View Expenses")
print("3. Filter by Category")
print("4. Total Expenses")

choice = input("Choose an option:")

if choice == "1":
    amount= float(input("Enter the amount: "))
    category= input("Enter the category: ")
    description= input("Enter the description: ")
    add(amount, category, description)
elif choice == "2":
    view()
elif choice == "3":
    category= input("Enter the category: ")
    filter_by_category(category)
elif choice == "4":
    total_expenses()
else:
    print("Invalid option.")




