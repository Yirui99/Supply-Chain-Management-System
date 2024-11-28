-- Non-clustered index on Product Name
CREATE NONCLUSTERED INDEX idx_product_name ON Product (Name);

-- Non-clustered index on Material Type
CREATE NONCLUSTERED INDEX idx_material_type ON Material (Type);

-- Non-clustered index on Shipment Destination
CREATE NONCLUSTERED INDEX idx_shipment_destination ON Shipment (Destination);

SELECT * 
FROM sys.indexes 
WHERE object_id = OBJECT_ID('Product') AND name = 'idx_product_name' ;

SELECT * 
FROM sys.indexes 
WHERE object_id = OBJECT_ID('Material') AND name = 'idx_material_type' ;

SELECT * 
FROM sys.indexes 
WHERE object_id = OBJECT_ID('Shipment') AND name = 'idx_shipment_destination' ;