
from datetime import date


class Transaction:
    VALID_TYPES = ["Income", "Expense"]

    def __init__(self, transaction_type, category, amount, description=""):

        # Validate transaction type
        transaction_type = transaction_type.strip().capitalize()

        if transaction_type not in self.VALID_TYPES:
            raise ValueError("Transaction type must be Income or Expense.")

        # Validate category
        if not category or not category.strip():
            raise ValueError("Category cannot be empty.")

        # Validate amount
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a valid number.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        self.transaction_type = transaction_type
        self.category = category.strip().title()
        self.amount = round(amount, 2)
        self.description = description.strip()
        self.transaction_date = date.today()

    def display(self):
        print("-----------------------------------")
        print(f"Type        : {self.transaction_type}")
        print(f"Category    : {self.category}")
        print(f"Amount      : ₹{self.amount:.2f}")
        print(f"Description : {self.description}")
        print(f"Date        : {self.transaction_date}")
        print("-----------------------------------")
