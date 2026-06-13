# Architecture

```mermaid
flowchart LR
    A["Sensor history and asset metadata"] --> B["Data cleaning"]
    B --> C["Feature engineering"]
    C --> D["RUL model training"]
    D --> E["Model artifact"]
    C --> F["Latest asset feature table"]
    E --> G["Batch scoring"]
    F --> G
    G --> H["Fleet prediction outputs"]
    H --> I["Streamlit dashboard"]
    I --> J["Maintenance planner decision"]
    J --> K["Planner feedback and outcome logging"]
    K --> B
```

## Design Choices

- Batch scoring is used because maintenance planning usually works on scheduled refreshes, not millisecond inference.
- The dashboard reads approved scoring outputs rather than querying raw operational systems directly.
- The model is deliberately simple and transparent for portfolio review and stakeholder explanation.
- Governance artefacts are versioned beside code so deployment thinking is visible, not hidden in slide decks.
