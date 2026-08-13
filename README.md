# AI Image Generator

An AI-powered image generation app built with **Python and Streamlit**.

The app takes a user's text prompt, enhances it using **Groq**, and generates an image using **Hugging Face FLUX.1-schnell**.

## Features

* Text-to-image generation
* AI prompt enhancement
* Prompt validation
* Loading state
* Error handling

## Tech Stack

* Python
* Streamlit
* Groq
* Hugging Face
* FLUX.1-schnell
* Pillow

## How It Works

```text
User Prompt
     ↓
Groq
     ↓
Enhanced Prompt
     ↓
Hugging Face FLUX.1-schnell
     ↓
Generated Image
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
```

Run the app:

```bash
streamlit run app.py
```

**Note:** Never share or upload your `.env` file or API keys.
