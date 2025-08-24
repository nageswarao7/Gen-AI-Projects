import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the GenAI client
client = genai.Client()

st.set_page_config(page_title="AI Image Generator & Editor", layout="wide")

st.title("🎨 AI Image Generator & Editor")

# Tabs for Generation, Editing, and Image Q&A
tab1, tab2, tab3 = st.tabs(["🖼️ Image Generation", "✂️ Image Editing", "🔎 Image Understanding"])

# ------------------- TAB 1: IMAGE GENERATION -------------------
with tab1:
    st.subheader("Generate a new AI image from text")

    prompt = st.text_area("Enter your prompt:", 
                          "A 3D rendered pig with wings and a top hat flying over a futuristic city.")

    if st.button("Generate Image"):
        with st.spinner("Generating image..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

                for part in response.candidates[0].content.parts:
                    if part.text:
                        st.write(part.text)
                    elif part.inline_data:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image, caption="Generated Image", use_container_width=True)

                        # Download button
                        img_bytes = BytesIO()
                        image.save(img_bytes, format="PNG")
                        st.download_button(
                            label="Download Image",
                            data=img_bytes.getvalue(),
                            file_name="gemini_generated.png",
                            mime="image/png"
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ------------------- TAB 2: IMAGE EDITING -------------------
with tab2:
    st.subheader("Edit an existing image with AI")

    uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        input_image = Image.open(uploaded_file)
        st.image(input_image, caption="Uploaded Image", use_container_width=True)

    edit_prompt = st.text_area("Enter your edit instruction:", "Add a llama next to me")

    if st.button("Edit Image"):
        if uploaded_file is None:
            st.warning("Please upload an image before editing.")
        else:
            with st.spinner("Editing image..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-preview-image-generation",
                        contents=[edit_prompt, input_image],
                        config=types.GenerateContentConfig(
                            response_modalities=['TEXT', 'IMAGE']
                        )
                    )

                    for part in response.candidates[0].content.parts:
                        if part.text:
                            st.write(part.text)
                        elif part.inline_data:
                            edited_image = Image.open(BytesIO(part.inline_data.data))
                            st.image(edited_image, caption="Edited Image", use_container_width=True)

                            # Download option
                            img_bytes = BytesIO()
                            edited_image.save(img_bytes, format="PNG")
                            st.download_button(
                                label="Download Edited Image",
                                data=img_bytes.getvalue(),
                                file_name="gemini_edited.png",
                                mime="image/png"
                            )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ------------------- TAB 3: IMAGE Q&A -------------------
with tab3:
    st.subheader("Ask questions about an image")

    qna_file = st.file_uploader("Upload an image for Q&A (PNG/JPG)", type=["png", "jpg", "jpeg"])
    query = st.text_input("Enter your query", "Caption this image.")

    if qna_file is not None:
        st.image(qna_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Get Answer"):
        if qna_file and query:
            with st.spinner("Analyzing image..."):
                try:
                    image_bytes = qna_file.read()

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Part.from_bytes(
                                data=image_bytes,
                                mime_type="image/jpeg"
                            ),
                            query
                        ]
                    )

                    st.subheader("Response:")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please upload an image and enter a query.")
