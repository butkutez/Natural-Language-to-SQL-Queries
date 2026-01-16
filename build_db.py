import pandas as pd
import sqlite3
import os
import glob

# 1. Setting the source directory and target database path
data_path = "./data/simpsons_raw"
db_name = "simpsons.db"

def build_database():
    # 2. Initializing the SQLite engine and creating the database file
    conn = sqlite3.connect(db_name)
    print(f"Created database file: {db_name}")

    # 3. Searching recursively for all CSV files in the raw data directory
    csv_files = glob.glob(os.path.join(data_path, "**", "*.csv"), recursive=True)

    if not csv_files:
        print("No CSV files found! Check your folder name.")
        return

    for file_path in csv_files:
        # 4. Cleaning filenames to create standardized SQL table names
        raw_name = os.path.basename(file_path).replace(".csv", "")
        table_name = raw_name.replace("simpsons_", "")
        print(f"Importing {table_name}...")
        
        try:
            # 5. Loading data into memory while skipping malformed rows for stability
            df = pd.read_csv(file_path, on_bad_lines='skip')
            
            # 6. Mapping DataFrames to SQL tables and replacing existing data for a fresh build
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' is ready!")
            
        except Exception as e:
            print(f"Could not import {table_name}: {e}")

    # 7. Finalizing transactions and closing the database connection
    conn.close()
    print("\n Database Build Complete! You now have a simpsons.db file.")

if __name__ == "__main__":
    build_database()