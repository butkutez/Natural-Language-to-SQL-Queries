import sqlite3

def save_schema_to_file():
    # 1. I establish a link to the database to begin the extraction process
    conn = sqlite3.connect('simpsons.db')
    cursor = conn.cursor()
    
    # 2. I query the system catalog to identify all tables
    # sqlite_master stores the actual information about the database schema (built-in function)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # 3. I create a new text file to store the AI's "knowledge map"
    with open("database_schema.txt", "w", encoding="utf-8") as f:
        f.write("--- SIMPSONS DATABASE SCHEMA ---\n")
        
        for table in tables:
            table_name = table[0]
            f.write(f"\nTable: {table_name}\n")
            f.write("Columns:\n")
            

            # 4. I use the PRAGMA command to inspect the internal structure of each table
            # This allows me to pull column names and data types (metadata)
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                f.write(f"  - {col[1]} ({col[2]})\n") # col[1] is name, col[2] is type

    # 5. I close the database connection after completing the extraction
    conn.close()
    print("Schema has been saved to database_schema.txt")

if __name__ == "__main__":
    save_schema_to_file()