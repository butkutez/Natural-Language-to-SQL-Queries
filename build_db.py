import pandas as pd
import sqlite3
import os
import glob

# 1. Point to your local data folder
data_path = "./data/simpsons_raw"
db_name = "simpsons.db"

def build_database():
    # Connect to (or create) the SQLite database file
    conn = sqlite3.connect(db_name)
    print(f"Created database file: {db_name}")

    # Find all CSV files in your simpsons_data folder
    # We look inside the subfolders created by kagglehub
    csv_files = glob.glob(os.path.join(data_path, "**", "*.csv"), recursive=True)

    if not csv_files:
        print("No CSV files found! Check your folder name.")
        return

    for file_path in csv_files:
        # Get a clean table name (e.g., 'simpsons_characters.csv' -> 'characters')
        raw_name = os.path.basename(file_path).replace(".csv", "")
        table_name = raw_name.replace("simpsons_", "")
        print(f"Importing {table_name}...")
        
        try:
            # Read CSV - we use 'on_bad_lines' to skip messy rows
            df = pd.read_csv(file_path, on_bad_lines='skip')
            
            # Write to SQL (this creates the table automatically)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' is ready!")
            
        except Exception as e:
            print(f"Could not import {table_name}: {e}")

    conn.close()
    print("\n Database Build Complete! You now have a simpsons.db file.")

if __name__ == "__main__":
    build_database()