"""Spell It page: sign the letter missing from a word."""

import streamlit as st

from utils import (
    text_to_image_spellit,
    take_random_letter,
    take_random_word,
    plot_landmarks,
)
from utils import (
    get_image_and_prediction,
    list_words,
)  # word_with_removed_letter, #removed_letter
from style import load_style

load_style()

st.set_page_config(page_title="HandSpell Spell It")


st.markdown(
    "# <span class='accent'>Spell</span>It",
    unsafe_allow_html=True,
)
st.subheader("Complete the word with an image !")


if "idx" not in st.session_state:

    st.session_state.idx = 0

if "random_word" not in st.session_state:

    st.session_state.random_word = take_random_word(list_words)

    st.session_state.word_with_removed_letter, st.session_state.removed_letter = take_random_letter(
        st.session_state.random_word
    )

text_to_image_spellit(st.session_state.word_with_removed_letter)


def compare_predict(true_missing_letter, uploaded_image):
    """Predict the letter in an image and check it against the missing letter.

    Shows the image with its hand landmarks, then a success or error message
    and the model's confidence in its prediction.

    Args:
        true_missing_letter: The upper-case letter removed from the word.
        uploaded_image: The Streamlit ``UploadedFile`` with the user's sign,
            or None.
    """
    image, predicted_letter, prediction = get_image_and_prediction(uploaded_image)
    if image is not None:

        if prediction["confidence"] is not None:
            f = plot_landmarks(image, prediction["landmarks"])
            st.pyplot(f, width=300)
        else:
            st.image(image, width=200)

        if predicted_letter:
            prediction_confidence = prediction["confidence"]
            if prediction["letter"] == true_missing_letter:
                st.success(
                    "That's right, word was missing a "
                    + f"**{true_missing_letter}**, good fingerspelling !"
                )
            else:
                st.error(
                    f"You signed **{predicted_letter}**" + ", it's not quite right. Try again !"
                )
            st.write(
                f"Model is {prediction_confidence*100:.0f}% "
                f"confident you signed **{predicted_letter}**."
            )


left, right = st.columns([1, 1], gap="large")
with left:
    st.header("Image input")
    st.caption("Use good lighting and keep the whole hand and wrist visible.")

    source = st.radio("Input", ["Upload image", "Take a photo"], horizontal=True)
    uploaded = (
        st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], key="single_upload")
        if source == "Upload image"
        else st.camera_input("Take a hand sign photo")
    )
    if uploaded is not None:
        st.session_state.readit_image_uploaded = uploaded
        st.image(uploaded)

with right:
    st.header("Translation results")
    compare_predict(st.session_state.removed_letter, uploaded)

if st.button("Refresh"):

    st.session_state.idx = (st.session_state.idx + 1) % len(list_words)

    st.session_state.random_word = take_random_word(list_words)

    st.session_state.word_with_removed_letter, st.session_state.removed_letter = take_random_letter(
        st.session_state.random_word
    )

    st.rerun()
