---
document_id: cross_column_consistency
version: "1.0"
section: Financial integrity
effective_date: "2026-01-01"
source_type: quality_policy
---

# Financial Integrity Rules

Cross-column consistency is critical for financial reporting.

## Sales Amount Verification
The `sales_amount` field must mathematically reconcile with the product of `quantity` multiplied by `unit_price`.
A small rounding tolerance (up to 0.01) is acceptable, but significant deviations suggest data corruption.

## Remediation Guidelines
Mismatched sales amounts should not be automatically recalculated without user authorization, as it is often unclear whether the quantity, price, or total is the incorrect value. Flag for human review.
