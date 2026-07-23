"""
Financial RAG Application
"""

import streamlit as st

from src.graph.workflow import build_graph

from src.ui.sidebar import render_sidebar
from src.ui.chat import (
    render_chat,
    get_user_input,
)

from src.chat.manager import (
    initialize_chat_manager,
    add_user_message,
    add_assistant_message,
)

from src.ui.status import StatusIndicator


# =====================================================
# Streamlit Configuration
# =====================================================

st.set_page_config(
    page_title="Financial RAG Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# Global CSS
# =====================================================

st.markdown(
    """
<style>

/* -----------------------------------------
   Hide Streamlit Menu/Footer
----------------------------------------- */

#MainMenu{
    display:none;
}

footer{
    display:none;
}

/* -----------------------------------------
   Main Container
----------------------------------------- */

.block-container{

    max-width:900px;

    margin:auto;

    padding-top:1.5rem;

    padding-bottom:7rem;

}

/* -----------------------------------------
   Chat Messages
----------------------------------------- */

.stChatMessage{

    padding-top:.4rem;

    padding-bottom:.4rem;

}

.stMarkdown p{

    line-height:1.75;

    font-size:16px;

}

/* -----------------------------------------
   Chat Input
----------------------------------------- */

.stChatInput{

    padding-top:1rem;

}

</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# Load Graph Once
# =====================================================

@st.cache_resource
def load_graph():

    return build_graph()


graph = load_graph()

# =====================================================
# Initialize Chat
# =====================================================

initialize_chat_manager()

# =====================================================
# Sidebar
# =====================================================

render_sidebar()

# =====================================================
# Chat UI
# =====================================================

render_chat()

# =====================================================
# User Input
# =====================================================

question = get_user_input()

if question:

    # Save user message
    add_user_message(question)
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # Show pipeline progress
    status = StatusIndicator()

    # -------------------------------------------------
    # Execute LangGraph
    # -------------------------------------------------

    result = graph.invoke(

        {
            "question": question,
            "status_callback": status.update,
            "stream_callback": None,
        }

    )

    # -------------------------------------------------
    # Success
    # -------------------------------------------------

    if result["success"]:

        status.clear()

        add_assistant_message(

            message=result["answer"],

            provider=result["provider"],

            model=result["model"],

            documents=result["reranked_documents"],

        )

        # Refresh chat from stored history
        st.rerun()

    # -------------------------------------------------
    # Error
    # -------------------------------------------------

    else:

        status.error("Unable to generate a response.")

        st.error(result["error"])