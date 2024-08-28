# Expense Tracker with AI Integration

## Introduction
The Expense Tracker is a Python-based application designed to help users manage and track their expenses. It features a modern graphical user interface (GUI) built using `tkinter` and `ttkbootstrap`, and includes functionalities for inputting, categorizing, and visualizing expenses. The application also integrates basic machine learning to predict future expenses based on past data.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ByteSlinger0307/Expense_Tracker.git
    cd Expense_Tracker
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```bash
    python main.py
    ```

2. **Using the GUI**:
   - Enter the description and amount of an expense in the provided fields.
   - Choose a category for the expense, or leave it uncategorized.
   - Use the buttons to add, edit, or remove expenses, and to generate reports.

3. **Predicting Future Expenses**:
   - The application uses historical data to forecast future expenses, providing insights into spending trends.

## Features

- **Expense Management**: Easily add, edit, and delete expense records.
- **Categorization**: Assign categories to expenses for better organization.
- **Data Visualization**: Generate and view charts of expenses over time.
- **AI Integration**: Predict future expenses using a linear regression model.
- **Persistent Storage**: Save and load expenses from CSV files.

## Dependencies

- `tkinter` - For the graphical user interface.
- `ttkbootstrap` - For modern theming of the UI.
- `csv`, `os`, `datetime` - For file handling and date management.
- `matplotlib` - For plotting graphs and visualizations.
- `pandas` - For data manipulation and analysis.
- `scikit-learn` - For implementing machine learning models.
- `numpy` - For numerical operations.

## Configuration

- **Expense File**: The default file for storing expenses is `expenses.csv`. You can change this by modifying the initialization parameters of the `ExpenseTracker` class.
- **Category File**: Categories are stored in `categories.csv`. Similar to the expense file, this can be configured as needed.

## Documentation

Further documentation on each module and method can be found in the `docs` directory or by accessing the in-application help menu.

## Examples

Here is a sample snippet to add a new expense programmatically:
```python
from expense_tracker import ExpenseTracker
expense_tracker = ExpenseTracker()
expense_tracker.add_expense("2024-08-29", "Lunch", 15.00, "Food")

## Troubleshooting

- **Installation Issues**: Ensure all dependencies are installed using the `requirements.txt` file.
- **CSV File Errors**: Check that your CSV files are properly formatted and accessible.
- **GUI Issues**: Ensure your Python environment supports `tkinter` and `ttkbootstrap`.

## Contributors

- [Krish Dubey](https://github.com/ByteSlinger0307)

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
