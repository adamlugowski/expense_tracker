import bcrypt
from email_validator import validate_email, EmailNotValidError


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

