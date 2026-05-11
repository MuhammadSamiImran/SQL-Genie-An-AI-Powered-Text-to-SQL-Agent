from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_sql(user_question, schema):
    """
    Takes a natural language question and the database schema,
    sends both to the LLM, and returns a clean SQL query.
    """

    # This prompt is carefully engineered.
    # We give the LLM:
    # 1. A clear role (SQL expert)
    # 2. The exact schema so it knows what exists
    # 3. Strict rules to prevent dangerous queries
    # 4. The user's question
    # 5. A clear instruction on output format
    prompt = f"""You are an expert SQL assistant for a business analytics system.
You convert natural language questions into valid SQLite SELECT queries.

{schema}

STRICT RULES:
- Only generate SELECT queries. Never use INSERT, UPDATE, DELETE, DROP.
- Only use table names and column names that exist in the schema above.
- Always use proper JOINs when data from multiple tables is needed.
- Use aliases (AS) to make column names readable in results.
- For revenue calculations always use: products.price * orders.quantity
- Return ONLY the SQL query. No explanation. No markdown. No backticks.
- The query must end with a semicolon.

USER QUESTION:
{user_question}

SQL QUERY:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1)

    raw_response = response.choices[0].message.content.strip()
    sql = clean_sql(raw_response)
    return sql


def clean_sql(raw_text):
    """
    Removes markdown formatting that the LLM sometimes adds
    even when instructed not to.
    Examples of what this cleans:
```sql SELECT * FROM ... ```  →  SELECT * FROM ...
      `SELECT * FROM ...`           →  SELECT * FROM ...
    """
    
    cleaned = re.sub(r"```(?:sql)?", "", raw_text, flags=re.IGNORECASE)
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.strip()
    return cleaned


def generate_chart_suggestion(user_question, columns, row_count):
    """
    Asks the LLM what chart type best suits the query results.
    Returns one of: bar, line, pie, table
    This makes chart selection intelligent rather than hardcoded.
    """
    prompt = f"""Given a SQL query result with these column names: {columns}
and {row_count} rows of data, for the question: "{user_question}"

What is the BEST chart type to visualize this data?
Choose ONLY ONE from: bar, line, pie, table

Rules:
- bar   → comparisons between categories
- line  → trends over time (monthly, yearly)
- pie   → proportions or percentages
- table → when data has many columns or is not visual

Reply with ONLY the single word. Nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    suggestion = response.choices[0].message.content.strip().lower()

    if suggestion not in ["bar", "line", "pie", "table"]:
        suggestion = "bar"

    return suggestion