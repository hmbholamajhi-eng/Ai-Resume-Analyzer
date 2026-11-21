"""Role ranking with TF-IDF cosine similarity plus transparent skill coverage."""
import csv
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(__file__).parent / "data"


def load_job_roles(path: Path | None = None) -> pd.DataFrame:
    source = path or DATA_DIR / "job_roles.csv"
    frame = pd.read_csv(source)
    required = {"role", "required_skills", "description"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Job-role CSV must contain columns: {sorted(required)}")
    if frame.empty:
        raise ValueError("Job-role dataset is empty.")
    frame["required_skills"] = frame["required_skills"].fillna("").astype(str)
    return frame


def _role_skills(row):
    return [skill.strip() for skill in row["required_skills"].split("|") if skill.strip()]


def _coverage(found_names, required):
    found = {x.casefold() for x in found_names}
    if not required:
        return 0.0
    return 100.0 * sum(s.casefold() in found for s in required) / len(required)


def rank_roles(resume_text: str, found_skills, roles_df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(resume_text, str):
        raise TypeError("resume_text must be a string.")
    if roles_df.empty:
        return pd.DataFrame(columns=["role", "match_score", "skill_coverage", "cosine_similarity"])
    role_docs = (roles_df["role"].astype(str) + " " +
                 roles_df["description"].astype(str) + " " +
                 roles_df["required_skills"].astype(str)).tolist()
    corpus = [resume_text] + role_docs
    try:
        matrix = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True).fit_transform(corpus)
        similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    except ValueError:
        similarities = [0.0] * len(role_docs)
    names = [item["skill"] for item in found_skills]
    records = []
    for index, (_, row) in enumerate(roles_df.iterrows()):
        required = _role_skills(row)
        coverage = _coverage(names, required)
        cosine_pct = float(similarities[index]) * 100.0
        # Explicitly documented heuristic: text similarity contributes 70%, skill coverage 30%.
        score = min(100.0, max(0.0, 0.70 * cosine_pct + 0.30 * coverage))
        records.append({"role": row["role"], "match_score": round(score, 1),
                        "skill_coverage": round(coverage, 1),
                        "cosine_similarity": round(cosine_pct, 1),
                        "required_skills": required})
    return pd.DataFrame(records).sort_values(
        ["match_score", "skill_coverage", "role"], ascending=[False, False, True]
    ).reset_index(drop=True)


def analyze_target_role(target_role: str, found_skills, roles_df: pd.DataFrame):
    matches = roles_df[roles_df["role"] == target_role]
    if matches.empty:
        raise ValueError("Selected role does not exist in the role dataset.")
    required = _role_skills(matches.iloc[0])
    found = {item["skill"].casefold(): item["skill"] for item in found_skills}
    present = [skill for skill in required if skill.casefold() in found]
    missing = [skill for skill in required if skill.casefold() not in found]
    coverage = _coverage(list(found.values()), required)
    return {"role": target_role, "required": required, "found": present,
            "missing": missing, "match_score": round(coverage, 1)}
