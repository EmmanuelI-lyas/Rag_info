"""
Professional Sidebar UI
"""

from datetime import datetime
import streamlit as st

from src.chat.storage import (
    list_chats,
    delete_chat,
)

from src.chat.manager import (
    get_current_chat,
    load_chat_session,
    new_chat,
)


# --------------------------------------------------
# Sidebar CSS
# --------------------------------------------------

st.markdown(
    """
<style>

/* Sidebar section labels */

section[data-testid="stSidebar"] .stCaption{
    font-size:11px;
    letter-spacing:1px;
    font-weight:600;
    opacity:.65;
}

/* Chat buttons */

section[data-testid="stSidebar"] .stButton>button{

    border:none !important;

    background:transparent !important;

    text-align:left !important;

    justify-content:flex-start !important;

    border-radius:10px !important;

    padding:.55rem .75rem !important;

    transition:.15s;

}

section[data-testid="stSidebar"] .stButton>button:hover{

    background:rgba(150,150,150,.12) !important;

}

/* Delete button */

section[data-testid="stSidebar"] .stButton>button[kind="secondary"]{

    justify-content:center !important;

}

</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Title
# --------------------------------------------------

def _format_title(chat):

    title = chat.get("title", "New Chat")

    if title == "New Chat" and chat.get("messages"):

        first = chat["messages"][0]

        if first.get("role") == "user":

            title = first.get("content", "New Chat")

    title = title.replace("\n", " ")

    if len(title) > 40:
        title = title[:40].rstrip() + "..."

    return title


# --------------------------------------------------
# Date
# --------------------------------------------------

def _chat_date(chat):

    for field in (
        "updated_at",
        "created_at",
        "timestamp",
    ):

        if chat.get(field):

            try:
                return datetime.fromisoformat(chat[field])

            except Exception:
                pass

    return datetime.now()


# --------------------------------------------------
# Chat Row
# --------------------------------------------------

def _render_chat(chat, current, prefix):

    title = _format_title(chat)

    is_current = (

        current is not None

        and chat["id"] == current["id"]

    )

    if is_current:

        title = "▍ " + title

    left, right = st.columns([9, 1])

    with left:

        if st.button(

            title,

            key=f"{prefix}_{chat['id']}",

            use_container_width=True,

        ):

            load_chat_session(chat["id"])

            st.rerun()

    with right:

        if st.button(

            "✕",

            key=f"delete_{chat['id']}",

            help="Delete chat",

        ):

            delete_chat(chat["id"])

            if is_current:

                new_chat()

            st.rerun()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

def render_sidebar():

    with st.sidebar:

        st.markdown("## 💬 Chats")

        if st.button(

            "＋ New Chat",

            use_container_width=True,

        ):

            new_chat()

            st.rerun()

        st.divider()

        chats = list_chats()

        current = get_current_chat()

        today = []

        yesterday = []

        older = []

        now = datetime.now().date()

        for chat in chats:

            delta = (

                now -

                _chat_date(chat).date()

            ).days

            if delta == 0:

                today.append(chat)

            elif delta == 1:

                yesterday.append(chat)

            else:

                older.append(chat)

        if today:

            st.caption("TODAY")

            for chat in today:

                _render_chat(

                    chat,

                    current,

                    "today",

                )

        if yesterday:

            st.markdown("")

            st.caption("YESTERDAY")

            for chat in yesterday:

                _render_chat(

                    chat,

                    current,

                    "yesterday",

                )

        if older:

            st.markdown("")

            st.caption("OLDER")

            for chat in older:

                _render_chat(

                    chat,

                    current,

                    "older",

                )

        st.divider()

        st.caption("Financial RAG Assistant")