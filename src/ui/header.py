from pathlib import Path
import streamlit as st

from src.config import PDF_PATH


def render_header():

    pdf_name = Path(PDF_PATH).stem.replace("_", " ").title()

    st.markdown(
        f"""
<div style="text-align:center;margin-top:110px;">

<h1 style="font-size:46px;font-weight:700;margin-bottom:10px;">
📊 Financial RAG Assistant
</h1>

<p style="font-size:20px;color:#9CA3AF;">
Ask questions about the BIS Annual Economic Report 2026
</p>

<p style="font-size:15px;color:#6B7280;margin-top:20px;">
📄 {pdf_name}
</p>

</div>
""",
        unsafe_allow_html=True,
    )