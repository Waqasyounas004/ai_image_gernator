def validate_prompt(prompt, min_length=3):
    """
    Check whether the user's prompt is valid.
    Returns True if valid and at least `min_length` characters, otherwise False.
    """
    if not prompt or not isinstance(prompt, str) or len(prompt.strip()) < min_length:
        return False

    return True


def clean_prompt(prompt):
    """
    Clean extra whitespace from the prompt.
    """
    return prompt.strip() if prompt and isinstance(prompt, str) else ""
