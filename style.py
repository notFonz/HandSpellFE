"""Shared CSS styling for the HandSpell pages."""

import streamlit as st


def load_style():
    """Inject the app's shared CSS into the current page.

    Defines the ``accent`` class used to colour words red and sets the font of
    ``h1`` headings.
    """
    st.html("""
    <style>
    .accent { color: #D23333; }
    h1 { font-family: 'Bricolage Grotesque', sans-serif !important; }
    </style>
    """)
