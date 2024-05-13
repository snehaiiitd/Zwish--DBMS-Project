from flask import Blueprint, render_template, request, redirect, url_for, flash
from .auth import cursor, mycon
# import mysql.connector
# mycon = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     passwd="rootuser",
#     database = "zwish_db_test7",
#     auth_plugin='mysql_native_password')
# cursor = mycon.cursor()

views = Blueprint('views', __name__)

@views.route('/customer-home', methods=['GET', 'POST'])
def itemlist():
    from .auth import current_user, current_user_type
    print("1:", current_user)
    cursor.execute("SELECT COUNT(*) FROM CartItem WHERE CustomerID = '{}' AND Status = 'In Cart'".format(current_user))
    item_count = int(cursor.fetchall()[0][0])

    return render_template("home.html", item_count = item_count, user_type = current_user_type)

@views.route('/add-to-cart', methods=['POST', 'GET'])
def add_to_cart():
    if request.method == 'POST':
        from .auth import current_user, current_user_type
        print("2", current_user)

        item_name = request.json.get('itemName')
        if item_name:
            query1 = "SELECT ItemID FROM Item WHERE Description = '{}'".format(item_name)
            cursor.execute(query1)

            item_id = cursor.fetchall()[0][0]

            query = "INSERT INTO CartItem (CustomerID, ItemID, Status) VALUES ('{0}', '{1}', 'In Cart')".format(current_user, item_id)
            cursor.execute(query)
            mycon.commit()

            return redirect(url_for('views.itemlist'))
    
    from .auth import current_user, current_user_type
    cursor.execute("SELECT COUNT(*) FROM CartItem WHERE CustomerID = '{}' AND Status = 'In Cart'".format(current_user))
    item_count = int(cursor.fetchall()[0][0])

    return render_template("home.html", item_count = item_count, user_type = current_user_type)


@views.route('/cart')
def viewcart():
    from .auth import current_user, current_user_type
    query = "SELECT ItemID, COUNT(*) FROM CartItem NATURAL JOIN Item WHERE CustomerID = '{}' AND Status = 'In Cart' GROUP BY ItemID".format(current_user)
    cursor.execute(query)
    items_list = cursor.fetchall()

    items_details = []
    total_sum = 0
    for items_id in items_list:
        query = "SELECT Description, Price FROM Item WHERE ItemID = '{}'".format(items_id[0])
        cursor.execute(query)
        items_list2 = cursor.fetchall()

        items_details.append([items_list2[0][0], float(items_list2[0][1]), items_id[1], float(items_list2[0][1])*int(items_id[1])])
        total_sum += items_details[-1][-1]
    
    print(items_details)

    query = "UPDATE Cart SET CurrentFinalAmount = {0} WHERE CustomerID = '{1}'".format(round(total_sum, 2), current_user)
    cursor.execute(query)
    mycon.commit()

    return render_template("cart.html", itemsDetails = items_details, totalSum = round(total_sum, 2), user_type = current_user_type)


@views.route('/checkout')
def checkout():
    from .auth import current_user, current_user_type, int_id_to_usable_id

    query = "SELECT PhoneNumber, PhysicalAddresses FROM PhoneNumbers NATURAL JOIN PhysicalAddresses WHERE CustomerID = '{}'".format(current_user)
    cursor.execute(query)
    customer_data = list(cursor.fetchone())

    query = "SELECT Full_Name, CurrentFinalAmount FROM Customer NATURAL JOIN Cart WHERE CustomerID = '{}'".format(current_user)
    cursor.execute(query)
    customer_data2 = list(cursor.fetchone())

    customer_data = customer_data2[:1] + customer_data + customer_data2[1:]

    query = "SELECT ItemID, COUNT(*) FROM CartItem WHERE CustomerID = '{}' AND Status = 'In Cart' GROUP BY ItemID".format(current_user)
    cursor.execute(query)
    cart_items = dict(cursor.fetchall())

    if cart_items == {}:
        flash("No items in Cart", category='error')
        return redirect(url_for('views.viewcart'))
    
    query = "SELECT VendorID FROM Vendor_Items"
    cursor.execute(query)
    all_vendors = cursor.fetchall()

    final_vendor_id = None

    for vendor in all_vendors:
        query = "SELECT ItemID, COUNT(*) FROM Vendor_Items WHERE VendorID = '{}' GROUP BY ItemID".format(vendor[0])
        cursor.execute(query)
        vendor_items = dict(cursor.fetchall())

        for cart_item in cart_items:
            if (cart_items[cart_item] > vendor_items.get(cart_item, 0)):
                continue
        
        query = "SELECT VendorID, Name, Location FROM Vendor WHERE VendorID = '{}'".format(vendor[0])
        cursor.execute(query)
        final_vendor_id = cursor.fetchone()
        break

    if final_vendor_id == None:
        return render_template("checkout.html", vendor=final_vendor_id, deliveryguy=None, customer_data=customer_data, user_type = current_user_type)
    
    query = "SELECT DeliveryManID, Name, PhoneNumber FROM DeliveryPartner WHERE Status = 'Available'"
    cursor.execute(query)
    deliveryguy = cursor.fetchone()

    if deliveryguy == None:
        return render_template("checkout.html", vendor=final_vendor_id, deliveryguy=deliveryguy, customer_data=customer_data, user_type = current_user_type)
    

    for cart_item in cart_items:
        query = "DELETE FROM Vendor_Items WHERE VendorID = '{0}' AND ItemID = '{1}' LIMIT {2}".format(final_vendor_id[0], cart_item, cart_items[cart_item])
        cursor.execute(query)
    

    cursor.execute("SELECT MAX(CAST(SUBSTRING(OrderID, 2) AS UNSIGNED)) FROM OrderLogBook")
    lastid = cursor.fetchone()[0]
    orderid = 'o' + int_id_to_usable_id(lastid+1)
    
    query = "INSERT INTO OrderLogBook VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, '{6}')".format(orderid, current_user, final_vendor_id[0], deliveryguy[0], customer_data[2], customer_data[1], 'Delivered')
    cursor.execute(query)
    mycon.commit()

    return render_template("checkout.html", vendor=final_vendor_id, deliveryguy=deliveryguy, customer_data=customer_data, user_type = current_user_type)

    # query = "SELECT VendorID FROM Vendor_Items WHERE ItemID = '{}'".format(cart_items[0][0])
    # cursor.execute(query)
    # suitable_vendor = cursor.fetchall()

    # for item in cart_items:
    #     query = "SELECT VendorID FROM Vendor_Items WHERE ItemID = '{}'".format(item[0])
    #     cursor.execute(query)
    #     vendor = cursor.fetchall()

@views.route('/cancel-order', methods=['GET', 'POST'])
def cancel_order():
    if request.method == 'POST':
        print(request.json.get('reason'))
        if request.json.get('reason') == '3':
            flash("Refreshed", category="success")
            return redirect(url_for('views.checkout'))

        flash("Order Cancelled", category="success")
        return redirect(url_for('views.itemlist'))
    
    return redirect(url_for('views.checkout'))


@views.route('/vendor-home', methods=['GET', 'POST'])
def vendor_itemlist():
    from .auth import current_user, current_user_type
    print("1:", current_user)
    cursor.execute("SELECT COUNT(*) FROM Vendor_Items WHERE VendorID = '{}'".format(current_user))
    item_count = int(cursor.fetchall()[0][0])

    return render_template("home_vendor.html", item_count = item_count, user_type = current_user_type)

@views.route('/add-to-inventory', methods=['POST', 'GET'])
def add_to_inventory():
    if request.method == 'POST':
        from .auth import current_user, current_user_type
        print("2", current_user)

        item_name = request.json.get('itemName')
        if item_name:
            query1 = "SELECT ItemID FROM Item WHERE Description = '{}'".format(item_name)
            cursor.execute(query1)

            item_id = cursor.fetchall()[0][0]

            query = "INSERT INTO Vendor_Items (VendorID, ItemID) VALUES ('{0}', '{1}')".format(current_user, item_id)
            cursor.execute(query)
            mycon.commit()

            return redirect(url_for('views.vendor_itemlist'))
    
    from .auth import current_user, current_user_type
    print("1:", current_user)
    cursor.execute("SELECT COUNT(*) FROM Vendor_Items WHERE VendorID = '{}'".format(current_user))
    item_count = int(cursor.fetchall()[0][0])

    return render_template("home_vendor.html", item_count = item_count, user_type = current_user_type)


@views.route('/inventory')
def viewinventory():
    from .auth import current_user, current_user_type
    query = "SELECT ItemID, COUNT(*) FROM Vendor_Items NATURAL JOIN Item WHERE VendorID = '{}' GROUP BY ItemID".format(current_user)
    cursor.execute(query)
    items_list = cursor.fetchall()

    items_details = []
    for items_id in items_list:
        query = "SELECT Description, Price FROM Item WHERE ItemID = '{}'".format(items_id[0])
        cursor.execute(query)
        items_list2 = cursor.fetchall()

        items_details.append([items_list2[0][0], float(items_list2[0][1]), items_id[1]])
    
    print(items_details)


    return render_template("inventory.html", itemsDetails = items_details, user_type = current_user_type)


# @views.route('/vendor-analysis')
# def vendor_analysis():
#     return render_template("vendor_analysis.html")

# @views.route('/customer-analysis')
# def customer_analysis():
#     return render_template("customer_analysis.html")


@views.route('/admin-home')
def admin_home():
    from .auth import current_user_type

    # Fetch customer information
    cursor.execute("SELECT CustomerID, Full_Name FROM Customer")
    customers = cursor.fetchall()

    cursor.execute("SELECT CustomerID, COUNT(*) FROM OrderLogBook GROUP BY CustomerID")
    no_of_orders = dict(cursor.fetchall())

    for i in range(len(customers)):
        customers[i] = customers[i] + (no_of_orders.get(customers[i][0], 0),)

    # Fetch vendor information
    cursor.execute("SELECT VendorID, Name FROM Vendor")
    vendors = cursor.fetchall()

    cursor.execute("SELECT VendorID, COUNT(*) FROM OrderLogBook GROUP BY VendorID")
    no_of_vendor_orders = dict(cursor.fetchall())

    for i in range(len(vendors)):
        vendors[i] = vendors[i] + (no_of_vendor_orders.get(vendors[i][0], 0),)

    cursor.execute("SELECT DeliveryManID, Name FROM DeliveryPartner")
    deliverymen = cursor.fetchall()

    cursor.execute("SELECT DeliveryManID, COUNT(*) FROM OrderLogBook GROUP BY DeliveryManID")
    no_of_delivery_orders = dict(cursor.fetchall())

    for i in range(len(deliverymen)):
        deliverymen[i] = deliverymen[i] + (no_of_delivery_orders.get(deliverymen[i][0], 0),)

    return render_template("admin_home.html", customers=customers, vendors=vendors, deliverymen=deliverymen, user_type = current_user_type)

@views.route('/delivery-man-dashboard', methods=['GET', 'POST'])
def delivery_man_dashboard():
    from .auth import current_user, current_user_type
    cursor.execute("SELECT COUNT(*) FROM OrderLogBook GROUP BY DeliveryManID HAVING DeliveryManID = '{}'".format(current_user))
    delivery_count = cursor.fetchall()

    if delivery_count == []:
        delivery_count = 0
    else:
        delivery_count = delivery_count[0][0]

    if request.method == 'POST':
        status = request.json.get('status')
        print(current_user)

        query = "UPDATE DeliveryPartner SET Status = '{0}' WHERE DeliveryManID = '{1}'".format(status, current_user)
        cursor.execute(query)
        mycon.commit()

    return render_template("deliveryman_home.html", delivery_count=delivery_count, user_type = current_user_type)

# @views.route('/update-availability', methods=['GET', 'POST'])
# def update_availability():
#     if request.method == 'POST':
#         from .auth import current_user, current_user_type
#         status = request.json.get('status')
#         print(current_user)

#         query = "UPDATE DeliveryPartner SET Status = '{0}' WHERE DeliveryManID = '{1}'".format(status, current_user)
#         cursor.execute(query)
#         mycon.commit()

#         return redirect(url_for('/delivery-man-dashboard'))

#     from .auth import current_user, current_user_type
#     cursor.execute("SELECT COUNT(*) FROM OrderLogBook GROUP BY DeliveryManID HAVING DeliveryManID = '{}'".format(current_user))
#     delivery_count = cursor.fetchall()

#     if delivery_count == []:
#         delivery_count = 0
#     else:
#         delivery_count = delivery_count[0][0]
    
#     return render_template("deliveryman_home.html", delivery_count=delivery_count, user_type = current_user_type)