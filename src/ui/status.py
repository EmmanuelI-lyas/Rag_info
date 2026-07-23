"""
Professional Status UI

Displays progress while the RAG pipeline runs.
"""

import streamlit as st


class StatusIndicator:

    def __init__(self):

        self.status = st.status(

            "Processing request...",

            expanded=False,

        )

    # --------------------------------------------------
    # Pipeline Updates
    # --------------------------------------------------

    def update(self, message: str):

        self.status.write(message)

    # --------------------------------------------------
    # Completed
    # --------------------------------------------------

    def success(self, message="Response generated"):

        self.status.update(

            label=message,

            state="complete",

            expanded=False,

        )

    # --------------------------------------------------
    # Error
    # --------------------------------------------------

    def error(self, message: str):

        self.status.update(

            label=message,

            state="error",

            expanded=True,

        )

    # --------------------------------------------------
    # Warning
    # --------------------------------------------------

    def warning(self, message: str):

        self.status.update(

            label=message,

            state="running",

            expanded=True,

        )

    # --------------------------------------------------
    # Remove
    # --------------------------------------------------

    def clear(self):

        self.status.empty()