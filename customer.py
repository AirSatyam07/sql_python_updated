from DatabaseManager import Database_manager

class Customer:
    def __init__(self, db):
        self.db = db
        self.accno = None

    def login(self, email, pwd):
        q = "SELECT * FROM customers WHERE email=? AND pwd=?"
        result = self.db.fetchone(q, (email, pwd))

        if not result:
            return False

        self.accno = result[7]
        print(f"Login Successful, Welcome {result[1]}")
        print("=========")
        return True

    def view_details(self):
        q = "SELECT * FROM customers WHERE ACCOUNT_NO=?"
        result = self.db.fetchone(q, (self.accno,))
        if result:
            print("Customer Details:")
            print("=================")
            print(f"SSN ID     : {result[0]}")
            print(f"First Name : {result[1]}")
            print(f"Last Name  : {result[2]}")
            print(f"Email      : {result[3]}")
            print(f"Phone      : {result[4]}")
            print(f"Username   : {result[5]}")
            print(f"Account No : {result[7]}")
            print(f"Balance    : {result[8]}")
            print("=================")
        else:
            print("No details found.")

    def deposit(self, amount):
        q1 = "SELECT AMOUNT FROM customers WHERE ACCOUNT_NO=?"
        pre = self.db.fetchone(q1, (self.accno,))
        if not pre:
            print("Account not found.")
            return

        new_amount = amount + pre[0]
        q2 = "UPDATE customers SET AMOUNT=? WHERE ACCOUNT_NO=?"
        self.db.execute(q2, (new_amount, self.accno))
        print(f"Previous Amount: {pre[0]}")
        print(f"Deposited Amount: {amount}")
        print(f"Updated Balance: {new_amount}")

    def withdraw(self, amount):
        q1 = "SELECT AMOUNT FROM customers WHERE ACCOUNT_NO=?"
        pre = self.db.fetchone(q1, (self.accno,))
        min_balance = 1000


        if not pre:
            print("Account not found.")
            return

        current_balance = pre[0]
        min_balance = 1000

        if amount > current_balance:
            print("Insufficient Balance")
            return

        if (current_balance - amount) < min_balance:
            print(f"Cannot withdraw. Minimum balance of {min_balance} must be maintained.")
            return

        new_amount = current_balance - amount
        q2 = "UPDATE customers SET AMOUNT=? WHERE ACCOUNT_NO=?"
        self.db.execute(q2, (new_amount, self.accno))
        print(f"Previous Amount: {current_balance}")
        print(f"Withdrawn Amount: {amount}")
        print(f"Updated Balance: {new_amount}")


