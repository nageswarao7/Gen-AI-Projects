import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

try:
    client = genai.Client(api_key= "AIzaSyB6K7d3wUm_qu9OSl8PDGwb4xsAYlyYmC4")
except Exception as e:
    raise RuntimeError(f"Failed to initialize GenAI client: {e}")

def generate_image(prompt: str) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        image = None
        text_response = ""
        for part in response.candidates[0].content.parts:
            if part.text:
                text_response = part.text
            elif part.inline_data:
                image = Image.open(BytesIO(part.inline_data.data))
        if image:
            return {"status": "success", "image": image, "text": text_response}
        else:
            return {"status": "error", "message": "No image data found in the response."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred during image generation: {str(e)}"}

def edit_image(prompt: str, input_image: Image.Image) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt, input_image],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        edited_image = None
        text_response = ""
        for part in response.candidates[0].content.parts:
            if part.text:
                text_response = part.text
            elif part.inline_data:
                edited_image = Image.open(BytesIO(part.inline_data.data))
        if edited_image:
            return {"status": "success", "image": edited_image, "text": text_response}
        else:
            return {"status": "error", "message": "No image data found in the response."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred during image editing: {str(e)}"}

def understand_image(query: str, image_bytes: bytes) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                query
            ]
        )
        return {"status": "success", "text": response.text}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred during image understanding: {str(e)}"}
