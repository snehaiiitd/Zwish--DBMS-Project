DROP DATABASE IF EXISTS zwish_db_test6;
CREATE DATABASE IF NOT EXISTS zwish_db_test6;
USE zwish_db_test6;

CREATE TABLE IF NOT EXISTS Customer
	(CustomerID CHAR(10) NOT NULL PRIMARY KEY,
	 Full_Name varchar(50),
	 Email varchar(50),
	 DOB date,
	 PaymentDetails varchar(250),
	 Status VARCHAR(50),
	 Age INT GENERATED ALWAYS AS (2024 - YEAR(dob)) STORED);
-- All the functions that return the Current Date and Time aren't working

CREATE TABLE IF NOT EXISTS PhysicalAddresses
	(CustomerID CHAR(10) NOT NULL,
    PhysicalAddresses varchar(250),
    FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID));

CREATE TABLE IF NOT EXISTS PhoneNumbers
	(CustomerID CHAR(10) NOT NULL,
    PhoneNumber BIGINT NOT NULL,
    FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID));
	 
CREATE TABLE IF NOT EXISTS Item
	(ItemID CHAR(10) NOT NULL PRIMARY KEY,
	 Name varchar(50),
	 Weight decimal(6,2),
	 Price decimal(12,4) NOT NULL,
	 Description varchar(250));

CREATE TABLE IF NOT EXISTS Vendor
	(VendorID CHAR(10) NOT NULL PRIMARY KEY,
	 Name varchar(50),
	 PhoneNumber BIGINT,
	 Email varchar(50),
	 Location varchar(250) NOT NULL);

CREATE TABLE IF NOT EXISTS Vendor_Items
	(VendorID CHAR(10) NOT NULL,
	 ItemID CHAR(10) NOT NULL,
	 FOREIGN KEY(VendorID) REFERENCES Vendor(VendorID),
	 FOREIGN KEY(ItemID) REFERENCES Item(ItemID));

CREATE TABLE IF NOT EXISTS DeliveryPartner
	(DeliveryManID CHAR(10) NOT NULL PRIMARY KEY,
	 Name varchar(50),
	 PhoneNumber BIGINT,
	 DOB date,
	 Age INT,
	 PhysicalAddresses varchar(250),
	 DrivingLicenseNumber char(16),
	 VehicleOwned varchar(50));

CREATE TABLE IF NOT EXISTS Admin
	(AdminID CHAR(10) NOT NULL PRIMARY KEY,
	 Password varchar(50),
	 Email varchar(50));

CREATE TABLE IF NOT EXISTS OrderLogBook
	(OrderID CHAR(10) NOT NULL PRIMARY KEY,
	 CustomerID CHAR(10) NOT NULL,
	 VendorID CHAR(10) NOT NULL,
	 DeliveryManID CHAR(10) NOT NULL,
	 FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
	 FOREIGN KEY(VendorID) REFERENCES Vendor(VendorID),
	 FOREIGN KEY(DeliveryManID) REFERENCES DeliveryPartner(DeliveryManID),
	 DeliveryAddress varchar(250),
	 DeliveryPhoneNumber BIGINT,
	 Status varchar(10));

CREATE TABLE IF NOT EXISTS Cart
	(CustomerID CHAR(10) NOT NULL,
	 FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
	 CouponApplied varchar(20),
	 CurrentFinalAmount decimal(12,4));
     
CREATE TABLE IF NOT EXISTS CartItem
	(CustomerID CHAR(10) NOT NULL,
    ItemID CHAR(10) NOT NULL,
    OrderID CHAR(10),
    FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY(OrderID) REFERENCES OrderLogBook(OrderID),
    Status VARCHAR(20));
    
CREATE TABLE IF NOT EXISTS Review
	(OrderID CHAR(10) NOT NULL PRIMARY KEY,
	 CustomerID CHAR(10) NOT NULL,
	 FOREIGN KEY(OrderID) REFERENCES OrderLogBook(OrderID),
     FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
	 Stars tinyint,
	 Content varchar(100),
	 DateTime datetime);

CREATE TABLE IF NOT EXISTS Refund
	(OrderID CHAR(10) NOT NULL,
	 CustomerID CHAR(10) NOT NULL,
	 AdminID CHAR(10) NOT NULL,
	 FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
	 FOREIGN KEY(OrderID) REFERENCES OrderLogBook(OrderID),
	 FOREIGN KEY(AdminID) REFERENCES Admin(AdminID),
	 Amount decimal(12,4),
	 Reason varchar(250));

INSERT INTO Customer (CustomerID, Full_Name, Email, DOB, PaymentDetails, Status) VALUES
('C1', 'John Doe', 'john@email.com', '1980-01-01', '6543 2109 8765 4321', 'Active'),
('C2', 'Jane Doe', 'jane@email.com', '1985-03-15', '1234 5678 9012 3457','Active'),
('C3', 'Bob Smith', 'bob@email.com', '1990-05-20', '1234 5678 9012 3458','Active'),
('C4', 'Susan Johnson', 'susan@email.com', '1995-07-10', '1234 5678 9012 3459','Active'),
('C5', 'Mike Wilson', 'mike@email.com', '1988-09-02', '1234 5678 9012 3460','Active'),
('C6', 'Jessica Lee', 'jessica@email.com', '1993-12-25', '1234 5678 9012 3461','Active'),
('C7', 'Chris Brown', 'chris@email.com', '1989-04-07', '1234 5678 9012 3462','Active'),
('C8', 'Amanda Clark', 'amanda@email.com', '1991-08-19', '1234 5678 9012 3463','Active'),
('C9', 'Ryan Hall', 'ryan@email.com', '1982-11-12', '1234 5678 9012 3464','Active'),
('C10', 'Samantha Moore', 'samantha@email.com', '1994-10-31', '1234 5678 9012 3465','Active');

INSERT INTO PhoneNumbers (CustomerID, PhoneNumber) VALUES 
('C1', 1234567890),
('C2', 9087654321),
('C3', 1112223333),
('C4', 4445556666),
('C5', 7776665555),
('C6', 3331119999),
('C7', 2223334444),
('C8', 5554447777),
('C9', 6668889999),
('C10', 1112224444);

INSERT INTO Vendor (VendorID, Name, PhoneNumber, Email, Location)
VALUES
('V1', 'Vendor 1', 1234567890, 'vendor1@email.com', 'New York, NY'),
('V2', 'Vendor 2', 9087654321, 'vendor2@email.com', 'Los Angeles, CA'),
('V3', 'Vendor 3', 1112223333, 'vendor3@email.com', 'Chicago, IL'),
('V4', 'Vendor 4', 4445556666, 'vendor4@email.com', 'Houston, TX'),
('V5', 'Vendor 5', 7776665555, 'vendor5@email.com', 'Phoenix, AZ'),
('V6', 'Vendor 6', 3331119999, 'vendor6@email.com', 'San Diego, CA'),
('V7', 'Vendor 7', 2223334444, 'vendor7@email.com', 'Dallas, TX'),
('V8', 'Vendor 8', 5554447777, 'vendor8@email.com', 'Seattle, WA'),
('V9', 'Vendor 9', 6668889999, 'vendor9@email.com', 'Denver, CO'), 
('V10', 'Vendor 10', 1112224444, 'vendor10@email.com', 'Miami, FL');

INSERT INTO Item (ItemID, Name, Weight, Price, Description)
VALUES 
('I101', 'Item 1', 10.5, 9.99, 'Description for item 1'),
('I102', 'Item 2', 5.5, 14.99, 'Description for item 2'),
('I103', 'Item 3', 8, 19.99, 'Description for item 3'),  
('I104', 'Item 4', 15, 24.99, 'Description for item 4'),
('I105', 'Item 5', 12, 29.99, 'Description for item 5'),
('I106', 'Item 6', 4, 39.99, 'Description for item 6'),
('I107', 'Item 7', 2.5, 49.99, 'Description for item 7'),
('I108', 'Item 8', 1, 59.99, 'Description for item 8'),
('I109', 'Item 9', 3, 69.99, 'Description for item 9'),
('I110', 'Item 10', 20, 79.99, 'Description for item 10');

INSERT INTO Vendor_Items (VendorID, ItemID) VALUES
('V1', 'I101'),
('V1', 'I102'),
('V2', 'I103'),
('V2', 'I104'),
('V3', 'I105'),
('V3', 'I106'),
('V4', 'I107'),
('V4', 'I108'),
('V5', 'I109'),
('V5', 'I110');

INSERT INTO DeliveryPartner (DeliveryManID, Name, PhoneNumber, DOB, Age, PhysicalAddresses, DrivingLicenseNumber, VehicleOwned)
VALUES
('D1', 'John Smith', 1234567890, '1980-05-06', 40, '111 Delivery Lane, New York, NY', 'DL1234', 'Truck'),
('D2', 'Mike Jones', 0987654321, '1990-09-15', 30, '222 Delivery Blvd, Los Angeles, CA', 'DL2345', 'Van'),  
('D3', 'Dave Wilson', 1112223333, '1985-12-25', 35, '333 Delivery Ave, Chicago, IL', 'DL3456', 'Bike'),
('D4', 'Henry Ford', 4445556666, '1995-03-17', 25, '444 Delivery St, Houston, TX', 'DL4567', 'Car'),
('D5', 'Bob Hope', 7776665555, '1992-07-08', 28, '555 Delivery Rd, Phoenix, AZ', 'DL5678', 'Motorcycle'),
('D6', 'Tom Cruise', 3331119999, '1988-01-20', 33, '666 Delivery Dr, San Diego, CA', 'DL6789', 'Truck'),
('D7', 'Brad Pitt', 2223334444, '1991-11-12', 29, '777 Delivery Ct, Dallas, TX', 'DL7890', 'Van'),
('D8', 'Will Smith', 5554447777, '1989-05-23', 31, '888 Delivery Way, Seattle, WA', 'DL8901', 'Bike'),  
('D9', 'Johnny Depp', 6668889999, '1994-08-30', 26, '999 Delivery Ln, Denver, CO', 'DL9012', 'Car'),
('D10', 'Robert Downey', 1112224444, '1997-10-10', 22, '123 Delivery View, Miami, FL', 'DL0123', 'Motorcycle');

INSERT INTO Admin (AdminID, Password, Email)
VALUES  
('A1', 'admin123', 'admin1@email.com'),
('A2', 'admin234', 'admin2@email.com'),
('A3', 'admin345', 'admin3@email.com'),
('A4', 'admin456', 'admin4@email.com'),  
('A5', 'admin567', 'admin5@email.com'),
('A6', 'admin678', 'admin6@email.com'),
('A7', 'admin789', 'admin7@email.com'),
('A8', 'admin890', 'admin8@email.com'),
('A9', 'admin901', 'admin9@email.com'),
('A10', 'admin012', 'admin10@email.com');

INSERT INTO OrderLogBook (OrderID, CustomerID, VendorID, DeliveryManID, DeliveryAddress, DeliveryPhoneNumber, Status)
VALUES
('o1', 'C1', 'V1', 'D1', '123 Main St, New York, NY', 1234567890, 'Delivered'),
('o2', 'C2', 'V2', 'D2', '456 Park Ave, New York, NY', 0987654321, 'Delivered'),
('o3', 'C3', 'V3', 'D3', '789 Elm St, Chicago, IL', 1112223333, 'Delivered'),
('o4', 'C4', 'V4', 'D4', '246 Oak Rd, Los Angeles, CA', 4445556666, 'Delivered'), 
('o5', 'C5', 'V5', 'D5', '135 Pine St, Houston, TX', 7776665555, 'Cancelled'),
('o6', 'C6', 'V6', 'D6', '951 Cedar Dr, Dallas, TX', 3331119999, 'Delivered'),
('o7', 'C7', 'V7', 'D7', '522 Elm St, Phoenix, AZ', 2223334444, 'Delivered'),
('o8', 'C8', 'V8', 'D8', '743 Oak Ln, San Diego, CA', 5554447777, 'Delivered'),
('o9', 'C9', 'V9', 'D9', '159 Birch Rd, Denver, CO', 6668889999, 'Cancelled'),
('o10', 'C10', 'V10', 'D10', '357 Park St, Seattle, WA', 1112224444,'Delivered');

INSERT INTO Cart (CustomerID, CouponApplied, CurrentFinalAmount)
VALUES
('C1', '10OFF', 89.91),
('C2', '20OFF', 119.99),
('C3', NULL, 19.99),
('C4', '5OFF', 23.74),
('C5', NULL, 29.99),
('C6', '10OFF', 35.99),
('C7', '20OFF', 39.99),
('C8', NULL, 59.99),
('C9', '5OFF', 66.49),
('C10', '10OFF', 71.99);

INSERT INTO CartItem (CustomerID, ItemID, Status) VALUES
('C1', 'I101', 'Delivered'),
('C1', 'I102', 'In Cart'),
('C2', 'I103', 'Delivered'),
('C2', 'I104', 'In Cart'),
('C3', 'I105', 'Delivered'),
('C3', 'I106', 'In Cart'),
('C4', 'I107', 'Delivered'),
('C4', 'I108', 'In Cart'),
('C5', 'I109', 'Delivered'),
('C5', 'I110', 'Cancelled'),
('C6', 'I101', 'Delivered'),
('C7', 'I102', 'Delivered'),
('C8', 'I103', 'Delivered'),
('C9', 'I104', 'Cancelled'),
('C10', 'I105','Cancelled'),
('C6', 'I106','In Cart'),
('C7', 'I107','Delivered'),
('C8', 'I108','Cancelled'),
('C9', 'I109','Cancelled'),
('C10', 'I110','Delivered');

INSERT INTO Review (OrderID, CustomerID, Stars, Content, DateTime)
VALUES
('o1', 'C1', 5, 'Great service!', '2023-02-10 10:23:54'), 
('o2', 'C2', 4, 'Pretty good overall.', '2023-02-11 12:45:32'),
('o3', 'C3', 3, 'Delivery was late but product was fine.', '2023-02-12 16:18:46'),
('o4', 'C4', 5, 'Arrived on time, very happy!', '2023-02-13 09:30:12'),
('o5', 'C5', 1, 'Terrible experience, order never arrived.', '2023-02-14 14:50:52'),
('o6', 'C6', 4, 'Minor issue but they handled it well.', '2023-02-15 08:40:24'),
('o7', 'C7', 5, 'Fast shipping, great condition.', '2023-02-16 11:12:56'),
('o8', 'C8', 2, 'Item was damaged, sad about that.', '2023-02-17 18:34:21'),
('o9', 'C9', 1, 'Complete disappointment, do not recommend.', '2023-02-18 13:24:35'), 
('o10', 'C10', 4, 'Pretty good but not the fastest shipping.', '2023-02-19 16:51:07');

INSERT INTO Refund (OrderID, CustomerID, AdminID, Amount, Reason)
VALUES
('o5', 'C5', 'A1', 29.99, 'Order never arrived'),
('o9', 'C9', 'A2', 66.49, 'Item arrived damaged'), 
('o3', 'C3', 'A3', 5, 'Delivery was late'),
('o8', 'C8', 'A4', 15, 'Item was incorrect'),
('o10', 'C10', 'A5', 10, 'Shipping costs were incorrect'),
('o2', 'C2', 'A1', 20, 'Wrong item shipped'),
('o4', 'C4', 'A2', 5, 'Item damaged during shipping'),
('o6', 'C6', 'A3', 12.99, 'Item missing from order'),  
('o7', 'C7', 'A4', 50, 'Unauthorized purchase'),
('o1', 'C1', 'A5', 25, 'Customer changed mind on purchase');