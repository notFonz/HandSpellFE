import requests
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image, ImageOps, UnidentifiedImageError

API_BASE_URL = st.secrets["API_URL"]
API_SIGN_ENDPOINT = API_BASE_URL + "sign/"
API_PREDICT_ENDPOINT = API_BASE_URL + "predict"

CONFIDENCE_THRESHOLD = 0.3

list_words = ["Hello", "Love", "Website", "No", "Yes"]

HAND_CONNECTIONS = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),  # thumb
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),  # index
    (9, 10),
    (10, 11),
    (11, 12),  # middle
    (13, 14),
    (14, 15),
    (15, 16),  # ring
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),  # pinky
    (5, 9),
    (9, 13),
    (13, 17),  # palm
]


def process_image_for_show(upload):
    return ImageOps.exif_transpose(Image.open(upload))


def get_uploaded_image(uploaded_file):
    processed_upload = None
    if uploaded_file is not None:
        try:
            processed_upload = process_image_for_show(uploaded_file)
        except (UnidentifiedImageError, OSError, ValueError):
            st.error("Could not read this files. Please try a different image!")
            st.stop()
    return processed_upload


def take_random_word(list_of_words: list):

    idx = st.session_state.idx

    return list_of_words[idx % len(list_of_words)]


def take_random_letter(word):

    r = np.random.choice(len(word))

    removed_letter = word[r]
    removed_letter = removed_letter.upper()

    random_word = []
    for index, letter in enumerate(list(word)):
        if index == r:
            random_word.append("_")
        else:
            random_word.append(letter)

    return "".join(random_word), removed_letter


def text_to_image_spellit(word: str):

    container = st.container(horizontal=True, wrap=True, border=True)

    with container:
        for letter in word:
            letter = letter.upper()
            if letter == "_":
                st.image(".images/question mark.png", caption="?", width=64)

            else:
                response = requests.get(API_SIGN_ENDPOINT + letter, timeout=120)
                st.image(response.content, caption=f"**{letter}**", width=64)

    return container


def get_image_and_prediction(uploaded_file):

    processed_upload = get_uploaded_image(uploaded_file)
    predicted_letter = None
    prediction = None

    if processed_upload is not None:
        with st.spinner("Reading hand signs…"):
            response = requests.post(
                API_PREDICT_ENDPOINT,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                },
                timeout=120,
            )
        if response.status_code == 200:
            prediction = response.json()
            if prediction["confidence"] is None:
                st.warning("No hand/sign detected. Try a clear photo of the whole hand.")
            else:
                predicted_letter = prediction["letter"]
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    return processed_upload, predicted_letter, prediction


def plot_landmarks(image: Image, landmarks: list) -> plt.figure:

    img = np.array(image.convert("RGB"))
    h, w = img.shape[:2]

    f, ax = plt.subplots()
    ax.imshow(img)
    hand = landmarks

    xs = [lm["x"] * w for lm in hand]
    ys = [lm["y"] * h for lm in hand]

    for a, b in HAND_CONNECTIONS:
        ax.plot([xs[a], xs[b]], [ys[a], ys[b]], color="white", linewidth=2)
    ax.scatter(xs, ys, s=20, c="cyan", zorder=3)

    ax.set_axis_off()
    return f
