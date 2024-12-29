import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    """
    This module defines the `Database` class, which provides an abstraction for interacting with a PostgreSQL database.

    The `Database` class includes methods to:
    - Establish and close database connections.
    - Initialize the database schema and seed it with initial data.
    - Add, retrieve, update, and delete user and transaction records.
    - Check user permissions for transaction operations.

    Usage:
    - Ensure the `.env` file contains the required database connection parameters (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) before using this class.
    - Use the `db_init` method to create necessary tables and seed initial data.
    """
    def __init__(self):
        """
        Initializes a Database instance.

        This constructor sets up the database connection parameters by reading environment variables
        defined in a `.env` file. It also initializes the `connection` attribute to `None`, which will
        later hold the active database connection.

        Attributes:
            db_name (str): The name of the database, fetched from the 'DB_NAME' environment variable.
            db_user (str): The username for database access, fetched from the 'DB_USER' environment variable.
            db_password (str): The password for the database user, fetched from the 'DB_PASSWORD' environment variable.
            db_host (str): The hostname of the database server, fetched from the 'DB_HOST' environment variable.
            db_port (str): The port number of the database server, fetched from the 'DB_PORT' environment variable.
            connection (psycopg2.extensions.connection or None): The database connection object, initially set to `None`.

        Notes:
            - Ensure that a `.env` file exists with the necessary environment variables before using this class.
            - The actual database connection is not established during initialization. Use the `connect` method
              to establish a connection.
        """

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
        except psycopg2.DatabaseError:
            print(f'A database error occurred.')

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
        except psycopg2.DatabaseError:
            print(f'A database error occurred.')
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
        except psycopg2.DatabaseError:
            print(f'An error occurred while adding the user.')
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
        except psycopg2.DatabaseError:
            print(f'A database error has occurred while retrieving the user {username}.')
            return None
        finally:
            self.close()

    def add_transaction(self, user_id, amount, category, description, date, type_of_transaction):
        """
        Add a transaction to the database.

        This method inserts a new transaction record into the `transactions` table with the provided details.
        It ensures the connection to the database, executes the SQL insert query, and handles errors.

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
        except psycopg2.DatabaseError:
            print(f'Failed to add transaction to database.')
            return False
        finally:
            self.close()

    def fetch_data(self, query, params):
        """
        Executes a database query with the provided parameters and returns the fetched results.

        This method establishes a connection to the database, executes the provided SQL query using the
        specified parameters, and retrieves the resulting data. It ensures proper resource management
        by closing the database connection after the query is executed, regardless of success or failure.

        Args:
            query (str): The SQL query to be executed. It should include parameter placeholders (e.g., %s).
            params (tuple): A tuple of parameters to be passed into the query, matching the placeholders.

        Returns:
            list: A list of records fetched from the database. Returns an empty list if an error occurs during execution.

        Raises:
            psycopg2.DatabaseError: If there is an error during the query execution.
        """

        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except psycopg2.DatabaseError:
            print(f'Database error occurred.')
            return []
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
        except psycopg2.DatabaseError:
            print(f'Error during deleting the transaction.')
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
        except psycopg2.DatabaseError:
            print(f'Error during updating the transaction.')
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
        except psycopg2.DatabaseError:
            print(f'Error during updating the transaction.')
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
        except psycopg2.DatabaseError:
            print(f'Error during checking the eligibility')
        finally:
            self.close()
