from database import Database
from user import User
from getpass4 import getpass


def main():
    db = Database()
    db.db_init()
    username = input('Enter your username: ')
    password = getpass('Enter your password: ')
    email = input('Enter your email: ')
    user = User(username, password, email)
    user.register(db)
    user.login(db)


if __name__ == '__main__':
    main()
