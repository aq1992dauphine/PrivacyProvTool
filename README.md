# PrivacyProv prototype skeleton

A small starter implementation for privacy-aware provenance propagation over instrumented Python tabular ML workflows.

This version implements the first component: **Workflow instrumentation layer**.
It captures step boundaries, operator types, dataframe artifacts, step runs, and PROV-style relationships.

Run the example:

```bash
python -m privacyprov.examples.asd_workflow_instrumented
```

It exports:

- `outputs/asd_instrumented_graph.json`
- `outputs/asd_nodes.csv`
- `outputs/asd_relationships.csv`

The next implementation layers can plug into this graph:

1. Privacy annotation loader
2. Operation policy dictionary
3. Privacy propagation engine
4. Audit query layer
5. MLProvLens UI extension
