``markdown
# Implementation Plan

## Step 1 — Main structure and instrumentation layer

Implement:
- `OperatorType`,
- `ArtifactType`,
- `Node`,
- `Relationship`,
- `ProvenanceGraph`,
- `WorkflowContext`,
- `@ctx.step(...)` decorator,
- DataFrame registration,
- Model registration,
- Metric registration,
- JSON export,
- CSV export.

Initial example:
- ASD workflow from D6 to D10 and M1:
  - S5 normalise,
  - S6 select modelling features,
  - S7 split train/test,
  - S8 train classifier.

## Step 2 — Privacy schema

Implement:
- `PrivacyAnnotation`,
- `SensitivityCategory`,
- `UsageConstraint`,
- `ErasureConstraint`,
- `AccessRole`.

Add YAML loader for:
- attribute annotations,
- dataset annotations,
- category implications.

## Step 3 — Operation policies

Implement:
- `OperationPolicy`,
- policy YAML loader.

Policies for:
- S5_normalise,
- S6_select_modelling_features,
- S7_split_train_test,
- S8_train_classifier.

## Step 4 — Propagation engine

Implement:
- base combination rule,
- implication closure,
- RED rule,
- TR rule,
- FUS rule,
- LEARN rule,
- EVAL rule.

## Step 5 — Queries

Implement:
- erasure impact,
- sensitivity exposure,
- transformation responsibility,
- consent compliance,
- role-aware view.

## Step 6 — Evaluation examples

Run same tool on:
- ASD,
- Census,
- COMPAS,
- German Credit.

For each:
- record supported operators,
- compare inferred annotations with expected annotations,
- run audit queries,
- measure graph size and runtime.