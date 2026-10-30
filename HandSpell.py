import streamlit as st

from style import load_style

load_style()
st.html("""
<style>
h1 { font-size: 4rem !important; }
</style>
""")

st.logo(".images/le-wagon-logo.png", size="large")

st.set_page_config(
    page_title="HandSpell", page_icon=".images/le-wagon-logo.png", layout="wide"
)


st.markdown(
    """# Hand<span class='accent'>Spell</span>
    """,
    unsafe_allow_html=True,
)

st.markdown("""


## Reading hands, one letter at a time



HandSpell is an ASL (American Sign Language) translator. For now, it works with fingerspelling: the signed alphabet.

**On HandSpell you can translate, learn or play!**

Translation works both ways: from image to text, and from text to image.
""")

st.markdown(
    "And there's the <span class='accent'>Spell it</span> game, to test what you've learned!",
    unsafe_allow_html=True,
)

left, mid, right = st.columns([1, 10, 4])
with mid:
    st.image(
        ".images/Asl-sign-language-coloring-at-coloring-pages-for-kids-boys-dotcom.svg",
        caption="By Coloringbuddymike - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=24802810",
    )
