import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import csv
import os
from datetime import datetime

class Expense:
    def __init__(self, date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount

class ExpenseTracker:
    def __init__(self, root, filename="expenses.csv"):
        self.expenses = []
        self.filename = filename
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
        date = datetime.now().strftime("%Y-%m-%d")  # Get current date

        if description and amount:
            try:
                amount = float(amount)
                expense = Expense(date, description, amount)
                self.expenses.append(expense)
                self.expense_listbox.insert(tk.END, f"Date: {date}, Description: {description}, Amount: ₹{amount:.2f}")
                self.save_expenses()  # Save the expense after adding it
                self.clear_entries()
                print(f"[INFO] Added Expense - Date: {date}, Description: {description}, Amount: ₹{amount:.2f}")
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
            print(f"[INFO] Removed Expense - Date: {removed_expense.date}, Description: {removed_expense.description}, Amount: ₹{removed_expense.amount:.2f}")
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

    def save_expenses(self):
        # Write expenses to the CSV file
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount"])  # Write header row
            for expense in self.expenses:
                writer.writerow([expense.date, expense.description, expense.amount])  # Write each expense

    def load_expenses(self):
        # Load expenses from the CSV file if it exists
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) == 3:
                        date, description, amount = row
                        try:
                            amount = float(amount)
                            expense = Expense(date, description, amount)
                            self.expenses.append(expense)
                        except ValueError:
                            continue  # Skip rows with invalid data

    def display_expenses(self):
        # Display loaded expenses in the listbox
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"Date: {expense.date}, Description: {expense.description}, Amount: ₹{expense.amount:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
