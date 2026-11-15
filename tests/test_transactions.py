
import pytest
from src.transactions import Transaction


def test_valid_income_transaction():
    transaction = Transaction(
        "Income", "Salary", 25000, "Monthly salary"
    )

    assert transaction.transaction_type == "Income"
    assert transaction.category == "Salary"
    assert transaction.amount == 25000.00


def test_valid_expense_transaction():
    transaction = Transaction(
        "Expense", "Food", 500, "Lunch"
    )

    assert transaction.transaction_type == "Expense"
    assert transaction.category == "Food"
    assert transaction.amount == 500.00


def test_transaction_type_is_case_insensitive():
    transaction = Transaction("income", "Salary", 1000)

    assert transaction.transaction_type == "Income"


def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        Transaction("Savings", "Salary", 1000)


def test_empty_category():
    with pytest.raises(ValueError):
        Transaction("Income", "", 1000)


def test_negative_amount():
    with pytest.raises(ValueError):
        Transaction("Expense", "Food", -500)


def test_zero_amount():
    with pytest.raises(ValueError):
        Transaction("Expense", "Food", 0)


def test_invalid_amount():
    with pytest.raises(ValueError):
        Transaction("Income", "Salary", "abc")


def test_display_transaction(capsys):
    transaction = Transaction(
        "Income",
        "Salary",
        50000,
        "Monthly salary"
    )

    transaction.display()

    captured = capsys.readouterr()

    assert "Income" in captured.out
    assert "Salary" in captured.out
    assert "50000.00" in captured.out
    assert "Monthly salary" in captured.out
