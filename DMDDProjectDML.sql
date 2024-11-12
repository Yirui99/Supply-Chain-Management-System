-- Insert Address Data
INSERT INTO Address (Street, City, State, PostalCode, Country, AddressType) VALUES
('123 Weld St', 'Los Angeles', 'California', '90001', 'USA', 'Supplier'),
('456 Walnut Ave', 'San Francisco', 'California', '94105', 'USA', 'Distributor'),
('789 Roxbury Blvd', 'Dallas', 'Texas', '75001', 'USA', 'Manufacturer'),
('101 Tremont Rd', 'New York', 'New York', '10001', 'USA', 'Retailer'),
('202 JP St', 'Chicago', 'Illinois', '60007', 'USA', 'User'),
('303 Kings Lane', 'Miami', 'Florida', '33101', 'USA', 'Supplier'),
('404 Jackson Blvd', 'Houston', 'Texas', '77001', 'USA', 'Distributor'),
('505 Ruggles Ave', 'Phoenix', 'Arizona', '85001', 'USA', 'Manufacturer'),
('606 Bray Lane', 'Boston', 'Massachusetts', '02110', 'USA', 'Retailer'),
('707 Cedar Rd', 'Seattle', 'Washington', '98101', 'USA', 'User');

-- Insert Supplier Data
INSERT INTO Supplier (Name, PhoneNumber, Email, AddressID) VALUES
('ABC Fresh Produce', '555-1234', 'abc@fresh.com', 1),
('XYZ Farm Goods', '555-5678', 'xyz@farm.com', 3),
('Fresh Greens Co', '555-8765', 'greens@co.com', 6),
('Eco Supply Ltd', '555-4321', 'eco@eco.com', 10),
('Sunshine Foods', '555-2468', 'sunshine@foods.com', 2),
('Green Valley Organics', '555-1357', 'green@valley.com', 7),
('Farm Fresh Supplies', '555-9876', 'farm@fresh.com', 9),
('Prime Produce Ltd', '555-6543', 'prime@produce.com', 8),
('Natures Bounty', '555-3210', 'nature@bounty.com', 5),
('Healthy Harvest', '555-7410', 'healthy@harvest.com', 4);

-- Insert Material Data
INSERT INTO Material (Name, Type, SupplierID) VALUES
('Tomatoes', 'Raw', 1),
('Cucumbers', 'Raw', 2),
('Lettuce', 'Raw', 3),
('Carrots', 'Raw', 4),
('Apples', 'Processed', 5),
('Oranges', 'Processed', 6),
('Pineapple', 'Processed', 7),
('Potatoes', 'Raw', 8),
('Strawberries', 'Raw', 9),
('Spinach', 'Raw', 10);

-- Insert SupplyReport Data
INSERT INTO SupplyReport (SupplierID, MaterialID, SupplyDate) VALUES
(1, 1, '2024-11-01'),
(2, 2, '2024-11-03'),
(3, 3, '2024-11-05'),
(4, 4, '2024-11-07'),
(5, 5, '2024-11-09'),
(6, 6, '2024-11-10'),
(7, 7, '2024-11-12'),
(8, 8, '2024-11-14'),
(9, 9, '2024-11-15'),
(10, 10, '2024-11-17');

-- Insert Manufacturer Data
INSERT INTO Manufacturer (Name, PhoneNumber, Email, AddressID) VALUES
('FreshPack Ltd', '555-2468', 'fresh@pack.com', 3),
('EcoTech Manufacturers', '555-8520', 'eco@tech.com', 5),
('GreenLeaf Co', '555-1530', 'green@leaf.com', 7),
('Fresh Produce Inc', '555-4569', 'fresh@produce.com', 9),
('Prime Goods Ltd', '555-6789', 'prime@goods.com', 8),
('Healthy Pack Ltd', '555-9871', 'healthy@pack.com', 6),
('Global Foods', '555-4325', 'global@foods.com', 4),
('Bountiful Harvest', '555-3512', 'bountiful@harvest.com', 2),
('GreenFields Corp', '555-1245', 'fields@green.com', 10),
('NaturePack Ltd', '555-7531', 'nature@pack.com', 1);

-- Insert MaterialDocument Data
INSERT INTO MaterialDocument (MaterialID, ManufacturerID, Description, CreatedDate) VALUES
(1, 1, 'Packaging for Tomato Supply', '2024-11-01'),
(2, 2, 'Cucumber Delivery Instructions', '2024-11-02'),
(3, 3, 'Lettuce Harvest Guidelines', '2024-11-03'),
(4, 4, 'Carrot Packing Specifications', '2024-11-04'),
(5, 5, 'Processed Apple Quality Checks', '2024-11-05'),
(6, 6, 'Orange Handling Procedures', '2024-11-06'),
(7, 7, 'Pineapple Export Documentation', '2024-11-07'),
(8, 8, 'Potato Storage Requirements', '2024-11-08'),
(9, 9, 'Strawberry Quality Control', '2024-11-09'),
(10, 10, 'Spinach Packaging Specifications', '2024-11-10');

-- Insert Product Data
INSERT INTO Product (Name, Price, Type, Weight, Size, ExpiryDate, ManufacturerID) VALUES
('Tomato Pack', 2.50, 'Perishable', 0.5, 'Medium', '2024-11-20', 1),
('Cucumber Fresh', 1.75, 'Perishable', 0.3, 'Small', '2024-11-18', 2),
('Lettuce Leaf', 1.20, 'Perishable', 0.2, 'Small', '2024-11-22', 3),
('Carrot Bunch', 1.80, 'Perishable', 0.6, 'Medium', '2024-11-24', 4),
('Apple Pack', 3.00, 'Non-Perishable', 0.4, 'Large', '2025-01-01', 5),
('Orange Fresh', 2.00, 'Non-Perishable', 0.5, 'Large', '2025-01-10', 6),
('Pineapple Slice', 5.00, 'Non-Perishable', 1.0, 'Medium', '2025-02-01', 7),
('Potato Bag', 2.30, 'Perishable', 1.5, 'Large', '2024-11-23', 8),
('Strawberry Box', 4.50, 'Perishable', 0.4, 'Small', '2024-11-25', 9),
('Spinach Leaves', 2.00, 'Perishable', 0.2, 'Small', '2024-11-28', 10);

-- Insert Distributor Data
INSERT INTO Distributor (Name, PhoneNumber, Email, AddressID) VALUES
('Global Distribution Inc', '555-3210', 'global@distribute.com', 4),
('Prime Distributors', '555-6543', 'prime@distribute.com', 6),
('FreshWorld Distributors', '555-7890', 'fresh@world.com', 2),
('EcoLogistics Inc', '555-9876', 'eco@logistics.com', 3),
('Sunshine Distributors', '555-1357', 'sunshine@distribute.com', 7),
('Greens Logistics', '555-9632', 'greens@logistics.com', 8),
('Natures Distributors', '555-4321', 'nature@distribute.com', 9),
('Harvest Express', '555-1234', 'harvest@express.com', 1),
('Prime Food Distribution', '555-8520', 'prime@food.com', 10),
('Fresh Delivery Services', '555-4567', 'fresh@delivery.com', 5);

-- Insert Warehouse Data
INSERT INTO Warehouse (Name, AddressID, DistributorID, Type, Capacity) VALUES
('Main Warehouse', 4, 1, 'Cold Storage', '50000kg'),
('Eco Warehouse', 6, 3, 'Cold Storage', '30000kg'),
('GreenWorld Warehouse', 2, 5, 'Cold Storage', '35000kg'),
('FreshLogistics Warehouse', 3, 2, 'Cold Storage', '45000kg'),
('Sunshine Warehouse', 7, 4, 'Cold Storage', '20000kg'),
('Greens Global Warehouse', 8, 6, 'Cold Storage', '40000kg'),
('Nature Fresh Warehouse', 9, 7, 'Cold Storage', '30000kg'),
('Harvest Hub', 1, 8, 'Cold Storage', '25000kg'),
('Prime Warehouse', 10, 9, 'Cold Storage', '60000kg'),
('Fresh Distribution Warehouse', 5, 10, 'Cold Storage', '50000kg');

-- Insert Inventory Data
INSERT INTO Inventory (Quantity, ExpiryDate, ProductID, WarehouseID) VALUES
(100, '2024-12-01', 1, 1),
(150, '2024-11-25', 2, 2),
(200, '2024-12-05', 3, 3),
(50, '2024-12-15', 4, 4),
(300, '2025-01-01', 5, 5),
(120, '2024-12-10', 6, 6),
(90, '2024-12-20', 7, 7),
(110, '2024-11-30', 8, 8),
(200, '2024-12-07', 9, 9),
(80, '2024-12-22', 10, 10);

-- Insert Transporter Data
INSERT INTO Transporter (Name, ContactInfo, ModeOfTransport, AddressID) VALUES
('XYZ Transport', '9876543210', 'Truck', 1),
('ABC Logistics', '9123456789', 'Van', 2),
('Speedy Movers', '9234567890', 'Truck', 3),
('QuickShip', '9345678901', 'Motorcycle', 4),
('Global Freight', '9456789012', 'Truck', 5),
('Fast Transport', '9567890123', 'Van', 6),
('EZ Delivery', '9678901234', 'Truck', 7),
('Movers Express', '9789012345', 'Van', 8),
('Rapid Shippers', '9890123456', 'Motorcycle', 9),
('Cargo Express', '9901234567', 'Truck', 10);

-- Insert Shipment Data
INSERT INTO Shipment (ShipmentDate, EstimatedDeliveryTime, Destination, OutOfShipmentTime, Status, MaximumCapacity) VALUES
('2024-11-01', '12:30:00', 'New York', '14:00:00', 'Pending', 500.00),
('2024-11-02', '14:00:00', 'Los Angeles', '15:30:00', 'In Transit', 300.00),
('2024-11-03', '09:00:00', 'Chicago', '10:30:00', 'Delivered', 400.00),
('2024-11-04', '16:00:00', 'Miami', '17:30:00', 'In Transit', 200.00),
('2024-11-05', '13:00:00', 'Houston', '14:30:00', 'Pending', 350.00),
('2024-11-06', '08:00:00', 'San Francisco', '09:30:00', 'Delivered', 250.00),
('2024-11-07', '17:00:00', 'Seattle', '18:30:00', 'In Transit', 450.00),
('2024-11-08', '10:00:00', 'Boston', '12:00:00', 'Pending', 300.00),
('2024-11-09', '11:00:00', 'Dallas', '12:30:00', 'In Transit', 500.00),
('2024-11-10', '15:00:00', 'Phoenix', '16:30:00', 'Canceled', 400.00);

-- Insert ShipmentTransport Data
INSERT INTO ShipmentTransport (DistributorID, TransporterID, ShipmentID) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7),
(8, 8, 8),
(9, 9, 9),
(10, 10, 10);

-- Insert DistributorManufacturerContract Data
INSERT INTO DistributorManufacturerContract (DistributorID, ManufacturerID, DistributorManufacturerContractStartDate, DistributorManufacturerContractEndDate) VALUES
(1, 1, '2024-01-01', '2025-01-01'),
(2, 2, '2024-02-01', '2025-02-01'),
(3, 3, '2024-03-01', '2025-03-01'),
(4, 4, '2024-04-01', '2025-04-01'),
(5, 5, '2024-05-01', '2025-05-01'),
(6, 6, '2024-06-01', '2025-06-01'),
(7, 7, '2024-07-01', '2025-07-01'),
(8, 8, '2024-08-01', '2025-08-01'),
(9, 9, '2024-09-01', '2025-09-01'),
(10, 10, '2024-10-01', '2025-10-01');

-- Insert Retailer Data
INSERT INTO Retailer (Name, PhoneNumber, Email, AddressID, DistributorID) VALUES
('Retailer A', '1234567890', 'retailera@example.com', 1, 1),
('Retailer B', '2345678901', 'retailerb@example.com', 2, 2),
('Retailer C', '3456789012', 'retailerc@example.com', 3, 3),
('Retailer D', '4567890123', 'retailerd@example.com', 4, 4),
('Retailer E', '5678901234', 'retailere@example.com', 5, 5),
('Retailer F', '6789012345', 'retailerf@example.com', 6, 6),
('Retailer G', '7890123456', 'retailerg@example.com', 7, 7),
('Retailer H', '8901234567', 'retailerh@example.com', 8, 8),
('Retailer I', '9012345678', 'retaileri@example.com', 9, 9),
('Retailer J', '0123456789', 'retailerj@example.com', 10, 10);

-- Insert TransporterContract Data
INSERT INTO TransporterContract (TransporterID, RetailerID, TransporterContractStartDate, TransporterContractEndDate) VALUES
(1, 1, '2024-01-01', '2025-01-01'),
(2, 2, '2024-02-01', '2025-02-01'),
(3, 3, '2024-03-01', '2025-03-01'),
(4, 4, '2024-04-01', '2025-04-01'),
(5, 5, '2024-05-01', '2025-05-01'),
(6, 6, '2024-06-01', '2025-06-01'),
(7, 7, '2024-07-01', '2025-07-01'),
(8, 8, '2024-08-01', '2025-08-01'),
(9, 9, '2024-09-01', '2025-09-01'),
(10, 10, '2024-10-01', '2025-10-01');

-- Insert UserTable Data
INSERT INTO UserTable (Name, Email, Contact, AddressID) VALUES
('John Doe', 'johndoe@example.com', '555-1234', 1),
('Jane Smith', 'janesmith@example.com', '555-5678', 2),
('Alice Brown', 'alicebrown@example.com', '555-8765', 3),
('Bob White', 'bobwhite@example.com', '555-4321', 4),
('Charlie Black', 'charlieblack@example.com', '555-1111', 5),
('David Green', 'davidgreen@example.com', '555-2222', 6),
('Eva Blue', 'evablue@example.com', '555-3333', 7),
('Frank Yellow', 'frankyellow@example.com', '555-4444', 8),
('Grace Red', 'gracered@example.com', '555-5555', 9),
('Henry Purple', 'henrypurple@example.com', '555-6666', 10);

-- Insert OrderTable Data
INSERT INTO OrderTable (UserID, Quantity, OrderDate) VALUES
(1, 5, '2024-11-01'),
(2, 3, '2024-11-02'),
(3, 10, '2024-11-03'),
(4, 7, '2024-11-04'),
(5, 8, '2024-11-05'),
(6, 12, '2024-11-06'),
(7, 15, '2024-11-07'),
(8, 20, '2024-11-08'),
(9, 9, '2024-11-09'),
(10, 6, '2024-11-10');

