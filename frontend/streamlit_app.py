# frontend/streamlit_app.py
import streamlit as st
from rag.chat import stream_answer

st.set_page_config(page_title="Asistente IRPF", layout="centered")
st.title("🤖 Asistente IRPF 2024")
st.markdown("_Haz una pregunta sobre la renta en España_")

question = st.text_input("Tu pregunta:")

if question:
    with st.spinner("Pensando..."):
        response = ""
        for chunk in stream_answer(question):
            response += chunk
            st.markdown(response, unsafe_allow_html=True)