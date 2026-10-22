
import pytest
from pydantic import ValidationError

from schemas import (
    Education,
    InvoiceData,
    InvoiceItem,
    ResumeData,
    WorkExperience,
)


def test_valid_invoice_item():
    item = InvoiceItem(
        description="Laptop",
        quantity=2.0,
        unit_price=500.0,
        total_price=1000.0,
    )

    assert item.description == "Laptop"
    assert item.quantity == 2.0


def test_invalid_invoice_quantity():
    with pytest.raises(ValidationError):
        InvoiceItem(
            description="Laptop",
            quantity=-1.0,
            unit_price=500.0,
            total_price=500.0,
        )


def test_negative_invoice_price_is_rejected():
    with pytest.raises(ValidationError):
        InvoiceItem(
            description="Laptop",
            quantity=1.0,
            unit_price=-500.0,
            total_price=500.0,
        )


def test_extra_invoice_field_is_rejected():
    with pytest.raises(ValidationError):
        InvoiceData(unexpected_field="not allowed")


def test_valid_resume():
    resume = ResumeData(
        full_name="Sara Ahmed",
        skills=["Python", "Machine Learning"],
        education=[
            Education(
                institution="Cairo University",
                degree="Engineering",
                graduation_year=2024,
            )
        ],
        work_experience=[
            WorkExperience(
                job_title="AI Engineer",
                company="ABC Technologies",
                responsibilities=["Built ML models"],
            )
        ],
    )

    assert resume.full_name == "Sara Ahmed"
    assert "Python" in resume.skills
    assert resume.education[0].graduation_year == 2024


def test_empty_resume_lists_default_correctly():
    resume = ResumeData()

    assert resume.skills == []
    assert resume.education == []
    assert resume.work_experience == []


def test_extra_resume_field_is_rejected():
    with pytest.raises(ValidationError):
        ResumeData(unexpected_field="not allowed")


def test_invalid_graduation_year_type_is_rejected():
    with pytest.raises(ValidationError):
        Education(
            institution="Cairo University",
            graduation_year="not-a-year",
        )

