"""Learn It page: show the ASL sign for a letter the user types."""

import requests
import streamlit as st

from style import load_style

load_style()

st.set_page_config(
    page_title="HandSpell Learn It",
    page_icon=".images/le-wagon-logo.png",
    layout="wide",
)

st.logo(".images/le-wagon-logo.png", size="large")

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + "sign/"
API_PREDICT_ENDPOINT = API_BASE_URL + "predict"

st.markdown(
    "# <span class='accent'>Learn</span>It",
    unsafe_allow_html=True,
)
st.subheader("Input a Letter to get its Sign Language gesture !")

LETTERS = list("ABCDEFGHIKLMNOPQRSTUVWXY")

letter = st.text_input("Letter", max_chars=1, width=50)

if letter:

    letter = letter.upper()

    if letter in LETTERS:
        st.write("Pumba approves :sunglasses:")

        try:
            with st.spinner("Getting image..."):
                response = requests.get(API_SIGN_ENDPOINT + letter, timeout=120)

            if response.status_code == 200:
                result = st.image(response.content)
                # st.success(f"Predicted letter: {result['letter']}")
                # st.write(f"Model score: {result['confidence']:.1%}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except (ValueError, KeyError, TypeError) as e:
            st.write(e)
            st.error("The prediction service returned an invalid response.")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            st.stop()

    else:
        st.write("Pumba is telling you to try a different letter -_-")
