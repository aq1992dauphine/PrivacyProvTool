# PrivacyProv

PrivacyProv is a research prototype for privacy-aware provenance propagation in
instrumented tabular machine-learning pipelines. It records fine-grained
workflow provenance, attaches privacy annotations to source artifacts, applies
operation-specific privacy policies, and propagates privacy metadata across
derived datasets, records, cells, models, and evaluation metrics.

The project is designed for pandas and scikit-learn style workflows that are
explicitly instrumented with PrivacyProv decorators. It does not attempt to
automatically analyse arbitrary Python programs.

## What the Repository Contains

- `privacyprov/core/`: provenance graph primitives, model references, and enums.
- `privacyprov/instrumentation/`: the workflow instrumentation layer.
- `privacyprov/privacy/`: privacy config loading, ontology handling, annotation,
  operation-policy materialisation, and propagation logic.
- `privacyprov/examples/`: runnable instrumented examples for ASD, Census,
  German Credit, and COMPAS-style workflows.
- `privacyprov/config/`: privacy annotations, operation policies, and copied
  instrumented scripts grouped by dataset.
- `outputs/`: generated graph, node, relationship, and summary files.
- `docs/`: background papers and implementation notes.

## Main Concepts

PrivacyProv combines two layers:

1. Provenance instrumentation captures a W3C PROV-style graph of a pipeline run.
   It records pipeline runs, step runs, datasets, records, cells, models,
   metrics, and relationships such as `used`, `wasGeneratedBy`,
   `wasDerivedFrom`, `containsDR`, and `containsRC`.
2. Privacy propagation attaches and derives privacy metadata over that graph.
   Each artifact can carry a privacy tuple:

```text
pi(e) = (C(e), U(e), R(e), A(e))
```

Where:

- `C`: sensitivity categories.
- `U`: authorised usage contexts.
- `R`: retention or erasure obligations.
- `A`: authorised access roles.

Operation policies define how privacy metadata should move through workflow
steps such as transformations, reductions, fusions, aggregations, learning, and
evaluation.

## Quick Start

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd PrivacyProv
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the package

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

The editable install reads dependencies from `pyproject.toml`, including
`pandas`, `scikit-learn`, and `pyyaml`.

### 4. Run the ASD walkthrough

```bash
python -m privacyprov.examples.asd_workflow_instrumented
```

This creates the main ASD propagation files in `outputs/`:

- `outputs/asd_propagation_summary.json`
- `outputs/asd_propagated_graph.json`
- `outputs/asd_propagated_nodes.csv`
- `outputs/asd_propagated_relationships.csv`

### 5. Run the other example pipelines

Each example can run with its built-in toy sample data:

```bash
python -m privacyprov.examples.census_instrumented --out-dir outputs/census
python -m privacyprov.examples.german_instrumented --out-dir outputs/german
python -m privacyprov.examples.compas_instrumented --out-dir outputs/compas
```

Each run writes:

- `<prefix>_summary.json`: seed, policy, propagation, graph, and output summary.
- `<prefix>_graph.json`: full provenance and privacy graph.
- `<prefix>_nodes.csv`: Neo4j-friendly node export.
- `<prefix>_relationships.csv`: Neo4j-friendly relationship export.

For example, the Census run writes:

```text
outputs/census/census_summary.json
outputs/census/census_graph.json
outputs/census/census_nodes.csv
outputs/census/census_relationships.csv
```

## Running with Your Own CSV Data

The Census, German Credit, and COMPAS examples accept a CSV path:

```bash
python -m privacyprov.examples.census_instrumented \
  --dataset path/to/census.csv \
  --frac 1.0 \
  --out-dir outputs/census_custom
```

Arguments:

- `--dataset`: optional CSV path. If omitted, a small built-in sample is used.
- `--frac`: optional fraction of the dataset to sample.
- `--out-dir`: output directory for generated graph files.

The input CSV must contain the columns expected by the selected example script.

## Step-by-Step Workflow

The typical PrivacyProv workflow is:

1. Create a `WorkflowContext`.
2. Register the initial input dataframe as a `DatasetArtifact`.
3. Decorate each pipeline function with `@ctx.step(...)`.
4. Run the actual pandas/scikit-learn pipeline.
5. Load initial privacy annotations from JSON.
6. Load operation policies from JSON.
7. Materialise annotations and policies into the provenance graph.
8. Run `PrivacyPropagationEngine`.
9. Export JSON and CSV graph files for inspection or Neo4j import.

A simplified pattern looks like this:

```python
from pathlib import Path

import pandas as pd

from privacyprov import (
    WorkflowContext,
    OperatorType,
    PrivacyConfigLoader,
    InitialPrivacyAnnotator,
    OperationPolicyConfigLoader,
    OperationPolicyMaterializer,
    PrivacyPropagationEngine,
)

ctx = WorkflowContext(
    pipeline_name="my_pipeline",
    run_id="run_001",
    purpose="research",
    materialize_records=True,
    materialize_cells=True,
)

raw = pd.DataFrame({"age": [30, 45], "label": [0, 1]})
ctx.register_dataframe("D0_RawData", raw, role="raw")

@ctx.step(
    name="S1_select_features",
    op=OperatorType.RED,
    inputs=["D0_RawData"],
    outputs=["D1_Features"],
    phase="Preparation",
    policy_id="S1_select_features_policy",
)
def select_features(df: pd.DataFrame) -> pd.DataFrame:
    return df[["age", "label"]].copy()

features = select_features(raw)

privacy_config = PrivacyConfigLoader.load("privacy_annotations.json")
InitialPrivacyAnnotator(ctx.graph, privacy_config).apply()

policy_config = OperationPolicyConfigLoader.load("operation_policies.json")
OperationPolicyMaterializer(ctx.graph, policy_config).apply()

PrivacyPropagationEngine(ctx.graph, privacy_config, policy_config).apply()

ctx.export_json(Path("outputs/my_pipeline_graph.json"))
ctx.export_neo4j_csv(
    Path("outputs/my_pipeline_nodes.csv"),
    Path("outputs/my_pipeline_relationships.csv"),
)
```

## Configuration Files

Each dataset has two main configuration files:

- `*_privacy_annotations.json`: ontology terms, category implications, access
  roles, usage constraints, erasure obligations, and initial annotations.
- `*_operation_policies.json`: operator-aware rules for propagating, rewriting,
  minting, attenuating, or removing privacy metadata.

Current configuration directories:

- `privacyprov/config/ASD/`
- `privacyprov/config/Census/`
- `privacyprov/config/German/`
- `privacyprov/config/Comaps/` for COMPAS-style examples.

## Output Files

The JSON graph contains all nodes, relationships, provenance metadata, privacy
annotations, policy nodes, and propagated privacy facets.

The CSV exports are intended for graph analysis and Neo4j import:

- Nodes include labels such as `Pipeline`, `PipelineRun`, `Step`, `StepRun`,
  `DatasetArtifact`, `DataRecordArtifact`, `DataCellArtifact`, `ModelArtifact`,
  `EvaluationMetric`, `PrivacyAnnotation`, and `OperationPolicy`.
- Relationships include provenance edges, containment edges, policy edges, and
  privacy annotation edges.

The `outputs/neo4j_import/` directory contains cleaned CSV files and helper
scripts for static Neo4j import experiments.

## Troubleshooting

If pandas fails with a NumPy binary compatibility error, use a fresh virtual
environment and reinstall:

```bash
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

If an example cannot find a config file, make sure you are running commands from
the repository root.

## Research Context

PrivacyProv extends a W3C PROV-aligned ML pipeline provenance model with privacy
concepts such as sensitivity categories, usage constraints, erasure obligations,
access roles, and operation policies. The prototype is intended to support
experiments around fine-grained privacy propagation in ML workflows and future
integration with provenance visualisation tools such as MLProvLens.
