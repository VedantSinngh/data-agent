import json
import pandas as pd
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.quality.rules import run_all_checks

def load_eval_cases(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

def run_evaluation():
    print("Starting Data Quality Engine Evaluation...\n")
    cases = load_eval_cases("evals/cases.json")
    df = pd.read_csv("data/samples/sales_defects.csv")
    
    findings = run_all_checks(df)
    
    true_positives = 0
    false_negatives = 0
    
    print("--- Detailed Evaluation ---")
    for case in cases:
        expected = case["expected_finding"]
        
        # Look for a finding that matches our expected rule and column
        match = next(
            (f for f in findings 
             if f["rule_id"] == expected["rule_id"] and f["column"] == expected["column"]), 
            None
        )
        
        if match:
            print(f"[PASS] {case['description']}")
            true_positives += 1
        else:
            print(f"[FAIL] {case['description']} - Expected finding not detected!")
            false_negatives += 1
            
    # Calculate simple Recall for deterministic engine based on labeled defects
    total_expected = len(cases)
    recall = true_positives / total_expected if total_expected > 0 else 0
    
    # Calculate Precision (Assuming all fired findings are true positives for now)
    # In a fully labeled dataset, we'd check if a fired finding was NOT in our expected list (False Positive)
    total_findings = len(findings)
    false_positives = total_findings - true_positives
    precision = true_positives / (true_positives + false_positives) if total_findings > 0 else 0
    
    print("\n--- Evaluation Metrics ---")
    print(f"Total Expected Defects: {total_expected}")
    print(f"Detected (True Positives): {true_positives}")
    print(f"Missed (False Negatives): {false_negatives}")
    print(f"Unexpected (False Positives): {false_positives}")
    print("-" * 25)
    print(f"Recall:    {recall:.2%}")
    print(f"Precision: {precision:.2%}")

if __name__ == "__main__":
    run_evaluation()
