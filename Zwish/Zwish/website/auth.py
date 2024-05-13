from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .views import cursor, mycon
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector


mycon = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="rootuser",
    database = "zwish_db_test7",
    auth_plugin='mysql_native_password')
cursor = mycon.cursor()

auth = Blueprint('auth', __name__)
current_user = None
current_user_type = None
customer_no = 1
admin_no = 1
vendor_no = 1
delivery_man_no = 1
password_db = []

def int_id_to_usable_id(id):
    id_length = len(str(id))
    return "0"*(4-id_length) + str(id)

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    global current_user_type
    global password_db

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT Password, CustomerID FROM Customer WHERE Email = '{}'".format(email)
        cursor.execute(query)
        password_db = cursor.fetchall()
        print(password_db)

        if password_db == []:
            flash('Account with this email doesn\'t exist', category='error')
        elif not check_password_hash(password_db[0][0], password):
            flash('Incorrect Password', category='error')
        else:
            current_user = password_db[0][1]
            current_user_type = 'customer'
            print(current_user)

            flash('Logged In successfully!', category='success')

            return redirect(url_for('views.itemlist'))

    return render_template("login.html", user_type = current_user_type)


@auth.route('/logout')
def logout():
    global current_user_type
    current_user_type = None
    return redirect(url_for('auth.login'))


@auth.route('/login-vendor', methods=['GET', 'POST'])
def login_vendor():
    global current_user
    global current_user_type
    global password_db

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT Password, VendorID FROM Vendor WHERE Email = '{}'".format(email)
        cursor.execute(query)
        password_db = cursor.fetchall()
        print(password_db)

        if password_db == []:
            flash('Account with this email doesn\'t exist', category='error')
        elif not check_password_hash(password_db[0][0], password):
            flash('Incorrect Password', category='error')
        else:
            current_user = password_db[0][1]
            current_user_type = 'vendor'
            print(current_user)

            flash('Logged In successfully!', category='success')

            return redirect(url_for('views.vendor_itemlist'))

    return render_template("login_vendor.html", user_type = current_user_type)


@auth.route('/login-deliveryman', methods=['GET', 'POST'])
def login_deliveryman():
    global current_user
    global current_user_type
    global password_db

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT Password, DeliveryManID FROM DeliveryPartner WHERE DrivingLicenseNumber = '{}'".format(email)
        cursor.execute(query)
        password_db = cursor.fetchall()
        print(password_db)

        if password_db == []:
            flash('Account with this email doesn\'t exist', category='error')
        elif not check_password_hash(password_db[0][0], password):
            flash('Incorrect Password', category='error')
        else:
            current_user = password_db[0][1]
            current_user_type = 'deliveryman'
            print(current_user)

            flash('Logged In successfully!', category='success')

            return redirect(url_for('views.delivery_man_dashboard'))

    return render_template("login_deliveryman.html", user_type = current_user_type)


@auth.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    global current_user
    global current_user_type
    global password_db

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = "SELECT Password, AdminID FROM Admin WHERE Email = '{}'".format(email)
        cursor.execute(query)
        password_db = cursor.fetchall()
        print(password_db)

        if password_db == []:
            flash('Account with this email doesn\'t exist', category='error')
        elif not check_password_hash(password_db[0][0], password):
            flash('Incorrect Password', category='error')
        else:
            current_user = password_db[0][1]
            current_user_type = 'admin'
            print(current_user)

            flash('Logged In successfully!', category='success')

            return redirect(url_for('views.admin_home'))

    return render_template("login_admin.html", user_type = current_user_type)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    global customer_no

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        dob = request.form.get('DOB')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len("".join(phoneNumber.split())) != 10:
            flash('Phone Number must be of length 10', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            cursor.execute("SELECT MAX(CAST(SUBSTRING(CustomerID, 2) AS UNSIGNED)) FROM Customer")
            lastid = cursor.fetchone()[0]

            customer_no = max(customer_no, lastid)
            customer_no += 1

            query = "INSERT INTO Customer (CustomerID, Full_Name, Email, DOB, Status, Password) VALUES ('C{0}', '{1}', '{2}', '{3}', 'Active', '{4}')".format(int_id_to_usable_id(customer_no), firstName, email, dob, generate_password_hash(password1, method='sha256'))
            cursor.execute(query)

            query2 = "INSERT INTO PhoneNumbers (CustomerID, PhoneNumber) VALUES ('C{0}', {1})".format(int_id_to_usable_id(customer_no), phoneNumber)
            cursor.execute(query2)

            query3 = "INSERT INTO Cart (CustomerID, CurrentFinalAmount) VALUES ('C{0}', 0)".format(int_id_to_usable_id(customer_no))
            cursor.execute(query3)

            query4 = "INSERT INTO PhysicalAddresses (CustomerID, PhysicalAddresses) VALUES ('C{0}', '{1}')".format(int_id_to_usable_id(customer_no), address)
            cursor.execute(query4)
            mycon.commit()

            print(query)
            print(query2)
            print(len(generate_password_hash(password1, method='sha256')))

            flash('Account created!', category='success')

            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user_type = current_user_type)


@auth.route('/delivery-man-sign-up', methods=['GET', 'POST'])
def delivery_man_sign_up():
    global delivery_man_no

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phoneNumber = request.form.get('phoneNumber')
        dob = request.form.get('DOB')
        age = request.form.get('age')
        licenseNumber = request.form.get('licenseNumber')
        address = request.form.get('address')
        vehicleOwned = request.form.get('vehicleOwned')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Perform validation checks
        if len(name) < 2:
            flash('Name must be greater than 1 character', category='error')
        elif len("".join(phoneNumber.split())) != 10:
            flash('Phone Number must be of length 10', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            cursor.execute("SELECT MAX(CAST(SUBSTRING(DeliveryManID, 2) AS UNSIGNED)) FROM DeliveryPartner")
            lastid_deliveryman = cursor.fetchone()[0]

            delivery_man_no = max(delivery_man_no, lastid_deliveryman)
            delivery_man_no += 1

            query = "INSERT INTO DeliveryPartner (DeliveryManID, Name, PhoneNumber, DOB, Age, PhysicalAddresses, DrivingLicenseNumber, VehicleOwned, Password) VALUES ('D{0}', '{1}', '{2}', '{3}', '{4}', '{5}' , '{6}' , '{7}' , '{8}')".format(int_id_to_usable_id(delivery_man_no), name, phoneNumber, dob, age, address, licenseNumber, vehicleOwned, generate_password_hash(password1, method='sha256'))
            cursor.execute(query)
            mycon.commit()

            print(query)
            print(len(generate_password_hash(password1, method='sha256')))
            flash('Delivery man account created!', category='success')
            return redirect(url_for('auth.login_deliveryman'))

    return render_template("signup_deliveryman.html", user_type = current_user_type)


@auth.route('/admin-sign-up', methods=['GET', 'POST'])
def admin_sign_up():
    global admin_no

    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Perform validation checks
        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            cursor.execute("SELECT MAX(CAST(SUBSTRING(AdminID, 2) AS UNSIGNED)) FROM Admin")
            lastid_admin = cursor.fetchone()[0]

            admin_no = max(admin_no, lastid_admin)
            admin_no += 1

            # print(len(generate_password_hash(password1, method='sha256')))

            query = "INSERT INTO Admin (AdminID, Password, Email) VALUES ('A{0}', '{1}', '{2}')".format(int_id_to_usable_id(admin_no), generate_password_hash(password1, method='sha256'), email)
            cursor.execute(query)
            mycon.commit()

            print(query)
            print(len(generate_password_hash(password1, method='sha256')))
            flash('Admin account created!', category='success')
            return redirect(url_for('auth.login_admin'))

    return render_template("signup_admin.html", user_type = current_user_type)

@auth.route('/vendor-sign-up', methods=['GET', 'POST'])
def vendor_sign_up():
    global vendor_no

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phoneNumber = request.form.get('phoneNumber')
        email = request.form.get('email')
        location = request.form.get('location')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Perform validation checks
        if len(name) < 2:
            flash('Name must be greater than 1 character', category='error')
        elif len("".join(phoneNumber.split())) != 10:
            flash('Phone Number must be of length 10', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            cursor.execute("SELECT MAX(CAST(SUBSTRING(VendorID, 2) AS UNSIGNED)) FROM Vendor")
            lastid_vendor = cursor.fetchone()[0]

            vendor_no = max(vendor_no, lastid_vendor)
            vendor_no += 1

            query = "INSERT INTO Vendor (VendorID, Name, PhoneNumber, Email, Location, Password) VALUES ('V{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(int_id_to_usable_id(vendor_no), name, phoneNumber, email, location, generate_password_hash(password1, method='sha256'))
            cursor.execute(query)

            mycon.commit()

            print(query)
            print(len(generate_password_hash(password1, method='sha256')))
            flash('Vendor account created!', category='success')
            return redirect(url_for('auth.login_vendor'))

    return render_template("signup_vendor.html", user_type = current_user_type)
