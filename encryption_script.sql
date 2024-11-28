-- Create a Master Key (if not already created)
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'DMDD!123';

-- Create a Symmetric Key for encryption
CREATE SYMMETRIC KEY SupplyChainKey
WITH ALGORITHM = AES_256
ENCRYPTION BY PASSWORD = 'DMDD!123';

-- Open the Symmetric Key for encryption
OPEN SYMMETRIC KEY SupplyChainKey
DECRYPTION BY PASSWORD = 'DMDD!123';

-- Add temporary columns to store the encrypted data
ALTER TABLE Supplier
ADD Name_encrypted VARBINARY(MAX)

-- Open the Symmetric Key for encryption
OPEN SYMMETRIC KEY SupplyChainKey
DECRYPTION BY PASSWORD = 'DMDD!123';

-- Encrypt the emp_fname and emp_lname columns and store in new columns
UPDATE Supplier
SET Name_encrypted = EncryptByKey(Key_GUID('SupplyChainKey'), Name)


-- Close the Symmetric Key
CLOSE SYMMETRIC KEY SupplyChainKey;

-- Drop the original columns
ALTER TABLE Supplier
DROP COLUMN Name

-- Rename the temporary columns to match the original names
EXEC sp_rename 'Supplier.Name_encrypted', 'Name', 'COLUMN';

-- Open the Symmetric Key for decryption
OPEN SYMMETRIC KEY SupplyChainKey
DECRYPTION BY PASSWORD = 'DMDD!123';

-- Decrypt and view the data
SELECT 
    SupplierID,
    CONVERT(VARCHAR(20), DecryptByKey(Name)) AS Name
FROM Supplier;

-- Close the Symmetric Key
CLOSE SYMMETRIC KEY SupplyChainKey;