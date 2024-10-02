import streamlit as st
from openai import OpenAI
import os

st.title("ChatGPT Like")

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

if "openai_model" not in st.session_state:
  st.session_state["openai_model"] = "gpt-4.0"

if "messages" not in st.session_state:
  st.session_state["messages"] = []
  
for message in st.session_state.messages:
  st.chat_message(message["role"]).write(message["content"])

    
if prompt := st.chat_input("What`s up?"):
  instructions = "Responda as perguntas do usuário de maneira informal"
  
  st.session_state.messages.append({"role":"user", "content":prompt})
  st.chat_message("user").write(prompt)
  
  response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
  msg = response.choices[0].message.content
  st.session_state.messages.append({"role": "assistant", "content": msg})
  st.chat_message("assistant").write(msg)