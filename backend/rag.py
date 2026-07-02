import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

os.environ["TOKENIZERS_PARALLELISM"] = "false"

vectorstore = None


def load_vectorstore():
    global vectorstore

    if vectorstore is not None:
        return vectorstore

    schema_path = Path(__file__).resolve().parent.parent / "docs" / "schema.txt"

    with open(schema_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(chunks, embeddings)

    return vectorstore


def retrieve_context(question: str):

    db = load_vectorstore()

    docs = db.similarity_search(question, k=2)

    return "\n".join(doc.page_content for doc in docs)