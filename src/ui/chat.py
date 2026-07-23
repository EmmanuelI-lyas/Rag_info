"""
Professional Chat UI
"""

import streamlit as st

from src.chat.manager import get_messages
from src.ui.source_card import render_sources


# --------------------------------------------------
# Welcome Screen
# --------------------------------------------------

def render_empty_chat():

    st.markdown(
        """
<div style="text-align:center;padding-top:70px;padding-bottom:30px;">

<h1 style="margin-bottom:10px;">
📊 Financial RAG Assistant
</h1>

<p style="
font-size:18px;
color:#8B949E;
margin-bottom:40px;
">

Ask questions about the BIS Annual Economic Report 2026.

</p>

</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💰 What is a Stablecoin?",
            use_container_width=True,
            key="example1",
        ):
            st.session_state.example_prompt = (
                "What is a stablecoin?"
            )

        if st.button(
            "🏦 Explain Unified Ledger",
            use_container_width=True,
            key="example2",
        ):
            st.session_state.example_prompt = (
                "Explain the Unified Ledger."
            )

    with col2:

        if st.button(
            "🤖 AI Investment Boom",
            use_container_width=True,
            key="example3",
        ):
            st.session_state.example_prompt = (
                "Explain the AI investment boom."
            )

        if st.button(
            "🌍 Global Growth Outlook",
            use_container_width=True,
            key="example4",
        ):
            st.session_state.example_prompt = (
                "Summarize the global growth outlook."
            )


# --------------------------------------------------
# Chat History
# --------------------------------------------------

def render_chat():

    messages = get_messages()

    if not messages:

        render_empty_chat()

        return
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    for message in messages:

        avatar = "👤" if message["role"] == "user" else "📊"

        with st.chat_message(

            message["role"],

            avatar=avatar,

        ):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                st.markdown("<br>", unsafe_allow_html=True)

                render_sources(

                    message.get("documents", [])

                )

                


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

def get_user_input():

    if "example_prompt" in st.session_state:

        prompt = st.session_state.example_prompt

        del st.session_state.example_prompt

        return prompt

    return st.chat_input(

        "Ask anything about the report..."

    )