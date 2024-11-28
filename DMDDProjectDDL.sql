CREATE DATABASE SupplyChain;

USE SupplyChain;



-- Address Table
CREATE TABLE Address (
    AddressID INT PRIMARY KEY IDENTITY,
    Street VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    PostalCode VARCHAR(20) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    AddressType VARCHAR(20) NOT NULL CHECK (AddressType IN ('Supplier', 'User', 'Distributor', 'Manufacturer', 'Retailer'))
);

-- Supplier Table
CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(15),
    Email VARCHAR(50),
    AddressID INT,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION
);

-- Material Table
CREATE TABLE Material (
    MaterialID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    Type VARCHAR(50) NOT NULL CHECK (Type IN ('Raw', 'Processed')),
    SupplierID INT NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE NO ACTION
);

-- SupplyReport Table
CREATE TABLE SupplyReport (
    ReportID INT PRIMARY KEY IDENTITY,
    SupplierID INT NOT NULL,
    MaterialID INT NOT NULL,
    SupplyDate DATE NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE NO ACTION,
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID) ON DELETE NO ACTION
);

-- Manufacturer Table
CREATE TABLE Manufacturer (
    ManufacturerID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(15),
    Email VARCHAR(50),
    AddressID INT,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION
);

-- MaterialDocument Table
CREATE TABLE MaterialDocument (
    DocumentID INT PRIMARY KEY IDENTITY,
    MaterialID INT NOT NULL,
    ManufacturerID INT NOT NULL,
    Description VARCHAR(255),
    CreatedDate DATE NOT NULL,
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID) ON DELETE NO ACTION,
    FOREIGN KEY (ManufacturerID) REFERENCES Manufacturer(ManufacturerID) ON DELETE NO ACTION
);

-- Product Table
CREATE TABLE Product (
    ProductID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) CHECK (Price > 0),
    Type VARCHAR(50) NOT NULL,
    Weight DECIMAL(5, 2) CHECK (Weight > 0),
    Size VARCHAR(20),
    ExpiryDate DATE,
    ManufacturerID INT NOT NULL,
    FOREIGN KEY (ManufacturerID) REFERENCES Manufacturer(ManufacturerID) ON DELETE NO ACTION
);

-- Distributor Table
CREATE TABLE Distributor (
    DistributorID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(15),
    Email VARCHAR(50),
    AddressID INT,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION
);

-- Warehouse Table
CREATE TABLE Warehouse (
    WarehouseID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    AddressID INT,
    DistributorID INT,
    Type VARCHAR(50) NOT NULL,
    Capacity VARCHAR(50) NOT NULL,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION,
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID) ON DELETE NO ACTION
);

-- Inventory Table
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY IDENTITY,
    Quantity INT CHECK (Quantity >= 0),
    ExpiryDate DATE,
    ProductID INT NOT NULL,
    WarehouseID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE NO ACTION,
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID) ON DELETE NO ACTION
);

-- Transporter Table
CREATE TABLE Transporter (
    TransporterID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(50),
    ModeOfTransport VARCHAR(50),
    AddressID INT,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION
);

-- Shipment Table
CREATE TABLE Shipment (
    ShipmentID INT PRIMARY KEY IDENTITY,
    ShipmentDate DATE NOT NULL,
    EstimatedDeliveryTime TIME NOT NULL,
    Destination VARCHAR(255) NOT NULL,
    OutOfShipmentTime TIME,
    Status VARCHAR(50) CHECK (Status IN ('Pending', 'In Transit', 'Delivered', 'Canceled')),
    MaximumCapacity DECIMAL(5, 2) CHECK (MaximumCapacity > 0)
);

-- ShipmentTransport Table
CREATE TABLE ShipmentTransport (
    ShipmentTransportID INT PRIMARY KEY IDENTITY,
    DistributorID INT NOT NULL,
    TransporterID INT NOT NULL,
    ShipmentID INT NOT NULL,
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID) ON DELETE NO ACTION,
    FOREIGN KEY (ShipmentID) REFERENCES Shipment(ShipmentID) ON DELETE NO ACTION,
    FOREIGN KEY (TransporterID) REFERENCES Transporter(TransporterID) ON DELETE NO ACTION
);

-- DistributorManufacturerContract Table
CREATE TABLE DistributorManufacturerContract (
    ContractID INT PRIMARY KEY IDENTITY,
    DistributorID INT NOT NULL,
    ManufacturerID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID) ON DELETE NO ACTION,
    FOREIGN KEY (ManufacturerID) REFERENCES Manufacturer(ManufacturerID) ON DELETE NO ACTION
);

-- Retailer Table
CREATE TABLE Retailer (
    RetailerID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(15),
    Email VARCHAR(50),
    AddressID INT,
    DistributorID INT NOT NULL,
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID) ON DELETE NO ACTION,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION
);

-- TransporterContract Table
CREATE TABLE TransporterContract (
    ContractID INT PRIMARY KEY IDENTITY,
    TransporterID INT NOT NULL,
    RetailerID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    FOREIGN KEY (TransporterID) REFERENCES Transporter(TransporterID) ON DELETE NO ACTION,
    FOREIGN KEY (RetailerID) REFERENCES Retailer(RetailerID) ON DELETE NO ACTION
);

-- UserTable
CREATE TABLE UserTable (
    UserID INT PRIMARY KEY IDENTITY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(50),
    Contact VARCHAR(15),
    AddressID INT,
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE NO ACTION
);

-- OrderTable
CREATE TABLE OrderTable (
    OrderID INT PRIMARY KEY IDENTITY,
    UserID INT NOT NULL,
    Quantity INT CHECK (Quantity > 0),
    OrderDate DATE NOT NULL,
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID) ON DELETE NO ACTION
);
