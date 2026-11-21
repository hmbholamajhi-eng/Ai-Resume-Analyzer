import pytest
from resume_parser import extract_resume_text, ResumeParseError


def test_empty_file_rejected():
    with pytest.raises(ResumeParseError):
        extract_resume_text(b"", "resume.pdf")


def test_unsupported_file_rejected():
    with pytest.raises(ResumeParseError):
        extract_resume_text(b"hello", "resume.txt")


def test_pdf_signature_checked():
    with pytest.raises(ResumeParseError):
        extract_resume_text(b"not a pdf", "resume.pdf")
