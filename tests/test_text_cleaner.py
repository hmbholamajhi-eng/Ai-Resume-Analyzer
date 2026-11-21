from text_cleaner import clean_text


def test_cleaner_preserves_technical_tokens():
    result = clean_text("C++, C#, .NET and Node.js   are useful!")
    assert "c++" in result
    assert "c#" in result
    assert ".net" in result
    assert "node.js" in result


def test_cleaner_collapses_whitespace():
    assert clean_text(" Python \n\n SQL ") == "python sql"
