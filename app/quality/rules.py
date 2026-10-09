import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

def check_missing_values(df: pd.DataFrame, required_columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    findings = []
    cols_to_check = required_columns if required_columns else df.columns
    for col in cols_to_check:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                findings.append({
                    "finding_id": f"DQ-MISSING-{col.upper()}",
                    "rule_id": "MISSING_VALUES",
                    "column": col,
                    "issue_type": "missing_value",
                    "severity": "high",
                    "affected_rows": int(missing_count),
                    "evidence": {"missing_percentage": float(missing_count / len(df) * 100)},
                    "recommended_action": f"Review missing values in {col}",
                    "auto_fix_allowed": False
                })
    return findings

def check_duplicate_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    findings = []
    duplicates = df[df.duplicated(keep=False)]
    if not duplicates.empty:
        findings.append({
            "finding_id": "DQ-DUPLICATE-ROWS",
            "rule_id": "DUPLICATE_RECORDS",
            "column": "all",
            "issue_type": "duplicate_row",
            "severity": "medium",
            "affected_rows": len(duplicates),
            "evidence": {"duplicate_count": len(duplicates)},
            "recommended_action": "Review duplicate rows for removal",
            "auto_fix_allowed": False
        })
    return findings

def check_duplicate_keys(df: pd.DataFrame, key_columns: List[str]) -> List[Dict[str, Any]]:
    findings = []
    for col in key_columns:
        if col in df.columns:
            duplicates = df[df.duplicated(subset=[col], keep=False)]
            if not duplicates.empty:
                findings.append({
                    "finding_id": f"DQ-DUPLICATE-KEY-{col.upper()}",
                    "rule_id": "UNIQUE_KEY",
                    "column": col,
                    "issue_type": "duplicate_key",
                    "severity": "high",
                    "affected_rows": len(duplicates),
                    "evidence": {"duplicate_key_count": len(duplicates[col].unique())},
                    "recommended_action": f"Review duplicate keys in {col}",
                    "auto_fix_allowed": False
                })
    return findings

def check_invalid_categories(df: pd.DataFrame, column: str, allowed_categories: List[str]) -> List[Dict[str, Any]]:
    findings = []
    if column in df.columns:
        # Check against allowed (case-sensitive)
        invalid_mask = ~df[column].isin(allowed_categories) & df[column].notna()
        invalid_rows = df[invalid_mask]
        if not invalid_rows.empty:
            invalid_values = invalid_rows[column].unique().tolist()
            findings.append({
                "finding_id": f"DQ-INVALID-CAT-{column.upper()}",
                "rule_id": "ALLOWED_CATEGORIES",
                "column": column,
                "issue_type": "invalid_category",
                "severity": "medium",
                "affected_rows": len(invalid_rows),
                "evidence": {"unexpected_values": invalid_values},
                "recommended_action": f"Map invalid categories in {column} to allowed values",
                "auto_fix_allowed": False
            })
    return findings

def check_negative_values(df: pd.DataFrame, numeric_columns: List[str]) -> List[Dict[str, Any]]:
    findings = []
    for col in numeric_columns:
        if col in df.columns:
            # Coerce to numeric
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            negative_mask = numeric_series < 0
            negative_rows = df[negative_mask]
            if not negative_rows.empty:
                findings.append({
                    "finding_id": f"DQ-NEGATIVE-{col.upper()}",
                    "rule_id": "NON_NEGATIVE",
                    "column": col,
                    "issue_type": "range_violation",
                    "severity": "high",
                    "affected_rows": len(negative_rows),
                    "evidence": {"negative_count": len(negative_rows)},
                    "recommended_action": f"Review negative values in {col}",
                    "auto_fix_allowed": False
                })
    return findings

def check_cross_column_consistency(df: pd.DataFrame) -> List[Dict[str, Any]]:
    # Example: sales_amount should equal quantity * unit_price
    findings = []
    if all(col in df.columns for col in ['sales_amount', 'quantity', 'unit_price']):
        try:
            qty = pd.to_numeric(df['quantity'], errors='coerce')
            price = pd.to_numeric(df['unit_price'], errors='coerce')
            sales = pd.to_numeric(df['sales_amount'], errors='coerce')
            
            calculated_sales = qty * price
            # Allow 0.01 tolerance for rounding
            mismatch = abs(calculated_sales - sales) > 0.01
            mismatch_rows = df[mismatch & calculated_sales.notna() & sales.notna()]
            
            if not mismatch_rows.empty:
                findings.append({
                    "finding_id": "DQ-INCONSISTENT-SALES",
                    "rule_id": "CROSS_COLUMN_CONSISTENCY",
                    "column": "sales_amount",
                    "issue_type": "cross_column_inconsistency",
                    "severity": "high",
                    "affected_rows": len(mismatch_rows),
                    "evidence": {"mismatched_rows": len(mismatch_rows)},
                    "recommended_action": "Reconcile sales_amount with quantity * unit_price",
                    "auto_fix_allowed": False
                })
        except Exception:
            pass
    return findings

def run_all_checks(df: pd.DataFrame) -> List[Dict[str, Any]]:
    all_findings = []
    
    # 1. Missing values
    all_findings.extend(check_missing_values(df, ['transaction_id', 'customer_id']))
    
    # 2. Duplicate records
    all_findings.extend(check_duplicate_records(df))
    
    # 3. Duplicate keys
    all_findings.extend(check_duplicate_keys(df, ['transaction_id']))
    
    # 4. Invalid categories
    allowed_categories = ['Electronics', 'Clothing', 'Home']
    allowed_regions = ['North', 'South', 'East', 'West']
    all_findings.extend(check_invalid_categories(df, 'product_category', allowed_categories))
    all_findings.extend(check_invalid_categories(df, 'region', allowed_regions))
    
    # 5. Negative values
    all_findings.extend(check_negative_values(df, ['quantity', 'unit_price']))
    
    # 6. Cross column
    all_findings.extend(check_cross_column_consistency(df))
    
    return all_findings
