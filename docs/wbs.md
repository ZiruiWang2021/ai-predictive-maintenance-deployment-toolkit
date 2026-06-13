# Work Breakdown Structure

| Phase | Work Package | Key Deliverables | Owner | Exit Criteria |
|---|---|---|---|---|
| 1. Initiation | Business framing | Problem statement, success metrics, stakeholder map | Product / PM | Maintenance use case and target assets agreed |
| 2. Data readiness | Source access | Sensor history, maintenance events, asset metadata | Data engineer | Data access approved and profiled |
| 2. Data readiness | Data quality | Missingness, sampling, label quality, leakage checks | Data scientist | Data quality report accepted |
| 3. Modelling | Feature engineering | Reusable feature pipeline and labelled training table | Data scientist | Features reproducible from source data |
| 3. Modelling | Model training | RUL model, validation metrics, model card | Data scientist | Metrics meet pilot threshold |
| 4. Dashboard | Planner workflow | Streamlit monitoring dashboard and intervention queue | Analytics engineer | Maintenance users can interpret outputs |
| 5. Deployment | Pilot release | Runbook, go/no-go checklist, rollback plan | PM / ML engineer | Go-live decision recorded |
| 6. Adoption | Training and handover | User guide, ownership model, feedback loop | PM | Users trained and support route live |
| 7. Monitoring | Post-release controls | Data drift, model performance, incident review cadence | ML engineer | Monitoring thresholds and owners active |

## Milestone View

| Milestone | Target Outcome |
|---|---|
| M1 Discovery complete | Use case, asset scope, and data sources confirmed |
| M2 Data baseline complete | Training dataset prepared and quality risks logged |
| M3 Model pilot ready | RUL model validated against agreed metrics |
| M4 Dashboard accepted | Planner-facing dashboard tested with sample users |
| M5 Go/no-go approved | Governance checklist completed |
| M6 Pilot live | Monitored deployment with human override and rollback |
