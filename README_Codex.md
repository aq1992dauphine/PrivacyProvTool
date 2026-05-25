# Codex Project Brief — Privacy-Aware MLProvLens / PrivacyProv

## Project goal

Build a Python prototype called `privacyprov` for privacy-aware provenance propagation in tabular ML pipelines.

The tool supports instrumented Python workflows using:
- pandas DataFrames for data preparation,
- scikit-learn-style training/evaluation,
- lightweight decorators to declare pipeline steps.

The goal is not to analyse arbitrary Python automatically. The supported class is **instrumented pandas/scikit-learn tabular ML pipelines**.

## Scientific context

This implementation extends a W3C PROV-aligned ML pipeline provenance meta-model and MLProvLens.

The existing provenance model captures:
- Pipeline, Stage, Step,
- PipelineRun, StepRun,
- Artifact and subtypes:
  - DatasetArtifact,
  - DataRecordArtifact,
  - DataCellArtifact,
  - ModelArtifact,
  - EvaluationMetric,
- PROV-style relations:
  - used,
  - wasGeneratedBy,
  - wasDerivedFrom,
  - containsDR,
  - containsRC.

The privacy extension adds:
- PrivacyAnnotation,
- SensitivityCategory,
- UsageConstraint,
- ErasureConstraint,
- AccessRole,
- OperationPolicy.

Each artifact can receive a privacy annotation:

pi(e) = (C(e), U(e), R(e), A(e))

where:
- C = sensitivity categories,
- U = authorised usage contexts,
- R = retention/erasure obligations,
- A = authorised access roles.

