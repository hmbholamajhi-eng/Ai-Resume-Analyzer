from skill_extractor import extract_skills


def test_alias_and_boundary_matching():
    dictionary = [
        {"skill": "Python", "category": "Programming", "aliases": "python3"},
        {"skill": "R", "category": "Programming", "aliases": ""},
        {"skill": "C++", "category": "Programming", "aliases": "c plus plus"},
    ]
    found = extract_skills("python3 and c++ are used in my career", dictionary)
    names = {item["skill"] for item in found}
    assert names == {"Python", "C++"}
    assert "R" not in names
