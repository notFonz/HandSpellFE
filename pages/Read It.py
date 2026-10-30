import streamlit as st


from utils import get_image_and_prediction, CONFIDENCE_THRESHOLD, plot_landmarks

from style import load_style

load_style()

st.set_page_config(
    page_title="HandSpell Read It", page_icon=".images/le-wagon-logo.png", layout="wide"
)

st.logo(".images/le-wagon-logo.png", size="large")


def render_result(result, predicted_letter, threshold=CONFIDENCE_THRESHOLD):
    letter = "?"
    if (result["confidence"] is not None) and result["confidence"] > threshold:
        letter = predicted_letter

    if letter == "?":
        st.warning("Confidence is too low... Try again.")
    a, b = st.columns(2)
    with a:
        st.metric("Predicted sign", letter if letter != "?" else "—")
    with b:
        score = result["confidence"]
        st.metric("Model score", "—" if score is None else f"{score:.1%}")
    if result["confidence"] is not None:
        st.progress(float(result["confidence"]))


st.markdown(
    "# <span class='accent'>Read</span>It",
    unsafe_allow_html=True,
)
st.subheader("Hand Sign Translation")


st.divider()
left, right = st.columns([1, 1], gap="large")

with left:
    st.header("Image input")
    st.caption("Use good lighting and keep the whole hand and wrist visible.")

    source = st.radio(
        "Input", ["Upload image", "Take a photo"], horizontal=True, key="readit_source"
    )

    if "readit_source" in st.session_state:
        source = st.session_state.readit_source
        if source == "Upload image":
            uploaded = st.file_uploader(
                "Choose an image",
                width=300,
                type=["jpg", "jpeg", "png"],
                key="readit_image_upload",
            )

        else:
            uploaded = st.camera_input(
                "Take a hand sign photo", width=300, key="readit_image_webcam"
            )

        if uploaded is not None:
            st.session_state.readit_image_uploaded = uploaded
            st.image(uploaded)


with right:
    st.header("Translation results")
    if "readit_image_uploaded" in st.session_state:
        uploaded_image = st.session_state.readit_image_uploaded
        image, letter1, prediction = get_image_and_prediction(uploaded_image)

        if image is not None:
            st.session_state.readit_image = image

            if prediction["confidence"] is not None:
                st.session_state.readit_letter = letter1
                st.session_state.results = prediction

                f = plot_landmarks(image, prediction["landmarks"])
                st.pyplot(f, width=300)
            else:
                st.image(image, width=200)

    results = st.session_state.get("results", [])

    if not results:
        st.info("Choose your images and select Translate.")
    elif results:
        letter2 = st.session_state.readit_letter
        render_result(results, letter2)
        with st.expander("All API responses"):
            st.json(results)
