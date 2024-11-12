# Expense Tracker Application

This project is a Python-based application integrated with PostgreSQL that allows users to track their income and expenses.

## Table of contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

## Introduction

This project is a Python-based application integrated with PostgreSQL that allows users to track their income and expenses. 
Users can register into database and log in to add transactions. Users can categorize transactions, generate reports, and analyze their spending habits. This project utilizes python-dotenv for managing environment variables.

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

4. **Initialize the database**:
    - Create database and tables using the provided schema (see [Database_Schema](#database-schema) section)

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
      - `transaction_id` (Primary Key)
      - `user_id` (Foreign Key referencing Users Table)
      - `amount` (Decimal)
      - `category` (Foreign Key referencing Categories Table
      - `description` (Text)
      - `date` (Date)
      - `type` (Foreign Key referencing Types Table
## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.
