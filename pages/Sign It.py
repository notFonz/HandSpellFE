import os
import requests
import numpy as np
import streamlit as st

from utils import get_image_and_prediction, plot_landmarks
from style import load_style

load_style()

st.set_page_config(
    page_title="HandSpell Sign It", page_icon=".images/le-wagon-logo.png", layout="wide"
)

st.logo(".images/le-wagon-logo.png", size="large")

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + "sign/"
API_PREDICT_ENDPOINT = API_BASE_URL + "predict"

LETTERS = list("ABCDEFGHIKLMNOPQRSTUVWXY")


def take_random_letter(LETTERS: list = LETTERS):
    random_letter = np.random.choice(LETTERS, 1)
    st.session_state.signit_letter = random_letter[0]


if "signit_letter" not in st.session_state:
    take_random_letter()

st.markdown(
    "# <span class='accent'>Sign</span>It",
    unsafe_allow_html=True,
)

st.subheader(
    "Try making the Sign of this letter: **{}**".format(st.session_state.signit_letter)
)


def compare_predict(correct_letter, uploaded_image):
    image, predicted_letter, prediction = get_image_and_prediction(uploaded_image)
    if image is not None:

        if prediction["confidence"] is not None:
            f = plot_landmarks(image, prediction["landmarks"])
            st.pyplot(f, width=300)
        else:
            st.image(image, width=200)

        if predicted_letter:
            prediction_confidence = prediction["confidence"]
            correct_letter = str(correct_letter)
            letter_idx = prediction["letters"].index(correct_letter)
            correct_letter_confidence = prediction["scores"][letter_idx]

            if prediction["letter"] == correct_letter:
                st.success(
                    f"That's right, you signed **{correct_letter}**, good fingerspelling !"
                )
                st.write(
                    f"Model is {prediction_confidence*100:.0f}% confident you signed **{predicted_letter}**."
                )
            else:
                st.error(
                    f"You signed **{predicted_letter}**, that's not a **{correct_letter}**... Try again !"
                )
                st.write(
                    f"Model is {int(round(prediction_confidence*100,0))}% confident you signed **{predicted_letter}**"
                )
                st.write(
                    f"... and {int(round(correct_letter_confidence*100, 0))}% confident you signed **{correct_letter}**."
                )


if st.button("Get a new random letter!"):

    take_random_letter(LETTERS)

    # RESET session state VARIABLES KIND SIR

    st.session_state.signit_upload = ""
    st.session_state.signit_source = ""
    st.session_state.signit_predicted_letter = ""
    st.session_state.signit_image_uploaded = None

left, right = st.columns([1, 1], gap="large")
with left:
    st.header("Image input")
    st.caption("Use good lighting and keep the whole hand and wrist visible.")
    source = st.radio(
        "Input", ["Upload image", "Take a photo"], horizontal=True, key="signit_source"
    )
    if "signit_source" in st.session_state:
        source = st.session_state.signit_source
        if source == "Upload image":
            uploaded = st.file_uploader(
                "Choose an image",
                width=300,
                type=["jpg", "jpeg", "png"],
                key="signit_image_upload",
            )

        else:
            uploaded = st.camera_input(
                "Take a hand sign photo", width=300, key="signit_image_webcam"
            )

        if uploaded is not None:
            st.session_state.signit_image_uploaded = uploaded
            st.image(uploaded)


with right:
    st.header("Translation results")
    if "signit_image_uploaded" in st.session_state:
        correct_letter = st.session_state.signit_letter
        uploaded_image = st.session_state.signit_image_uploaded
        compare_predict(correct_letter, uploaded_image)
