# Self-Correcting AI Entity Extraction & Validation Pipeline

An Applied AI Engineering solution implementing a two-pass architecture to extract structured financial data from conversational text, perform deterministic arithmetic validation, and render an interactive Streamlit dashboard.

## Architecture

1. **Pass 1: Entity Extraction (Draft)**
   - Parses unstructured invoice text into structured JSON schema containing line items, quantities, unit prices, line totals, and overall total.

2. **Pass 2: Deterministic Verification (Check & Correct)**
   - Intercepts Pass 1 draft using a Python-based engine.
   - Mathematically verifies line item totals ($qty \times price$) and calculates grand totals.
   - Flags discrepancies, logs error types, and applies automated self-corrections without overwriting historical draft metadata.

3. **Pass 3: Web Dashboard (Streamlit UI)**
   - Renders interactive metric cards, real-time error alerts, inspection controls, and full audit logs on a web interface.

## Pipeline Outputs

- **Streamlit Web Dashboard:** `http://localhost:8501`
- **Executable Application:** `main.py`
- **Structured Audit Trail:** `results.json` (covers 6 standardized test cases demonstrating clean passes and self-corrections)

## Setup & Running

1. Install dependencies:
```bash
pip install streamlit
