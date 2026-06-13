# Risk Register

| ID | Risk | Impact | Likelihood | Severity | Mitigation | Owner | Status |
|---|---|---:|---:|---:|---|---|---|
| R1 | Historical failure labels are incomplete or inconsistent | High | Medium | High | Reconcile sensor data with work orders and failure codes before training | Data engineer | Open |
| R2 | Model overestimates RUL for safety-critical assets | High | Medium | High | Use conservative thresholds, uncertainty bands, and human approval before deferral | Data scientist | Open |
| R3 | Asset operating conditions differ from training data | Medium | Medium | Medium | Monitor input drift by route, asset class, and operating regime | ML engineer | Open |
| R4 | Maintenance teams do not trust recommendations | High | Medium | High | Co-design dashboard, expose drivers, and run shadow-mode pilot | PM | Open |
| R5 | Dashboard becomes stale because data refresh fails | Medium | Medium | Medium | Add freshness checks, alerting, and fallback process | Analytics engineer | Open |
| R6 | False positives overload maintenance capacity | Medium | Medium | Medium | Tune intervention threshold with planner capacity and criticality | Operations lead | Open |
| R7 | Production data contains PII or sensitive operational detail | High | Low | Medium | Complete data governance review and role-based access controls | Governance lead | Open |
| R8 | Model ownership is unclear after pilot | Medium | Medium | Medium | Assign service owner, monitoring owner, and business decision owner before launch | Sponsor | Open |

## Review Cadence

- Weekly during build and pilot.
- Fortnightly during the first two months after go-live.
- Monthly once monitoring is stable.
