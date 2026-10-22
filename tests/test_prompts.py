
import pytest

from prompts import build_prompt


def test_invoice_prompt_contains_required_information():
    prompt = build_prompt(
        "invoice",
        "Invoice Number: INV-001\nTotal: 114.00",
    )

    assert "Document type: invoice" in prompt
    assert "INV-001" in prompt
    assert "JSON Schema:" in prompt


def test_resume_prompt_contains_document_text():
    prompt = build_prompt(
        "resume",
        "Name: Sara Ahmed\nSkills: Python",
    )

    assert "Document type: resume" in prompt
    assert "Sara Ahmed" in prompt
    assert "Python" in prompt


def test_unsupported_document_type_is_rejected():
    with pytest.raises(ValueError):
        build_prompt("contract", "Sample document")


@pytest.mark.parametrize("document_text", ["", " ", "\n\t"])
def test_empty_document_is_rejected(document_text):
    with pytest.raises(ValueError):
        build_prompt("invoice", document_text)


def test_non_string_document_is_rejected():
    with pytest.raises(ValueError):
        build_prompt("resume", None)

