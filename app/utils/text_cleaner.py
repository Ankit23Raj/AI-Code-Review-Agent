import re


def clean_text(text):
    if not text:
        return ""

    text = str(text)

    # Remove ANSI escape sequences
    text = re.sub(
        r"\x1B\[[0-?]*[ -/]*[@-~]",
        "",
        text,
    )

    # Remove extra spaces/newlines
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()
