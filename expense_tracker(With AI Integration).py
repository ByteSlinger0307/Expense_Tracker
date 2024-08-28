import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import csv
import os
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

class Expense:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

class ExpenseTracker:
    def __init__(self, root, filename="expenses.csv", categories_file="categories.csv"):
        self.expenses = []
        self.filename = filename
        self.categories_file = categories_file
        self.categories = self.load_categories()  # Load categories from file
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x700")
        self.style = Style(theme='superhero')  # Setting a modern theme

        # Load expenses from file if it exists
        self.load_expenses()

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

        # Category dropdown
        ttk.Label(input_frame, text="Category:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.categories, font=("Arial", 12))
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.category_dropdown.set("Uncategorized")

        input_frame.columnconfigure(1, weight=1)  # Make entry fields expand with the window

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=0, column=0, padx=10)

        remove_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_expense)
        remove_button.grid(row=0, column=1, padx=10)

        total_button = ttk.Button(button_frame, text="Show Total", command=self.show_total_expenses)
        total_button.grid(row=0, column=2, padx=10)

        manage_categories_button = ttk.Button(button_frame, text="Manage Categories", command=self.open_category_management)
        manage_categories_button.grid(row=0, column=3, padx=10)

        add_category_button = ttk.Button(button_frame, text="Add Category", command=self.open_add_category_window)
        add_category_button.grid(row=0, column=4, padx=10)

        predict_button = ttk.Button(button_frame, text="Predict Future Expenses", command=self.predict_future_expenses)
        predict_button.grid(row=0, column=5, padx=10)

        exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack(pady=20)

        # Listbox to display expenses
        self.expense_listbox = tk.Listbox(self.root, font=("Arial", 12), width=70, height=15, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.expense_listbox.pack(pady=10, padx=20, fill='x')

        # Load existing expenses into the listbox
        self.display_expenses()

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
                self.expense_listbox.insert(tk.END, f"Date: {date}, Description: {description}, Amount: ₹{amount:.2f}, Category: {category}")
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
        # Load expenses from the CSV file if it exists
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) == 4:
                        date, description, amount, category = row
                        try:
                            amount = float(amount)
                            expense = Expense(date, description, amount, category)
                            self.expenses.append(expense)
                        except ValueError:
                            continue  # Skip rows with invalid data

    def load_categories(self):
        # Load categories from the CSV file if it exists
        if os.path.exists(self.categories_file):
            with open(self.categories_file, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                return [row[0] for row in reader]  # Return a list of categories
        else:
            return ["Uncategorized"]

    def save_categories(self):
        # Save categories to the CSV file
        with open(self.categories_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Category"])  # Write header row
            for category in self.categories:
                writer.writerow([category])  # Write each category

    def open_category_management(self):
        # Open a new window for category management
        CategoryManagementWindow(self)

    def open_add_category_window(self):
        # Open a new window to add a category
        AddCategoryWindow(self)

    def display_expenses(self):
        # Display loaded expenses in the listbox
        self.expense_listbox.delete(0, tk.END)  # Clear existing entries
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"Date: {expense.date}, Description: {expense.description}, Amount: ₹{expense.amount:.2f}, Category: {expense.category}")

    def predict_future_expenses(self):
        # Predict future expenses using a simple linear regression model
        if len(self.expenses) < 2:
            messagebox.showwarning("Insufficient Data", "Not enough data to make predictions.")
            return

        data = {
            "Date": [expense.date for expense in self.expenses],
            "Amount": [expense.amount for expense in self.expenses]
        }
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Date"] = (df["Date"] - df["Date"].min()).dt.days

        X = df[["Date"]].values
        y = df["Amount"].values

        model = LinearRegression()
        model.fit(X, y)

        future_dates = np.arange(df["Date"].max() + 1, df["Date"].max() + 31).reshape(-1, 1)
        predictions = model.predict(future_dates)

        future_expenses = list(zip(future_dates.flatten(), predictions))
        future_expenses_text = "\n".join(f"Day {int(date)}: ₹{amount:.2f}" for date, amount in future_expenses)

        messagebox.showinfo("Expense Predictions", f"Predicted Future Expenses:\n{future_expenses_text}")
        print(f"[INFO] Future Expense Predictions:\n{future_expenses_text}")

class CategoryManagementWindow:
    def __init__(self, tracker):
        self.tracker = tracker
        self.window = tk.Toplevel()
        self.window.title("Manage Categories")
        self.window.geometry("400x300")
        self.window.transient(tracker.root)
        self.window.grab_set()

        self.label = ttk.Label(self.window, text="Manage Categories", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)

        self.new_category_entry = ttk.Entry(self.window, font=("Arial", 12))
        self.new_category_entry.pack(pady=5, padx=20)

        self.category_listbox = tk.Listbox(self.window, font=("Arial", 12), width=50, height=10, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.category_listbox.pack(pady=10, padx=20)

        self.load_categories()

        self.add_category_button = ttk.Button(self.window, text="Add Category", command=self.add_category)
        self.add_category_button.pack(pady=5, padx=20)

        self.remove_category_button = ttk.Button(self.window, text="Remove Category", command=self.remove_category)
        self.remove_category_button.pack(pady=5, padx=20)

    def load_categories(self):
        # Load categories into the listbox
        self.category_listbox.delete(0, tk.END)  # Clear existing entries
        for category in self.tracker.categories:
            self.category_listbox.insert(tk.END, category)

    def add_category(self):
        new_category = self.new_category_entry.get().strip()
        if new_category:
            if new_category not in self.tracker.categories:
                self.tracker.categories.append(new_category)
                self.tracker.save_categories()
                self.load_categories()  # Reload categories in listbox
                self.new_category_entry.delete(0, tk.END)
                print(f"[INFO] Added Category: {new_category}")
            else:
                messagebox.showwarning("Category Exists", "Category already exists.")
        else:
            messagebox.showwarning("Empty Entry", "Please enter a category name.")

    def remove_category(self):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            category_to_remove = self.category_listbox.get(selected_index)
            if category_to_remove in self.tracker.categories:
                self.tracker.categories.remove(category_to_remove)
                self.tracker.save_categories()
                self.load_categories()  # Reload categories in listbox
                print(f"[INFO] Removed Category: {category_to_remove}")
            else:
                messagebox.showwarning("Category Error", "Category not found.")
        else:
            messagebox.showwarning("Selection Error", "Please select a category to remove.")

class AddCategoryWindow:
    def __init__(self, tracker):
        self.tracker = tracker
        self.window = tk.Toplevel()
        self.window.title("Add Category")
        self.window.geometry("300x150")
        self.window.transient(tracker.root)
        self.window.grab_set()

        self.label = ttk.Label(self.window, text="Add New Category", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)

        self.new_category_entry = ttk.Entry(self.window, font=("Arial", 12))
        self.new_category_entry.pack(pady=5, padx=20)

        self.add_category_button = ttk.Button(self.window, text="Add Category", command=self.add_category)
        self.add_category_button.pack(pady=10, padx=20)

    def add_category(self):
        new_category = self.new_category_entry.get().strip()
        if new_category:
            if new_category not in self.tracker.categories:
                self.tracker.categories.append(new_category)
                self.tracker.save_categories()
                self.tracker.category_dropdown['values'] = self.tracker.categories  # Update dropdown values
                self.new_category_entry.delete(0, tk.END)
                print(f"[INFO] Added Category: {new_category}")
                self.window.destroy()  # Close the window after adding the category
            else:
                messagebox.showwarning("Category Exists", "Category already exists.")
        else:
            messagebox.showwarning("Empty Entry", "Please enter a category name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
