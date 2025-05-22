# frontend/streamlit_app.py
import streamlit as st
from rag.chat import stream_answer
import re

st.set_page_config(page_title="Asistente IRPF", layout="centered")
st.title("🤖 Asistente IRPF 2024")
st.markdown("_Haz una pregunta sobre el Manual práctico de Renta 2024_")

# Session state initialization
if "llm_answer" not in st.session_state:
    st.session_state.llm_answer = None
if "last_question" not in st.session_state:
    st.session_state.last_question = None

# Input
question = st.text_input("Tu pregunta:")

# On new question
if question and question != st.session_state.last_question:
    with st.spinner("Pensando..."):
        response = ""
        for chunk in stream_answer(question):
            response += chunk
        st.session_state.llm_answer = response
        st.session_state.last_question = question

# Display cached answer
if st.session_state.llm_answer:
    # def make_clickable(match):
    #     page = match.group(1)
    #     return f'<a href="#" onclick="window.parent.postMessage({{ type: \'pdfPage\', page: {page} }}, \'*\');">[p{page}]</a>'

    # html_answer = re.sub(r"\[p(\d+)\]", make_clickable, st.session_state.llm_answer)
    # st.markdown(html_answer, unsafe_allow_html=True)
    st.markdown(st.session_state.llm_answer)

st.markdown("Puedes navegar el manual de la renta 2024 con la siguiente herramienta:")
# PDF page input
page_num = 1 #st.number_input("Ir a página del PDF:", min_value=1, max_value=1000, value=1)

# Show embedded PDF
PDF_URL = "https://manuelescola.github.io/GenAI_IRPF_chatbot/RENTA_2024.pdf"
st.markdown(f"""
<iframe src="{PDF_URL}#page={page_num}" width="100%" height="600px"></iframe>
""", unsafe_allow_html=True)

# Add external download message
st.markdown("""
\n
**📄 Puedes descargar el manual completo en:**  
[https://sede.agenciatributaria.gob.es/Sede/manuales-practicos.html](https://sede.agenciatributaria.gob.es/Sede/manuales-practicos.html)
""")
