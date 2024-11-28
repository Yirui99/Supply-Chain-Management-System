import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk
import csv

# Define connection string
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  
    "DATABASE=SupplyChain;" 
    "UID=sa;" 
    "PWD=MyStrongPassword123;"
)


def connect_db():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT SYSTEM_USER")
        current_user = cursor.fetchone()[0]
        print(f"Connected as user: {current_user}")  # Debugging: Print connected user
        return connection
    except pyodbc.Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None
def index_operations_menu():
    root = tk.Tk()
    root.title("Index Operations")
    root.geometry("500x400")

    # Function to create non-clustered indexes
    def create_indexes():
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            # Creating indexes
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_product_name')
            BEGIN
                CREATE NONCLUSTERED INDEX idx_product_name ON Product (Name);
            END
            """)
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_material_type')
            BEGIN
                CREATE NONCLUSTERED INDEX idx_material_type ON Material (Type);
            END
            """)
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_shipment_destination')
            BEGIN
                CREATE NONCLUSTERED INDEX idx_shipment_destination ON Shipment (Destination);
            END
            """)
            connection.commit()
            messagebox.showinfo("Index Creation", "Indexes created successfully.")
        except pyodbc.Error as e:
            messagebox.showerror("Index Creation Error", str(e))
        finally:
            connection.close()

    # Function to verify indexes
    def verify_indexes():
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            # Verifying Product index
            cursor.execute("""
            SELECT * 
            FROM sys.indexes 
            WHERE object_id = OBJECT_ID('Product') AND name = 'idx_product_name';
            """)
            product_index = cursor.fetchone()

            # Verifying Material index
            cursor.execute("""
            SELECT * 
            FROM sys.indexes 
            WHERE object_id = OBJECT_ID('Material') AND name = 'idx_material_type';
            """)
            material_index = cursor.fetchone()

            # Verifying Shipment index
            cursor.execute("""
            SELECT * 
            FROM sys.indexes 
            WHERE object_id = OBJECT_ID('Shipment') AND name = 'idx_shipment_destination';
            """)
            shipment_index = cursor.fetchone()

            # Display results
            result_message = ""
            result_message += "Product Name Index: " + ("Exists\n" if product_index else "Not Found\n")
            result_message += "Material Type Index: " + ("Exists\n" if material_index else "Not Found\n")
            result_message += "Shipment Destination Index: " + ("Exists\n" if shipment_index else "Not Found\n")

            messagebox.showinfo("Index Verification", result_message)
        except pyodbc.Error as e:
            messagebox.showerror("Index Verification Error", str(e))
        finally:
            connection.close()

    # UI Components for creating indexes
    tk.Label(root, text="Create Indexes", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(root, text="Create Non-clustered Indexes", command=create_indexes).pack(pady=10)

    # UI Components for verifying indexes
    tk.Label(root, text="Verify Indexes", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(root, text="Verify Indexes", command=verify_indexes).pack(pady=10)

    root.mainloop()

def udf_operations_menu():
    root = tk.Tk()
    root.title("User Defined Function Operations")
    root.geometry("600x700")

    # Function to calculate product price after discount
    def calculate_discounted_price():
        product_id = int(product_id_entry.get())
        discount_rate = float(discount_rate_entry.get())
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT dbo.CalculateFinalPrice(?, ?);", (product_id, discount_rate))
            final_price = cursor.fetchone()[0]
            messagebox.showinfo("Final Price", f"The final price after discount is: {final_price:.2f}")
        except pyodbc.Error as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            connection.close()

    # Function to get product category
    def get_product_category():
        product_id = int(product_id_entry_cat.get())
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT dbo.GetProductCategory(?);", (product_id,))
            category = cursor.fetchone()[0]
            messagebox.showinfo("Product Category", f"The category of product ID {product_id} is: {category}")
        except pyodbc.Error as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            connection.close()

    # Function to check material availability
    def check_material_availability():
        product_id = int(product_id_entry_avail.get())
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT dbo.CheckMaterialAvailability(?);", (product_id,))
            availability = cursor.fetchone()[0]
            messagebox.showinfo("Material Availability", f"Product ID {product_id} is: {availability}")
        except pyodbc.Error as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            connection.close()

    # UI Components for calculating final price after discount
    tk.Label(root, text="Calculate Final Price After Discount", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="Product ID:").pack()
    product_id_entry = tk.Entry(root)
    product_id_entry.pack()
    tk.Label(root, text="Discount Rate (%):").pack()
    discount_rate_entry = tk.Entry(root)
    discount_rate_entry.pack()
    tk.Button(root, text="Calculate Final Price", command=calculate_discounted_price).pack(pady=10)

    # UI Components for getting product category
    tk.Label(root, text="Get Product Category", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="Product ID:").pack()
    product_id_entry_cat = tk.Entry(root)
    product_id_entry_cat.pack()
    tk.Button(root, text="Get Category", command=get_product_category).pack(pady=10)

    # UI Components for checking material availability
    tk.Label(root, text="Check Material Availability", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="Product ID:").pack()
    product_id_entry_avail = tk.Entry(root)
    product_id_entry_avail.pack()
    tk.Button(root, text="Check Availability", command=check_material_availability).pack(pady=10)

    root.mainloop()

# Create ProductChangeHistory table if it does not exist
def create_product_change_history_table():
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ProductChangeHistory')
        BEGIN
            CREATE TABLE ProductChangeHistory (
                ChangeID INT IDENTITY(1,1) PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                OldPrice DECIMAL(10,2) NULL,
                NewPrice DECIMAL(10,2) NOT NULL,
                ChangeDate DATETIME NOT NULL DEFAULT GETDATE()
            )
        END
        """)
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Table Creation Error", str(e))
    finally:
        connection.close()

# Create trigger to record product price changes
def create_price_change_trigger():
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'PriceChange')
        BEGIN
            EXEC('CREATE TRIGGER PriceChange
            ON Product
            AFTER UPDATE
            AS
            BEGIN
                SET NOCOUNT ON;

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
                        inserted i ON d.ProductID = i.ProductID
                    WHERE 
                        d.Price <> i.Price;
                END
            END')
        END
        """)
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Trigger Creation Error", str(e))
    finally:
        connection.close()
def execute_product_change_history_trigger():
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        # Execute trigger operation (if needed, depending on your trigger logic, it might run automatically)
        # Here we assume it's already running automatically on updates, so we just fetch the history.

        # Fetch product change history
        cursor.execute("""
        SELECT ChangeID, Name, OldPrice, NewPrice, ChangeDate
        FROM ProductChangeHistory
        ORDER BY ChangeDate DESC;
        """)
        rows = cursor.fetchall()

        # Create a new window to display the history
        history_window = tk.Toplevel()
        history_window.title("Product Change History")
        history_window.geometry("600x400")

        # Treeview to display the history
        tree = ttk.Treeview(history_window, columns=("ChangeID", "Name", "OldPrice", "NewPrice", "ChangeDate"), show="headings")
        tree.heading("ChangeID", text="Change ID")
        tree.heading("Name", text="Product Name")
        tree.heading("OldPrice", text="Old Price")
        tree.heading("NewPrice", text="New Price")
        tree.heading("ChangeDate", text="Change Date")

        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
    except pyodbc.Error as e:
        messagebox.showerror("Product Change History Error", str(e))
    finally:
        connection.close()

# Create stored procedure to update shipment status
def create_update_shipment_status_procedure():
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'UpdateShipmentStatus')
        BEGIN
            EXEC('CREATE PROCEDURE UpdateShipmentStatus
                @ShipmentID INT,
                @NewStatus VARCHAR(50),
                @OldStatus VARCHAR(50) OUTPUT
            AS
            BEGIN
                SELECT @OldStatus = Status
                FROM Shipment
                WHERE ShipmentID = @ShipmentID;

                UPDATE Shipment
                SET Status = @NewStatus
                WHERE ShipmentID = @ShipmentID;
            END')
        END
        """)
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Stored Procedure Creation Error", str(e))
    finally:
        connection.close()

# Create stored procedure to get product stock
def create_get_product_stock_procedure():
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'GetProductStock')
        BEGIN
            EXEC('CREATE PROCEDURE GetProductStock
                @ProductID INT,
                @StockCount INT OUTPUT
            AS
            BEGIN
                SELECT @StockCount = Quantity
                FROM Inventory
                WHERE ProductID = @ProductID;
            END')
        END
        """)
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Stored Procedure Creation Error", str(e))
    finally:
        connection.close()

# Create stored procedure to update warehouse capacity and calculate total capacity
def create_update_warehouse_capacity_procedure():
    connection = connect_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'UpdateWarehouseAndCalculateTotal')
        BEGIN
            EXEC('CREATE PROCEDURE UpdateWarehouseAndCalculateTotal
                @WarehouseName VARCHAR(100),
                @NewCapacity VARCHAR(50)
            AS
            BEGIN
                UPDATE Warehouse
                SET Capacity = @NewCapacity
                WHERE Name = @WarehouseName;

                DECLARE @TotalCapacity INT;
                SELECT @TotalCapacity = SUM(CAST(REPLACE(Capacity, ''kg'', '''') AS INT))
                FROM Warehouse;

                SELECT @TotalCapacity AS TotalWarehouseCapacity;
                SELECT * FROM Warehouse WHERE Name = @WarehouseName;
            END')
        END
        """)
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Stored Procedure Creation Error", str(e))
    finally:
        connection.close()

# Create GUI
def main_menu():
    create_product_change_history_table()  # Ensure history table is created at startup
    create_price_change_trigger()  # Ensure trigger is created at startup
    create_update_shipment_status_procedure()  # Ensure stored procedure is created at startup
    create_get_product_stock_procedure()  # Ensure stored procedure is created at startup
    create_update_warehouse_capacity_procedure()  # Ensure stored procedure is created at startup

    root = tk.Tk()
    root.title("Supply Chain Management System Main Menu")
    root.geometry("800x900")

    # Add title label
    tk.Label(root, text="Supply Chain Management System", font=("Helvetica", 20, "bold")).pack(pady=20)

    # Create frame to hold buttons in two columns
    frame_buttons = tk.Frame(root)
    frame_buttons.pack()

    table_buttons = [
        ("Address Management", lambda: manage_table("Address", address_columns)),
        ("Supplier Management", lambda: manage_table("Supplier", supplier_columns)),
        ("Material Management", lambda: manage_table("Material", material_columns)),
        ("Supply Report Management", lambda: manage_table("SupplyReport", supply_report_columns)),
        ("Manufacturer Management", lambda: manage_table("Manufacturer", manufacturer_columns)),
        ("Material Document Management", lambda: manage_table("MaterialDocument", material_document_columns)),
        ("Product Management", lambda: manage_table("Product", product_columns)),
        ("Distributor Management", lambda: manage_table("Distributor", distributor_columns)),
        ("Warehouse Management", lambda: manage_table("Warehouse", warehouse_columns)),
        ("Inventory Management", lambda: manage_table("Inventory", inventory_columns)),
        ("Transporter Management", lambda: manage_table("Transporter", transporter_columns)),
        ("Shipment Management", lambda: manage_table("Shipment", shipment_columns)),
        ("Shipment Transport Management", lambda: manage_table("ShipmentTransport", shipment_transport_columns)),
        ("Distributor-Manufacturer Contracts", lambda: manage_table("DistributorManufacturerContract", distributor_manufacturer_contract_columns)),
        ("Retailer Management", lambda: manage_table("Retailer", retailer_columns)),
        ("Transporter Contracts", lambda: manage_table("TransporterContract", transporter_contract_columns)),
        ("User Management", lambda: manage_table("UserTable", user_table_columns)),
        ("Order Management", lambda: manage_table("OrderTable", order_table_columns)),
        ("Stored Procedure Operations", manage_stored_procedures),
        ("View Reports", manage_views),
        ("User Defined Function Operations", udf_operations_menu),
        ("Index Operations", index_operations_menu),
        ("Product Change History", execute_product_change_history_trigger),
    ]

    # Add buttons in two columns
    for idx, (text, command) in enumerate(table_buttons):
        column = idx % 2
        row = idx // 2
        tk.Button(frame_buttons, text=text, command=command, width=30, height=2).grid(row=row, column=column, padx=10, pady=5)

    # Add exit button
    tk.Button(root, text="Exit", command=root.quit, width=30, height=2).pack(pady=20)

    root.mainloop()

# Generic function to manage tables
def manage_table(table_name, columns):
    root = tk.Tk()
    root.title(f"{table_name} Management - Supply Chain System")
    root.geometry("1000x600")

    def fetch_data():
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)
            for row in rows:
                formatted_row = tuple(str(value).strip() if value else '' for value in row)
                tree.insert("", tk.END, values=formatted_row)
        except pyodbc.Error as e:
            messagebox.showerror("Query Error", str(e))
        finally:
            connection.close()

    def export_to_csv():
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            with open(f"{table_name}_data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([col[1] for col in columns])
                writer.writerows(rows)

            messagebox.showinfo("Export Success", f"Data exported to {table_name}_data.csv")
        except pyodbc.Error as e:
            messagebox.showerror("Export Error", str(e))
        finally:
            connection.close()

    def add_record():
        add_window = tk.Toplevel(root)
        add_window.title(f"Add Record to {table_name}")
        add_window.geometry("500x400")

        entries = {}
        for idx, (col_id, col_name) in enumerate(columns[1:]):  # Skip the primary key column
            tk.Label(add_window, text=f"{col_name}:").grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[col_id] = entry

        def save_record():
            values = [entry.get() for entry in entries.values()]
            if not all(values):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()
            try:
                placeholders = ', '.join(['?'] * len(values))
                columns_str = ', '.join(entries.keys())
                print(
                    f"Executing SQL: INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) with values: {values}")  # Debug log
                cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
                connection.commit()
                messagebox.showinfo("Success", f"Record added to {table_name} successfully.")
                fetch_data()
                add_window.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Insert Error", str(e))
            finally:
                connection.close()

        tk.Button(add_window, text="Save", command=save_record).grid(row=len(columns), column=1, pady=10)

    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        record_id = tree.item(selected_item[0], 'values')[0]

        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE {columns[0][0]} = ?", (record_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Record deleted from {table_name} successfully.")
            fetch_data()
        except pyodbc.Error as e:
            messagebox.showerror("Delete Error", str(e))
        finally:
            connection.close()

    def update_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return

        record_values = tree.item(selected_item[0], 'values')
        update_window = tk.Toplevel(root)
        update_window.title(f"Update Record in {table_name}")
        update_window.geometry("500x400")

        entries = {}
        for idx, (col_id, col_name) in enumerate(columns[1:]):
            tk.Label(update_window, text=f"{col_name}:").grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(update_window)
            entry.insert(0, record_values[idx + 1])
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[col_id] = entry

        def save_update():
            values = [entry.get() for entry in entries.values()]
            if not all(values):
                messagebox.showwarning("Input Error", "Please enter all fields.")
                return

            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()
            try:
                placeholders = ', '.join([f"{col} = ?" for col in entries.keys()])
                cursor.execute(f"UPDATE {table_name} SET {placeholders} WHERE {columns[0][0]} = ?", values + [record_values[0]])
                connection.commit()
                messagebox.showinfo("Success", f"Record updated in {table_name} successfully.")
                fetch_data()
                update_window.destroy()

                # If the product price is updated, add an entry to the history table
                if table_name == "Product" and "Price" in entries:
                    try:
                        old_price = float(record_values[columns.index(("Price", "Price"))])
                        new_price = float(entries["Price"].get())
                        if old_price != new_price:
                            cursor.execute(
                                "INSERT INTO ProductChangeHistory (Name, OldPrice, NewPrice, ChangeDate) VALUES (?, ?, ?, GETDATE())",
                                (record_values[columns.index(("Name", "Name"))], old_price, new_price)
                            )
                            connection.commit()
                            print("Product price updated. History recorded.")
                    except Exception as e:
                        print(f"Error recording price change: {e}")
            except pyodbc.Error as e:
                messagebox.showerror("Update Error", str(e))
            finally:
                connection.close()

        tk.Button(update_window, text="Save", command=save_update).grid(row=len(columns), column=1, pady=10)

    def search_record():
        search_window = tk.Toplevel(root)
        search_window.title(f"Search Record in {table_name}")
        search_window.geometry("500x200")

        tk.Label(search_window, text="Search by Column:").grid(row=0, column=0, padx=10, pady=5)
        column_combobox = ttk.Combobox(search_window, values=[col[1] for col in columns])
        column_combobox.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(search_window, text="Search Value:").grid(row=1, column=0, padx=10, pady=5)
        search_entry = tk.Entry(search_window)
        search_entry.grid(row=1, column=1, padx=10, pady=5)

        def execute_search():
            search_column = column_combobox.get()
            search_value = search_entry.get()

            if not search_column or not search_value:
                messagebox.showwarning("Input Error", "Please select a column and enter a value to search.")
                return

            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()
            try:
                column_id = [col[0] for col in columns if col[1] == search_column][0]
                cursor.execute(f"SELECT * FROM {table_name} WHERE {column_id} LIKE ?", (f"%{search_value}%",))
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    formatted_row = tuple(str(value).strip() if value else '' for value in row)
                    tree.insert("", tk.END, values=formatted_row)
                search_window.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Search Error", str(e))
            finally:
                connection.close()

        tk.Button(search_window, text="Search", command=execute_search).grid(row=2, column=1, pady=10)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)

    tk.Button(frame_buttons, text="Fetch Data", command=fetch_data).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Export to CSV", command=export_to_csv).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Back to Main Menu", command=lambda: [root.destroy(), main_menu()]).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Add Record", command=add_record).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Delete Record", command=delete_record).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Update Record", command=update_record).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Search Record", command=search_record).pack(side=tk.LEFT, padx=10)
    tree = ttk.Treeview(root, columns=[col[0] for col in columns], show="headings")
    for col_id, col_name in columns:
        tree.heading(col_id, text=col_name)
    tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

    fetch_data()
    root.mainloop()

# Function to manage stored procedures
def manage_stored_procedures():
    root = tk.Tk()
    root.title("Stored Procedure Operations")
    root.geometry("600x600")

    def execute_update_shipment_status():
        shipment_id = int(shipment_id_entry.get())
        new_status = new_status_entry.get()
        connection = connect_db()
        if connection is None:
            print("No connection")
            return

        cursor = connection.cursor()
        try:
            print("Start Execute")
            cursor.execute("DECLARE @OldStatus VARCHAR(50); "
                           "EXEC UpdateShipmentStatus ?, ?, @OldStatus OUTPUT; SELECT @OldStatus;", (shipment_id, new_status))
            connection.commit()
            print("Start Declare")
            print("Update Shipment")
            messagebox.showinfo("Shipment Status Update", f"Shipment ID {shipment_id} status updated to '{new_status}'.")
        except pyodbc.Error as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            connection.close()

    def execute_get_product_stock():
        product_id = int(product_id_entry.get())
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("DECLARE @StockCount INT; EXEC GetProductStock ?, @StockCount OUTPUT; SELECT @StockCount;", product_id)
            stock_count = cursor.fetchone()[0]
            messagebox.showinfo("Product Stock", f"Product ID {product_id} has {stock_count} units in stock.")
        except pyodbc.Error as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            connection.close()

    def execute_update_warehouse_capacity():
        warehouse_name = warehouse_name_entry.get()
        new_capacity = new_capacity_entry.get()
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("EXEC UpdateWarehouseAndCalculateTotal ?, ?;", (warehouse_name, new_capacity))
            connection.commit()
            messagebox.showinfo("Warehouse Update", f"Warehouse '{warehouse_name}' updated to new capacity '{new_capacity}' kg.")
        except pyodbc.Error as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            connection.close()

    # UI for Update Shipment Status
    tk.Label(root, text="Shipment ID:").grid(row=0, column=0, padx=10, pady=5)
    shipment_id_entry = tk.Entry(root)
    shipment_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="New Status:").grid(row=1, column=0, padx=10, pady=5)
    new_status_entry = tk.Entry(root)
    new_status_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(root, text="Update Shipment Status", command=execute_update_shipment_status).grid(row=2, column=1, pady=10)

    # UI for Get Product Stock
    tk.Label(root, text="Product ID:").grid(row=3, column=0, padx=10, pady=5)
    product_id_entry = tk.Entry(root)
    product_id_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(root, text="Get Product Stock", command=execute_get_product_stock).grid(row=4, column=1, pady=10)

    # UI for Update Warehouse Capacity
    tk.Label(root, text="Warehouse Name:").grid(row=5, column=0, padx=10, pady=5)
    warehouse_name_entry = tk.Entry(root)
    warehouse_name_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(root, text="New Capacity (e.g., '50000kg'):").grid(row=6, column=0, padx=10, pady=5)
    new_capacity_entry = tk.Entry(root)
    new_capacity_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Button(root, text="Update Warehouse Capacity", command=execute_update_warehouse_capacity).grid(row=7, column=1, pady=10)

    root.mainloop()

# Function to manage views
def manage_views():
    root = tk.Tk()
    root.title("View Reports")
    root.geometry("600x400")

    def display_view(view_name):
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {view_name}")
            rows = cursor.fetchall()
            for row in view_tree.get_children():
                view_tree.delete(row)
            if rows:
                columns = [desc[0] for desc in cursor.description]
                view_tree["columns"] = columns
                for col in columns:
                    view_tree.heading(col, text=col)
                    view_tree.column(col, width=100)
                for row in rows:
                    formatted_row = tuple(str(value).strip() if value else '' for value in row)
                    view_tree.insert("", tk.END, values=formatted_row)
            else:
                messagebox.showinfo("No Data", f"No data found in view: {view_name}")
        except pyodbc.Error as e:
            messagebox.showerror("View Error", str(e))
        finally:
            connection.close()

    tk.Button(root, text="Supplier Material Report View", command=lambda: display_view("SupplierMaterialReportView")).pack(pady=5)
    tk.Button(root, text="Inventory Report View", command=lambda: display_view("InventoryReportView")).pack(pady=5)
    tk.Button(root, text="Product Expiry Report View", command=lambda: display_view("ProductExpiryReportView")).pack(pady=5)

    view_tree = ttk.Treeview(root, show="headings")
    view_tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

    root.mainloop()


# Column definitions for each table
address_columns = [
    ("AddressID", "Address ID"),
    ("Street", "Street"),
    ("City", "City"),
    ("State", "State"),
    ("PostalCode", "Postal Code"),
    ("Country", "Country"),
    ("AddressType", "Address Type")
]

supplier_columns = [
    ("SupplierID", "Supplier ID"),
    ("Name", "Name"),
    ("PhoneNumber", "Phone Number"),
    ("Email", "Email"),
    ("AddressID", "Address ID")
]

material_columns = [
    ("MaterialID", "Material ID"),
    ("Name", "Name"),
    ("Type", "Type"),
    ("SupplierID", "Supplier ID")
]

supply_report_columns = [
    ("ReportID", "Report ID"),
    ("SupplierID", "Supplier ID"),
    ("MaterialID", "Material ID"),
    ("SupplyDate", "Supply Date")
]

manufacturer_columns = [
    ("ManufacturerID", "Manufacturer ID"),
    ("Name", "Name"),
    ("PhoneNumber", "Phone Number"),
    ("Email", "Email"),
    ("AddressID", "Address ID")
]

material_document_columns = [
    ("DocumentID", "Document ID"),
    ("MaterialID", "Material ID"),
    ("ManufacturerID", "Manufacturer ID"),
    ("Description", "Description"),
    ("CreatedDate", "Created Date")
]

product_columns = [
    ("ProductID", "Product ID"),
    ("Name", "Name"),
    ("Price", "Price"),
    ("Type", "Type"),
    ("Weight", "Weight"),
    ("Size", "Size"),
    ("ExpiryDate", "Expiry Date"),
    ("ManufacturerID", "Manufacturer ID")
]

distributor_columns = [
    ("DistributorID", "Distributor ID"),
    ("Name", "Name"),
    ("PhoneNumber", "Phone Number"),
    ("Email", "Email"),
    ("AddressID", "Address ID")
]

warehouse_columns = [
    ("WarehouseID", "Warehouse ID"),
    ("Name", "Name"),
    ("AddressID", "Address ID"),
    ("DistributorID", "Distributor ID"),
    ("Type", "Type"),
    ("Capacity", "Capacity")
]

inventory_columns = [
    ("InventoryID", "Inventory ID"),
    ("Quantity", "Quantity"),
    ("ExpiryDate", "Expiry Date"),
    ("ProductID", "Product ID"),
    ("WarehouseID", "Warehouse ID")
]

transporter_columns = [
    ("TransporterID", "Transporter ID"),
    ("Name", "Name"),
    ("ContactInfo", "Contact Info"),
    ("ModeOfTransport", "Mode Of Transport"),
    ("AddressID", "Address ID")
]

shipment_columns = [
    ("ShipmentID", "Shipment ID"),
    ("ShipmentDate", "Shipment Date"),
    ("EstimatedDeliveryTime", "Estimated Delivery Time"),
    ("Destination", "Destination"),
    ("OutOfShipmentTime", "Out Of Shipment Time"),
    ("Status", "Status"),
    ("MaximumCapacity", "Maximum Capacity")
]

shipment_transport_columns = [
    ("ShipmentTransportID", "Shipment Transport ID"),
    ("DistributorID", "Distributor ID"),
    ("TransporterID", "Transporter ID"),
    ("ShipmentID", "Shipment ID")
]

distributor_manufacturer_contract_columns = [
    ("ContractID", "Contract ID"),
    ("DistributorID", "Distributor ID"),
    ("ManufacturerID", "Manufacturer ID"),
    ("StartDate", "Start Date"),
    ("EndDate", "End Date")
]

retailer_columns = [
    ("RetailerID", "Retailer ID"),
    ("Name", "Name"),
    ("PhoneNumber", "Phone Number"),
    ("Email", "Email"),
    ("AddressID", "Address ID"),
    ("DistributorID", "Distributor ID")
]

transporter_contract_columns = [
    ("ContractID", "Contract ID"),
    ("TransporterID", "Transporter ID"),
    ("RetailerID", "Retailer ID"),
    ("StartDate", "Start Date"),
    ("EndDate", "End Date")
]

user_table_columns = [
    ("UserID", "User ID"),
    ("Name", "Name"),
    ("Email", "Email"),
    ("Contact", "Contact"),
    ("AddressID", "Address ID")
]

order_table_columns = [
    ("OrderID", "Order ID"),
    ("UserID", "User ID"),
    ("Quantity", "Quantity"),
    ("OrderDate", "Order Date")
]

# Start the application
if __name__ == "__main__":
    main_menu()
