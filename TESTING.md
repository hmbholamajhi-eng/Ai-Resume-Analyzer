# Testing and acceptance checklist

Run automated tests with `pytest -q`.

## Automated coverage
- Empty and unsupported files are rejected.
- PDF extension/content mismatch is rejected.
- Technical tokens such as C++, C# and .NET survive cleaning.
- Skill aliases are detected, and short skills do not match inside unrelated words.
- Roles are ranked and skill gaps are reported consistently.

## Manual user acceptance test
| Case | Action | Expected result |
|---|---|---|
| UAT-01 | Upload a valid text PDF | All extractable pages appear in preview |
| UAT-02 | Upload a valid DOCX | Paragraph and table text is extracted |
| UAT-03 | Upload an unsupported file | Clear validation error |
| UAT-04 | Upload file larger than 5 MB | Upload is rejected |
| UAT-05 | Upload resume with Python and SQL | Those skills are detected |
| UAT-06 | Select Machine Learning Engineer | Found and missing skills are shown |
| UAT-07 | Compare role recommendations | Roles are sorted by estimated score |
| UAT-08 | Download report | JSON and CSV downloads open correctly |
| UAT-09 | Upload a scanned PDF | App explains that little/no text was extracted |
| UAT-10 | Review privacy statement | User is told files are not persisted |

## Evaluation worksheet
Record extraction quality, skill precision/recall, expected vs actual top role, score consistency after adding/removing a skill, and usability feedback. Use consented, anonymized sample resumes only.
