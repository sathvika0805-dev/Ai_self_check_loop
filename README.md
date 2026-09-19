# Self-Correcting AI Entity Extraction & Validation Pipeline

An Applied AI Engineering solution implementing a two-pass architecture to extract structured financial data from conversational text and perform deterministic arithmetic validation.

## Architecture

1. **Pass 1: Entity Extraction (Draft)**
   - Parses unstructured invoice text into structured JSON schema containing line items, quantities, unit prices, line totals, and overall total.

2. **Pass 2: Deterministic Verification (Check & Correct)**
   - Intercepts Pass 1 draft using a Python-based engine.
   - Mathematically verifies line item totals ($qty \times price$) and calculates grand totals.
   - Flags discrepancies, logs error types, and applies automated self-corrections without overwriting historical draft metadata.

## Pipeline Outputs

- Executable code: `main.py`
- Structured output audit trail: `results.json` (covers 6 comprehensive test cases demonstrating clean passes and self-corrections)

## Setup & Running

```bash
python main.py
