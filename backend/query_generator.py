import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_sql(question: str):
    prompt = f"""
You are an expert SQL developer.

Database Table:

employees(
    id,
    name,
    age,
    department,
    salary,
    city
)

Convert the following English question into ONLY SQL.

Question:
{question}

Return ONLY the SQL query.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    sql = response.text.strip()

    # Remove markdown formatting
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    # Remove trailing semicolon if needed
    sql = sql.strip()

    return sql