import pandas as pd
from database import Database


class FinancialReport:
    def __init__(self, db: Database):
        """
        Initializes the FinancialReport class.

        Args:
            db (Database): An instance of the Database class used to interact with the database.
        """

        self.db = db

    def fetch_all_transactions_from_db(self, user_id):
        """
        Fetches all transactions for a given user from the database.

        This method executes a SQL query to retrieve all transactions associated
        with a specific user, including details such as transaction ID, user ID,
        amount, category, description, date, and transaction type.

        Args:
            user_id (int or str): The ID of the user whose transactions are to be fetched.

        Returns:
            list: A list of transaction records where each record is a tuple containing
                  transaction details. Returns `None` if an error occurs.
        """

        query = '''SELECT 
                    transactions.transaction_id, 
                    transactions.user_id, 
                    transactions.amount, 
                    categories.category_name, 
                    transactions.description, 
                    transactions.date, 
                    types.type_name
                    FROM transactions 
                    LEFT JOIN categories 
                    ON transactions.category = categories.category_id
                    LEFT JOIN types
                    ON transactions.type = types.type_id
                    WHERE user_id=%s;'''
        try:
            return self.db.fetch_data(query, (user_id,))
        except Exception as error:
            print(f'Error fetching transactions: {error}')
            return None

    def generate_all_transactions_report(self, user_id):
        """
        Generates a detailed report of all transactions for a given user.

        This method fetches all transactions from the database for the specified user
        and organizes them into a pandas DataFrame with labeled columns. The report
        includes details such as transaction ID, user ID, amount, category, description,
        date, and type. If no transactions are found, an empty DataFrame is returned.

        Args:
            user_id (int or str): The ID of the user whose transaction report is to be generated.

        Returns:
            pd.DataFrame: A DataFrame containing the user's transactions. If no transactions
                          are found, an empty DataFrame is returned.
        """

        transactions = self.fetch_all_transactions_from_db(user_id)
        if transactions:
            columns = [
                "Transaction ID", "User ID", "Amount (PLN)",
                "Category", "Description", "Date", "Type"
            ]
            df = pd.DataFrame(transactions, columns=columns)
            print(f'This is user {user_id} transactions. ')
            print(df)
            return df
        else:
            print('No transactions found. ')
            return pd.DataFrame()

    def fetch_total_income_from_db(self, user_id):
        """
        Fetches all income transactions for a given user from the database.

        This method executes a SQL query to retrieve the amounts of all transactions
        categorized as "Income" for a specific user.

        Args:
            user_id (int or str): The ID of the user whose income transactions are to be fetched.

        Returns:
            list: A list of tuples where each tuple contains the amount of an income transaction.
                  Returns `None` if an error occurs during the database query.
        """

        query = '''SELECT amount
                FROM transactions
                LEFT JOIN types ON transactions.type = types.type_id
                WHERE transactions.user_id = %s AND types.type_name = 'Income';'''
        try:
            return self.db.fetch_data(query, user_id)
        except Exception as error:
            print(f'Error fetching result: {error}')
            return None

    def generate_total_income_report(self, user_id):
        """
        Generates a report of the total income for a given user.

        This method retrieves all income transactions for the specified user, calculates
        the total income, and organizes the result into a pandas DataFrame with columns
        for the user ID and total income. If no income transactions are found, an empty
        DataFrame is returned.

        Args:
            user_id (int or str): The ID of the user whose total income report is to be generated.

        Returns:
            pd.DataFrame: A DataFrame containing the user ID and the total income.
                          If no income transactions are found, an empty DataFrame is returned.
        """

        result = self.fetch_total_income_from_db(user_id)
        df = pd.DataFrame(result, columns=['Amount'])
        if df.empty:
            print('No transactions found. ')
            return pd.DataFrame()
        else:
            total_income = df['Amount'].sum()
            income_df = pd.DataFrame({'User ID': [user_id], 'Total Income': [total_income]})
            print(f'Total income of user {user_id} is {total_income}')
            return income_df

    def fetch_total_expenses_from_db(self, user_id):
        """
        Fetches all expense transactions for a given user from the database.

        This method executes a SQL query to retrieve the amounts of all transactions
        categorized as "Expense" for a specific user.

        Args:
            user_id (int or str): The ID of the user whose expense transactions are to be fetched.

        Returns:
            list: A list of tuples where each tuple contains the amount of an expense transaction.
                  Returns `None` if an error occurs during the database query.
        """

        query = '''SELECT amount 
                FROM transactions 
                LEFT JOIN types ON transactions.type = types.type_id 
                WHERE transactions.user_id = %s AND types.type_name = 'Expense';'''

        try:
            return self.db.fetch_data(query, user_id)
        except Exception as error:
            print(f'Error fetching result: {error}')
            return None

    def generate_total_expenses_report(self, user_id):
        """
        Generates a report of the total expenses for a given user.

        This method retrieves all expense transactions for the specified user, calculates
        the total expenses, and organizes the result into a pandas DataFrame with columns
        for the user ID and total expenses. If no expense transactions are found, an empty
        DataFrame is returned.

        Args:
            user_id (int or str): The ID of the user whose total expenses report is to be generated.

        Returns:
            pd.DataFrame: A DataFrame containing the user ID and the total expenses.
                          If no expense transactions are found, an empty DataFrame is returned.
        """

        result = self.fetch_total_expenses_from_db(user_id)
        df = pd.DataFrame(result, columns=['Amount'])
        if df.empty:
            print('No transactions found. ')
            return pd.DataFrame()
        else:
            total_expenses = df['Amount'].sum()
            expenses_df = pd.DataFrame({'User ID': [user_id], 'Total expenses': [total_expenses]})
            print(f'Total expenses of user {user_id} is {total_expenses}')
            return expenses_df

    def calculate_total_income(self, user_id):
        """
        Calculates the total income for a given user.

        This method calls the `generate_total_income_report` method to retrieve the total
        income for the specified user. If the report is empty (i.e., no income transactions),
        it returns 0. Otherwise, it returns the total income value.

        Args:
            user_id (int or str): The ID of the user whose total income is to be calculated.

        Returns:
            float: The total income of the user. Returns 0 if no income transactions are found.
        """

        income_df = self.generate_total_income_report(user_id)
        if income_df.empty:
            return 0
        return income_df["Total Income"].iloc[0]

    def calculate_total_expenses(self, user_id):
        """
        Calculates the total expenses for a given user.

        This method calls the `total_expenses` method to retrieve the total expenses for
        the specified user. If the report is empty (i.e., no expense transactions), it returns 0.
        Otherwise, it returns the total expenses value.

        Args:
            user_id (int or str): The ID of the user whose total expenses are to be calculated.

        Returns:
            float: The total expenses of the user. Returns 0 if no expense transactions are found.
        """

        expenses_df = self.generate_total_expenses_report(user_id)
        if expenses_df.empty:
            return 0
        return expenses_df["Total expenses"].iloc[0]

    def generate_balance_report(self, user_id):
        """
        Generates a balance report showing the total income, total expenses, and balance for a given user.

        This method calculates the total income and total expenses for the specified user,
        then computes the balance as the difference between the total income and total expenses.
        The result is organized into a pandas DataFrame with columns for the user ID, total income,
        total expenses, and balance. The report is also printed to the console.

        Args:
            user_id (int or str): The ID of the user whose balance report is to be generated.

        Returns:
            pd.DataFrame: A DataFrame containing the user ID, total income, total expenses, and balance.
        """

        total_income = self.calculate_total_income(user_id)
        total_expenses = self.calculate_total_expenses(user_id)

        balance = total_income - total_expenses
        balance_df = pd.DataFrame({
            'User ID': [user_id],
            'Total income': [total_income],
            'Total expenses': [total_expenses],
            'Balance': [balance]
        })
        print(f'Balance of user {user_id} is {balance}')
        print(balance_df)
        return balance_df

