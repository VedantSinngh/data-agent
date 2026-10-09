import pandas as pd
import json
from app.quality.rules import run_all_checks

def main():
    print("Loading data...")
    df = pd.read_csv("data/samples/sales_defects.csv")
    print(f"Loaded {len(df)} rows.")
    
    print("\nRunning Data Quality Checks...")
    findings = run_all_checks(df)
    
    print("\nFindings:")
    print(json.dumps(findings, indent=2))

if __name__ == "__main__":
    main()
