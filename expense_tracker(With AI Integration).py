import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class Expense:
    def __init__(self, date, description, amount, category="Uncategorized"):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

class ExpenseTracker:
    def __init__(self, root, expense_file="expenses.csv", category_file="categories.csv"):
        self.expenses = []
        self.filename = expense_file
        self.category_file = category_file
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x700")
        self.style = Style(theme='superhero')  # Setting a modern theme

        # Load expenses and categories from files if they exist
        self.load_expenses()
        self.load_categories()

        # Set up the UI components
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ttk.Label(self.root, text="Expense Tracker", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        # Frame for input fields
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20, padx=20, fill='x')

        # Description input
        ttk.Label(input_frame, text="Description:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.description_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Amount input
        ttk.Label(input_frame, text="Amount:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Category input
        ttk.Label(input_frame, text="Category:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.get_categories(), font=("Arial", 12))
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.category_dropdown.set("Uncategorized")

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=0, column=0, padx=10)

        remove_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_expense)
        remove_button.grid(row=0, column=1, padx=10)

        total_button = ttk.Button(button_frame, text="Show Total", command=self.show_total_expenses)
        total_button.grid(row=0, column=2, padx=10)

        graph_button = ttk.Button(button_frame, text="Show Expenses Graph", command=self.show_expenses_graph)
        graph_button.grid(row=0, column=3, padx=10)

        bar_graph_button = ttk.Button(button_frame, text="Show Category Bar Graph", command=self.show_category_bar_graph)
        bar_graph_button.grid(row=0, column=4, padx=10)

        manage_categories_button = ttk.Button(button_frame, text="Manage Categories", command=self.open_category_manager)
        manage_categories_button.grid(row=0, column=5, padx=10)

        exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack(pady=20)

        # Listbox to display expenses
        self.expense_listbox = tk.Listbox(self.root, font=("Arial", 12), width=70, height=15, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.expense_listbox.pack(pady=10, padx=20, fill='x')

        # Load existing expenses into the listbox
        self.display_expenses()

    def display_expenses(self):
        # Clear the listbox
        self.expense_listbox.delete(0, tk.END)
        # Add each expense to the listbox
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"Date: {expense.date}, Description: {expense.description}, Amount: ₹{expense.amount:.2f}, Category: {expense.category}")

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()
        date = datetime.now().strftime("%Y-%m-%d")  # Get current date

        if description and amount:
            try:
                amount = float(amount)
                expense = Expense(date, description, amount, category)
                self.expenses.append(expense)
                self.display_expenses()  # Update the display
                self.save_expenses()  # Save the expense after adding it
                self.clear_entries()
                print(f"[INFO] Added Expense - Date: {date}, Description: {description}, Amount: ₹{amount:.2f}, Category: {category}")
            except ValueError:
                messagebox.showerror("Invalid Input", "Amount must be a number.")
        else:
            messagebox.showwarning("Missing Data", "Please fill all fields.")

    def remove_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            removed_expense = self.expenses[selected_index[0]]
            self.expense_listbox.delete(selected_index)
            del self.expenses[selected_index[0]]
            self.save_expenses()
            print(f"[INFO] Removed Expense - Date: {removed_expense.date}, Description: {removed_expense.description}, Amount: ₹{removed_expense.amount:.2f}, Category: {removed_expense.category}")
            messagebox.showinfo("Success", "Expense removed successfully.")
        else:
            messagebox.showwarning("Selection Error", "Please select an expense to remove.")

    def show_total_expenses(self):
        total = sum(expense.amount for expense in self.expenses)
        messagebox.showinfo("Total Expenses", f"Total Expenses: ₹{total:.2f}")
        print(f"[INFO] Total Expenses: ₹{total:.2f}")

    def show_expenses_graph(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses to show.")
            return

        # Convert expenses to DataFrame
        data = {
            "Date": [expense.date for expense in self.expenses],
            "Amount": [expense.amount for expense in self.expenses],
            "Category": [expense.category for expense in self.expenses]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', inplace=True)

        # Plot
        plt.figure(figsize=(12, 6))
        categories = df['Category'].unique()
        colors = plt.get_cmap('tab10').colors  # Use a color map
        for i, category in enumerate(categories):
            category_data = df[df['Category'] == category]
            plt.plot(category_data['Date'], category_data['Amount'], marker='o', linestyle='-', color=colors[i % len(colors)], label=category)
        plt.title('Expenses Over Time by Category')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def show_category_bar_graph(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses to show.")
            return

        # Convert expenses to DataFrame
        data = {
            "Category": [expense.category for expense in self.expenses],
            "Amount": [expense.amount for expense in self.expenses]
        }
        df = pd.DataFrame(data)
        category_totals = df.groupby('Category').sum().reset_index()

        # Plot
        plt.figure(figsize=(10, 6))
        plt.bar(category_totals['Category'], category_totals['Amount'], color='skyblue')
        plt.title('Total Expenses by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def clear_entries(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.set("Uncategorized")

    def save_expenses(self):
        # Write expenses to the CSV file
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Category"])  # Write header row
            for expense in self.expenses:
                writer.writerow([expense.date, expense.description, expense.amount, expense.category])  # Write each expense

    def load_expenses(self):
        # Load expenses from the CSV file
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)
                self.expenses = [Expense(row["Date"], row["Description"], float(row["Amount"]), row["Category"]) for row in reader]

    def get_categories(self):
        # Return categories from the file
        if os.path.exists(self.category_file):
            with open(self.category_file, "r") as file:
                return [row[0] for row in csv.reader(file)]
        return ["Uncategorized"]

    def load_categories(self):
        # Initialize categories if the file does not exist
        if not os.path.exists(self.category_file):
            with open(self.category_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Uncategorized"])

    def open_category_manager(self):
        CategoryManager(self)

class CategoryManager:
    def __init__(self, tracker):
        self.tracker = tracker
        self.top = tk.Toplevel()
        self.top.title("Category Manager")
        self.top.geometry("400x300")

        # Frame for category management
        category_frame = ttk.Frame(self.top)
        category_frame.pack(pady=20, padx=20, fill='x')

        # Category listbox
        self.category_listbox = tk.Listbox(category_frame, font=("Arial", 12), width=30, height=10, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.category_listbox.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(category_frame, orient=tk.VERTICAL, command=self.category_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.category_listbox.config(yscrollcommand=scrollbar.set)

        # Frame for adding categories
        add_frame = ttk.Frame(self.top)
        add_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(add_frame, text="New Category:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.new_category_entry = ttk.Entry(add_frame, font=("Arial", 12))
        self.new_category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        add_button = ttk.Button(add_frame, text="Add Category", command=self.add_category)
        add_button.grid(row=0, column=2, padx=10)

        # Update the listbox with existing categories
        self.update_category_list()

    def add_category(self):
        new_category = self.new_category_entry.get()
        if new_category and new_category not in self.tracker.get_categories():
            self.tracker.get_categories().append(new_category)
            self.update_category_file()
            self.update_category_list()
            self.new_category_entry.delete(0, tk.END)
            print(f"[INFO] Added new category: {new_category}")
        else:
            messagebox.showwarning("Invalid Category", "Category is either empty or already exists.")

    def update_category_file(self):
        with open(self.tracker.category_file, "w", newline="") as file:
            writer = csv.writer(file)
            for category in self.tracker.get_categories():
                writer.writerow([category])

    def update_category_list(self):
        self.category_listbox.delete(0, tk.END)
        for category in self.tracker.get_categories():
            self.category_listbox.insert(tk.END, category)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
