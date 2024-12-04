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
    # user.register(db)
    if user.login(db):
        print("Login successful.")
        user_id = db.get_user(user.username)['user_id']
        while True:
            print('[1] View Transactions\n'
                  '[2] Add Transaction\n'
                  '[3] Delete Transaction\n'
                  '[4] Update transaction\n'
                  '[5] Exit')
            try:
                choice = int(input("Choose an option: "))

                if choice == 1:
                    user.show_transactions(user_id, db)
                elif choice == 2:
                    user.create_transaction(user_id, db)
                elif choice == 3:
                    user.delete_transaction(user_id, db)
                elif choice == 4:
                    user.update_transaction(user_id, db)
                elif choice == 5:
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again. ")
            except ValueError as error:
                print('Input should be an integer. ')


if __name__ == '__main__':
    main()
