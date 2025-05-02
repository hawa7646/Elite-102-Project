# Banking System 

import sqlite3

# Connect to database (creates file if not there)
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Create accounts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_number INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pin TEXT NOT NULL,
    balance REAL DEFAULT 0.0
)
''')
conn.commit()

# Create new account
def create_account():
    print("=== Create Account ===")
    name = input("Enter full name: ")
    pin = input("Choose 4-digit PIN: ")
    cursor.execute("INSERT INTO accounts (name, pin) VALUES (?, ?)", (name, pin))
    conn.commit()
    print("Account created. Your account number is:", cursor.lastrowid)

# Login
def login():
    print("=== Login ===")
    acc_num = input("Enter account number: ")
    pin = input("Enter PIN: ")
    cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (acc_num, pin))
    user = cursor.fetchone()
    if user:
        print("Welcome,", user[1])
        return user
    else:
        print("Login failed.")
        return None

# Check balance
def check_balance(user):
    print("Your balance is $", user[3])

# Deposit
def deposit(user):
    amount = float(input("Enter amount to deposit: "))
    new_balance = user[3] + amount
    cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, user[0]))
    conn.commit()
    print("Deposited. New balance: $", new_balance)

# Withdraw
def withdraw(user):
    amount = float(input("Enter amount to withdraw: "))
    if amount > user[3]:
        print("Not enough funds.")
    else:
        new_balance = user[3] - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, user[0]))
        conn.commit()
        print("Withdrawn. New balance: $", new_balance)

# Modify account
def modify_account():
    acc_num = input("Account number to update: ")
    new_name = input("New name: ")
    new_pin = input("New PIN: ")
    cursor.execute("UPDATE accounts SET name = ?, pin = ? WHERE account_number = ?", (new_name, new_pin, acc_num))
    conn.commit()
    print("Account updated.")

# Delete account
def delete_account():
    acc_num = input("Enter account number to delete: ")
    cursor.execute("DELETE FROM accounts WHERE account_number = ?", (acc_num,))
    conn.commit()
    print("Account deleted.")

# User menu (after login)
def user_menu(user):
    while True:
        print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout")
        choice = input("Choose: ")
        if choice == '1':
            check_balance(user)
        elif choice == '2':
            deposit(user)
            user = get_user(user[0])  # Refresh data after deposit
        elif choice == '3':
            withdraw(user)
        elif choice == '4':
            break
        else:
            print("Invalid option")

# Get user again (used after deposit)
def get_user(acc_num):
    cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (acc_num,))
    return cursor.fetchone()

# Main menu function
def main_menu():
    while True:
        print("\n=== Beginner Bank ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Modify Account (Admin)")
        print("4. Delete Account (Admin)")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            user = login()
            if user:
                user_menu(user)
        elif choice == '3':
            modify_account()
        elif choice == '4':
            delete_account()
        elif choice == '5':
            print("Thanks for using the app.")
            break
        else:
            print("Invalid input.")

# Run
main_menu()

