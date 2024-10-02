import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
  

st.title("📝 File Q&A with ChatGPT")

def pdf_to_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

uploaded_file = st.file_uploader("Carregue um arquivo PDF", type=["pdf"])

if uploaded_file:
    text = pdf_to_text(uploaded_file)

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if "messages" not in st.session_state:
  st.session_state["messages"] = []
  
for message in st.session_state.messages:
  st.chat_message(message["role"]).write(message["content"])

if uploaded_file and question:
    article = text
    prompt = f"""Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}"""
    
    st.session_state.messages.append({"role":"user", "content":prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)