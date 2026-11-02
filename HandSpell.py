"""Entrypoint of the HandSpell web app: shared setup and page menu."""

import streamlit as st

from style import load_style

st.set_page_config(page_icon=".images/le-wagon-logo.png", layout="wide")

load_style()

st.logo(".images/le-wagon-logo.png", size="large")

pages = [
    st.Page("pages/home.py", title="HandSpell", default=True),
    st.Page("pages/read_it.py", title="Read It", url_path="Read_It"),
    st.Page("pages/learn_it.py", title="Learn It", url_path="Learn_It"),
    st.Page("pages/name_it.py", title="Name It", url_path="Name_It"),
    st.Page("pages/sign_it.py", title="Sign It", url_path="Sign_It"),
    st.Page("pages/spell_it.py", title="Spell It", url_path="Spell_It"),
]

st.navigation(pages).run()
