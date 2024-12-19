# Expense Tracker Application

This project is a Python-based application integrated with PostgreSQL that enables users to track their income and expenses using the Pandas library.

## Table of contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

## Introduction

This project is a Python-based application integrated with PostgreSQL database that allows users to track their income and expenses. 
Users can register into database and log in to add transactions. Users can categorize transactions, generate reports to analyze their spending habits. 
Fetching data is supported by `pandas` library for better readability and analytics. In this project, the `categories` table is seeded with initial categories: Food, Transportation, Utilities, Entertainment, Health and Account to set up a basic structure and enable users to start using the application immediately. Users can add two types of entries: Income or Expense (also populated in the `types` table). This project utilizes python-dotenv for managing environment variables.

## Features

- **User Authentication:**
  - Sign up and log in to access the system.
  
- **Transaction Management:**
  - Add income and expense entries.
  - Update or delete entries.
  
- **Reports:**
  - View total income, total expenses, and balance.
  - Generate categorized reports based on user-defined time periods (e.g., monthly, yearly).

## Technologies used

- **Programming Language**: Python 3.11
- **Database**: PostgreSQL
- **Libraries**:
  - `python-dotenv`
  - `psycopg2`
  - `getpass4`
  - `bcrypt`
  - `email-validator`
  - `pandas`
  
## Setup and Installation

### Prerequisites

- Python 3.x installed on your machine.
- PostgreSQL installed and running.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/adamlugowski/expense-tracker.git
   ```
2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```
3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up a PostgreSQL database**:

    - Make sure you have PostgreSQL installed on your system. If not, you can download it from [https://www.postgresql.org/download/](https://www.postgresql.org/download/).
    - Create a new database:
      1. Open the PostgreSQL shell or a database client (e.g., pgAdmin).
      2. Create a database for the application:
         ```sql
         CREATE DATABASE expense_tracker;
         ```
      3. (Optional) Create a dedicated user for this database and grant privileges:
         ```sql
         CREATE USER app_user WITH PASSWORD 'yourpassword';
         GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO app_user;
         ```

5. **Configure environment variables**:
    - Create a `.env` file in the project root directory and add your database credentials. For example:
      ```
      DB_NAME=expense_tracker
      DB_USER=app_user
      DB_PASSWORD=yourpassword
      DB_HOST=localhost
      DB_PORT=5432
      ```
    - Replace the placeholders with your actual database details.

6. **Initialize the database**:
    - Run the script to set up the necessary tables and seed data:
      ```bash
      python -c "from app import Database; db = Database(); db.db_init()"
      ```

7. **Run the application**:
    ```bash
    python app.py
    ```
## Usage

1. **Run the script**:
    ```bash
    python main.py
    ```
## Database Schema

   This project uses PostgreSQL as the database with following schema:
   1. **Users Table**:
      - `user_id` (Serial, Primary Key)
      - `username` (Varchar Not Null)
      - `password` (Bytea Not Null)
      - `email` (Varchar Not Null)
   2. **Categories Table**:
      - `category_id` (Serial, Primary Key)
      - `category_name` (Varchar)
   3. **Types**:
      - `type_id` (Serial, Primary Key)
      - `type_name` (Varchar)
   4. **Transactions Table**:
      - `transaction_id` (Serial, Primary Key)
      - `user_id` (Foreign Key referencing Users Table)
      - `amount` (Decimal)
      - `category` (Foreign Key referencing Categories Table)
      - `description` (Text)
      - `date` (Date)
      - `type` (Foreign Key referencing Types Table
## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.
