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

    /* Hide top Streamlit colored decoration bar if present */
    div[data-testid="stDecoration"] {
        display: none !important;
        height: 0px !important;
    }

    /* Top Streamlit Header Bar */
    header[data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid #2A3348 !important;
    }

    /* Target all header containers, toolbar & status widgets to ensure transparent backgrounds */
    header[data-testid="stHeader"] *,
    div[data-testid="stStatusWidget"],
    div[data-testid="stStatusWidget"] *,
    div[data-testid="stToolbar"],
    div[data-testid="stToolbar"] *,
    div[data-testid="stAppDeployButton"],
    div[data-testid="stAppDeployButton"] * {
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        outline: none !important;
    }

    /* Remove outline boxes, borders, and frames from all header buttons & toolbar icons */
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] [role="button"],
    div[data-testid="stToolbar"] button,
    div[data-testid="stToolbar"] [role="button"],
    div[data-testid="stHeaderIconButton"],
    div[data-testid="stMainMenu"] button,
    div[data-testid="stAppDeployButton"] button,
    div[data-testid="stActionButton"] button {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }

    header[data-testid="stHeader"] button:focus,
    header[data-testid="stHeader"] button:active,
    header[data-testid="stHeader"] button:hover,
    div[data-testid="stToolbar"] button:focus,
    div[data-testid="stToolbar"] button:active,
    div[data-testid="stToolbar"] button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border: none !important;
        border-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Make all SVG icons, paths, circles, polygons, lines, and shapes in Header pure white and fully visible */
    header[data-testid="stHeader"] svg,
    header[data-testid="stHeader"] svg *,
    div[data-testid="stStatusWidget"] svg,
    div[data-testid="stStatusWidget"] svg *,
    div[data-testid="stToolbar"] svg,
    div[data-testid="stToolbar"] svg *,
    div[data-testid="stAppDeployButton"] svg,
    div[data-testid="stAppDeployButton"] svg *,
    .stStatusWidget svg,
    .stStatusWidget svg * {
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
        fill: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* Prevent SVG canvas rectangles from turning into solid white or border boxes */
    header[data-testid="stHeader"] svg rect,
    div[data-testid="stStatusWidget"] svg rect,
    div[data-testid="stToolbar"] svg rect,
    div[data-testid="stAppDeployButton"] svg rect,
    .stStatusWidget svg rect {
        fill: transparent !important;
        stroke: transparent !important;
        border: none !important;
    }

    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] span,
    header[data-testid="stHeader"] label,
    header[data-testid="stHeader"] p,
    header[data-testid="stHeader"] a,
    div[data-testid="stStatusWidget"] span,
    div[data-testid="stStatusWidget"] label {
        color: #FFFFFF !important;
        opacity: 1 !important;
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

    /* Primary Action Button */
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

    /* Inline Spinner (NO BOX / NO WHITE RECTANGLES) */
    div[data-testid="stSpinner"],
    div[data-testid="stSpinner"] *,
    div[data-testid="stSpinner"] > div,
    div[data-testid="stSpinner"] [data-testid="stAlert"],
    div[data-testid="stSpinner"] [data-baseweb="notification"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stSpinner"] {
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
        fill: none !important;
        background: transparent !important;
    }

    div[data-testid="stSpinner"] svg rect {
        fill: transparent !important;
        stroke: none !important;
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

        except Exception as e:
            st.error(f"Something went wrong while generating your image: {e}")
