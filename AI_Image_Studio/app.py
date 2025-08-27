import streamlit as st
from PIL import Image
from io import BytesIO
import core

st.set_page_config(page_title="🎨 AI Image Studio", layout="wide")

# ------------------- Custom CSS -------------------
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
            font-weight: bold;
        }
        .main-header {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.02);
            transition: all 0.2s ease-in-out;
        }
        .stSpinner > div > div {
            border-color: #4CAF50 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🎨 AI Image Studio</h1>", unsafe_allow_html=True)

# ------------------- Tabs -------------------
tab1, tab2, tab3 = st.tabs(["🖼️ Image Generation", "✂️ Image Editing", "🔎 Image Understanding"])

# ------------------- TAB 1: IMAGE GENERATION -------------------
with tab1:
    st.subheader("Generate a new AI image from text")
    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("📝 Enter your prompt below", expanded=True):
            prompt = st.text_area(
                "Describe the image you want to create:",
                "A 3D rendered pig with wings and a top hat flying over a futuristic city.",
                height=150
            )
            st.info("Tip: Be descriptive! Mention style, setting, and subject for better results.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ Generate Image"):
            with st.spinner("Generating image..."):
                result = core.generate_image(prompt)
                if result["status"] == "success":
                    st.success("Image generated successfully!")
                    st.session_state.gen_result = result
                else:
                    st.error(result["message"])
                    st.session_state.gen_result = None

    with col2:
        if "gen_result" in st.session_state and st.session_state.gen_result is not None:
            st.image(st.session_state.gen_result["image"], caption="Generated Image", use_container_width=True)

            d_col1, d_col2, d_col3 = st.columns([1, 1, 1])
            with d_col2:
                img_bytes = BytesIO()
                st.session_state.gen_result["image"].save(img_bytes, format="PNG")
                st.download_button(
                    label="⬇️ Download Image",
                    data=img_bytes.getvalue(),
                    file_name="gemini_generated.png",
                    mime="image/png"
                )
            if st.session_state.gen_result["text"]:
                st.markdown("---")
                st.caption("Model Notes:")
                st.write(st.session_state.gen_result["text"])

# ------------------- TAB 2: IMAGE EDITING -------------------
with tab2:
    st.subheader("Edit an existing image with AI")
    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])

        with st.expander("✏️ Enter your edit instruction", expanded=True):
            edit_prompt = st.text_area(
                "Describe the change you want to make:",
                "Add a llama next to me",
                height=100
            )
            st.info("Tip: The model works best with clear, specific instructions.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎨 Edit Image"):
            if uploaded_file is None:
                st.warning("Please upload an image before editing.")
            else:
                input_image = Image.open(uploaded_file)
                with st.spinner("Editing image..."):
                    result = core.edit_image(edit_prompt, input_image)
                    if result["status"] == "success":
                        st.success("Image edited successfully!")
                        st.session_state.edit_result = result
                    else:
                        st.error(result["message"])
                        st.session_state.edit_result = None

    with col2:
        if uploaded_file is not None:
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption="Uploaded Image", use_container_width=True)

        st.markdown("---")

        if "edit_result" in st.session_state and st.session_state.edit_result is not None:
            st.image(st.session_state.edit_result["image"], caption="Edited Image", use_container_width=True)
            d_col1, d_col2, d_col3 = st.columns([1, 1, 1])
            with d_col2:
                img_bytes = BytesIO()
                st.session_state.edit_result["image"].save(img_bytes, format="PNG")
                st.download_button(
                    label="⬇️ Download Edited Image",
                    data=img_bytes.getvalue(),
                    file_name="gemini_edited.png",
                    mime="image/png"
                )
            if st.session_state.edit_result["text"]:
                st.markdown("---")
                st.caption("Model Notes:")
                st.write(st.session_state.edit_result["text"])

# ------------------- TAB 3: IMAGE Q&A -------------------
with tab3:
    st.subheader("Ask questions about an image")
    col1, col2 = st.columns([1, 2])

    with col1:
        qna_file = st.file_uploader("Upload an image for Q&A (PNG/JPG)", type=["png", "jpg", "jpeg"], key="qna_uploader")
        st.markdown("<br>", unsafe_allow_html=True)
        query = st.text_input("Enter your query", "Caption this image.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Get Answer"):
            if qna_file and query:
                with st.spinner("Analyzing image..."):
                    image_bytes = qna_file.read()
                    result = core.understand_image(query, image_bytes)
                    if result["status"] == "success":
                        st.session_state.qna_result = result
                        st.success("Analysis complete!")
                    else:
                        st.error(result["message"])
                        st.session_state.qna_result = None
            else:
                st.warning("Please upload an image and enter a query.")

    with col2:
        if qna_file is not None:
            st.image(qna_file, caption="Uploaded Image", use_container_width=True)

        st.markdown("---")

        if "qna_result" in st.session_state and st.session_state.qna_result is not None:
            st.subheader("Response:")
            st.write(st.session_state.qna_result["text"])
