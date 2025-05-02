# Banking System
import sqlite3  # This connects me to a small local database

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Create a table called 'accounts' to store  users
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_number INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pin TEXT NOT NULL,
    balance REAL DEFAULT 0.0
)
''')
conn.commit()  # Save changes

# Step 1: Create an account
def create_account():
    print("=== Create a New Account ===")
    name = input("Enter your full name: ")
    pin = input("Choose a 4-digit PIN: ")

    # Add new user to the database
    cursor.execute("INSERT INTO accounts (name, pin) VALUES (?, ?)", (name, pin))
    conn.commit()

    # Get the new account number
    account_number = cursor.lastrowid
    print("Account created successfully!")
    print("Your account number is:", account_number)
    print("Please remember your account number and PIN for future logins.")
    print("You can now log in to your account.")
# Step 2: Log into account
def login():
    print("=== Login ===")
    acc_num = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (acc_num, pin))
    user = cursor.fetchone()  # Get result

    if user:
        print("Login successful! Welcome", user[1])
        return user
    else:
        print("Incorrect account number or PIN.")
        return None

# Step 3: Check balance
def check_balance(user):
    print("Your current balance is: $", user[3])
# Step 4: Deposit money
def deposit(user):
    print("=== Deposit ===")
    amount = float(input("Enter amount to deposit: "))
    new_balance = user[3] + amount

    cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, user[0]))
    conn.commit()
    print("Deposit successful. New balance: $", new_balance)
# Step 5: Withdraw money
def withdraw(user):
    print("=== Withdraw ===")
    amount = float(input("Enter amount to withdraw: "))

    if amount > user[3]:
        print("You don't have enough money.")
    else:
        new_balance = user[3] - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, user[0]))
        conn.commit()
        print("Withdrawal successful. New balance: $", new_balance)
# Step 6: Modify account (Admin)
def modify_account():
    print("=== Modify Account ===")
    acc_num = input("Enter account number to update: ")
    new_name = input("Enter new name: ")
    new_pin = input("Enter new PIN: ")

    cursor.execute("UPDATE accounts SET name = ?, pin = ? WHERE account_number = ?", (new_name, new_pin, acc_num))
    conn.commit()
    print("Account updated!")
# Step 7: Delete account (Admin)
def delete_account():
    print("=== Delete Account ===")
    acc_num = input("Enter account number to delete: ")
    cursor.execute("DELETE FROM accounts WHERE account_number = ?", (acc_num,))
    conn.commit()
    print("Account deleted.")
# Menu after logging in
def user_menu(user):
    while True:
        print("\n1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            check_balance(user)
        elif choice == '2':
            deposit(user)
            user = get_user(user[0])  # Refresh user data
        elif choice == '3':
            withdraw(user)
            user = get_user(user[0])  # Refresh user data
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Not a valid choice.")

# Refresh the user's data (to get new balance after deposit/withdraw)
def get_user(account_number):
    cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
    return cursor.fetchone()
# Main menu
def main_menu():
    while True:
        print("\n=== Welcome to the Beginner Bank ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Admin: Modify Account")
        print("4. Admin: Delete Account")
        print("5. Exit")

        choice = input("Choose an option: ")

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
            print("Exiting. Thanks for using Beginner Bank.")
            break
        else:
            print("That is not a valid option. Please try again.")

# Run the main menu
main_menu()
