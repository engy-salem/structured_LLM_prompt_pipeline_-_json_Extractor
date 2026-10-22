# Structured LLM Prompt Pipeline & JSON Extractor

A Python-based document information extraction pipeline that uses Google's Gemini API, structured prompting, and Pydantic validation to convert unstructured text into structured, validated JSON.

## Overview

Extracting information from documents such as invoices and resumes can be time-consuming and error-prone. This project provides a reusable pipeline that processes document text using a Large Language Model (LLM) and validates the generated output against predefined data schemas.

The pipeline is designed to improve output consistency, reject invalid data, and handle temporary API failures through retry logic.

## Key Features

- **LLM Integration:** Uses Google's Gemini API to process document text.
- **Parameterized Prompt Templates:** Builds prompts dynamically based on document type.
- **Few-Shot Prompting:** Includes examples to guide structured information extraction.
- **Structured JSON Output:** Requests JSON responses using the expected schema.
- **Pydantic Validation:** Validates extracted fields and rejects invalid data.
- **Multiple Document Types:** Supports invoice and resume extraction.
- **Error Handling:** Handles empty input, invalid JSON, and validation errors.
- **Retry Mechanism:** Retries requests after supported temporary API errors.
- **Automated Testing:** Includes unit tests for schemas, prompts, extraction, and retry behavior.

## Tech Stack

- Python
- Google Gemini API (`google-genai`)
- Pydantic
- Pytest
- JSON Schema
- Prompt Engineering

## Project Structure

```text
structured_LLM_prompt_pipeline_-_json_Extractor/
├── schemas.py
├── prompts.py
├── extractor.py
├── requirements.txt
├── README.md
└── tests/
    ├── test_extractor.py
    ├── test_prompts.py
    └── test_schemas.py
```

## How It Works

1. **Input:** Accepts unstructured text from an invoice or resume.
2. **Prompt Construction:** Creates a document-specific prompt using a template, schema, and few-shot examples.
3. **LLM Processing:** Sends the prompt to the Gemini API and requests JSON output.
4. **JSON Parsing:** Parses the model response.
5. **Schema Validation:** Validates the extracted data using Pydantic models.
6. **Error Handling:** Rejects invalid inputs or outputs and retries eligible temporary API failures.

## Supported Data Schemas

### Invoice

The invoice schema supports fields such as:

- Invoice number
- Vendor name
- Invoice date
- Currency
- Subtotal, tax, and total amount
- Line items, including description, quantity, unit price, and total price

### Resume

The resume schema supports fields such as:

- Full name
- Email and phone
- Skills
- Education
- Work experience and responsibilities

Optional fields can remain `null` when information is unavailable, while list fields default to empty lists.

## Installation

Clone the repository:

```bash
git clone https://github.com/engy-salem/structured_LLM_prompt_pipeline_-_json_Extractor.git
cd structured_LLM_prompt_pipeline_-_json_Extractor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set your Gemini API key using an environment variable named `GEMINI_API_KEY`.

For example, in a Linux or macOS terminal:

```bash
export GEMINI_API_KEY="your-api-key"
```

In Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Replace the placeholder with your own API key. Never commit API keys or other secrets to GitHub.

## Usage

Run the extraction script:

```bash
python extractor.py
```

Enter the document type when prompted:

```text
invoice
```

Paste the document text, then type `END` on a new line to finish the input.

The script prints the extracted information as formatted JSON after successful validation.

You can also use the extraction function in another Python script:

```python
from extractor import extract_document

document_text = """
Invoice Number: INV-001
Vendor: ABC Supplies
Date: 2026-10-10
Currency: USD
Subtotal: 100.00
Tax: 14.00
Total: 114.00
"""

result = extract_document(
    document_type="invoice",
    document_text=document_text,
)

print(result.model_dump_json(indent=2))
```

The `extract_document` function returns a validated Pydantic model. A valid `GEMINI_API_KEY` must be configured when using the real Gemini API.

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The current test suite contains **21 passing tests**, covering prompt construction, schema validation, extraction errors, and retry behavior.

The tests use mock API responses where appropriate, so the unit tests do not require live Gemini API calls.

## Limitations

- The current pipeline accepts document text; PDF file parsing and image-based OCR are not included.
- Extraction quality depends on the input text and the model response.
- Schema validation checks structure and field constraints but does not independently verify every extracted fact against the original document.
- A Gemini API key and network access are required for live extraction.

## Future Improvements

- Add PDF and image document ingestion.
- Expand the test suite for additional API error scenarios.
- Add evaluation datasets and extraction-quality metrics.
- Add a command-line interface with more configuration options.
- Support additional document types and schemas.
