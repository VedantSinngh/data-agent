---
document_id: missing_value_policy
version: "1.0"
section: Data completeness
effective_date: "2026-01-01"
source_type: quality_policy
---

# Missing Value Policy

Critical business fields must not contain missing (null or empty) values. 

## Customer Identifiers
The `customer_id` field is required for all valid transactions. Customer-level reporting may be incomplete if this field is missing. 
Do not invent customer IDs or silently discard affected rows, as this alters the business reality of the dataset.

## Remediation Guidelines
Missing critical fields should always be flagged for review. If non-critical fields are missing, standard imputation (like replacing missing text with "Unknown") may only be applied if explicitly authorized by a category mapping rule.
