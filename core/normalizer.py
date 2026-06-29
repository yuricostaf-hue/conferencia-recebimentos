"""Text normalization utilities."""

import unicodedata
from typing import Optional


def remove_accents(text: str) -> str:
    """Remove accents from text.

    Args:
        text: Input text.

    Returns:
        Text without accents.
    """
    nfd = unicodedata.normalize("NFD", text)
    return "".join(char for char in nfd if unicodedata.category(char) != "Mn")


def normalize_name(name: Optional[str]) -> str:
    """Normalize a patient name for comparison.

    Converts to uppercase, removes accents, and normalizes whitespace.

    Args:
        name: Patient name.

    Returns:
        Normalized name.
    """
    if not name:
        return ""

    # Convert to uppercase
    text = name.upper()
    # Remove accents
    text = remove_accents(text)
    # Remove extra spaces
    text = " ".join(text.split())
    return text.strip()


def normalize_procedure(procedure: Optional[str]) -> str:
    """Normalize a procedure name for comparison.

    Converts to uppercase, removes accents, and normalizes whitespace.

    Args:
        procedure: Procedure name.

    Returns:
        Normalized procedure.
    """
    if not procedure:
        return ""

    # Convert to uppercase
    text = procedure.upper()
    # Remove accents
    text = remove_accents(text)
    # Remove extra spaces
    text = " ".join(text.split())
    return text.strip()
