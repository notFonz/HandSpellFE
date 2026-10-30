import streamlit as st


def load_style():
    st.html("""
    <style>
    .accent { color: #D23333; }
    h1 { font-family: 'Bricolage Grotesque', sans-serif !important; }
    </style>
    """)
