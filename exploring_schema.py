import sqlite3

def save_schema_to_file():
    conn = sqlite3.connect('simpsons.db')
    cursor = conn.cursor()
    
    # Get all table names
    # sqlite_master stores the actual information about the database schema (built-in function)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Open the text file in 'write' mode
    with open("database_schema.txt", "w", encoding="utf-8") as f:
        f.write("--- SIMPSONS DATABASE SCHEMA ---\n")
        
        for table in tables:
            table_name = table[0]
            f.write(f"\nTable: {table_name}\n")
            f.write("Columns:\n")
            
            # Get column details
            # # PRAGMA is a special SQLite command used to inspect the database structure (metadata) rather than the data itself.
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                # col[1] is name, col[2] is type
                f.write(f"  - {col[1]} ({col[2]})\n")
    
    conn.close()
    print("Schema has been saved to database_schema.txt")

if __name__ == "__main__":
    save_schema_to_file()