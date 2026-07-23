"""
Chat Manager

Responsible for:

1. Current active chat
2. Loading chats
3. Saving messages
4. Switching chats
5. Converting LangChain Documents to JSON-safe data
6. Automatically naming chats from the first user question
"""

import streamlit as st

from src.chat.storage import (
    create_chat,
    save_chat,
    load_chat,
    list_chats,
)


# --------------------------------------------------
# Convert Documents to JSON-safe dictionaries
# --------------------------------------------------

def serialize_documents(documents):

    serialized = []

    for doc in documents:

        # Already serialized dictionary
        if isinstance(doc, dict):

            serialized.append(doc)

        # LangChain Document object
        else:

            serialized.append({

                "page_content": doc.page_content,

                "metadata": doc.metadata

            })

    return serialized


# --------------------------------------------------
# Initialize
# --------------------------------------------------

def initialize_chat_manager():
    """
    Initialize with no active chat.

    A chat is created only when the user sends
    the first message.
    """

    if "current_chat" not in st.session_state:

        st.session_state.current_chat = None

        st.session_state.messages = []


# --------------------------------------------------
# Get Current Chat
# --------------------------------------------------

def get_current_chat():

    return st.session_state.current_chat


# --------------------------------------------------
# Get Messages
# --------------------------------------------------

def get_messages():

    return st.session_state.messages


# --------------------------------------------------
# Load Existing Chat
# --------------------------------------------------

def load_chat_session(chat_id):

    chat = load_chat(chat_id)

    if chat is None:

        return

    st.session_state.current_chat = chat

    st.session_state.messages = chat["messages"]


# --------------------------------------------------
# Create New Chat
# --------------------------------------------------

def new_chat():
    """
    Start a blank conversation.

    The actual chat object will be created when
    the first user message is sent.
    """

    st.session_state.current_chat = None

    st.session_state.messages = []


# --------------------------------------------------
# Save Current Chat
# --------------------------------------------------

def save_current_chat():

    chat = st.session_state.current_chat

    if chat is None:

        return

    chat["messages"] = st.session_state.messages

    save_chat(chat)


# --------------------------------------------------
# Add User Message
# --------------------------------------------------

def add_user_message(message):

    # --------------------------------------------------
    # Create chat only when the first message arrives
    # --------------------------------------------------

    if st.session_state.current_chat is None:

        chat = create_chat()

        st.session_state.current_chat = chat

    # --------------------------------------------------
    # Add message
    # --------------------------------------------------

    st.session_state.messages.append({

        "role": "user",

        "content": message

    })

    # --------------------------------------------------
    # Automatically name chat from first question
    # --------------------------------------------------

    chat = st.session_state.current_chat

    if (

        len(st.session_state.messages) == 1

        and chat.get("title") in [

            None,

            "",

            "New Chat"

        ]

    ):

        title = message.strip()

        if len(title) > 40:

            title = title[:40].strip() + "..."

        chat["title"] = title

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    save_current_chat()


# --------------------------------------------------
# Add Assistant Message
# --------------------------------------------------

def add_assistant_message(

    message,

    provider,

    model,

    documents

):

    serialized_documents = serialize_documents(

        documents

    )

    st.session_state.messages.append({

        "role": "assistant",

        "content": message,

        "provider": provider,

        "model": model,

        "documents": serialized_documents

    })

    save_current_chat()