# Architecture and workflow

```mermaid
flowchart TD
    A[PDF / DOCX upload] --> B[File type and size validation]
    B --> C[Resume parser: pypdf / python-docx]
    C --> D[Text normalization]
    D --> E[Controlled skill dictionary]
    D --> F[TF-IDF vectorization]
    G[Job roles CSV] --> H[Role descriptions and required skills]
    E --> I[Skill coverage]
    F --> J[Cosine similarity]
    H --> F
    H --> I
    I --> K[Weighted role ranking]
    J --> K
    K --> L[Top 3 recommendations]
    K --> M[Target role skill-gap analysis]
    M --> N[Rule-based learning roadmap]
    L --> O[Streamlit dashboard and downloads]
    N --> O
```

## Boundaries
- `resume_parser.py`: untrusted file input and extraction.
- `text_cleaner.py`: normalization only; preserves technical punctuation.
- `skill_extractor.py`: controlled-vocabulary detection.
- `job_matcher.py`: TF-IDF/cosine similarity and transparent score.
- `roadmap_generator.py`: deterministic learning suggestions.
- `app.py`: UI orchestration and report downloads.

## Score
`final_score = 0.70 * cosine_similarity_percent + 0.30 * required_skill_coverage_percent`

This is a heuristic for educational exploration, not a probability of being hired.
