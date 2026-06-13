# Data Directory

This project keeps raw, external, and processed data out of git by default.

- `external/`: manually downloaded public benchmark files, such as NASA C-MAPSS ZIPs.
- `raw/`: generated or prepared asset-cycle sensor logs.
- `processed/`: feature tables, validation predictions, and latest fleet scores.

Run:

```bash
python scripts/train_model.py --generate-sample --n-units 90
```

to generate the demo data and dashboard inputs.
