import os
import sqlite3
from google import genai  
from dotenv import load_dotenv

# Loading environment variables and authenticating the Gemini API client
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_schema_from_file():
    """Reading the database structural map to provide the LLM with table context."""
    if not os.path.exists("database_schema.txt"):
        return "Error: database_schema.txt not found."
    with open("database_schema.txt", "r") as f:
        return f.read()

def run_query(sql):
    """Executing the generated SQL against the SQLite database and fetching raw results."""
    conn = sqlite3.connect('simpsons.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        # Ensuring the database connection is closed safely
        conn.close()

def generate_sql(user_question):
    """Translating natural language into SQL by injecting the schema into the prompt."""
    schema = get_schema_from_file()

    # Engineering the prompt to enforce a 'SQL-only' output format
    prompt = f"Schema: {schema}\nRequest: {user_question}\nReturn only SQL."
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    
    # Sanitizing the response by stripping backticks and markdown formatting
    return response.text.strip().replace("```sql", "").replace("```", "")

def main():
    """Orchestrating the core application workflow."""
    print("--- 🍩 Simpsons AI Assistant 🍩 ---")
    question = input("Ask a question (e.g., 'Who is the wife of Homer?'): ")
    
    # Step A: Translating - Converting user input into a machine-readable query
    sql = generate_sql(question)
    print(f"\n[AI Generated SQL]:\n{sql}")
    
    # Step B: Querying - Pulling data from the Simpson's SQLite database
    results = run_query(sql)
    
    # Step C: Output & Persistence - Displaying results and logging the transaction
    print(f"\n[Results]:")
    if isinstance(results, list):
        for row in results:
            print(f" - {row}")
    else:
        print(results)

    # Appending the interaction to a log file for history tracking    
    with open("assignment_results.txt", "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nSQL: {sql}\nResult: {results}\n\n")

if __name__ == "__main__":
    main()