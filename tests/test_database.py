
import os
import pytest
from datetime import date, timedelta
from src import database
from src.transactions import Transaction


@pytest.fixture
def test_db(monkeypatch):
    # Redirect database operations to the test database.
    test_db_name = os.getenv("TEST_DB_NAME")

    if not test_db_name:
        pytest.fail("TEST_DB_NAME is missing from .env")

    monkeypatch.setenv("DB_NAME", test_db_name)

    # Clear only the test database before testing.
    connection = database.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM transactions")
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    yield

    # Clean up test records afterwards.
    connection = database.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM transactions")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def test_add_transaction(test_db):
    transaction = Transaction(
        "Income", "Salary", 25000, "Monthly salary"
    )

    database.add_transaction(transaction)

    records = database.get_all_transactions()

    assert len(records) == 1
    assert records[0]["category"] == "Salary"
    assert records[0]["transaction_type"] == "Income"


def test_delete_transaction(test_db):
    transaction = Transaction(
        "Expense", "Food", 500, "Lunch"
    )

    database.add_transaction(transaction)

    records = database.get_all_transactions()
    transaction_id = records[0]["id"]

    deleted = database.delete_transaction(transaction_id)

    assert deleted is True
    assert database.get_all_transactions() == []


def test_financial_summary(test_db):
    income = Transaction("Income", "Salary", 25000)
    expense = Transaction("Expense", "Food", 500)

    database.add_transaction(income)
    database.add_transaction(expense)

    summary = database.get_financial_summary()

    assert summary["total_income"] == 25000
    assert summary["total_expenses"] == 500
    assert summary["balance"] == 24500


def test_category_expenses(test_db):
    database.add_transaction(
        Transaction("Expense", "Food", 500)
    )
    database.add_transaction(
        Transaction("Expense", "Food", 300)
    )
    database.add_transaction(
        Transaction("Expense", "Travel", 1000)
    )

    reports = database.get_category_expenses()

    totals = {
        item["category"]: float(item["total"])
        for item in reports
    }

    assert totals["Food"] == 800
    assert totals["Travel"] == 1000


def test_transactions_by_date(test_db):
    today = date.today()

    income = Transaction("Income", "Salary", 30000, "Monthly salary")
    expense = Transaction("Expense", "Food", 500, "Lunch")

    database.add_transaction(income)
    database.add_transaction(expense)

    results = database.get_transactions_by_date(
        today,
        today
    )

    assert len(results) == 2
    assert all(
        today <= row["transaction_date"] <= today
        for row in results
    )


def test_delete_nonexistent_transaction(test_db):
    result = database.delete_transaction(999999)

    assert result is False


def test_get_all_transactions_empty(test_db):
    results = database.get_all_transactions()

    assert results == []
