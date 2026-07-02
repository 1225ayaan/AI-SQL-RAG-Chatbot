import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI SQL RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL RAG Chatbot")
st.caption("Ask questions in English. AI will generate SQL, retrieve context, and execute the query.")

# -------------------------------
# Chat History
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input(
    "💬 Enter your question",
    placeholder="Example: Show all employees from Pune"
)

if st.button("🚀 Generate SQL"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:

        with st.spinner("🤖 AI is thinking..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/generate-sql",
                    json={
                        "question": question
                    }
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])

                else:

                    st.session_state.history.append(data)

            except Exception as e:
                st.error(f"Cannot connect to FastAPI server.\n\n{e}")

# -------------------------------
# Display Chat History
# -------------------------------

for chat in reversed(st.session_state.history):

    st.markdown("---")

    st.subheader("👤 Question")
    st.write(chat["question"])

    st.subheader("📚 Retrieved Context")
    st.code(chat["context"])

    st.subheader("🧠 Generated SQL")
    st.code(chat["sql"], language="sql")

    st.subheader("📊 Query Result")

    if len(chat["result"]) > 0:

        df = pd.DataFrame(chat["result"])

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="query_result.csv",
            mime="text/csv"
        )

    else:
        st.info("No records found.")