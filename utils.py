"""Shared helpers for the HandSpell Streamlit pages.

Wraps calls to the HandSpell backend API (sign images and letter predictions),
image loading, the Spell It word game logic, and plotting of detected hand
landmarks.

Attributes:
    API_BASE_URL (str): Base URL of the HandSpell API, read from Streamlit secrets.
    API_SIGN_ENDPOINT (str): Endpoint returning the sign image for a letter.
    API_PREDICT_ENDPOINT (str): Endpoint predicting the letter signed in an image.
    CONFIDENCE_THRESHOLD (float): Minimum model confidence to accept a prediction.
    list_words (list[str]): Words used by the Spell It game.
    HAND_CONNECTIONS (list[tuple[int, int]]): Pairs of hand landmark indices
        joined by a line when drawing the hand skeleton.
"""

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
    """Open an uploaded image and fix its orientation from EXIF data.

    Args:
        upload: A file path or file-like object containing the image.

    Returns:
        PIL.Image.Image: The image, rotated according to its EXIF orientation tag.

    Raises:
        PIL.UnidentifiedImageError: If the file is not a readable image.
    """
    return ImageOps.exif_transpose(Image.open(upload))


def get_uploaded_image(uploaded_file):
    """Load an uploaded file as an image, stopping the page if it is invalid.

    Shows a Streamlit error and stops the script run when the file cannot be
    read as an image.

    Args:
        uploaded_file: The Streamlit ``UploadedFile`` from a file uploader or
            camera input, or None if nothing was uploaded.

    Returns:
        PIL.Image.Image | None: The oriented image, or None if no file was given.
    """
    processed_upload = None
    if uploaded_file is not None:
        try:
            processed_upload = process_image_for_show(uploaded_file)
        except (UnidentifiedImageError, OSError, ValueError):
            st.error("Could not read this files. Please try a different image!")
            st.stop()
    return processed_upload


def take_random_word(list_of_words: list):
    """Pick the current word of the Spell It game.

    The word is chosen from ``st.session_state.idx``, so it advances through the
    list in order as the index changes rather than being truly random.

    Args:
        list_of_words: The words to choose from.

    Returns:
        str: The word at the session index, wrapping around the list length.
    """
    idx = st.session_state.idx

    return list_of_words[idx % len(list_of_words)]


def take_random_letter(word):
    """Hide a random letter of a word behind an underscore.

    Args:
        word: The word to remove a letter from.

    Returns:
        tuple[str, str]: The word with one letter replaced by ``"_"``, and the
        removed letter in upper case.
    """
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
    """Render a word as a row of sign images, one per letter.

    Each letter's sign image is fetched from the API; an underscore is shown as
    a question mark image.

    Args:
        word: The word to render, possibly containing ``"_"`` for a hidden letter.

    Returns:
        streamlit.delta_generator.DeltaGenerator: The container holding the images.
    """
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
    """Load an uploaded image and ask the API which letter it signs.

    Shows a Streamlit warning when no hand is detected and an error when the
    API returns a non-200 status.

    Args:
        uploaded_file: The Streamlit ``UploadedFile`` to classify, or None.

    Returns:
        tuple: A 3-tuple ``(image, predicted_letter, prediction)`` where
        ``image`` is the oriented ``PIL.Image.Image`` (None if no file),
        ``predicted_letter`` is the predicted letter (None if no hand was
        detected or the request failed), and ``prediction`` is the API's JSON
        response as a dict (None if the request failed).
    """
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
    """Draw the detected hand skeleton on top of an image.

    Args:
        image: The PIL image the landmarks were detected on.
        landmarks: Hand landmarks, each a dict with ``"x"`` and ``"y"``
            coordinates normalised to the [0, 1] range.

    Returns:
        matplotlib.figure.Figure: A figure showing the image with landmarks
        and their connections drawn over it.
    """
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
