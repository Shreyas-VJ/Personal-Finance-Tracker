
from datetime import date
from src.transactions import Transaction
from src.database import (
    add_transaction,
    get_all_transactions,
    get_financial_summary,
    delete_transaction,
    get_transactions_by_date,
    get_category_expenses
)


def add_new_transaction(transaction_type):
    print(f"\n--- Add {transaction_type} ---")

    try:
        category = input("Enter category: ")
        amount = input("Enter amount (₹): ")
        description = input("Enter description: ")

        transaction = Transaction(
            transaction_type,
            category,
            amount,
            description
        )

        add_transaction(transaction)

    except ValueError as error:
        print(f"\nError: {error}")

    except Exception as error:
        print(f"\nDatabase error: {error}")


def view_transactions():
    print("\n========== ALL TRANSACTIONS ==========")

    try:
        transactions = get_all_transactions()

        if not transactions:
            print("No transactions found.")
            return

        for transaction in transactions:
            print("-----------------------------------")
            print(f"ID          : {transaction['id']}")
            print(f"Type        : {transaction['transaction_type']}")
            print(f"Category    : {transaction['category']}")
            print(f"Amount      : ₹{transaction['amount']}")
            print(f"Description : {transaction['description']}")
            print(f"Date        : {transaction['transaction_date']}")
            print("-----------------------------------")

    except Exception as error:
        print(f"Database error: {error}")


def view_balance():
    try:
        summary = get_financial_summary()

        print("\n========== FINANCIAL SUMMARY ==========")
        print(f"Total Income    : ₹{summary['total_income']:.2f}")
        print(f"Total Expenses  : ₹{summary['total_expenses']:.2f}")
        print("--------------------------------------")
        print(f"Current Balance : ₹{summary['balance']:.2f}")
        print("======================================")

    except Exception as error:
        print(f"Database error: {error}")


def remove_transaction():
    try:
        transaction_id = int(input("\nEnter transaction ID to delete: "))

        if transaction_id <= 0:
            print("Please enter a valid positive ID.")
            return

        confirm = input(
            f"Are you sure you want to delete transaction #{transaction_id}? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            deleted = delete_transaction(transaction_id)

            if deleted:
                print("Transaction deleted successfully!")
            else:
                print("No transaction found with that ID.")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid numeric ID.")

    except Exception as error:
        print(f"Database error: {error}")


def filter_transactions():
    try:
        start_date = date.fromisoformat(
            input("\nEnter start date (YYYY-MM-DD): ").strip()
        )

        end_date = date.fromisoformat(
            input("Enter end date (YYYY-MM-DD): ").strip()
        )

        if start_date > end_date:
            print("Start date cannot be after end date.")
            return

        transactions = get_transactions_by_date(start_date, end_date)

        print("\n========== FILTERED TRANSACTIONS ==========")

        if not transactions:
            print("No transactions found in this date range.")
            return

        for transaction in transactions:
            print("-----------------------------------")
            print(f"ID       : {transaction['id']}")
            print(f"Type     : {transaction['transaction_type']}")
            print(f"Category : {transaction['category']}")
            print(f"Amount   : ₹{transaction['amount']}")
            print(f"Date     : {transaction['transaction_date']}")
            print("-----------------------------------")

    except ValueError:
        print("Invalid date! Use YYYY-MM-DD format.")

    except Exception as error:
        print(f"Database error: {error}")


def view_category_report():
    try:
        reports = get_category_expenses()

        print("\n========== CATEGORY-WISE EXPENSE REPORT ==========")

        if not reports:
            print("No expense records found.")
            return

        grand_total = 0

        for item in reports:
            category = item["category"]
            total = float(item["total"])

            grand_total += total

            print(f"{category:<20} ₹{total:.2f}")

        print("-----------------------------------------------")
        print(f"{'Total Expenses':<20} ₹{grand_total:.2f}")
        print("================================================")

    except Exception as error:
        print(f"Database error: {error}")


def main():
    while True:
        print("\n===================================")
        print("     PERSONAL FINANCE TRACKER")
        print("===================================")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. View Balance")
        print("5. Delete Transaction")
        print("6. Filter Transactions by Date")
        print("7. Category-wise Expense Report")
        print("8. Exit")
        print("===================================")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_new_transaction("Income")

        elif choice == "2":
            add_new_transaction("Expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_balance()

        elif choice == "5":
            remove_transaction()

        elif choice == "6":
            filter_transactions()

        elif choice == "7":
            view_category_report()

        elif choice == "8":
            print("\nThank you for using Personal Finance Tracker!")
            break

        else:
            print("\nInvalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
