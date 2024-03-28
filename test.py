import hashlib
import generator
import validator 
import sqlite3
import os

def sha256_hash(input_string):
    # Convert input string to bytes
    input_bytes = input_string.encode('utf-8')
    
    # Compute SHA-256 hash
    sha256_hash = hashlib.sha256(input_bytes)
    
    # Get the hexadecimal representation of the hash
    hashed_string = sha256_hash.hexdigest()
    
    return hashed_string

def sign_in():
    print('                        Sign up                     \n')
    print('Note : You can use only one profile at once.\n')
    name = input('Enter your name : ')
    shopname = input('Enter your shop/startup name : ')
    username = input('Enter your username : ')
    password = input('Enter your password : ')
    key = generator.generate()
    try:
        with open('pass.txt', 'w') as f:
            f.write(username + ' ' + sha256_hash(password) +  ' ' + name + ' ' + '0\n')
        with open ('key.txt', 'w') as k:
            k.write(key + '\n')
        print('Sign up successful\n')
        print(f'This is your recovery key. You will need it if you forget your password. Make sure to keep it safe : {key}\n')
        log_in()
    except Exception as e:
        print('Error please retry\n')
        sign_in()

def log_in():
    print('Log in\n')
    username = input('Enter your username : ')
    password = input('Enter your password : ')
    try:
        with open('pass.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.split(' ')[0] == username and line.split(' ')[1] == sha256_hash(password):
                    print('Login successful\n')
                    ims()
                else:
                    print('Invalid username or password\n')
                    print('1) Reset Password        2) Retry\n')
                    a = input(': ')
                    if a == '1':
                        reset_password()
                    elif a == '2':
                        log_in()
                    else:
                        print('Error please retry\n')
    except Exception as e:
        print('Error please retry\n')
        log_in()

def reset_password():
    print('Reset Password\n')
    print('Enter your username :\n')
    usr = input(': ')
    try:
        with open('pass.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.split(' ')[0] == usr:
                    re_key = input('Enter your recover key  :\n')
                    cor = validator.vldtr(re_key)
                    if cor == 'z':
                        new_pass = input('Enter your new password :\n')
                        with open('pass.txt', 'w') as f:
                            f.write(usr + ' ' + sha256_hash(new_pass) + ' ' + line.split(' ')[2] + ' ' + '0\n')
                        print('Password reset successful\n')
                    else:
                        print('Invalid recover key\n')
                        print('1) Retry        2) Back\n')
                        a = input(': ')
                        if a == '1':
                            reset_password()
                        elif a == '2':
                            log_in()
                        else:
                            print('Error please retry\n')
                else:
                    print('Invalid username\n')
                    print('1) Retry        2) Back\n')
                    a = input(': ')
                    if a == '1':
                        reset_password()
                    elif a == '2':
                        log_in()
                    else:
                        print('Error please retry\n')
    except Exception as e:
        print(f'Error please retry {e}\n')
        reset_password()

def create_inventory_table():
    # Check if the database file already exists
    if os.path.exists('inventory.db'):
        print("Database file 'inventory.db' already exists. Skipping creation.\n")
        return
    
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a new table for inventory
    cursor.execute('''CREATE TABLE inventory (
                        id INTEGER PRIMARY KEY,
                        item TEXT NOT NULL,
                        current_amount INTEGER NOT NULL,
                        required_amount INTEGER NOT NULL
                    )''')

    # Save (commit) the changes
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    print("Table 'inventory' created successfully.\n")

def add_stock():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Ask the user for input
    item_name = input("Enter the name of the item: \n")
    current_amount = int(input("Enter the current amount of the item: \n"))
    required_amount = int(input("Enter the required amount of the item: \n"))

    # Insert the new item into the inventory table
    cursor.execute("INSERT INTO inventory (item, current_amount, required_amount) VALUES (?, ?, ?)", 
                    (item_name, current_amount, required_amount))

    # Save (commit) the changes
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    print("Item added to inventory successfully.\n")

def remove_stock():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Display all items in the inventory
    print("Current items in inventory:\n")
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Item: {row[1]}, Current Amount: {row[2]}, Required Amount: {row[3]}")

    # Ask the user for input
    item_id = int(input("Enter the ID of the item you want to remove: \n"))

    # Check if the item ID exists in the inventory
    cursor.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
    existing_item = cursor.fetchone()
    if existing_item:
        # Remove the item from the inventory table
        cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        print(f"Item with ID {item_id} removed from inventory successfully.\n")
    else:
        print(f"No item found with ID {item_id}.\n")

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def update_usage():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Display all items in the inventory
    print("Current items in inventory:\n")
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Item: {row[1]}, Current Amount: {row[2]}, Required Amount: {row[3]}")

    # Ask the user for input
    item_id = int(input("Enter the ID of the item you want to update: \n"))
    new_amount = int(input("Enter the new current amount for the item: \n"))

    # Check if the item ID exists in the inventory
    cursor.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
    existing_item = cursor.fetchone()
    if existing_item:
        # Update the current amount of the item in the inventory table
        cursor.execute("UPDATE inventory SET current_amount=? WHERE id=?", (new_amount, item_id))
        conn.commit()
        print(f"Current amount for item with ID {item_id} updated successfully.\n")
    else:
        print(f"No item found with ID {item_id}.\n")

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def low_alert():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Retrieve items where current amount is less than required amount
    cursor.execute("SELECT * FROM inventory WHERE current_amount < required_amount")
    insufficient_items = cursor.fetchall()

    # Print items with insufficient inventory levels
    if insufficient_items:
        print("Items with insufficient inventory levels:\n")
        for item in insufficient_items:
            print(f"Item: {item[1]}, Current Amount: {item[2]}, Required Amount: {item[3]}")
    else:
        print("All items have sufficient inventory levels.\n")

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def view_stock():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Retrieve all items from the inventory table
    cursor.execute("SELECT * FROM inventory")
    inventory_items = cursor.fetchall()

    # Print all inventory items with their details
    if inventory_items:
        print("Inventory:\n")
        print("{:<5} {:<20} {:<15} {:<15}".format("ID", "Item", "Current Amount", "Required Amount"))
        print("-" * 55)
        for item in inventory_items:
            print("{:<5} {:<20} {:<15} {:<15}".format(item[0], item[1], item[2], item[3]))
    else:
        print("Inventory is empty.\n")

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def view_left_stock():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Retrieve items from the inventory table where current amount is more than or equal to required amount
    cursor.execute("SELECT * FROM inventory WHERE current_amount >= required_amount")
    surplus_items = cursor.fetchall()

    # Print surplus inventory items with their details
    if surplus_items:
        print("Items with surplus inventory:\n")
        print("{:<5} {:<20} {:<15} {:<15}".format("ID", "Item", "Current Amount", "Required Amount"))
        print("-" * 55)
        for item in surplus_items:
            print("{:<5} {:<20} {:<15} {:<15}".format(item[0], item[1], item[2], item[3]))
    else:
        print("No surplus inventory items found.\n")

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def ims():
    query = input("Enter your query (? for help). 'exit' to close : \n")
    if query == '?':
        print(''' Use the following keywords to perform related queries :\n
              1. Add a new item in stock => add_stock\n
              2. Update the available amount of a stock item => update_stock\n
              3. View all the item in stock=> view_stock\n
              4. View items which are more than the required amount=> view_left_stock\n
              5. View all the items less than their required amount => low_alert\n
              6. Remove an item from stock => remove_stock\n
              7. Exit
              \n''')

    elif query == 'add_stock':
        add_stock()
        ims()
    elif query == 'update_stock':
        update_usage()
        ims()
    elif query == 'view_stock':
        view_stock()
        ims()
    elif query == 'view_left_stock':
        view_left_stock()
        ims()
    elif query == 'low_alert':
        low_alert()
        ims()
    elif query == 'remove_stock':
        remove_stock()
        ims()
    elif query == 'exit':
        exit()
    else:
        print('Invalid query\n')
        ims()

def main():
    create_inventory_table()
    print('Hello! Welcome to the Inventory Management System.\n')
    print('Choose :  1) Log in   2) Sign up\n')
    a = input(': ')
    b = '2'
    c = '1'
    if a == c :
        log_in()
    elif a == b :
        sign_in()
    else :
        print('Error please retry\n')

main()
