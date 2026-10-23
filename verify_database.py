
import sqlite3

DATABASE_NAME = "sales_data.db"


def verify_database():
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        cursor = connection.cursor()

        # Check how many records were saved.
        cursor.execute("SELECT COUNT(*) FROM sales_data")
        total_records = cursor.fetchone()[0]

        print(f"Total records in database: {total_records}")

        # Check the table columns.
        cursor.execute("PRAGMA table_info(sales_data)")
        columns = [row[1] for row in cursor.fetchall()]

        print("\nTable columns:")
        for column in columns:
            print(f"- {column}")

        # Preview a few records without printing every sale.
        cursor.execute("""
            SELECT receipt_number, sale_date, sale_amount, net_sale
            FROM sales_data
            LIMIT 3
        """)

        print("\nSample records:")
        for row in cursor.fetchall():
            print(row)

    finally:
        connection.close()


if __name__ == "__main__":
    verify_database()
