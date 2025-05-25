from DatabaseManager import Database_manager
from employee import Employee
from customer import Customer
from SessionManager import SessionManager

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def admin_menu(db):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. View All Employees")
        print("2. View All Customers")
        print("3. Delete Employee")
        print("4. Delete Customer")
        print("b. Back to Main Menu")
        choice = input("Enter your choice (1-4 or b): ").strip().lower()

        if choice == "1":
            print("\n--- ALL EMPLOYEES ---")
            employees = db.fetchall("SELECT * FROM employees")
            for emp in employees:
                print(f"User ID: {emp[0]}, Password  :{emp[1]}")

        elif choice == "2":
            print("\n--- ALL CUSTOMERS ---")
            customers = db.fetchall("SELECT * FROM customers")
            for cust in customers:
                print(f"SSN ID: {cust[0]}, Account No: {cust[7]}, Name: {cust[1]} {cust[2]}, Email: {cust[3]}, Phone: {cust[4]}, Username: {cust[5]}, Balance:{cust[8]}, Password: {cust[6]}")

        elif choice == "3":
            uid = input("Enter Employee User ID to delete: ")
            db.execute("DELETE FROM employees WHERE userid = ?", (uid,))
            print(f"Employee '{uid}' deleted (if existed).")

        elif choice == "4":
            acc_no = input("Enter Customer Account Number to delete: ")
            db.execute("DELETE FROM customers WHERE ACCOUNT_NO = ?", (acc_no,))
            print(f"Customer with Account No '{acc_no}' deleted (if existed).")

        elif choice == "b":
            return

        else:
            print("Invalid choice. Select 1-4 or b.")


def employee_menu(emp, session):
    while True:
        if not session.is_active():
            print("\nSession expired. Please log in again.\n")
            return

        print("\n--- EMPLOYEE MENU ---\n")
        print(f"Welcome to the Employee Portal ... {session.user}")
        print("1. Create Customer")
        print("2. Edit Customer")
        print("3. View All Customers")
        print("4. View One Customer")
        print("5. Delete Customer")
        print("6. Logout")
        print("b. Back to Main Menu")
        choice = input("Enter your choice (1-6 or b): ").strip().lower()
        if choice == 'b':
            return
        session.refresh()

        if choice == "1":
            print("\n--- CREATE CUSTOMER ---")
            ssn_id = int(input("Enter SSN ID: "))
            fname = input("Enter First Name: ")
            lname = input("Enter Last Name: ")
            email = input("Enter Email Address: ")
            phone = int(input("Enter Phone Number: "))
            usrname = input("Create Username: ")
            pwd = input("Create Password: ")

            success = emp.create_customer(ssn_id, fname, lname, email, phone, usrname, pwd)
            print("Customer Creation Successful" if success else "Invalid Credentials")

        elif choice == "2":
            print("\n--- EDIT CUSTOMER ---")
            acc_no = input("Enter Account Number: ")
            field = input("Enter field to update (Note: 'account_no' and 'ssn_id' cannot be updated): ").strip().lower()
            value = input(f"Enter new value for {field}: ")
            emp.edit_customer(acc_no, field, value)

        elif choice == "3":
            print("\n--- ALL CUSTOMERS ---")
            emp.view_customers()

        elif choice == "4":
            acc_no = input("Enter Account Number to view: ")
            emp.view_customer(acc_no)

        elif choice == "5":
            acc_no = input("Enter Account Number to delete: ")
            customer = emp.db.fetchone("SELECT * FROM customers WHERE ACCOUNT_NO = ?", (acc_no,))
            if not customer:
                print("Customer not found.")
                continue

            print("\n--- Customer Details ---")
            print("Username       :", customer[6])
            print("Name           :", customer[1], customer[2])
            print("Email          :", customer[3])
            print("Phone          :", customer[4])
            print("Username       :", customer[5])
            print("Account Number :", customer[7])
            print("Balance        :", customer[8])

            confirm = input("Are you sure you want to delete this customer? (yes/no): ").lower()
            if confirm != 'yes':
                print("Deletion cancelled.")
                continue

            emp_pass = input("Enter your employee password to confirm: ")
            if emp.login(session.user, emp_pass):
                emp.del_customer(acc_no)
                print("Customer deleted.")
            else:
                print("Wrong password. Deletion aborted.")

            session.refresh()

        elif choice == "6":
            print("Logging out...")
            session.end_session()
            return

        else:
            print("Invalid choice. Please select a valid option (1-6).")

def customer_menu(customer, session):
    while True:
        if not session.is_active():
            print("\nSession expired. Please log in again.\n")
            return

        print("\n--- CUSTOMER MENU ---")
        print("1. View Account Details")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Logout")
        print("b. Back to Main Menu")
        choice = input("Enter your choice (1-4 or b): ").strip().lower()
        if choice == 'b':
            return
        session.refresh()

        if choice == "1":
            print("\n--- ACCOUNT DETAILS ---")
            customer.view_details()

        elif choice == "2":
            print("\n--- DEPOSIT MONEY ---")
            amount = float(input("Enter amount to deposit: "))
            customer.deposit(amount)

        elif choice == "3":
            print("\n--- WITHDRAW MONEY ---")
            amount = float(input("Enter amount to withdraw: "))
            customer.withdraw(amount)

        elif choice == "4":
            print("Logging out...")
            session.end_session()
            return

        else:
            print("Invalid choice. Please select a valid option (1-4).")

def main():
    db = Database_manager()
    db.create_table()

    while True:
        print("\n=== BANKING SYSTEM ===")
        print("1. Employee Portal")
        print("2. Customer Portal")
        print("3. Admin Portal")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()


        if choice == "1":
            emp_object = Employee(db)
            session = SessionManager(timeout_seconds=300)
            while True:
                print("\n--- EMPLOYEE ACCESS ---")

                ch = input("1. Login\n2. Sign Up\nb. Back\nEnter your choice: ").strip()
                if ch == "1":
                    uid = input("Enter Employee User ID: ")
                    pwd = input("Enter Password: ")
                    if emp_object.login(uid, pwd):
                        session.start_session(user=uid)  # store logged-in user in session
                        employee_menu(emp_object, session)
                        break
                    else:
                        print("Invalid Username or Password")

                elif ch == "2":
                    uid = input("Create Employee User ID: ")
                    pwd = input("Create Password: ")
                    if emp_object.signup(uid, pwd):
                        print("Signup Successful. Please login.")
                    else:
                        print("Signup Failed.")

                elif ch == 'b':
                    break
                else:
                    print("Invalid option. Choose 1 or 2.")

        elif choice == "2":
            customer_object = Customer(db)
            uid = input("Enter Customer Username: ")
            pwd = input("Enter Password: ")
            if customer_object.login(uid, pwd):
                session = SessionManager(timeout_seconds=300)
                session.start_session(user=uid)
                customer_menu(customer_object, session)
            else:
                print("Invalid Username or Password")

        elif choice == "3":
            uid = input("Enter Admin Username: ")
            pwd = input("Enter Admin Password: ")
            if uid == ADMIN_USER and pwd == ADMIN_PASS:
                admin_menu(db)
            else:
                print("Invalid Admin Credentials.")

        elif choice == "4":
            print("Exiting system...")
            db.close()
            break

        else:
            print("Please enter a valid input (1, 2 or 3).")

if __name__ == "__main__":
    main()
