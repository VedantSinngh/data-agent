---
document_id: duplicate_transaction_rules
version: "1.0"
section: Transaction uniqueness
effective_date: "2026-01-01"
source_type: quality_policy
---

# Transaction Uniqueness Policy

Each transaction must have a unique transaction identifier (`transaction_id`). 
Rows with repeated identifiers should be flagged for investigation as they may artificially inflate sales totals or corrupt downstream reporting.

## Remediation Guidelines
Do not automatically delete duplicate records unless the duplicate policy confirms that they represent the exact same transaction across all fields. 
If the identities are ambiguous or other fields (like `sales_amount` or `transaction_date`) differ between the rows sharing an ID, you must require human review.
