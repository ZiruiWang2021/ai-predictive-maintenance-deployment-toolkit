# Limitations and Future Work

## Current Limitations

- The default dataset is synthetic and should be treated as a reproducible demo, not operational evidence.
- The model assumes complete run-to-failure histories; real maintenance data is often censored by inspection and component replacement.
- The simple ridge model is transparent, but it does not fully capture sequence dynamics or asset-specific physics.
- Risk thresholds are illustrative and need calibration with asset criticality, possession windows, safety rules, and maintenance capacity.
- The dashboard reads batch scoring outputs; it is not a real-time condition monitoring system.

## Future Work

| Area | Improvement | Why It Matters |
|---|---|---|
| Public benchmark | Add a full C-MAPSS FD001 benchmark run with documented metrics | Makes the portfolio comparison more credible |
| Model | Add random forest, gradient boosting, or sequence model baselines | Shows tradeoffs between transparency and accuracy |
| Explainability | Add feature contribution or sensor trend explanations | Helps planners understand why an asset is high risk |
| Uncertainty | Replace residual bands with calibrated prediction intervals | Better supports risk-based planning |
| MLOps | Add model registry, versioned scoring outputs, and drift reports | Moves the demo closer to production operation |
| Product workflow | Add planner feedback capture and override analytics | Connects model performance to real adoption |
| Costing | Estimate avoided downtime and inspection cost tradeoffs | Makes the business case more concrete |
