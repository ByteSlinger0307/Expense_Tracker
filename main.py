import os
import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import csv
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

        reset_button = ttk.Button(button_frame, text="Reset Data", command=self.reset_data)
        reset_button.grid(row=0, column=7, padx=10)

        exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack(pady=20)

        # Listbox to display expenses
        self.expense_listbox = tk.Listbox(self.root, font=("Arial", 12), width=70, height=15, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.expense_listbox.pack(pady=10, padx=20, fill='x')

        # Load existing expenses into the listbox
        self.display_expenses()

    def display_expenses(self):
        print("Displaying expenses...")
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

        # Aggregate expenses by category
        category_totals = df.groupby('Category').sum()

        # Plot
        plt.figure(figsize=(12, 6))
        category_totals.plot(kind='bar', legend=False)
        plt.title('Total Expenses by Category')
        plt.xlabel('Category')
        plt.ylabel('Total Amount')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def predict_future_expenses(self):
        if len(self.expenses) < 2:
            messagebox.showwarning("Insufficient Data", "Not enough data to make predictions.")
            return

        # Convert expenses to DataFrame
        data = {
            "Date": [expense.date for expense in self.expenses],
            "Amount": [expense.amount for expense in self.expenses]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df = df.resample('M').sum()  # Resample to monthly data

        # Prepare data for prediction
        df['Month'] = df.index.to_period('M').astype('int')
        X = df[['Month']].values
        y = df['Amount'].values
        model = LinearRegression()
        model.fit(X, y)

        future_months = np.arange(len(df) + 1, len(df) + 13).reshape(-1, 1)
        future_amounts = model.predict(future_months)
        future_dates = [df.index[-1] + pd.DateOffset(months=i) for i in range(1, 13)]

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Amount'], marker='o', linestyle='-', color='blue', label='Actual')
        plt.plot(future_dates, future_amounts, marker='o', linestyle='--', color='red', label='Predicted')
        plt.title('Expense Prediction for Next 12 Months')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def open_category_manager(self):
        CategoryManager(self.root, self.category_file).run()

    def reset_data(self):
        # Confirm reset
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to delete existing data and start fresh?"):
            # Delete existing files
            if os.path.exists(self.filename):
                os.remove(self.filename)
                print(f"[INFO] Deleted file: {self.filename}")
            if os.path.exists(self.category_file):
                os.remove(self.category_file)
                print(f"[INFO] Deleted file: {self.category_file}")
            # Clear internal data
            self.expenses = []
            self.display_expenses()
            # Reset categories (if needed, e.g., by creating a default categories file)
            with open(self.category_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Category"])  # Write header
            print(f"[INFO] Created new category file: {self.category_file}")
            messagebox.showinfo("Reset Successful", "Data has been reset. You can now add new expenses and categories.")

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    # Check if the row has the expected number of values
                    if len(row) == 4:
                        date, description, amount, category = row
                        self.expenses.append(Expense(date, description, float(amount), category))
                    else:
                        print(f"[WARNING] Skipped row with unexpected format: {row}")
            print(f"[INFO] Loaded expenses from file: {self.filename}")


    def save_expenses(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Category"])
            for expense in self.expenses:
                writer.writerow([expense.date, expense.description, expense.amount, expense.category])
        print(f"[INFO] Saved expenses to file: {self.filename}")

    def load_categories(self):
        if os.path.exists(self.category_file):
            with open(self.category_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                categories = [row[0] for row in reader if row]
                self.categories = categories
            print(f"[INFO] Loaded categories from file: {self.category_file}")
        else:
            self.categories = ["Uncategorized"]  # Default category
            print(f"[INFO] Created default category file: {self.category_file}")

    def get_categories(self):
        return self.categories

    def clear_entries(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_var.set("Uncategorized")

class CategoryManager:
    def __init__(self, root, category_file="categories.csv"):
        self.root = root
        self.category_file = category_file
        self.categories = self.load_categories()
        self.window = tk.Toplevel(root)
        self.window.title("Manage Categories")
        self.window.geometry("300x300")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ttk.Label(self.window, text="Manage Categories", font=("Arial", 18, "bold"))
        header.pack(pady=20)

        # Listbox to display categories
        self.category_listbox = tk.Listbox(self.window, font=("Arial", 12), width=40, height=10, bg="#FFFFFF", selectbackground="#D1D1D1")
        self.category_listbox.pack(pady=10, padx=20)

        # Add initial categories to the listbox
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

        # Add and remove buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Add Category", command=self.add_category)
        add_button.grid(row=0, column=0, padx=10)

        remove_button = ttk.Button(button_frame, text="Remove Category", command=self.remove_category)
        remove_button.grid(row=0, column=1, padx=10)

        # Category entry
        self.category_entry = ttk.Entry(self.window, font=("Arial", 12))
        self.category_entry.pack(pady=10, padx=20)

        # Save and close buttons
        save_button = ttk.Button(self.window, text="Save & Close", command=self.save_and_close)
        save_button.pack(pady=10)

    def add_category(self):
        category = self.category_entry.get().strip()
        if category and category not in self.categories:
            self.categories.append(category)
            self.category_listbox.insert(tk.END, category)
            self.category_entry.delete(0, tk.END)
            print(f"[INFO] Added Category: {category}")
        else:
            messagebox.showwarning("Invalid Input", "Category is either empty or already exists.")

    def remove_category(self):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            category = self.category_listbox.get(selected_index)
            if category in self.categories:
                self.categories.remove(category)
                self.category_listbox.delete(selected_index)
                print(f"[INFO] Removed Category: {category}")
            else:
                messagebox.showwarning("Removal Error", "Selected category does not exist.")
        else:
            messagebox.showwarning("Selection Error", "Please select a category to remove.")

    def save_and_close(self):
        with open(self.category_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category"])
            for category in self.categories:
                writer.writerow([category])
        print(f"[INFO] Saved categories to file: {self.category_file}")
        self.window.destroy()

    def load_categories(self):
        if os.path.exists(self.category_file):
            with open(self.category_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                return [row[0] for row in reader if row]
        else:
            return ["Uncategorized"]  # Default category

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()