import mysql.connector
from datetime import datetime

def connect():
    mycon = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="rootuser",
        database="zwish_db_test6")
    if mycon.is_connected():
        print("Successfully connected to Zwish database")
    return mycon


def admin_login():
    adminname = input("Enter admin username: ")
    adminpass = input("Enter admin password: ")
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM Admin WHERE AdminID = %s AND Password = %s", (adminname, adminpass))
    admin = cursor.fetchone()
    if admin:
        print("Admin is successfully logged in.")
        return True
    else:
        print("Incorrect credentials given.")
        return False

def view_customer_analysis():
    try:
        cursor.execute("SELECT CustomerID, COUNT(OrderID) AS OrderCount FROM OrderLogBook GROUP BY CustomerID")
        results = cursor.fetchall()
        print("Orders each customer has placed till now:")
        for row in results:
            print(row)
    except mysql.connector.Error as e:
        print("Error", e)

def view_inventory_analysis():
    try:
        cursor.execute("SELECT Vendor.Name, COUNT(OrderLogBook.OrderID) AS OrderCount FROM Vendor LEFT JOIN OrderLogBook ON Vendor.VendorID = OrderLogBook.VendorID GROUP BY Vendor.Name")
        results = cursor.fetchall()
        print("Orders each vendor has delivered till now:")
        for row in results:
            print(row)
    except mysql.connector.Error as e:
        print("Error", e)


def generate_customer_id():
    cursor.execute("SELECT MAX(CAST(SUBSTRING(CustomerID, 2) AS UNSIGNED)) FROM Customer")
    lastid = cursor.fetchone()[0]
    if lastid is None:
        newid = 1
    else:
        newid = lastid + 1
    return "C" + str(newid).zfill(2)

def user_register():
    full_name = input("Enter your Full Name: ")
    email = input("Enter your EmailID: ")
    dob = input("Enter your Date of Birth (YYYY-MM-DD): ")
    payment_details = input("Enter your Payment Details: ")
    customer_id = generate_customer_id()
    try:
        cursor.execute("INSERT INTO Customer (CustomerID, Full_Name, Email, DOB, PaymentDetails, Status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (customer_id, full_name, email, dob, payment_details, 'Active'))
        mycon.commit()
        print(f"Registration successful! Your CustomerID is: {customer_id}")
        return customer_id
    except mysql.connector.Error as e:
        print("Error registering user:", e)
        return None

def user_login():
    while True:
        customer_id = input("Enter your CustomerID: ")
        cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (customer_id,))
        user = cursor.fetchone()
        if user:
            print("User login successful.")
            return customer_id
        else:
            print("Incorrect credentials given.")

def order_items(customer_id, item_id):
    try:
        cursor.execute("INSERT INTO CartItem (CustomerID, ItemID) VALUES (%s, %s)", (customer_id, item_id))
        mycon.commit()
        print("Item ordered successfully!")
    except mysql.connector.Error as e:
        print("Error ordering item:", e)

def main():
    while True:
        print("\nWelcome to the Zwish - Delivery in a Snap")
        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Register as User")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            if admin_login():
                while True:
                    print("\nMenu:")
                    print("1. View Customer Analysis")
                    print("2. View Inventory Analysis")
                    print("3. Logout")
                    cha = input("Enter your choice: ")
                    if cha == "1":
                        view_customer_analysis()
                    elif cha == "2":
                        view_inventory_analysis()
                    elif cha == "3":
                        break
                    else:
                        print("Invalid choice! Try again.")

        elif choice == "2":
            customer_id = user_login()
            if customer_id:
                while True:
                    item_id = input("Enter the ItemID to add to cart (type 'e' to exit): ")
                    if item_id.lower() == 'e':
                        break
                    order_items(customer_id, item_id)

        elif choice == "3":
            user_register()

        elif choice == "4":
            print("You have been exited")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    mycon = connect()
    cursor = mycon.cursor()
    main()
    mycon.close()
