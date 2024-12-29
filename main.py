from database import Database
from user import User
from getpass4 import getpass


def get_user_details():
    username = input('Enter your username: ')
    password = getpass('Enter your password: ')
    email = input('Enter your email: ')
    return User(username, password, email)


def main():
    db = Database()
    db.db_init()
    user_choice = int(input('Select: [0] Register [1] Login'))
    if user_choice == 0:
        user = get_user_details()
        user.register(db)
        print('Run the application again to be able to log in. ')
    elif user_choice == 1:
        user = get_user_details()
        if user.login(db, user.email):
            print("Login successful.")
            user_id = db.get_user(user.username)['user_id']
            while True:
                print('[1] View Transactions\n'
                      '[2] Add Transaction\n'
                      '[3] Delete Transaction\n'
                      '[4] Update transaction\n'
                      '[0] Exit')
                try:
                    choice = int(input("Choose an option: "))

                    if choice == 0:
                        print("Goodbye!")
                        break
                    elif choice == 1:
                        user.show_transactions(user_id, db)
                    elif choice == 2:
                        user.create_transaction(user_id, db)
                    elif choice == 3:
                        user.delete_transaction(user_id, db)
                    elif choice == 4:
                        user.update_transaction(user_id, db)
                    else:
                        print("Invalid option. Please try again. ")
                except ValueError:
                    print(f'Input should be an integer.')
    else:
        print('Choose right option')


if __name__ == '__main__':
    main()
