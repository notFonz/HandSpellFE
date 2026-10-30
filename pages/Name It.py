"""Name It page: guess which letter a random ASL sign image shows."""

import numpy as np
import streamlit as st

from style import load_style

load_style()

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + "sign/"
API_PREDICT_ENDPOINT = API_BASE_URL + "predict"

st.set_page_config(
    page_title="HandSpell Name It", page_icon=".images/le-wagon-logo.png", layout="wide"
)

st.logo(".images/le-wagon-logo.png", size="large")

st.markdown(
    "# <span class='accent'>Name</span>It",
    unsafe_allow_html=True,
)

LETTERS = list("ABCDEFGHIKLMNOPQRSTUVWXY")


def random_image():
    """Pick a random letter and its reference sign image.

    Returns:
        tuple[str, str]: The letter and the path to its sign image.
    """
    r = np.random.choice(len(LETTERS))
    letter = LETTERS[r]
    image_path = f".images/ASL Letter Reference/{letter}.jpg"
    return letter, image_path


left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("Guess what sign this is!")
    if st.button("Get a new sign !", width=400):

        st.session_state.nameit_true_letter, st.session_state.nameit_image_path = random_image()
        st.session_state.nameit_guess = ""  # clear the previous guess

    if "nameit_image_path" in st.session_state:
        st.image(st.session_state.nameit_image_path)

with right:

    st.subheader("Your guess:")
    if "nameit_image_path" in st.session_state:
        letter1 = st.text_input("", max_chars=1, width=50, key="nameit_guess")

        if letter1:
            true_letter = st.session_state.nameit_true_letter
            if letter1.lower() == true_letter.lower():
                st.success(f"You guessed it right, the sign represents **{true_letter}** !")
            else:
                st.error("You guessed it wrong, try again !")
