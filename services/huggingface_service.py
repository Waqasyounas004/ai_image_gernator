import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


def generate_image(enhanced_prompt: str, model: str = "black-forest-labs/FLUX.1-schnell"):
    """
    Generates an image from an enhanced prompt using Hugging Face InferenceClient.

    Args:
        enhanced_prompt (str): The detailed image prompt.
        model (str): Hugging Face model repository ID.

    Returns:
        PIL.Image.Image: Generated PIL Image object.
    """
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "HF_TOKEN" in st.secrets:
                hf_token = st.secrets["HF_TOKEN"]
        except Exception:
            pass

    if not hf_token:
        raise ValueError(
            "HF_TOKEN is not set. Please add HF_TOKEN to your Streamlit App Secrets "
            "(App Settings -> Secrets) or set it in your local .env file."
        )

    client = InferenceClient(
        provider="auto",
        api_key=hf_token,
    )

    try:
        image = client.text_to_image(
            enhanced_prompt,
            model=model,
        )
        return image
    except Exception as e:
        raise RuntimeError(f"Hugging Face image generation failed: {e}") from e
