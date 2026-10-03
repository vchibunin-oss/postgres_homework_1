import csv
from datetime import datetime
from pathlib import Path

import psycopg2


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "north_data"


def get_connection():
    """Создает подключение к базе данных."""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="north",
        user="postgres",
        password="0890",
    )


def load_employees(cursor):
    """Загружает сотрудников из CSV."""
    file_path = DATA_DIR / "employees_data.csv"

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for employee_id, row in enumerate(reader, start=1):
            birth_date = datetime.strptime(
                row["birth_date"],
                "%Y-%m-%d",
            ).date()

            cursor.execute(
                """
                INSERT INTO employees (
                    employee_id,
                    first_name,
                    last_name,
                    title,
                    birth_date,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    employee_id,
                    row["first_name"],
                    row["last_name"],
                    row["title"],
                    birth_date,
                    row["notes"],
                ),
            )


def load_customers(cursor):
    """Загружает клиентов из CSV."""
    file_path = DATA_DIR / "customers_data.csv"

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO customers (
                    customer_id,
                    company_name,
                    contact_name
                )
                VALUES (%s, %s, %s)
                """,
                (
                    row["customer_id"],
                    row["company_name"],
                    row["contact_name"],
                ),
            )


def load_orders(cursor):
    """Загружает заказы из CSV."""
    file_path = DATA_DIR / "orders_data.csv"

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            order_date = datetime.strptime(
                row["order_date"],
                "%Y-%m-%d",
            ).date()

            cursor.execute(
                """
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    employee_id,
                    order_date,
                    ship_city
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    int(row["order_id"]),
                    row["customer_id"],
                    int(row["employee_id"]),
                    order_date,
                    row["ship_city"],
                ),
            )


def main():
    """Загружает данные из CSV в PostgreSQL."""
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Очищаем таблицы перед повторной загрузкой.
        cursor.execute(
            """
            TRUNCATE TABLE
                orders,
                customers,
                employees
            RESTART IDENTITY CASCADE
            """
        )

        load_employees(cursor)
        load_customers(cursor)
        load_orders(cursor)

        connection.commit()

        print("Данные успешно загружены в базу north.")

    except Exception as error:
        connection.rollback()
        print(f"Ошибка при загрузке данных: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()