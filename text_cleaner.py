"""Text normalization while preserving common technical skill tokens."""
import re
import unicodedata


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Resume text must be a string.")
    text = unicodedata.normalize("NFKC", text).lower()
    # Preserve meaningful punctuation in C++, C#, .NET, node.js and CI/CD.
    text = re.sub(r"[^a-z0-9+#./-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
