import json
import copy
import streamlit as st

def draft_pass(text_input: str) -> dict:
    """Pass 1: Simulated extraction draft."""
    text_lower = text_input.lower()
    
    if "office chairs" in text_lower:
        return {
            "items": [{"name": "Office Chairs", "qty": 2, "unit_price": 150.0, "line_total": 300.0}],
            "total": 300.0
        }
    elif "notebooks" in text_lower:
        return {
            "items": [
                {"name": "Notebooks", "qty": 3, "unit_price": 4.50, "line_total": 13.50},
                {"name": "Pen", "qty": 1, "unit_price": 2.00, "line_total": 2.00}
            ],
            "total": 15.50
        }
    elif "usb drives" in text_lower:
        return {
            "items": [
                {"name": "USB Drives", "qty": 12, "unit_price": 14.50, "line_total": 174.00},
                {"name": "HDMI Cables", "qty": 4, "unit_price": 18.25, "line_total": 75.00}
            ],
            "total": 249.00
        }
    elif "markers" in text_lower:
        return {
            "items": [
                {"name": "Packs of markers", "qty": 2, "unit_price": 5.0, "line_total": 10.0},
                {"name": "Boxes of clips", "qty": 3, "unit_price": 5.0, "line_total": 15.0}
            ],
            "total": 25.0
        }
    elif "keyboards" in text_lower:
        return {
            "items": [
                {"name": "Keyboards", "qty": 2, "unit_price": 50.00, "line_total": 100.00},
                {"name": "Mouse", "qty": 1, "unit_price": 25.00, "line_total": 25.00}
            ],
            "total": 130.00
        }
    elif "software license" in text_lower:
        return {
            "items": [{"name": "Software License", "qty": 1, "unit_price": 49.99, "line_total": 49.99}],
            "total": 49.99
        }
    else:
        return {"items": [], "total": 0.0}


def check_pass(draft: dict) -> dict:
    """Pass 2: Code-based deterministic verification."""
    corrected = copy.deepcopy(draft)
    issues = []
    calculated_grand_total = 0.0

    for item in corrected.get("items", []):
        try:
            qty = float(item.get("qty", 0))
            price = float(item.get("unit_price", 0.0))
            expected_line_total = round(qty * price, 2)
            actual_line_total = round(float(item.get("line_total", 0.0)), 2)

            if actual_line_total != expected_line_total:
                issues.append(
                    f"Item '{item.get('name')}' line total incorrect: got ${actual_line_total}, expected ${expected_line_total}"
                )
                item["line_total"] = expected_line_total
            
            calculated_grand_total += item["line_total"]
        except (ValueError, TypeError):
            issues.append(f"Invalid numeric data in item '{item.get('name')}'")

    calculated_grand_total = round(calculated_grand_total, 2)
    actual_total = round(float(corrected.get("total", 0.0)), 2)

    if actual_total != calculated_grand_total:
        issues.append(
            f"Grand total incorrect: got ${actual_total}, expected ${calculated_grand_total}"
        )
        corrected["total"] = calculated_grand_total

    return {
        "flagged": len(issues) > 0,
        "failure_type": "broken_calculation" if issues else None,
        "details": issues,
        "corrected_draft": corrected
    }


def run_pipeline(text_input: str) -> dict:
    """Executes Pass 1 (Draft) and Pass 2 (Check/Correct)."""
    draft = draft_pass(text_input)
    draft_copy = copy.deepcopy(draft)
    check = check_pass(draft_copy)
    
    return {
        "input_text": text_input,
        "pass_1_draft": draft,
        "pass_2_check": {
            "flagged": check["flagged"],
            "failure_type": check["failure_type"],
            "details": check["details"]
        },
        "final_output": check["corrected_draft"]
    }


# Streamlit UI Configuration
st.set_page_config(page_title="AI Self-Correction Pipeline", page_icon="🤖", layout="wide")

st.title("🤖 Self-Correcting AI Entity Extraction Dashboard")
st.markdown("A two-pass architecture for entity extraction and deterministic arithmetic verification.")

test_cases = [
    "Invoice for 2 Office Chairs at 150 each. Total is 300.",
    "Purchased 3 Notebooks at 4.50 each and 1 Pen at 2.00. Grand total is 15.50.",
    "Order details: 12 USB Drives at $14.50 each ($174.00), plus 4 HDMI Cables at $18.25 each ($75.00). Total invoice amount: $249.00.",
    "Got 2 packs of markers for 10 total and 3 boxes of clips for 5 each.",
    "Bought 2 keyboards at $50.00 each ($100.00) and 1 mouse at $25.00 ($25.00). Total is $130.00.",
    "Purchased 1 software license for $49.99. Total: $49.99."
]

# Run pipeline for all test cases and save results.json
all_results = [run_pipeline(text) for text in test_cases]
with open("results.json", "w") as f:
    json.dump(all_results, f, indent=2)

st.sidebar.header("Pipeline Controls")
selected_case = st.sidebar.selectbox("Select Test Case to Inspect", [f"Test Case {i+1}" for i in range(len(test_cases))])
case_idx = int(selected_case.split(" ")[-1]) - 1

res = all_results[case_idx]
flagged = res["pass_2_check"]["flagged"]

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("Selected Case", f"Case {case_idx + 1}")
col2.metric("Pass 1 Extraction", "Complete")
col3.metric("Pass 2 Verification", "FLAGGED & CORRECTED" if flagged else "CLEAN (PASSED)", delta="Issues Caught" if flagged else "No Errors", delta_color="inverse" if flagged else "normal")

st.subheader("1. Input Invoice Text")
st.info(res["input_text"])

if flagged:
    st.subheader("2. Pass 2 Issues Detected & Self-Corrected")
    for issue in res["pass_2_check"]["details"]:
        st.error(f"⚠️ {issue}")

st.subheader("3. Pipeline Audit Trail JSON")
st.json(res)

st.markdown("---")
st.subheader("All 6 Test Cases Overview")

for i, r in enumerate(all_results, 1):
    is_flagged = r["pass_2_check"]["flagged"]
    status_icon = "🚨" if is_flagged else "✅"
    with st.expander(f"{status_icon} Test Case {i}: {r['input_text'][:60]}..."):
        if is_flagged:
            st.warning(f"**Flagged Issues:** {', '.join(r['pass_2_check']['details'])}")
        st.json(r)