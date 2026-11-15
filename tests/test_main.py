
from src import main as app
from datetime import date


def test_main_exit(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "8")

    app.main()

    captured = capsys.readouterr()
    assert "Thank you for using Personal Finance Tracker!" in captured.out


def test_main_invalid_choice(monkeypatch, capsys):
    inputs = iter(["9", "8"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.main()

    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out


def test_add_new_transaction_success(monkeypatch, capsys):
    inputs = iter(["Salary", "50000", "Monthly salary"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    saved_transactions = []
    monkeypatch.setattr(
        app,
        "add_transaction",
        lambda transaction: saved_transactions.append(transaction)
    )

    app.add_new_transaction("Income")

    assert len(saved_transactions) == 1
    assert saved_transactions[0].category == "Salary"
    assert saved_transactions[0].amount == 50000


def test_add_new_transaction_invalid_amount(monkeypatch, capsys):
    inputs = iter(["Salary", "invalid", "Monthly salary"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.add_new_transaction("Income")

    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_view_transactions_empty(monkeypatch, capsys):
    monkeypatch.setattr(app, "get_all_transactions", lambda: [])

    app.view_transactions()

    captured = capsys.readouterr()
    assert "No transactions found." in captured.out


def test_view_balance(monkeypatch, capsys):
    monkeypatch.setattr(
        app,
        "get_financial_summary",
        lambda: {
            "total_income": 50000,
            "total_expenses": 10000,
            "balance": 40000
        }
    )

    app.view_balance()

    captured = capsys.readouterr()
    assert "50000.00" in captured.out
    assert "10000.00" in captured.out
    assert "40000.00" in captured.out


def test_remove_transaction_success(monkeypatch, capsys):
    inputs = iter(["1", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    deleted_ids = []
    monkeypatch.setattr(
        app,
        "delete_transaction",
        lambda transaction_id: deleted_ids.append(transaction_id) or True
    )

    app.remove_transaction()

    captured = capsys.readouterr()
    assert deleted_ids == [1]
    assert "Transaction deleted successfully!" in captured.out


def test_remove_transaction_cancelled(monkeypatch, capsys):
    inputs = iter(["1", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.remove_transaction()

    captured = capsys.readouterr()
    assert "Deletion cancelled." in captured.out


def test_filter_transactions_invalid_date(monkeypatch, capsys):
    inputs = iter(["invalid-date"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.filter_transactions()

    captured = capsys.readouterr()
    assert "Invalid date!" in captured.out


def test_view_category_report_empty(monkeypatch, capsys):
    monkeypatch.setattr(app, "get_category_expenses", lambda: [])

    app.view_category_report()

    captured = capsys.readouterr()
    assert "No expense records found." in captured.out


def test_view_transactions_with_records(monkeypatch, capsys):
    monkeypatch.setattr(
        app,
        "get_all_transactions",
        lambda: [{
            "id": 1,
            "transaction_type": "Income",
            "category": "Salary",
            "amount": 50000,
            "description": "Monthly salary",
            "transaction_date": date.today()
        }]
    )

    app.view_transactions()

    captured = capsys.readouterr()
    assert "Salary" in captured.out
    assert "Monthly salary" in captured.out


def test_remove_transaction_invalid_id(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    app.remove_transaction()

    captured = capsys.readouterr()
    assert "valid positive ID" in captured.out


def test_remove_transaction_not_found(monkeypatch, capsys):
    inputs = iter(["999", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(app, "delete_transaction", lambda _: False)

    app.remove_transaction()

    captured = capsys.readouterr()
    assert "No transaction found" in captured.out


def test_remove_transaction_invalid_input(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "abc")

    app.remove_transaction()

    captured = capsys.readouterr()
    assert "valid numeric ID" in captured.out


def test_filter_transactions_reversed_dates(monkeypatch, capsys):
    inputs = iter(["2026-11-15", "2026-11-01"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.filter_transactions()

    captured = capsys.readouterr()
    assert "Start date cannot be after end date" in captured.out


def test_filter_transactions_empty(monkeypatch, capsys):
    inputs = iter(["2026-11-01", "2026-11-15"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(app, "get_transactions_by_date", lambda *_: [])

    app.filter_transactions()

    captured = capsys.readouterr()
    assert "No transactions found in this date range" in captured.out


def test_category_report_with_records(monkeypatch, capsys):
    monkeypatch.setattr(
        app,
        "get_category_expenses",
        lambda: [
            {"category": "Food", "total": 800},
            {"category": "Travel", "total": 1200}
        ]
    )

    app.view_category_report()

    captured = capsys.readouterr()
    assert "Food" in captured.out
    assert "Travel" in captured.out
    assert "2000.00" in captured.out
