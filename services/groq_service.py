import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def enhance_prompt(user_prompt: str, fallback_on_failure: bool = True) -> str:
    """
    Enhances a simple user prompt into a detailed image-generation prompt using Groq API.

    Args:
        user_prompt (str): The initial prompt from the user.
        fallback_on_failure (bool): If True, returns original user prompt if Groq API fails.

    Returns:
        str: The enhanced, detailed image generation prompt.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the .env file.")

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI image prompt engineer. "
                        "Your job is to transform a simple user prompt into a detailed "
                        "and high-quality prompt for an AI image generation model. "
                        "Improve the prompt by adding appropriate details about: "
                        "subject, environment, lighting, composition, camera perspective, "
                        "visual style, and important visual details. "
                        "Do not change the main idea of the user's prompt. "
                        "Do not add unrelated objects or concepts. "
                        "Return only the improved image prompt. "
                        "Do not provide explanations, headings, or extra text."
                    ),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.7,
            max_tokens=300,
        )

        enhanced_prompt = response.choices[0].message.content.strip()
        return enhanced_prompt

    except Exception as e:
        if fallback_on_failure:
            print(f"[Warning] Groq API call failed: {e}. Using original prompt as fallback.")
            return user_prompt.strip()
        else:
            raise RuntimeError(f"Groq API call failed: {e}") from e
