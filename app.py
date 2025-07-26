import streamlit as st
import openai
from llama_index.core import VectorStoreIndex, Document  # ✅ Corrected import
from reader import read_pdf, read_docx, read_txt


# 🔐 Set your OpenAI API key here
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Talk to Your Document 🤖")
st.title("📄 Talk to Your Document")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        file_text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        file_text = read_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        file_text = read_txt(uploaded_file)
    else:
        st.error("Unsupported file type!")
        st.stop()

    st.success("✅ File uploaded and read successfully!")

    user_question = st.text_input("Ask something about the document 👇")

    if user_question:
        with st.spinner("Thinking... 💭"):
            doc = Document(text=file_text)
            index = VectorStoreIndex.from_documents([doc])
            query_engine = index.as_query_engine()
            response = query_engine.query(user_question)
            st.write("🧠 Answer:", response.response)
