import os
import socket
import sqlite3
import sys
import time

# connects to database
connection = sqlite3.connect('database.db')
c = connection.cursor()


def abort_process():
    # function for aborting the process
    print('Aborting process')
    time.sleep(2)
    sys.exit()


def add_password(password):
    # adds a password to the database
    website = input("Enter website name: ")
    if not website.endswith('.com'):
        print('Website MUST end with ".com"')
        abort_process()
    email = input("Enter email: ")
    if not email.endswith('.com'):
        print('Email must end with .com')
        abort_process()
    username = input("Enter username: ")
    c.execute("INSERT INTO Passwords VALUES (?, ?, ?, ?, ?)",
              (email, username, password, website, socket.gethostbyname(socket.gethostname())))
    connection.commit()
    print("Password added.")


def show_passwords():
    # lists all of the stored passwords
    # TODO: change format of outputted results.
    check_password = input('Input admin password: ')
    if check_password != 'monkeys':
        print('Wrong password')
        abort_process()
    # returning all rows to user
    os.system('cls')
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    print('Password List:')
    print(rows)


def search_passwords(search):
    # searches for a specific password.
    c.execute("SELECT * FROM passwords WHERE website = ? OR username = ?", (search, search))
    rows = c.fetchall()
    if not rows:
        print("No passwords found.")
    else:
        for row in rows:
            print(
                f'Website: "{row[0]}", Username: "{row[1]}", Password: "{row[2]}"')


def update_password(password):
    # updates a specific password that can be searched for.
    enter = input('Input website name: ')
    c.execute("SELECT * FROM passwords WHERE website = ?", (enter,))
    result = c.fetchone()
    if result is None:
        os.system('cls')
        print('Cannot find that website.')
        time.sleep(2)
        os.system('cls')
    else:
        c.execute("UPDATE passwords SET password = ? WHERE website = ?", (password, enter))
        connection.commit()
        print('Password updated')
        time.sleep(2)
        os.system('cls')


def delete_password():
    # deletes the specified password.
    website = input('Input the website you would like to delete: ')
    c.execute("SELECT * FROM passwords WHERE website = ?", (website,))
    result = c.fetchone()
    if result is None:
        os.system('cls')
        print('Cannot find that website.')
        time.sleep(2)
    else:
        c.execute("DELETE FROM passwords WHERE website = ?", (website,))
        connection.commit()
        os.system('cls')
        print('Password has been deleted.')
        time.sleep(2)
        os.system('cls')


def password_strength(password):
    # checks the strength of the inputted password
    if len(password) < 5:
        print('Your password is too weak.')
        abort_process()
    special_chars = "!@#$%^&*()_-+={}[]|\:;'<>,./?"

    for char in password:
        if char in special_chars:
            return
        else:
            print('Your password must contain at least 1 special character')
            abort_process()


while True:
    print("""
    Password Manager Menu:
    1. Show all passwords
    2. Search for a password
    3. Add a new password
    4. Update a password
    5. Delete a password
    6. Exit"
    """)
    choice = input("Enter your choice (1-6): ")
    os.system('cls')
    match choice:
        case '1':
            show_passwords()
            input('Press any key to continue: ')
            os.system('cls')
        case '2':
            query = input("Enter search: ")
            search_passwords(query)
        case '3':
            psd = input('Enter your password: ')
            password_strength(psd)
            add_password(psd)
            os.system('cls')
        case '4':
            psd = input('Enter your password: ')
            password_strength(psd)
            update_password(psd)
        case '5':
            delete_password()
        case '6':
            break
        case _:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            os.system('cls')