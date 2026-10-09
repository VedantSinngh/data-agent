---
document_id: category_mapping_rules
version: "1.0"
section: Categorical consistency
effective_date: "2026-01-01"
source_type: quality_policy
---

# Category Mapping Rules

The `product_category` field is strictly controlled to ensure accurate grouped reporting.

## Allowed Categories
- Electronics
- Clothing
- Home

## Inconsistent Categories
Category variants (e.g., `electronics`, `ELECTRONICS`, `Clothing Item`) may split reporting totals. 

## Remediation Guidelines
Normalize category variants only when a verified mapping exists (e.g., converting lowercase `electronics` to `Electronics`). 
If a completely unrecognized category is found, do not map it automatically. Flag it for manual review.
