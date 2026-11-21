"""Controlled-vocabulary skill detection using escaped, boundary-aware patterns."""
import csv
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_skill_dictionary(path: Path | None = None):
    source = path or DATA_DIR / "skill_dictionary.csv"
    with open(source, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return rows


def _contains_skill(text: str, alias: str) -> bool:
    alias = alias.strip().lower()
    if not alias:
        return False
    # Whitespace in aliases can be represented by flexible whitespace.
    escaped = re.escape(alias).replace(r"\ ", r"\s+")
    # Avoid matching short skills inside unrelated words (e.g. R in "career").
    left = r"(?<![a-z0-9])" if alias[0].isalnum() else ""
    right = r"(?![a-z0-9])" if alias[-1].isalnum() else ""
    return re.search(left + escaped + right, text, flags=re.IGNORECASE) is not None


def extract_skills(cleaned_text: str, dictionary=None):
    if not isinstance(cleaned_text, str):
        raise TypeError("cleaned_text must be a string.")
    rows = dictionary if dictionary is not None else load_skill_dictionary()
    results = []
    seen = set()
    for row in rows:
        skill = row["skill"].strip()
        key = skill.casefold()
        aliases = [x.strip() for x in row.get("aliases", "").split("|") if x.strip()]
        candidates = [skill] + aliases
        if key not in seen and any(_contains_skill(cleaned_text, alias.lower()) for alias in candidates):
            results.append({"skill": skill, "category": row["category"]})
            seen.add(key)
    return results
