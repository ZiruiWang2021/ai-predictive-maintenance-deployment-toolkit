# Go/No-Go Checklist

| Area | Check | Evidence | Decision |
|---|---|---|---|
| Business | Maintenance use case has named owner and agreed success metric | Signed pilot brief | Pending |
| Data | Sensor data, work orders, and asset metadata reconcile at asset-cycle grain | Data quality report | Pending |
| Data | Refresh cadence is reliable and has freshness alerting | Pipeline run history | Pending |
| Model | Validation metrics meet threshold for pilot assets | Model card and metrics | Pending |
| Model | Failure-risk threshold is calibrated with maintenance capacity | Threshold review notes | Pending |
| Model | Human override process is documented | Runbook | Pending |
| Safety | Recommendations cannot automatically defer safety-critical maintenance | Control design | Pending |
| Dashboard | Maintenance planners can interpret risk tiers and action queue | UAT notes | Pending |
| Operations | Monitoring, incident response, and rollback owners are assigned | RACI / support rota | Pending |
| Governance | Limitations and intended use are approved | Model card | Pending |
| Training | Users know how to read the dashboard and challenge outputs | Training completion | Pending |

## No-Go Triggers

- Missing or stale production data with no manual fallback.
- Evidence that the model systematically overestimates RUL for high-criticality assets.
- No named owner for operational response to high-risk predictions.
- Users cannot interpret or challenge model outputs during UAT.
- Safety, compliance, or cybersecurity approval is incomplete.
