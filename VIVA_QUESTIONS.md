# Viva preparation

1. **How is resume text extracted?** `pypdf` reads PDF pages; `python-docx` reads DOCX paragraphs and tables.
2. **What is TF-IDF?** A weighting method that gives higher importance to terms frequent in one document but less common across the document collection.
3. **What does cosine similarity measure?** The cosine of the angle between two vectors; it compares their orientation, often used as a similarity measure.
4. **Why can keyword matching miss skills?** The resume may use synonyms, abbreviations, context, or evidence not represented in the controlled dictionary.
5. **When use Sentence Transformers?** When semantic similarity beyond exact vocabulary is needed and the extra model/deployment cost is acceptable.
6. **Why exclude protected attributes?** They are not job-related evidence and can introduce unfair discrimination.
7. **How is the match score calculated?** 70% TF-IDF cosine similarity plus 30% required-skill coverage in this implementation.
8. **What are limitations?** Keyword false negatives, small manually maintained role dataset, no proficiency/experience calibration, no OCR, and scores are not hiring probabilities.
