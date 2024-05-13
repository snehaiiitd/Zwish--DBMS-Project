USE zwish_db_test6;

-- Trigger to block a customer after three order cancellations
DELIMITER $$
CREATE TRIGGER IF NOT EXISTS BlockCustomerAfterCancellations
AFTER INSERT OR UPDATE ON OrderLogBook
FOR EACH ROW
BEGIN
    DECLARE cancellation_count INT;
    SELECT COUNT(*) INTO cancellation_count FROM OrderLogBook WHERE CustomerID = NEW.CustomerID AND Status = 'Cancelled';
    IF cancellation_count >= 3 THEN
        UPDATE Customer SET Status = 'Blocked' WHERE CustomerID = NEW.CustomerID;
    END IF;
END$$
DELIMITER ;

-- Trigger to update inventory when an order is delivered
DELIMITER $$
CREATE TRIGGER IF NOT EXISTS UpdateInventoryOnDelivery
AFTER INSERT OR UPDATE ON OrderLogBook
FOR EACH ROW
BEGIN
    DECLARE item_id CHAR(10);
    DECLARE quantity_ordered INT;
    SELECT ItemID INTO item_id FROM CartItem WHERE CustomerID = NEW.CustomerID AND Status = 'In Cart';
	UPDATE CartItem SET Status = NEW.Status WHERE CustomerID = NEW.CustomerID AND ItemID = item_id;
    UPDATE CartItem SET OrderID = NEW.OrderID WHERE CustomerID = NEW.CustomerID AND ItemID = item_id;
    
    IF NEW.Status = 'Delivered' THEN
		DELETE FROM VendorItems WHERE VendorID = NEW.VendorID AND ItemID = item_id;
	END IF;
END$$
DELIMITER ;