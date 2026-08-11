import re


def normalize_whitespace(text: str) -> str:
    """
    Normalize spaces and tabs while preserving line structure.
    """

    text = text.replace("\t", " ")

    text = re.sub(
        r"[ ]{2,}",
        " ",
        text,
    )

    return text


def normalize_line_breaks(text: str) -> str:
    """
    Normalize line breaks and remove excessive blank lines.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text


def remove_page_number_lines(text: str) -> str:
    """
    Remove lines that contain only page numbers.
    """

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        if re.fullmatch(
            r"(page\s+)?\d+",
            stripped,
            flags=re.IGNORECASE,
        ):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_text(text: str) -> str:
    """
    Run the complete text cleaning pipeline.
    """

    text = normalize_whitespace(text)

    text = normalize_line_breaks(text)

    text = remove_page_number_lines(text)

    text = text.strip()

    return text