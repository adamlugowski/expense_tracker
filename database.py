import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    """
    A class to manage the PostgreSQL database connection and setup for an application.

    This class utilizes environment variables to establish a database connection and
    provides methods to initialize the database with tables for users, categories, types,
    and transactions.

    Attributes:
    ----------
    db_name : str
        The name of the database, sourced from environment variables.
    db_user : str
        The database user, sourced from environment variables.
    db_password : str
        The password for the database user, sourced from environment variables.
    db_host : str
        The host address of the database, sourced from environment variables.
    db_port : str
        The port number of the database, sourced from environment variables.
    connection : psycopg2.connection or None
        The current database connection, initially set to None.

    Methods:
    -------
    connect():
        Establishes a connection to the PostgreSQL database using provided credentials.
    close():
        Closes the current database connection if it exists.
    db_init():
        Initializes the database tables (users, categories, types, transactions) if they do not exist.
    add_user():
        Inserts a new user to the 'users' table.
    get_user():
        Retrieves a user's data from the database based on their username.
    """

    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.connection = None

    def connect(self):
        """
        This method is for establishing the connection using the environment variables.
        """
        try:
            self.connection = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.db_host,
                    port=self.db_port)
        except psycopg2.DatabaseError as error:
            print(f'A database error occurred: {error}')

    def close(self):
        """
        This method is for closing the connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def db_init(self):
        """
        Initialize the database by creating the users, transactions, categories, types tables if it does not exist
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id serial PRIMARY KEY, 
                        username VARCHAR(50) UNIQUE NOT NULL, 
                        password BYTEA NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL);''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS categories(
                        category_id serial PRIMARY KEY,
                        category_name VARCHAR(255));''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS types(
                        type_id serial PRIMARY KEY,
                        type_name VARCHAR(10));''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(
                        transaction_id serial PRIMARY KEY,
                        user_id INTEGER REFERENCES users(user_id),
                        amount DECIMAL,
                        category INTEGER REFERENCES categories(category_id),
                        description TEXT,
                        date DATE NOT NULL,
                        type INTEGER REFERENCES types(type_id));''')
                cursor.execute('''INSERT INTO categories (category_name) VALUES 
                ('Food'), ('Transportation'), ('Utilities'), ('Entertainment'), ('Health'), ('Account') 
                ON CONFLICT DO NOTHING;''')
                cursor.execute('''INSERT INTO types (type_name) VALUES 
                ('Income'), ('Expense') ON CONFLICT DO NOTHING;''')
            self.connection.commit()
        except psycopg2.DatabaseError as error:
            print(f'A database error occurred: {error}')
        finally:
            self.close()

    def add_user(self, username, hashed_password, email):
        """
        Inserts a new user into the 'users' table.

        Args:
        - username (str): The username of the user.
        - hashed_password (bytes): The hashed password of the user.
        - email (str): The email address of the user.

        Returns:
        - bool: True if the insertion was successful, False otherwise.
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('INSERT INTO users(username, password, email) VALUES (%s, %s, %s);',
                               (username, hashed_password, email))
                self.connection.commit()
                return True
        except psycopg2.DatabaseError as error:
            print(f'An error occurred while adding the user: {error}')
            return False
        finally:
            self.close()

    def get_user(self, username):
        """
        Retrieves a user's data from the database based on their username.

        This method connects to the database, executes a query to find a user
        by the given username, and returns a dictionary containing the user's
        username, hashed password, and email if found. If the user does not
        exist, or if a database error occurs, it returns None.

        Args:
        - username (str): The username of the user to retrieve.

        Returns:
        - dict or None: A dictionary with keys 'username', 'password', and 'email'
          containing the user's data if the user is found, or None if the user
          does not exist or if a database error occurs.

        Exceptions:
        - Prints an error message if a psycopg2.DatabaseError is raised during the query.
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT user_id, username, password, email FROM users WHERE username = %s;', (username,))
                user = cursor.fetchone()
                if user:
                    return {'user_id': user[0], 'username': user[1], 'password': user[2], 'email': user[3]}
                else:
                    return None
        except psycopg2.DatabaseError as error:
            print(f'A database error has occurred while retrieving the user {username}: {error}')
            return None
        finally:
            self.close()

    def add_transaction(self, user_id, amount, category, description, date, type_of_transaction):
        """
        Add a transaction to the database.

        This method inserts a new transaction record into the `transactions` table with the provided details.
        It ensures the connection to the database, executes the SQL insert query, and handles errors gracefully.

        Args:
            user_id (int): The ID of the user associated with the transaction.
            amount (float): The amount of the transaction (must be a positive value).
            category (int): The transaction category, represented as an integer.
            description (str): A brief description of the transaction.
            date (datetime): The transaction date .
            type_of_transaction (int): The type of transaction, where 1 represents Income and 2 represents Expense.

        Returns:
            bool:
                - `True` if the transaction is successfully added to the database.
                - `False` if an error occurs during the database operation.

        Exceptions:
            psycopg2.DatabaseError: Raised if there is an error interacting with the database.

        Notes:
            - The database connection is established before the operation and closed afterward.
            - Changes are committed to the database upon successful insertion.
            - Any database errors are caught, and a message is printed for debugging purposes.
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('''INSERT INTO 
                transactions (user_id, amount, category, description, date, type) 
                VALUES (%s, %s, %s, %s, %s, %s);''', (user_id, amount, category, description, date, type_of_transaction))
                self.connection.commit()
                print('Transaction added successfully. ')
                return True
        except psycopg2.DatabaseError as error:
            print(f'Failed to add transaction to database: {error}')
            return False
        finally:
            self.close()

    def show_all_transactions(self, user_id):
        """
        Retrieve and display all transactions for a specific user in a formatted, user-friendly way.

        This function connects to a PostgreSQL database, queries the `transactions` table for all
        records associated with the given `user_id`, and prints the results. Each transaction is
        displayed with details such as transaction ID, user ID, amount, category name, description,
        date, and type of transaction. The output is formatted for better readability.

        Args:
            user_id (int): The ID of the user whose transactions are to be retrieved.
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('''SELECT 
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
                 WHERE user_id=%s;''', (user_id, ))
                transactions = cursor.fetchall()
                for t in transactions:
                    transaction_details = (
                        f"Transaction ID: {t[0]}\n"
                        f"User ID: {t[1]}\n"
                        f"Amount: PLN{t[2]:,.2f}\n"
                        f"Category: {t[3]}\n"
                        f"Description: {t[4]}\n"
                        f"Date: {t[5].strftime('%Y-%m-%d')}\n"
                        f"Type: {t[6]}"
                    )
                    print(transaction_details)
                    print("-" * 30)
        except psycopg2.DatabaseError as error:
            print(f'Database error occurred: {error}')
        finally:
            self.close()

    def show_total_income(self, user_id):
        """
        Calculates and displays the total income for a specific user.

        This method connects to the database, retrieves the sum of all transaction amounts
        categorized as income (type = 1) for the specified user, and prints the total income.

        Args:
            user_id (int): The ID of the user whose total income is being calculated.

        Returns:
            float: The total income amount if the query is successful; None otherwise.

        Behavior:
            - Connects to the database.
            - Executes a query to calculate the total income for the user.
            - Prints the total income to the console.
            - Ensures the database connection is closed after the operation.

        Exceptions:
            - Handles psycopg2.DatabaseError, printing an error message if a database error occurs.
        """

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('select sum(amount) from transactions where user_id = %s and type = 1;', (user_id,))
                result = cursor.fetchone()
                print(f'Your total income: {result[0]}')
                return result[0]
        except psycopg2.DatabaseError as error:
            print(f'Database error occurred: {error}')
        finally:
            self.close()

    def show_total_expenses(self, user_id):
        """
        Calculates and displays the total expenses for a specific user.

        This method connects to the database, retrieves the sum of all transaction amounts
        categorized as expenses (type = 2) for the specified user, and prints the total expenses.

        Args:
            user_id (int): The ID of the user whose total expenses are being calculated.

        Returns:
            float: The total expense amount if the query is successful; None otherwise.

        Behavior:
            - Connects to the database.
            - Executes a query to calculate the total expenses for the user.
            - Prints the total expenses to the console.
            - Ensures the database connection is closed after the operation.

        Exceptions:
            - Handles psycopg2.DatabaseError, printing an error message if a database error occurs.
        """

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('select sum(amount) from transactions where user_id = %s and type = 2;', (user_id, ))
                result = cursor.fetchone()
                print(f'Your total expenses: {result[0]}')
                return result[0]
        except psycopg2.DatabaseError as error:
            print(f'Database error occurred: {error}')
        finally:
            self.close()

    def delete_transaction(self, transaction_id):
        """
        Deletes a transaction from the database.

        This method removes a transaction record from the `transactions` table based
        on the specified `transaction_id`. It establishes a connection to the database,
        executes the deletion query, and commits the changes.

        Args:
        transaction_id (int): The ID of the transaction to be deleted.
        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('DELETE FROM transactions WHERE transaction_id=%s;', (transaction_id, ))
                print('Transaction deleted successfully. ')
                self.connection.commit()
        except psycopg2.DatabaseError as error:
            print(f'Error during deleting the transaction: {error}')
        finally:
            self.close()

    def update_amount_of_transaction(self, amount, transaction_id):
        """
        Update the amount of a specific transaction in the database.

        This method connects to the database and updates the `amount` field of a
        transaction identified by its `transaction_id`. It commits the changes and
        provides feedback on the success or failure of the operation.

        Parameters:
            amount (float): The new amount to update in the transaction.
            transaction_id (int): The ID of the transaction to be updated.
        """

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('UPDATE transactions set amount=%s WHERE transaction_id=%s', (amount, transaction_id))
                print(f'New amount: {amount}. ')
                print(f'Amount updated successfully in transaction {transaction_id}. ')
                self.connection.commit()
        except psycopg2.DatabaseError as error:
            print(f'Error during updating the transaction: {error}')
        finally:
            self.close()

    def update_description_of_transaction(self, description, transaction_id):
        """
        Update the description of a specific transaction in the database.

        This method connects to the database and updates the `description` field
        of a transaction identified by its `transaction_id`. It commits the changes
        and provides feedback on the success or failure of the operation.

        Parameters:
            description (str): The new description to update in the transaction.
            transaction_id (int): The ID of the transaction to be updated.
        """

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('UPDATE transactions set description=%s WHERE transaction_id=%s',
                               (description, transaction_id))
                print(f'New description: {description}. ')
                print(f'Description updated successfully in transaction {transaction_id}. ')
                self.connection.commit()
        except psycopg2.DatabaseError as error:
            print(f'Error during updating the transaction: {error}')
        finally:
            self.close()

    def check_if_eligible(self, user_id, transaction_id):
        """
        Checks if a user is eligible to modify or delete a specific transaction.

        This method verifies whether a given `user_id` is associated with a transaction
        identified by `transaction_id`. It connects to the database, retrieves the `user_id`
        associated with the transaction, and checks if it matches the provided `user_id`.

        Args:
            user_id (int): The ID of the user attempting to access the transaction.
            transaction_id (int): The ID of the transaction to verify.

        Returns:
            bool:
            - `True` if the `user_id` is associated with the given `transaction_id`.
            - `False` if no matching transaction is found or if the `user_id` does not match.

        """
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT user_id FROM transactions WHERE transaction_id = %s;', (transaction_id,))
                result = cursor.fetchone()
                if result is None:
                    print(f'No transaction found with ID {transaction_id}. ')
                    return False
                if user_id == result[0]:
                    return True
                else:
                    return False
        except psycopg2.DatabaseError as error:
            print(f'{error}')
        finally:
            self.close()

