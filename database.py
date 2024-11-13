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
                cursor.execute('''create table if not exists users(
                        user_id serial primary key, 
                        username varchar(50) unique not null, 
                        password BYTEA not null,
                        email varchar(100) unique not null);''')
                cursor.execute('''create table if not exists categories(
                        category_id serial primary key,
                        category_name varchar(255));''')
                cursor.execute('''create table if not exists types(
                        type_id serial primary key,
                        type_name varchar(10));''')
                cursor.execute('''create table if not exists transactions(
                        transaction_id serial primary key,
                        user_id integer references users(user_id),
                        amount decimal,
                        category integer references categories(category_id),
                        description text,
                        date date not null,
                        type integer references types(type_id));''')
                cursor.execute('''insert into categories (category_name) values 
                ('Food'), ('Transportation'), ('Utilities'), ('Entertainment'), ('Health') on conflict do nothing;''')
                cursor.execute('''insert into types (type_name) values 
                ('Income'), ('Expense') on conflict do nothing;''')
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
                cursor.execute('SELECT username, password, email FROM users WHERE username = %s;', (username,))
                user = cursor.fetchone()
                if user:
                    return {'username': user[0], 'password': user[1], 'email': user[2]}
                else:
                    return None
        except psycopg2.DatabaseError as error:
            print(f'A database error has occurred while retrieving the user {username}: {error}')
            return None
        finally:
            self.close()
