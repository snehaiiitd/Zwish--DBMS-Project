from auth import cursor, current_user, password_db

cursor.execute("SELECT COUNT(*) FROM OrderLogBook GROUP BY DeliveryManID HAVING DeliveryManID = '{}'".format('D1000'))
delivery_count = cursor.fetchone()

print(delivery_count)
print((1,) + (2,))