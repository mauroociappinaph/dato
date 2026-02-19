---
name: data-quality-frameworks
description: Data quality validation (GX, dbt, Contracts). 2026 Edition.
---

# Data Quality Frameworks (Compressed)

## Purpose
Implement automated validation to ensure data reliability and pipeline integrity. Focus on **Data Contracts** and preventive checks.

## Quality Dimensions (2026)
| Dimension | Check Example |
| :--- | :--- |
| **Completeness** | `not_be_null` on primary keys. |
| **Uniqueness** | `be_unique` on ID columns. |
| **Validity** | `in_set` for categorical statuses. |
| **Consistency** | Cross-table relationship validation. |
| **Timeliness** | Freshness checks (max_age < 24h). |

## Testing Pyramid
1. **Schema Tests**: Structural integrity (Types, Nulls).
2. **Unit Tests**: Single column logic.
3. **Integration Tests**: Cross-table/business logic.

## Financial Guardrail (Mandatory)
Before running expensive validation suites (Great Expectations, Soda) on datasets > 1M rows, MANDATORILY consult the **Financial-Controller** to audit ROI and token/compute costs.

## Patterns
- **dbt Tests**: Use `dbt_utils` for recency and uniqueness.
- **Great Expectations**: Use `GX Context` for daily checkpoints.
- **Data Contracts**: Define YAML contracts for inter-team data sharing.

## Protocols
1. **Test Early**: Validate source data before ingestion.
2. **Alerting**: Integrate failures with PagerDuty/Slack via **observability-engineer**.
3. **Documentation**: Auto-generate data docs after each successful run.