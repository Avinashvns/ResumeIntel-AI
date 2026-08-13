from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 120


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Create the LangChain text splitter used by ResumeIntel AI.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
        length_function=len,
    )


def chunk_text(
    text: str,
) -> list[str]:
    """
    Split cleaned resume text into RAG-ready chunks.
    """

    if not text.strip():
        return []

    splitter = create_text_splitter()

    return splitter.split_text(text)