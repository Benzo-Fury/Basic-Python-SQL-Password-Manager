import os
import random
import socket
import sqlite3
import string
import sys
import time

# connects to database
connection = sqlite3.connect('database.db')
c = connection.cursor()


# MISC FUNCTIONS


def abort_process():
    # function to abort the process
    print('Aborting process')
    time.sleep(2)
    sys.exit()


def generate_password(length):
    # generates a strong password
    special_chars = (random.choice(["!@#$%^&*()_+{}:\"<>?,./;'[]\\"]) for _ in range(length))
    letters_lower = (random.choice(string.ascii_lowercase) for _ in range(length))
    letters_upper = (random.choice(string.ascii_uppercase) for _ in range(length))
    result_str = ''.join(letters_lower) + ''.join(letters_upper) + ''.join(special_chars)
    shuffle = random.sample(result_str, len(result_str))
    return ''.join(shuffle)


# PASSWORD FUNCTIONS


def add_password(password):
    # function to add a password to the database
    website = input("Enter website name: ")
    if not website.endswith('.com'):
        print('Website MUST end with ".com"')
        abort_process()
    c.execute("SELECT * FROM passwords WHERE website = ?", (website,))
    result = c.fetchone()
    if result:
        print('That website is already in the database.')
        time.sleep(2)
        os.system('cls')
        return
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
    # function to list all the stored passwords

    check_password = input('Input admin password: ')
    if check_password != 'monkeys':
        print('Wrong password')
        abort_process()
    os.system('cls')
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    print(rows)


def search_passwords(search):
    # function to search for a specific password.
    c.execute("SELECT * FROM passwords WHERE website = ? OR username = ?", (search, search))
    rows = c.fetchall()
    if not rows:
        print("No passwords found.")
    else:
        for row in rows:
            print(
                f'Website: "{row[0]}", Username: "{row[1]}", Password: "{row[2]}"')


def update_password(password):
    # function to update a specific password that can be searched for.
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
    # function to delete the specified password.
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


# Checks and misc


def password_strength(password):
    # function to check the strength of the inputted password
    if len(password) < 5:
        print('Your password is too weak.')
        abort_process()
    special_chars = [i for i in "!@#$%^&*()_-+={}[]|\:;'<>,./?"]

    for char in special_chars:
        if char in password:
            break
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
            # Show all passwords
            show_passwords()
            input('Press any key to continue: ')
            os.system('cls')
        case '2':
            # Search for a specific password
            query = input("Enter search: ")
            search_passwords(query)
        case '3':
            # Add a new password
            psd = input('Enter your password or enter 1 to auto generate: ')
            if psd == '1':
                psd = generate_password(4)
            password_strength(psd)
            add_password(psd)
            os.system('cls')
        case '4':
            # Update a password
            psd = input('Enter your password or enter 1 to auto generate: ')
            if psd == '1':
                psd = generate_password(4)
            password_strength(psd)
            update_password(psd)
        case '5':
            # Delete a password
            delete_password()
        case '6':
            # Abort the process
            abort_process()
        case _:
            # anything else inputted
            print("Invalid choice. Please try again.")
            time.sleep(1)
            os.system('cls')
