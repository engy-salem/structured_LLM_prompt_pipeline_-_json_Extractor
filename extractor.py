
import json
import os
import random
import time

from google import genai
from google.genai import errors
from pydantic import ValidationError

from prompts import build_prompt
from schemas import InvoiceData, ResumeData

SCHEMAS = {
    "invoice": InvoiceData,
    "resume": ResumeData,
}

DEFAULT_MODEL = "gemini-flash-lite-latest"


def generate_with_retry(
    client,
    model: str,
    prompt: str,
    response_schema: dict,
    max_attempts: int = 3,
):
    for attempt in range(max_attempts):
        try:
            return client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": response_schema,
                },
            )

        except errors.APIError as error:
            retryable = (
                error.code == 429
                or error.code in (500, 502, 503, 504)
            )

            if not retryable or attempt == max_attempts - 1:
                raise

            delay = min(2 ** attempt, 8) + random.uniform(0, 0.5)
            time.sleep(delay)


def extract_document(
    document_type: str,
    document_text: str,
    client=None,
    model: str = DEFAULT_MODEL,
):
    prompt = build_prompt(document_type, document_text)
    schema = SCHEMAS[document_type]

    if client is None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )

        client = genai.Client(api_key=api_key)

    
response = generate_with_retry(
    client=client,
    model=model,
    prompt=prompt,
    response_schema=schema.model_json_schema(),
)


    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    try:
        raw_data = json.loads(response.text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned invalid JSON."
        ) from error

    try:
        validated_data = schema.model_validate(raw_data)
    except ValidationError:
        raise

    return validated_data


def main():
    document_type = input(
        "Enter document type (invoice/resume): "
    ).strip().lower()

    print("Enter the document text. Type END on a new line to finish:")

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    document_text = "\n".join(lines)

    try:
        result = extract_document(
            document_type=document_type,
            document_text=document_text,
        )

        print("\nValidated JSON output:")
        print(result.model_dump_json(indent=2))

    except (ValueError, ValidationError) as error:
        print(f"Extraction failed: {error}")


if __name__ == "__main__":
    main()

