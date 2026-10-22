
import json

import pytest
from pydantic import ValidationError

from extractor import extract_document


class MockResponse:
    def __init__(self, text):
        self.text = text


class MockModels:
    def __init__(self, response_text):
        self.response_text = response_text
        self.last_request = None

    def generate_content(self, **kwargs):
        self.last_request = kwargs
        return MockResponse(self.response_text)


class MockClient:
    def __init__(self, response_text):
        self.models = MockModels(response_text)


def test_extract_valid_invoice():
    invoice_json = {
        "invoice_number": "INV-001",
        "vendor_name": "ABC Supplies",
        "invoice_date": "2026-10-10",
        "currency": "USD",
        "subtotal": 100.0,
        "tax_amount": 14.0,
        "total_amount": 114.0,
        "items": [],
    }

    client = MockClient(json.dumps(invoice_json))

    result = extract_document(
        document_type="invoice",
        document_text="Invoice INV-001. Total: 114 USD.",
        client=client,
    )

    assert result.invoice_number == "INV-001"
    assert result.total_amount == 114.0
    assert client.models.last_request["config"]["response_mime_type"] == "application/json"


def test_invalid_json_is_rejected():
    client = MockClient("This is not JSON")

    with pytest.raises(ValueError, match="invalid JSON"):
        extract_document(
            document_type="invoice",
            document_text="Invoice INV-001",
            client=client,
        )


def test_invalid_extracted_data_is_rejected():
    invalid_invoice = {
        "invoice_number": "INV-001",
        "items": [
            {
                "description": "Laptop",
                "quantity": -2,
                "unit_price": 500,
                "total_price": 1000,
            }
        ],
    }

    client = MockClient(json.dumps(invalid_invoice))

    with pytest.raises(ValidationError):
        extract_document(
            document_type="invoice",
            document_text="Invoice for a laptop",
            client=client,
        )


def test_empty_document_is_rejected_before_api_call():
    client = MockClient("{}")

    with pytest.raises(ValueError, match="non-empty"):
        extract_document(
            document_type="invoice",
            document_text="   ",
            client=client,
        )

    assert client.models.last_request is None


def test_unsupported_document_type_is_rejected():
    client = MockClient("{}")

    with pytest.raises(ValueError, match="document_type"):
        extract_document(
            document_type="contract",
            document_text="Sample contract",
            client=client,
        )

    assert client.models.last_request is None

