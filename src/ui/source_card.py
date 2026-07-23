"""
Professional Source Cards
"""

import streamlit as st


def render_sources(documents):

    if not documents:
        return

    st.markdown("##### Sources")

    for i, doc in enumerate(documents, start=1):

        # -----------------------------------------
        # Support dicts & LangChain Documents
        # -----------------------------------------

        if isinstance(doc, dict):

            metadata = doc.get("metadata", {})
            page_content = doc.get("page_content", "")

        else:

            metadata = doc.metadata
            page_content = doc.page_content

        page = metadata.get("page", "N/A")

        source = metadata.get("source", "Unknown")

        content_type = metadata.get("content_type", "Text").title()

        if source != "Unknown":
            source = source.split("/")[-1]

        preview = page_content.strip()

        if len(preview) > 280:
            preview = preview[:280].rstrip() + "..."

        with st.expander(

            f"📄 Page {page}   •   {content_type}",

            expanded=False,

        ):

            c1, c2 = st.columns([1, 5])

            with c1:

                st.caption("Document")

            with c2:

                st.caption(source)

            st.markdown("---")

            st.markdown(preview)

            if len(page_content) > len(preview):

                st.markdown("")

                st.caption("Full excerpt")

                st.write(page_content)