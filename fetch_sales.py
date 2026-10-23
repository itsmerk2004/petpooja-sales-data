import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("PETPOOJA_API_URL")
APP_KEY = os.getenv("PETPOOJA_APP_KEY")
APP_SECRET = os.getenv("PETPOOJA_APP_SECRET")
ACCESS_TOKEN = os.getenv("PETPOOJA_ACCESS_TOKEN")
RESTAURANT_ID = os.getenv("PETPOOJA_RESTAURANT_ID")

FROM_DATE = "2025-05-03 00:00:00"
TO_DATE = "2025-05-30 23:59:19"

DATABASE_NAME = "sales_data.db"



def fetch_sales_data():
    """Fetch sales data from the Petpooja API with retries."""

    if not all([API_URL, APP_KEY, APP_SECRET, ACCESS_TOKEN, RESTAURANT_ID]):
        raise ValueError("Missing API configuration. Check your .env file.")

    params = {
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "access_token": ACCESS_TOKEN,
        "restID": RESTAURANT_ID,
        "from_date": FROM_DATE,
        "to_date": TO_DATE,
    }

    for attempt in range(1, 4):
        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                raise RuntimeError("Unexpected API response format.")

            if str(data.get("success")) != "1":
                raise RuntimeError("The API did not report a successful response.")

            records = data.get("Records")

            if not isinstance(records, list):
                raise RuntimeError("The API response does not contain a valid Records list.")

            print(f"Successfully fetched {len(records)} sales records.")
            return records

        except requests.RequestException as error:
            if attempt == 3:
                raise RuntimeError("API request failed after 3 attempts.") from error

            print(f"Request failed on attempt {attempt}. Retrying...")
            import time
            time.sleep(2)

        except ValueError as error:
            raise RuntimeError("The API returned invalid JSON.") from error

    raise RuntimeError("Unable to fetch sales data.")



def create_database():
    """Create the SQLite database and sales_data table."""

    connection = sqlite3.connect(DATABASE_NAME)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_number TEXT,
                sale_date TEXT,
                transaction_time TEXT,
                sale_amount REAL,
                tax_amount REAL,
                discount_amount REAL,
                round_off REAL,
                net_sale REAL,
                payment_mode TEXT,
                order_type TEXT,
                transaction_status TEXT
            )
        """)

        connection.commit()
        print("Database and sales_data table are ready.")

    finally:
        connection.close()



def store_sales_data(records):
    """Replace existing sales data with the latest API response."""

    connection = sqlite3.connect(DATABASE_NAME)

    try:
        cursor = connection.cursor()

        rows = [
            (
                record.get("Receipt number"),
                record.get("Receipt Date"),
                record.get("Transaction Time"),
                record.get("Invoice amount"),
                record.get("Tax amount"),
                record.get("Discount amount"),
                record.get("Round Off"),
                record.get("Net sale"),
                record.get("Payment Mode"),
                record.get("Order Type"),
                record.get("Transaction status"),
            )
            for record in records
        ]

        # Start a transaction so the old data is preserved
        # if replacing it fails.
        cursor.execute("DELETE FROM sales_data")

        cursor.executemany("""
            INSERT INTO sales_data (
                receipt_number,
                sale_date,
                transaction_time,
                sale_amount,
                tax_amount,
                discount_amount,
                round_off,
                net_sale,
                payment_mode,
                order_type,
                transaction_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)

        connection.commit()
        print(f"Successfully stored {len(rows)} sales records.")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def main():
    """Fetch sales data and save it to SQLite."""

    try:
        records = fetch_sales_data()
        create_database()
        store_sales_data(records)
        print(f"Done. Database saved as {DATABASE_NAME}.")

    except (ValueError, RuntimeError, sqlite3.Error) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()