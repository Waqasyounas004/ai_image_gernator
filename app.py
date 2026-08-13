import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

from utils.prompt_utils import validate_prompt, clean_prompt
from services.groq_service import enhance_prompt
from services.huggingface_service import generate_image

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Theme, Pure White Spinner Loading Cycle & Header Dark Styling
st.markdown(
    """
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Main App Background - Rich Navy Backdrop */
    .stApp {
        background-color: #0B0F19;
        color: #CBD5E1;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    /* Container Bounds */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        max-width: 800px;
    }

    /* Title Styling */
    h1 {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.3rem;
    }

    .sub-title {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1.8rem;
    }

    /* Text Area Component */
    .stTextArea label {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        margin-bottom: 0.4rem !important;
    }

    .stTextArea textarea {
        background-color: #141B2D !important;
        color: #CBD5E1 !important;
        border: 1px solid #2A3348 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        padding: 0.9rem !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stTextArea textarea:focus {
        border: 1px solid #38BDF8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
    }

    .stTextArea textarea::placeholder {
        color: #64748B !important;
    }

    /* Primary Action Button (No Icon) */
    div.stButton > button {
        width: 100%;
        background-color: #4F46E5;
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.75em 1.5em;
        margin-top: 0.4rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
        cursor: pointer;
    }

    div.stButton > button:hover {
        background-color: #6366F1;
        box-shadow: 0 0 18px rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }

    /* Inline Spinner (NO BOX / NO WHITE RECTANGLES) - Pure White Stroke for Loading Cycle Only */
    div[data-testid="stSpinner"] {
        background-color: transparent !important;
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.8rem 0 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }

    div[data-testid="stSpinner"] p,
    div[data-testid="stSpinner"] span,
    div[data-testid="stSpinner"] label {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSpinner"] svg {
        stroke: #FFFFFF !important;
    }

    div[data-testid="stSpinner"] svg path,
    div[data-testid="stSpinner"] svg circle {
        stroke: #FFFFFF !important;
        fill: none !important;
    }

    /* Subheadings */
    h2, h3, p, label, .stMarkdown {
        color: #CBD5E1 !important;
    }

    /* Enhanced Prompt Display Box */
    .enhanced-card {
        background-color: #141B2D;
        border-left: 4px solid #38BDF8;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-top: 0.8rem;
        margin-bottom: 1.8rem;
        color: #CBD5E1;
        font-size: 0.98rem;
        line-height: 1.65;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }

    .prompt-header {
        color: #38BDF8;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }

    /* Generated Image Container with Soft Glowing Border */
    .image-glow-container {
        border: 2px solid #2DD4BF;
        border-radius: 16px;
        padding: 8px;
        box-shadow: 0 0 24px rgba(45, 212, 191, 0.35);
        background-color: #141B2D;
        margin-top: 0.8rem;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.title("AI Image Generator")
st.markdown(
    '<div class="sub-title">Transform your text ideas into detailed AI artwork.</div>',
    unsafe_allow_html=True,
)

# Main Form Area
prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Describe the image you want to generate...",
    height=110,
)

# Generate Image Button (No Icon)
generate_btn = st.button("Generate Image")

# Workflow Execution
if generate_btn:
    cleaned_input = clean_prompt(prompt)

    if not validate_prompt(cleaned_input):
        st.error("Please enter a prompt.")
    else:
        try:
            with st.spinner("Generating your image..."):
                enhanced_prompt = enhance_prompt(cleaned_input)
                generated_image = generate_image(enhanced_prompt)

                # Save generated image
                os.makedirs("generated_images", exist_ok=True)
                saved_path = f"generated_images/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                generated_image.save(saved_path)

            # Display Enhanced Prompt (No Icon)
            st.subheader("Enhanced Prompt")
            st.markdown(
                f"""
                <div class="enhanced-card">
                    <div class="prompt-header">Enhanced Prompt:</div>
                    {enhanced_prompt}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Display Generated Image (No Icon)
            st.subheader("Generated Image")
            st.markdown('<div class="image-glow-container">', unsafe_allow_html=True)
            st.image(generated_image, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.success(f"Image generated and saved to `{saved_path}`")

        except Exception:
            st.error(
                "Something went wrong while generating your image. "
                "Please check your API keys and try again."
            )
