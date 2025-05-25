from validators import Validator
import random
import time


class Employee:
    def __init__(self, db):
        self.db = db

    def login(self, uid, pwd):
        q = "SELECT * FROM employees WHERE userid=? AND password=?"
        result = self.db.fetchone(q, (uid, pwd))
        if result is None:
            return
        print("Login success")
        return True

    def signup(self, uid, pwd):
        q = "SELECT * FROM employees WHERE userid=?"
        if self.db.fetchone(q, (uid,)):
            print("Existing user name in the system, choose another one")
            return
        if not Validator.password_check(pwd):
            print("Invalid password format")
            return
        self.db.execute("INSERT INTO employees (userid, password) VALUES (?, ?)", (uid, pwd))
        print("Employee ID created")

    def generate_accNumber(self, ssn_id):
        timestamp = str(int(time.time() * 1000))[-5:]
        rand = str(random.randint(100, 999))
        acc_num = f"{ssn_id}{timestamp}{rand}"
        return acc_num

    def create_customer(self, ssn_id, fname, lname, email, phone, usrname, pwd):
        if not Validator.email_check(email):
            print("Please enter a valid email")
            return

        if not Validator.usrname_check(usrname):
            print("Please enter a valid username")
            return

        if not Validator.password_check(pwd):
            print("Please enter a valid password")
            return

        if not Validator.mobile_number_check(phone):
            print("Enter a valid phone number")
            return

        account_number = self.generate_accNumber(ssn_id)
        initial_amount = 1000
        q = "INSERT INTO customers (ssn_id, first_name, last_name, email, phone, usrname, pwd, ACCOUNT_NO, AMOUNT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.db.execute(q, (ssn_id, fname, lname, email, phone, usrname, pwd, account_number, initial_amount))

        q1 = "SELECT * FROM customers WHERE ACCOUNT_NO=?"
        res = self.db.fetchone(q1, (account_number,))
        if res is None:
            print("Customer account not created due to an error in the details entered")
            return

        print("Customer created successfully and added to the Database")
        return True

    def edit_customer(self, accno, field, value):
        restricted_fields = ["ACCOUNT_NO", "ssn_id"]
        if field.upper() in restricted_fields:
            print("You are not allowed to update ACCOUNT_NO or SSN ID.")
            return
        q = f"UPDATE customers SET {field.lower()} = ? WHERE ACCOUNT_NO = ?"
        self.db.execute(q, (value, accno))
        print("Customer Updated")

    def del_customer(self, accno):
        q = "DELETE FROM customers WHERE ACCOUNT_NO = ?"
        self.db.execute(q, (accno,))
        print("Customer Deleted")

    def view_customers(self):
        customers = self.db.fetchall("SELECT * FROM customers")

        if not customers:
            print("No customers found.")
            return
        for c in customers:
            for cust in customers:
                print(f"SSN ID: {cust[0]}, Account No: {cust[7]}, Name: {cust[1]} {cust[2]}, Email: {cust[3]}, Phone: {cust[4]}, Username: {cust[5]}, Balance:{cust[8]}")



    def view_customer(self, accno):
        q = "SELECT * FROM customers WHERE ACCOUNT_NO = ?"
        customer = self.db.fetchone(q, (accno,))
        if not customer:
            print("Customer not found.")
            return

        print("\n--- Customer Details ---")
        print("Username       :", customer[6])
        print("Name           :", customer[1], customer[2])
        print("Email          :", customer[3])
        print("Phone          :", customer[4])
        print("Username       :", customer[5])
        print("Account Number :", customer[7])
        print("Balance        :", customer[8])

