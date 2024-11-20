from database import Database
from user import User
from getpass4 import getpass
from datetime import datetime


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


def get_description():
    """
    Prompt the user to input a description for the transaction.

    This function collects a free-text input from the user, which serves 
    as a brief explanation or note about the transaction.

    Returns:
        str: The description entered by the user.
    """
    return input('Description: ')


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


def create_transaction(db, user_id):
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
    amount = get_amount()
    category = get_category()
    description = get_description()
    valid_date = get_valid_date()
    type_of_transaction = get_transaction_type()
    db.add_transaction(user_id, amount, category, description, valid_date, type_of_transaction)


def main():
    db = Database()
    db.db_init()
    username = input('Enter your username: ')
    password = getpass('Enter your password: ')
    email = input('Enter your email: ')
    user = User(username, password, email)
    # user.register(db)
    if user.login(db):
        print("Login successful.")
        user_id = db.get_user(user.username)['user_id']
        #     create_transaction(db, user_id)
        db.show_transactions(user_id)


if __name__ == '__main__':
    main()
