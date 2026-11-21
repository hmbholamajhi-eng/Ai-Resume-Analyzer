import pandas as pd
from job_matcher import rank_roles, analyze_target_role


def test_rank_and_skill_gap():
    roles = pd.DataFrame([
        {"role":"Data Analyst", "required_skills":"Python|SQL", "description":"Analyse data"},
        {"role":"NLP Engineer", "required_skills":"Python|NLP", "description":"Process language"},
    ])
    found = [{"skill":"Python","category":"Programming"},{"skill":"SQL","category":"Database"}]
    ranked = rank_roles("python sql analyse data", found, roles)
    assert ranked.iloc[0]["role"] == "Data Analyst"
    gap = analyze_target_role("NLP Engineer", found, roles)
    assert gap["found"] == ["Python"]
    assert gap["missing"] == ["NLP"]
