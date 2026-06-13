# Building an AI Predictive Maintenance Deployment Toolkit

## Problem

Maintenance teams often have large volumes of equipment sensor data but limited time to decide which assets need attention first. A predictive maintenance model can estimate Remaining Useful Life (RUL), but a useful deployment needs more than a model notebook. It needs a repeatable data pipeline, a dashboard, and a clear operating plan.

This project builds a small deployment toolkit for a Network Rail-style maintenance scenario: predict RUL from sensor histories, highlight high-risk assets, and document how the system would move from pilot to operational use.

## Why It Matters

Unplanned failures can cause service disruption, safety concerns, emergency repair cost, and poor passenger or customer experience. Replacing assets too early is also expensive. Predictive maintenance sits between these two problems: it helps teams intervene earlier, but only when the evidence is strong enough to justify action.

For AI projects, the biggest challenge is often not model training. It is adoption. Maintenance planners need clear recommendations, asset engineers need to trust the assumptions, and project sponsors need to understand the delivery risks.

## My Approach

I designed the repo as both a technical demo and a deployment pack:

1. Generate or prepare CMAPSS-style run-to-failure sensor data.
2. Clean and label the data at asset-cycle grain.
3. Build rolling sensor features that capture degradation trends.
4. Train a transparent RUL regression model.
5. Score the latest record for each asset and assign risk tiers.
6. Present the results in a Streamlit dashboard.
7. Add delivery artefacts: WBS, risk register, go/no-go checklist, stakeholder map, deployment runbook, and model card.

## Technical Implementation

The model pipeline is implemented in `src/pdm_toolkit/`:

- `data.py` generates or loads sensor logs, handles cleaning, and adds RUL labels.
- `features.py` builds rolling means, rolling standard deviations, deltas, and engineering proxy features.
- `model.py` trains a ridge regression model using `numpy`, avoiding a black-box dependency for the core algorithm.
- `pipeline.py` orchestrates data generation, training, evaluation, and output creation.
- `scoring.py` converts predicted RUL into operational risk tiers and maintenance actions.

The dashboard in `app/streamlit_app.py` reads generated CSV outputs, not raw model internals. That mirrors a practical deployment pattern: scoring jobs publish approved outputs, and the dashboard stays focused on decision support.

## Results / Demo

The demo produces:

- a fleet-level intervention queue;
- high, medium, and low risk asset tiers;
- RUL prediction intervals;
- validation metrics including MAE, RMSE, bias, precision, and recall;
- a dashboard preview image for GitHub readers.

Example output:

```text
unit_id=1, predicted_rul=22.6, failure_risk=high
action=Plan intervention in next maintenance window
```

Run locally:

```bash
pip install -r requirements.txt
python scripts/train_model.py --generate-sample --n-units 90
streamlit run app/streamlit_app.py
```

## Limitations

The included demo data is synthetic, so it should not be used as operational evidence. The model is intentionally simple and transparent; production environments may need richer sequence models, calibrated uncertainty, drift monitoring, and tighter asset-domain validation.

The RUL labelling approach assumes complete run-to-failure histories. In real rail or industrial settings, asset histories can be censored by inspections, repairs, component swaps, or data gaps.

## What I Learned

The most valuable part of a predictive maintenance project is connecting model outputs to operational decisions. A model score is only useful if a planner understands what action to take, a sponsor understands the risk, and a technical owner can monitor whether the system is still reliable.

This project helped me frame AI delivery as an end-to-end system: data readiness, modelling, dashboard design, stakeholder adoption, governance, and post-launch monitoring.

## GitHub Link

https://github.com/ZiruiWang2021/ai-predictive-maintenance-deployment-toolkit
