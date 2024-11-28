--Stored Procedure 1

-- Create the stored procedure
CREATE PROCEDURE GetProductStock
    @ProductID INT,
    @StockCount INT OUTPUT
AS
BEGIN
    SELECT @StockCount = Quantity
    FROM Inventory
    WHERE ProductID = @ProductID;
END;
GO -- Add GO to signal the end of the procedure creation

-- Declare the output variable
DECLARE @StockCount INT;

-- Execute the stored procedure
EXEC GetProductStock 
    @ProductID = 1,        -- Input parameter
    @StockCount = @StockCount OUTPUT; -- Output parameter

-- Display the output value
SELECT @StockCount AS StockCount;






--Stored Procedure 2

SELECT * FROM Shipment
CREATE PROCEDURE UpdateShipmentStatus
    @ShipmentID INT,
    @NewStatus VARCHAR(50),  -- The new status to set
    @OldStatus VARCHAR(50) OUTPUT  -- Output the old status
AS
BEGIN
    -- Retrieve the current status of the shipment before updating
    SELECT @OldStatus = Status
    FROM Shipment
    WHERE ShipmentID = @ShipmentID;

    -- Update the status of the shipment
    UPDATE Shipment
    SET Status = @NewStatus
    WHERE ShipmentID = @ShipmentID;

    -- Optionally, you can return the old and new status as output
    -- SELECT @OldStatus AS OldStatus, @NewStatus AS NewStatus;
END;
-- Declare a variable to hold the old status
DECLARE @OldStatus VARCHAR(50);

-- Execute the stored procedure
EXEC UpdateShipmentStatus
    @ShipmentID = 1,              -- The ID of the shipment you want to update
    @NewStatus = 'Pending',     -- The new status to set
    @OldStatus = @OldStatus OUTPUT;  -- Output parameter for the old status

-- Display the old status after execution
SELECT @OldStatus AS OldStatus;








--Stored Procedure 3

-- Stored Procedure to Update Warehouse Capacity and Calculate Total Capacity
SELECT * FROM Warehouse
CREATE PROCEDURE UpdateWarehouseAndCalculateTotal
    @WarehouseName VARCHAR(100),
    @NewCapacity VARCHAR(50)  -- New capacity to update for the given warehouse
AS
BEGIN
    -- Task 1: Update the warehouse capacity
    UPDATE Warehouse
    SET Capacity = @NewCapacity
    WHERE Name = @WarehouseName;

    -- Task 2: Calculate and display the total capacity of all warehouses
    DECLARE @TotalCapacity INT;

    -- Convert capacity to integer for calculation (remove 'kg' and cast to INT)
    SELECT @TotalCapacity = SUM(CAST(REPLACE(Capacity, 'kg', '') AS INT))
    FROM Warehouse;

    -- Display the total capacity
    SELECT @TotalCapacity AS TotalWarehouseCapacity;

    -- Optionally, display the updated warehouse details
    SELECT * FROM Warehouse WHERE Name = @WarehouseName;
END;
GO

-- Execute the stored procedure
EXEC UpdateWarehouseAndCalculateTotal 
    @WarehouseName = 'Main Warehouse',   -- Warehouse name to update
    @NewCapacity = '57000kg';            -- New capacity to set for 'Main Warehouse'




--View 1
SELECT * FROM Supplier
CREATE VIEW SupplierMaterialReportView AS
SELECT s.Name AS SupplierName, m.Name AS MaterialName, sr.SupplyDate
FROM Supplier s
JOIN SupplyReport sr ON s.SupplierID = sr.SupplierID
JOIN Material m ON sr.MaterialID = m.MaterialID;

SELECT * FROM SupplierMaterialReportView;

--View 2
CREATE VIEW InventoryReportView AS
SELECT p.Name AS ProductName, i.Quantity, w.Name AS WarehouseName, i.ExpiryDate
FROM Inventory i
JOIN Product p ON i.ProductID = p.ProductID
JOIN Warehouse w ON i.WarehouseID = w.WarehouseID;

SELECT * FROM InventoryReportView;

--View 3
CREATE VIEW ProductExpiryReportView AS
SELECT p.Name AS ProductName, i.ExpiryDate
FROM Product p
JOIN Inventory i ON p.ProductID = i.ProductID
WHERE i.ExpiryDate < GETDATE();

SELECT * FROM ProductExpiryReportView;




--UDF 1

-- Function to Calculate Product Price after Discount
SELECT * FROM PRODUCT
CREATE FUNCTION CalculateFinalPrice(
    @productID INT,              -- Input parameter for the product ID
    @discountRate DECIMAL(5,2)   -- Input parameter for the discount rate (as percentage)
)
RETURNS DECIMAL(10,2)          -- Return type for the final price after discount
AS
BEGIN
    DECLARE @originalPrice DECIMAL(10,2);   -- Variable to store the original price of the product
    DECLARE @discountAmount DECIMAL(10,2);  -- Variable to store the discount amount
    DECLARE @finalPrice DECIMAL(10,2);      -- Variable to store the final price after discount

    -- Get the original price from the Product table based on the product ID
    SELECT @originalPrice = Price
    FROM Product
    WHERE ProductID = @productID;

    -- Calculate the discount amount
    SET @discountAmount = (@originalPrice * @discountRate) / 100;

    -- Calculate the final price after applying the discount
    SET @finalPrice = @originalPrice - @discountAmount;

    -- Return the final price
    RETURN @finalPrice;
END;

-- Example of executing the function with input parameters
SELECT dbo.CalculateFinalPrice(1, 10.00) AS FinalPrice;



--UDF 2

-- Function to Get Product Category
CREATE FUNCTION GetProductCategory(
@productID INT
) 
RETURNS VARCHAR(50)
BEGIN
    DECLARE @category VARCHAR(50);
    SELECT @category = Type FROM Product WHERE ProductID = productID;
    RETURN @category;
END;

SELECT dbo.GetProductCategory(1) AS Category;



--UDF 3

-- Function to Check Material Availability
CREATE FUNCTION CheckMaterialAvailability(
    @productID INT
)
RETURNS VARCHAR(50)
AS
BEGIN
    DECLARE @status VARCHAR(50);
    
    -- Check if the product quantity is greater than 0
    IF (SELECT Quantity FROM Inventory WHERE ProductID = @productID) > 0
    BEGIN
        SET @status = 'Available';
    END
    ELSE
    BEGIN
        SET @status = 'Out of Stock';
    END
    
    -- Return the status
    RETURN @status;
END;

SELECT dbo.CheckMaterialAvailability(1) AS Availability;







--Trigger

CREATE TABLE ProductChangeHistory (
    ChangeID INT IDENTITY(1,1) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,           -- Change to VARCHAR for storing product name
    OldPrice DECIMAL(10,2) NULL,          -- Use DECIMAL for prices
    NewPrice DECIMAL(10,2) NOT NULL,
    ChangeDate DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TRIGGER PriceChange
ON Product
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Insert into auditing table only if the Price column is updated
    IF (UPDATE(Price))
    BEGIN
        INSERT INTO ProductChangeHistory (Name, OldPrice, NewPrice, ChangeDate)
        SELECT 
            d.Name,
            d.Price AS OldPrice,
            i.Price AS NewPrice,
            GETDATE() AS ChangeDate
        FROM 
            deleted d
        INNER JOIN 
            inserted i ON d.ProductID = i.ProductID    -- Join on ProductID for accurate mapping
        WHERE 
            d.Price <> i.Price;  -- Ensure it's an actual change in price
    END
END;

-- Example Update operation that will trigger the PriceChange trigger
UPDATE Product
SET Price = 3.50
WHERE Name = 'Tomato Pack';

-- Verify the auditing table
SELECT * FROM ProductChangeHistory;

SELECT * FROM Product;






