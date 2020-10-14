# Write your code here
from random import randint
import sqlite3


def run_query(query, msg = ""):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute(query)
    if msg = "":
        data = cur.fetchone()
    conn.commit()
    conn.close()
    if msg = "":
        return data

def create_db():

    create_table = """CREATE TABLE IF NOT EXISTS card   (
                        id INTEGER,
                        number TEXT,
                        pin TEXT,
                        balance INTEGER DEFAULT 0
                                                        )"""
    run_query(create_table, "No return")


count = 1
def create_account():
    global count
    IIN = str(400000)
    account_id = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + \
                 str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + \
                 str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
    checksum = str(Luhn_algorithm(IIN + account_id))
    PIN = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
    card_number = IIN + account_id + checksum
    cur.execute("INSERT INTO card VALUES(?, ?, ?)",(count,card_number, PIN))
    conn.commit()
    count += 1
    return card_number, PIN

def Luhn_algorithm(id):
    number = id[0:15]
    temp = []
    for index, number in enumerate(number,1):
        if index % 2 != 0:
            temp.append(int(number) * 2)
        else:
            temp.append(int(number))

    for a, b in enumerate(temp):
        if b > 9:
            temp[a] -= 9

    total = sum(temp)
    if  total % 10 == 0:
        checksum = 0
    else:
        checksum = 10 - total % 10
    return checksum




def log_in(card_number, PIN):
    cur.execute("SELECT * FROM card")
    results = cur.fetchall()
    for account in results:
        if str(card_number) in account and str(PIN) in account:
            return True
    else:
        return False


def account_options(card_number, PIN):
    cur.execute("SELECT * FROM card")
    results = cur.fetchall()
    for account in results:
        if str(card_number) in account and str(PIN) in account:
            balance = str(account[3])
    while True:
        account_info = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
        print()
        if account_info == "1": # Check balance
            # check_balance()
            cur.execute("SELECT * FROM card")
            results = cur.fetchall()
            for account in results:
                if str(card_number) in account and str(PIN) in account:
                    print(account[3])
                    print()
            continue
        elif account_info == "2": # Add income
            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ? AND PIN = ?  ",
                        (int(input("Enter income:\n")), int(card_number), int(PIN)))
            cur.execute("SELECT * FROM card")
            results = cur.fetchall()
            for account in results:
                if str(card_number) in account and str(PIN) in account:
                    balance = str(account[3])
            conn.commit()

            print("Income was added!\n")
            continue
            # action = "Add income"

        elif account_info == "3": # Transfer
            print("Transfer")
            transfer_number = input("Enter card number:\n")
            real_checksum = str(Luhn_algorithm(transfer_number))
            if real_checksum == transfer_number[-1]:
                cur.execute("SELECT number FROM card")
                columns = cur.fetchall()
                if (transfer_number,) in columns:
                    if transfer_number == card_number:
                        print("You can't transfer money to the same account!\n")
                    else:
                        transfer_amount = input("Enter how much money you want to transfer:\n")
                        if int(transfer_amount) > int(balance):
                            print("Not enough money!\n")
                        else:
                            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ? ",
                                        (int(transfer_amount), int(transfer_number)))
                            cur.execute("UPDATE card SET balance = balance - ? WHERE number = ? ",
                                        (int(transfer_amount), int(card_number)))
                            conn.commit()
                            print("Success!\n")
                else:
                    print("Such a card does not exist.\n")
            else:
                print("Probably you made mistake in the card number. Please try again!\n")
        elif account_info == "4": # Close account
            cur.execute("DELETE FROM card WHERE number = ?", (card_number,))
            conn.commit()
            action = "Close Account"
            break
        elif account_info == "5":
            action = "log out"
            break
        elif account_info == "0":
            action = "exit"
            break
    return action


while True:
    menu = input("1. Create an account\n2. Log into account\n0. Exit\n")
    print()

    if menu == "1": # Create Account
        card_number, PIN = create_account()
        print(f"Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{PIN}\n")

    elif menu == "2": # Log In
        card_input = input("Enter your card number:\n")
        PIN_input = input("Enter your PIN:\n")
        print()

        if log_in(card_input, PIN_input): # Check if in DB
            print("You have successfully logged in!\n")
            action = account_options(card_input, PIN_input)
            if action == "Close Account": # Close Account
                print("The account has been closed!\n")
                continue
            elif action == "log out": # Log Out
                print("You have successfully logged out!\n")
                continue
            else: # Exit
                break
        else: # if NOT in DB
            print("Wrong card number or PIN!")
            print()

    else: # Exit
        break
print("Bye!")
conn.commit()
conn.close()