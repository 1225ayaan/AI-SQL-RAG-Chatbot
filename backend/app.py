from fastapi import FastAPI
from pydantic import BaseModel

from backend.query_generator import generate_sql
from backend.database import execute_sql
from backend.security import is_safe_sql
from backend.rag import retrieve_context

app = FastAPI(
    title="AI SQL RAG Chatbot",
    version="1.0.0"
)

class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI SQL RAG Chatbot Running 🚀"
    }


@app.post("/generate-sql")
def generate(query: Query):

    try:
        # 1. RAG context
        context = retrieve_context(query.question)

        # 2. Generate SQL
        sql = generate_sql(query.question + "\n\nContext:\n" + context)

        # 3. Safety check
        if not is_safe_sql(sql):
            return {
                "error": "Unsafe SQL query detected",
                "sql": sql
            }

        # 4. Execute SQL
        result = execute_sql(sql)

        # 5. Response
        return {
            "question": query.question,
            "context": context,
            "sql": sql,
            "result": result
        }

    except Exception as e:
        return {
            "error": "Internal server error",
            "detail": str(e)
        }