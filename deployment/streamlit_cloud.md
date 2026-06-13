# Streamlit Deployment Notes

## Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new Streamlit app from the repository.
3. Set the main file path to `app/streamlit_app.py`.
4. Add a setup command in the app settings if needed:

```bash
python scripts/train_model.py --generate-sample --n-units 90
```

For production-style hosting, pre-generate model artifacts in CI/CD or mount a managed object store containing approved model and scoring outputs.

## Environment Variables

No secrets are required for the offline demo. A production deployment should add:

- approved data source connection;
- model registry URI;
- monitoring sink or telemetry endpoint;
- incident contact list.
