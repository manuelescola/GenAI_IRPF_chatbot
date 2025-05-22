# frontend/streamlit_app.py
import streamlit as st
from rag.chat import stream_answer
import re

st.set_page_config(page_title="Asistente IRPF", layout="centered")
st.title("🤖 Asistente IRPF 2024")
st.markdown("_Haz una pregunta sobre la renta en España_")

# Session state for storing selected page
if "selected_page" not in st.session_state:
    st.session_state.selected_page = None

question = st.text_input("Tu pregunta:")

if question:
    with st.spinner("Pensando..."):
        response = ""
        for chunk in stream_answer(question):
            response += chunk

        # Convert [pXXX] into clickable links
        def make_clickable(match):
            page = match.group(1)
            return f'<a href="#" onclick="window.parent.postMessage({{ type: \'pdfPage\', page: {page} }}, \'*\');">[p{page}]</a>'

        html_answer = re.sub(r"\[p(\d+)\]", make_clickable, response)
        st.markdown(html_answer, unsafe_allow_html=True)

# Handle PDF page viewing with a number input or query param
page_num = st.number_input("Ir a página del PDF:", min_value=1, max_value=1000, value=st.session_state.selected_page or 1)

# Show PDF viewer
PDF_URL = "https://manuelescola.github.io/GenAI_IRPF_chatbot/RENTA_2024.pdf"
pdf_url_with_page = f"{PDF_URL}#page={page_num}"
st.markdown(f"""
<iframe src="{pdf_url_with_page}" width="100%" height="600px"></iframe>
""", unsafe_allow_html=True)
