
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def add_transaction(transaction):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO transactions
        (transaction_type, category, amount, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        transaction.transaction_type,
        transaction.category,
        transaction.amount,
        transaction.description,
        transaction.transaction_date
    )

    try:
        cursor.execute(query, values)
        connection.commit()
        print("\nTransaction saved to MySQL successfully!")
    finally:
        cursor.close()
        connection.close()


def get_all_transactions():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_date DESC, id DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_financial_summary():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE
                    WHEN transaction_type = 'Income' THEN amount
                    ELSE 0
                END), 0) AS total_income,

                COALESCE(SUM(CASE
                    WHEN transaction_type = 'Expense' THEN amount
                    ELSE 0
                END), 0) AS total_expenses

            FROM transactions
        """)

        result = cursor.fetchone()

        return {
            "total_income": float(result[0]),
            "total_expenses": float(result[1]),
            "balance": float(result[0] - result[1])
        }
    finally:
        cursor.close()
        connection.close()


def delete_transaction(transaction_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM transactions WHERE id = %s"

        cursor.execute(query, (transaction_id,))
        connection.commit()

        return cursor.rowcount > 0

    finally:
        cursor.close()
        connection.close()


def get_transactions_by_date(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM transactions
            WHERE transaction_date BETWEEN %s AND %s
            ORDER BY transaction_date DESC, id DESC
        """

        cursor.execute(query, (start_date, end_date))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_category_expenses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT
                category,
                SUM(amount) AS total
            FROM transactions
            WHERE transaction_type = 'Expense'
            GROUP BY category
            ORDER BY total DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
