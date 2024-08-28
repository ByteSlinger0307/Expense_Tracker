import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

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

        predict_button = ttk.Button(button_frame, text="Predict Future Expenses", command=self.predict_future_expenses)
        predict_button.grid(row=0, column=5, padx=10)

        manage_categories_button = ttk.Button(button_frame, text="Manage Categories", command=self.open_category_manager)
        manage_categories_button.grid(row=0, column=6, padx=10)

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
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def predict_future_expenses(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "Not enough data to make predictions.")
            return

        # Convert expenses to DataFrame
        data = {
            "Date": [expense.date for expense in self.expenses],
            "Amount": [expense.amount for expense in self.expenses]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Days'] = (df['Date'] - df['Date'].min()).dt.days

        # Prepare data for model
        X = df[['Days']].values.reshape(-1, 1)
        y = df['Amount'].values

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Predict future expenses
        future_days = np.arange(df['Days'].max() + 1, df['Days'].max() + 31).reshape(-1, 1)  # Next 30 days
        predictions = model.predict(future_days)

        # Plot predictions
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Amount'], marker='o', linestyle='-', color='blue', label='Historical Data')
        future_dates = [df['Date'].max() + pd.Timedelta(days=int(day)) for day in future_days.flatten()]
        plt.plot(future_dates, predictions, marker='x', linestyle='--', color='red', label='Predicted Data')
        plt.title('Expense Prediction')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def open_category_manager(self):
        CategoryManager(self.root, self.category_file)

    def clear_entries(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.set("Uncategorized")

    def save_expenses(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Category"])
            for expense in self.expenses:
                writer.writerow([expense.date, expense.description, expense.amount, expense.category])

    def load_expenses(self):
        if os.path.isfile(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) == 4:
                        date, description, amount, category = row
                        self.expenses.append(Expense(date, description, float(amount), category))

    def load_categories(self):
        if os.path.isfile(self.category_file):
            with open(self.category_file, mode='r') as file:
                reader = csv.reader(file)
                self.categories = [row[0] for row in reader]
        else:
            self.categories = []

    def get_categories(self):
        return self.categories if self.categories else ["Uncategorized"]

class CategoryManager:
    def __init__(self, root, category_file):
        self.root = root
        self.category_file = category_file
        self.window = tk.Toplevel(root)
        self.window.title("Manage Categories")
        self.window.geometry("400x300")
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.window, text="Manage Categories", font=("Arial", 18, "bold")).pack(pady=10)

        self.category_listbox = tk.Listbox(self.window, font=("Arial", 12), width=50, height=10, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.category_listbox.pack(pady=10)

        add_category_frame = ttk.Frame(self.window)
        add_category_frame.pack(pady=10)

        ttk.Label(add_category_frame, text="Category Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.new_category_entry = ttk.Entry(add_category_frame, font=("Arial", 12))
        self.new_category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        add_button = ttk.Button(add_category_frame, text="Add Category", command=self.add_category)
        add_button.grid(row=1, column=0, columnspan=2, pady=10)

        remove_button = ttk.Button(add_category_frame, text="Remove Selected", command=self.remove_category)
        remove_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.load_categories()

    def load_categories(self):
        if os.path.isfile(self.category_file):
            with open(self.category_file, mode='r') as file:
                reader = csv.reader(file)
                self.category_listbox.delete(0, tk.END)
                for row in reader:
                    if row:
                        self.category_listbox.insert(tk.END, row[0])

    def add_category(self):
        new_category = self.new_category_entry.get().strip()
        if new_category:
            if not self.category_exists(new_category):
                with open(self.category_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([new_category])
                self.category_listbox.insert(tk.END, new_category)
                self.new_category_entry.delete(0, tk.END)
                print(f"[INFO] Added Category: {new_category}")
            else:
                messagebox.showwarning("Duplicate Category", "This category already exists.")
        else:
            messagebox.showwarning("Invalid Input", "Category name cannot be empty.")

    def remove_category(self):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            selected_category = self.category_listbox.get(selected_index)
            if messagebox.askyesno("Confirm", f"Are you sure you want to remove the category '{selected_category}'?"):
                self.category_listbox.delete(selected_index)
                self.update_category_file()
                print(f"[INFO] Removed Category: {selected_category}")
        else:
            messagebox.showwarning("Selection Error", "Please select a category to remove.")

    def update_category_file(self):
        with open(self.category_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for category in self.category_listbox.get(0, tk.END):
                writer.writerow([category])

    def category_exists(self, category):
        with open(self.category_file, mode='r') as file:
            reader = csv.reader(file)
            return any(row[0] == category for row in reader)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()