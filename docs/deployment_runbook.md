# Deployment Runbook

## Purpose

Deploy the predictive maintenance model as decision support for maintenance planners. The model recommends inspection or intervention priority; it does not automatically defer safety-critical work.

## Pre-Deployment

1. Confirm asset scope, data sources, and refresh cadence.
2. Run data quality checks against recent production extracts.
3. Train or load the approved model artifact.
4. Review model card, risk register, and go/no-go checklist.
5. Complete planner UAT with representative high, medium, and low risk assets.

## Local Demo Deployment

```bash
pip install -r requirements.txt
python scripts/train_model.py --generate-sample --n-units 90
streamlit run app/streamlit_app.py
```

## Container Deployment

```bash
docker build -f deployment/Dockerfile -t predictive-maintenance-toolkit .
docker run -p 8501:8501 predictive-maintenance-toolkit
```

## Production Pattern

1. Source system exports sensor readings and asset metadata.
2. Feature job creates asset-cycle features on a controlled schedule.
3. Model scoring job writes latest asset predictions and uncertainty bands.
4. Dashboard reads only approved scoring outputs.
5. Planner actions and overrides are logged for retraining and audit.

## Monitoring

| Monitor | Threshold | Action |
|---|---|---|
| Data freshness | No successful refresh within expected SLA | Alert data owner and mark dashboard stale |
| Feature drift | Any core sensor PSI above agreed threshold | Review asset mix and retraining need |
| Prediction drift | High-risk asset count shifts outside expected band | Compare with incident and maintenance context |
| Model performance | Recall below pilot threshold on reviewed outcomes | Freeze automated recommendations and retrain |
| User feedback | Repeated rejected recommendations | Convene review with planners and asset engineers |

## Rollback

Rollback means reverting to the previous approved scoring output and marking the dashboard as advisory only. If data quality or model safety is in doubt, maintenance planners should use existing inspection prioritization until the issue is resolved.
