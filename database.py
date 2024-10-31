import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
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
        except psycopg2.DatabaseError as e:
            print(f"A database error occurred: {e}")

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
                        password varchar(255) not null,
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
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            print(f"A database error occurred: {e}")
        finally:
            self.close()
