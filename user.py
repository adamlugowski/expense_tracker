import bcrypt
from email_validator import validate_email, EmailNotValidError
from database import Database
from datetime import datetime


class User:
    """
    A class representing a user with a username, password and email address.

    Attributes:
    - username (str): The username of the user.
    - password (str): The plain-text password of the user, which will be hashed upon registration.
    - email (str): The user's email address.

    Methods:
    - __str__(): Returns a string representation of the user.
    - check_email(): Validates the email format.
    - register(db): Registers the user by hashing the password and saving the data to the database.
    """
    def __init__(self, username: str, password: str, email: str):
        """
        Initializes a User instance with a username, password, and email address.

        Args:
        - username (str): The username of the user.
        - password (str): The plain-text password of the user.
        - email (str): The email address of the user.
        """
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
        - str: A string in the format "username email".
        """
        return f'{self.username} {self.email}'

    def check_email(self):
        """
        Validates the user's email address.

        Returns:
        - str: The normalized email address if valid.
        - None: If the email address is not valid.

        Raises:
        - EmailNotValidError: If the email is not in a valid format.
        """
        try:
            validated_email = validate_email(self.email).normalized
            return validated_email
        except EmailNotValidError as error:
            print(f'Invalid email: {error}')
            return None

    def register(self, db):
        """
        Registers the user by hashing the password and saving the user's data to the database.

        Args:
        - db: A database connection object with an add_user method for saving user data.

        Returns:
        - bool: True if registration is successful; False if email validation fails.
        """
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        valid_email = self.check_email()
        if valid_email is None:
            return False

        data = db.add_user(self.username, hashed_password, valid_email)
        return data

    def login(self, db):
        """
        Authenticates the user by verifying the  provided password with the stored hashed password.

        This method retrieves the user's data from the database, converts the stored hashed password 
        to bytes, and uses bcrypt to check if the provided password matches the stored hash. If 
        authentication succeeds, the method returns True; otherwise, it returns False. If there 
        is an issue accessing the database or retrieving the user data, an error is printed, and 
        the method returns False.

        Args:
        - db: A database connection object with a `get_user` method to retrieve user data by username.

        Returns:
        - bool: True if authentication is successful; False otherwise.

        Exceptions:
        - Catches any exception during database access or password verification, printing an error 
          message and returning False.
        """
        try:
            user_data = db.get_user(self.username)
            hashed_password_from_db = bytes(user_data['password'])
            if bcrypt.checkpw(self.password.encode('utf-8'), hashed_password_from_db):
                return True
            else:
                print("Invalid password.")
                return False
        except Exception as error:
            print(f"Error accessing the database: {error}")
            return False

    def create_transaction(self, user_id, db):
        """
        Create a new transaction by collecting all necessary details from the user.

        This function gathers transaction details including the amount, category,
        description, date, and type (Income or Expense). After validating user inputs,
        it adds the transaction to the database using the provided `db` object.

        Args:
            db (Database): The database object used to store the transaction.
            user_id (int): The ID of the user creating the transaction.

        Inputs:
            - Amount (float): Positive numeric value for the transaction amount.
            - Category (int): One of the predefined categories.
            - Description (str): A description of the transaction.
            - Date (datetime): Transaction date in the format YYYY-MM-DD.
            - Transaction Type (int): 1 for Income, 2 for Expense.

        Adds:
            The validated transaction to the database using the `db.add_transaction` method.
        """
        amount = self.get_amount()
        category = self.get_category()
        description = self.get_description()
        valid_date = self.get_valid_date()
        type_of_transaction = self.get_transaction_type()
        db.add_transaction(user_id, amount, category, description, valid_date, type_of_transaction)

    def show_transactions(self, user_id, db):
        """
        Display all transactions associated with this user.
        """
        db.show_transactions(user_id)

    def delete_transaction(self, user_id, db):
        """
        Deletes a specific transaction based on user input.

        This method prompts the user to input a `transaction_id` and checks if the user
        is eligible to delete the transaction using the `db.check_eligible` method.
        If the user is eligible, the transaction is deleted using `db.delete_transaction`.
        If the user is not eligible, a message is displayed. If the input is invalid,
        an error message is shown prompting for a valid transaction ID.

        Args:
            user_id (int): The ID of the user attempting to delete the transaction.
            db (Database): The database object used to check eligibility and delete the transaction.

        Raises:
            ValueError: If the input `transaction_id` cannot be converted to an integer.
        """
        try:
            transaction_id = int(input('Type the transaction_id to delete the transaction: '))
            if db.check_eligible(user_id, transaction_id):
                db.delete_transaction(transaction_id)
            else:
                print('You are not eligible to delete this transaction. ')
        except ValueError:
            print('Invalid input. Please enter a valid transaction ID.')

    @staticmethod
    def get_amount():
        """
        Prompt the user to input a positive transaction amount.

        The function ensures the input is a valid number and greater than zero.
        If the input is invalid, it provides feedback and prompts the user to try again.

        Returns:
            float: The valid positive transaction amount entered by the user.

        Raises:
            ValueError: If the input cannot be converted to a float or is non-numeric.
        """
        while True:
            try:
                amount = float(input('Amount: '))
                if amount > 0:
                    return amount
                else:
                    print('Amount must be positive.')
            except ValueError:
                print('You should type a valid number. ')

    @staticmethod
    def get_category():
        """
        Prompt the user to select a transaction category from a predefined list.

        The function displays a list of categories, validates the user's input,
        and ensures the selection is a valid number corresponding to an available category.

        Categories:
            1: Food
            2: Transportation
            3: Utilities
            4: Entertainment
            5: Health
            6: Account

        Returns:
            int: The number corresponding to the selected category.

        Raises:
            ValueError: If the input is not a valid integer.
        """
        categories = {
            1: 'Food',
            2: 'Transportation',
            3: 'Utilities',
            4: 'Entertainment',
            5: 'Health',
            6: 'Account'
        }
        while True:
            print('Select a category: ')
            for key, value in categories.items():
                print(f'{key}: {value}')
            try:
                category = int(input('Select a category: '))
                if category in categories:
                    return category
                    break
                print('Invalid choice. Please select a valid category.  ')
            except ValueError:
                print('You should type a number corresponding to a category. ')

    @staticmethod
    def get_description():
        """
        Prompt the user to input a description for the transaction.

        This function collects a free-text input from the user, which serves
        as a brief explanation or note about the transaction.

        Returns:
            str: The description entered by the user.
        """
        return input('Description: ')

    @staticmethod
    def get_valid_date():
        """
        Prompt the user to input a transaction date in the format YYYY-MM-DD.

        The function validates the input to ensure it follows the correct date format.
        If the input is invalid, it provides feedback and prompts the user to try again.

        Returns:
            datetime: A `datetime` object representing the valid transaction date.

        Raises:
            ValueError: If the input is not in the correct YYYY-MM-DD format.
        """
        while True:
            try:
                transaction_date = input('Enter date (YYYY-MM-DD: ')
                return datetime.strptime(transaction_date, '%Y-%m-%d')
            except ValueError:
                print('Invalid date format. Please use YYYY-MM-DD. Try again:')

    @staticmethod
    def get_transaction_type():
        """
        Prompt the user to select the type of transaction.

        The function ensures the input is a valid integer corresponding to one of the following options:
            1: Income
            2: Expense
        If the input is invalid, it provides feedback and prompts the user to try again.

        Returns:
            int: The number corresponding to the selected transaction type (1 for Income, 2 for Expense).

        Raises:
            ValueError: If the input is not a valid integer or not within the allowed options.
        """
        while True:
            print('Select type of transaction [1] Income [2] Expense: ')
            try:
                type_of_transaction = int(input('Select number: '))
                if type_of_transaction in [1, 2]:
                    return type_of_transaction
                print('Invalid choice. Please select 1 or 2.')
            except ValueError:
                print('You should type a number (1 or 2). ')
