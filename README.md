# Petpooja Sales Data Fetch & Store

## Overview

This project fetches sales data from the Petpooja API and stores the records in a local SQLite database.

The script uses Python's `requests` library to make API requests and `sqlite3` to create and manage the database.

## Features

- Fetch sales records for the required date range.
- Read API credentials from environment variables using a `.env` file.
- Retry API requests after temporary request failures.
- Create the SQLite database and `sales_data` table automatically.
- Store sales records using parameterized SQL queries.
- Handle API and database errors.
- Replace existing records when refreshing the dataset.

## Technologies Used

- Python
- Requests
- python-dotenv
- SQLite

## Project Structure

```text
petpooja-sales-data/
├── fetch_sales.py
├── verify_database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── sales_data.db
```

## Setup

### 1. Install Python

Install Python 3 if it is not already installed.

### 2. Install dependencies

Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure API credentials

Create a `.env` file in the project folder using `.env.example` as a template.

Fill in the API URL, app key, app secret, access token, and restaurant ID supplied for the assignment.

Do not commit the `.env` file or expose API credentials publicly.

### 4. Fetch and store sales data

Run:

```bash
python fetch_sales.py
```

The script fetches the records for the configured date range and stores them in `sales_data.db`.

### 5. Verify the database

Run:

```bash
python verify_database.py
```

This displays the record count, table columns, and a small sample of the stored records.

## Database Schema

The `sales_data` table contains:

- `id`
- `receipt_number`
- `sale_date`
- `transaction_time`
- `sale_amount`
- `tax_amount`
- `discount_amount`
- `round_off`
- `net_sale`
- `payment_mode`
- `order_type`
- `transaction_status`

## Date Range

- From: `2025-05-03 00:00:00`
- To: `2025-05-30 23:59:19`

## Notes

The database file is included in the repository as requested by the assignment. API credentials are kept separate from the source code.

