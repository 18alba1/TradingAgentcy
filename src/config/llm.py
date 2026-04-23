import streamlit as st
from langchain_openai import ChatOpenAI

def get_llm(temperature=0.2):
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=st.secrets["OPENAI_API_KEY"],
        temperature=temperature
    )