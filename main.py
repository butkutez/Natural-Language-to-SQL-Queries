import os
import sqlite3
from google import genai  
from dotenv import load_dotenv

# 1. Initialization
load_dotenv()

# We explicitly pass the key here to avoid the 'DefaultCredentialsError'
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# CHECK WHY THIS IS IMPORTANT
def get_schema_from_file():
    """Reads the schema we saved to the txt file."""
    if not os.path.exists("database_schema.txt"):
        return "Error: database_schema.txt not found."
    with open("database_schema.txt", "r") as f:
        return f.read()

def run_query(sql):
    """Executes the SQL and returns results."""
    conn = sqlite3.connect('simpsons.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        conn.close()

def generate_sql(user_question):
    schema = get_schema_from_file()
    prompt = f"Schema: {schema}\nRequest: {user_question}\nReturn only SQL."
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    return response.text.strip().replace("```sql", "").replace("```", "")

def main():
    print("--- 🍩 Simpsons AI Assistant 🍩 ---")
    question = input("Ask a question (e.g., 'Who is the wife of Homer?'): ")
    
    # Step A: Get SQL
    sql = generate_sql(question)
    print(f"\n[AI Generated SQL]:\n{sql}")
    
    # Step B: Run Query
    results = run_query(sql)
    
    # Step C: Display & Log
    print(f"\n[Results]:")
    if isinstance(results, list):
        for row in results:
            print(f" - {row}")
    else:
        print(results)
        
    with open("assignment_results.txt", "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nSQL: {sql}\nResult: {results}\n\n")

if __name__ == "__main__":
    main()