
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InvoiceItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    description: str = Field(min_length=1)
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    total_price: float = Field(ge=0)


class InvoiceData(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    invoice_number: Optional[str] = None
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    currency: Optional[str] = None
    subtotal: Optional[float] = Field(default=None, ge=0)
    tax_amount: Optional[float] = Field(default=None, ge=0)
    total_amount: Optional[float] = Field(default=None, ge=0)
    items: list[InvoiceItem] = Field(default_factory=list)


class Education(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    institution: str
    degree: Optional[str] = None
    graduation_year: Optional[int] = None


class WorkExperience(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    job_title: str
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: list[str] = Field(default_factory=list)


class ResumeData(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    work_experience: list[WorkExperience] = Field(default_factory=list)

