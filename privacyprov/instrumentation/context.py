from __future__ import annotations

from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
import inspect
import time
import uuid

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None  # type: ignore

from privacyprov.core.enums import ArtifactType, OperatorType
from privacyprov.core.graph import ProvenanceGraph
from privacyprov.core.models import ArtifactRef


class WorkflowContext:
    """Workflow instrumentation layer for pandas/scikit-learn-style ML scripts.

    The context records:
    - design-time Step nodes with operator type;
    - retrospective StepRun nodes;
    - DatasetArtifact / ModelArtifact / EvaluationMetric nodes;
    - used, wasGeneratedBy, wasDerivedFrom, containsDR, containsRC relationships.

    It does not compute privacy propagation yet. Later components consume this graph.
    """

    def __init__( # THIS OBJECT WOULD INTIALIZE THE workflow context, it will create the initial nodes in the provenance graph for the pipeline and the pipeline run, it will also set up the properties of the context such as the pipeline name, run id, purpose and materialization options for records and cells. this context object will be used to track the execution of the workflow and to register the steps and artifacts in the provenance graph.
        self,
        pipeline_name: str,
        run_id: Optional[str] = None,
        purpose: Optional[str] = None,
        materialize_records: bool = True,
        materialize_cells: bool = False,
    ) -> None:
        self.pipeline_name = pipeline_name
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:10]}"
        self.purpose = purpose
        self.materialize_records = materialize_records
        self.materialize_cells = materialize_cells
        self.graph = ProvenanceGraph()
        self.artifacts: Dict[str, ArtifactRef] = {}
        self._step_counter = 0

        # Core pipeline nodes
        self.graph.get_or_create_node("Pipeline", pipeline_name, name=pipeline_name)
        self.graph.get_or_create_node(
            "PipelineRun",
            self.run_id,
            Pipeline_id=pipeline_name,
            purpose=purpose,
            started_at=time.time(),
        )
        self.graph.add_rel("executes", "PipelineRun", self.run_id, "Pipeline", pipeline_name)

    # ------------------------------------------------------------------
    # Artifact registration
    # ------------------------------------------------------------------
    def register_dataframe( # this funciton is used to register a pandas dataframe as a dataset artifact in the provenance graph, it will also create record and cell artifacts if materialize_records and materialize_cells are set to True respectively.
        self,
        artifact_id: str,
        df: Any, 
        *, # the * in the function signature means that all the parameters after it must be passed as keyword arguments, this is a common pattern in python to make the code more readable and to avoid mistakes when passing arguments to the function.
        role: Optional[str] = None,
        record_id_col: Optional[str] = None,
        source: str = "manual_register",
        materialize_records: Optional[bool] = None,
        materialize_cells: Optional[bool] = None,
    ) -> ArtifactRef:
        """Register a pandas DataFrame as a DatasetArtifact.

        record_id_col controls record-level provenance. If absent, row index values
        are used as record identifiers.
        """
        if pd is None:
            raise RuntimeError("pandas is required to register DataFrame artifacts")
        if not hasattr(df, "columns"):
            raise TypeError("register_dataframe expects a pandas DataFrame-like object")

        materialize_records = self.materialize_records if materialize_records is None else materialize_records
        materialize_cells = self.materialize_cells if materialize_cells is None else materialize_cells

        columns = [str(c) for c in list(df.columns)]
        props = {
            "name": artifact_id,
            "role": role,
            "source": source,
            "n_rows": int(len(df)),
            "n_cols": int(len(columns)),
            "columns": columns,
            "record_id_col": record_id_col,
            "artifact_kind": ArtifactType.DATASET.value,
        }
        self.graph.get_or_create_node("DatasetArtifact", artifact_id, **props)
        ref = ArtifactRef( # this is the reference that will be stored in the context for the registered artifact, it will be used to link the artifact to the steps that produce and consume it.
            key=artifact_id,
            label="DatasetArtifact",
            name=artifact_id,
            artifact_type=ArtifactType.DATASET,
            props=props,
        )
        self.artifacts[artifact_id] = ref

        if materialize_records:
            for idx, row in df.iterrows():
                rid = str(row[record_id_col]) if record_id_col and record_id_col in df.columns else str(idx)
                record_key = f"{artifact_id}::record::{rid}"
                self.graph.get_or_create_node(
                    "DataRecordArtifact",
                    record_key,
                    record_id=rid,
                    dataset_id=artifact_id,
                    artifact_kind=ArtifactType.RECORD.value,
                )
                self.graph.add_rel(
                    "containsDR",
                    "DatasetArtifact", artifact_id,
                    "DataRecordArtifact", record_key,
                )

                if materialize_cells:
                    for attr in columns:
                        value = row[attr]
                        cell_key = f"{artifact_id}::record::{rid}::cell::{attr}"
                        self.graph.get_or_create_node(
                            "DataCellArtifact",
                            cell_key,
                            record_id=rid,
                            dataset_id=artifact_id,
                            attribute=attr,
                            value=value.item() if hasattr(value, "item") else value,
                            dtype=str(df[attr].dtype),
                            artifact_kind=ArtifactType.CELL.value,
                        )
                        self.graph.add_rel(
                            "containsRC",
                            "DataRecordArtifact", record_key,
                            "DataCellArtifact", cell_key,
                        )
        return ref # this ref represents a reference to the registered dataframe artifact, it contains the key, label, name, artifact type and properties of the artifact, it will be used to link the artifact to the steps that produce and consume it.

    def register_model( 
        self,
        artifact_id: str,
        model: Any,
        *,
        role: str = "model",
        framework: str = "scikit-learn",
        source: str = "manual_register",
    ) -> ArtifactRef:
        props = {
            "name": artifact_id,
            "role": role,
            "framework": framework,
            "source": source,
            "model_class": model.__class__.__name__,
            "artifact_kind": ArtifactType.MODEL.value,
        }
        self.graph.get_or_create_node("ModelArtifact", artifact_id, **props)
        ref = ArtifactRef(
            key=artifact_id,
            label="ModelArtifact",
            name=artifact_id,
            artifact_type=ArtifactType.MODEL,
            props=props,
        )
        self.artifacts[artifact_id] = ref
        return ref

    def register_metric(
        self,
        artifact_id: str,
        name: str,
        value: float,
        *,
        split: Optional[str] = None,
        source: str = "manual_register",
    ) -> ArtifactRef:
        props = {
            "name": name,
            "value": float(value),
            "split": split,
            "source": source,
            "artifact_kind": ArtifactType.METRIC.value,
        }
        self.graph.get_or_create_node("EvaluationMetric", artifact_id, **props)
        ref = ArtifactRef(
            key=artifact_id,
            label="EvaluationMetric",
            name=name,
            artifact_type=ArtifactType.METRIC,
            props=props,
        )
        self.artifacts[artifact_id] = ref
        return ref

    # ------------------------------------------------------------------
    # Step decorator
    # ------------------------------------------------------------------
    def step(
        self,
        *,# 
        name: str,
        op: OperatorType | str,
        inputs: Sequence[str],
        outputs: Sequence[str],
        phase: str = "",
        policy_id: Optional[str] = None,
        output_roles: Optional[Mapping[str, str]] = None,
        record_id_col: Optional[str] = None,
        props: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]: # callable that takes a function and returns a function, this is the signature of a decorator in python, the decorator will be used to wrap the functions that represent the steps in the workflow, it will record the execution of the steps and the artifacts that are produced and consumed by each step in the provenance graph.
        """Decorator for instrumenting a workflow step.

        The wrapped function should return either:
        - one object when outputs has length 1;
        - a tuple/list matching outputs;
        - a dict mapping output artifact IDs to objects.
        """
        operator_type = OperatorType(op) if isinstance(op, str) else op
        props = props or {}
        output_roles = output_roles or {}

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]: # here, it receives the real use function fpr example train_classifier
            # Design-time Step node.
            self.graph.get_or_create_node(# creates a design-time Step node for this step, this represents the abstract step in the pipeline, such as "tran classifer"
                "Step",
                name,
                name=name,
                phase=phase,
                operator=operator_type.value,
                policy_id=policy_id,
                function=f"{func.__module__}.{func.__name__}",
                **props,
            )

            @wraps(func)# this is the funciotn that actually runs whenever the user calls the decorated function
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                self._step_counter += 1
                step_run_id = f"{self.run_id}::{self._step_counter:03d}::{name}" # it creates a unique StepRun ID, so one pipeline step can have many executions
                start = time.time()

                self.graph.get_or_create_node(  # it creates a retrospective StepRun node for this step execution, it will be linked to the design-time Step node and to the PipelineRun node, it will also be linked to the input and output artifacts of this step execution.
                    "StepRun",
                    step_run_id,
                    step_id=name,
                    phase=phase,
                    framework="python",
                    operatorType=operator_type.value,
                    policy_id=policy_id,
                    input_artifacts=list(inputs),
                    output_artifacts=list(outputs),
                )
                self.graph.add_rel("contains", "PipelineRun", self.run_id, "StepRun", step_run_id) # link the StepRun to the PipelineRun
                self.graph.add_rel("executes", "StepRun", step_run_id, "Step", name) # link the StepRun to the Step

                # Link inputs to StepRun.
                for input_id in inputs:
                    input_ref = self.artifacts.get(input_id)
                    if input_ref is None:
                        raise KeyError(f"Input artifact '{input_id}' is not registered")
                    self.graph.add_rel("used", "StepRun", step_run_id, input_ref.label, input_ref.key) # links all declared inout artifact. 

                result = func(*args, **kwargs)
                result_map = self._normalise_outputs(outputs, result) # it normalizes the outputs of the step fucniton into a dictionary mapping

                # Register outputs and link to StepRun + inputs.
                for output_id, output_obj in result_map.items():
                    if pd is not None and hasattr(output_obj, "columns"): # regsiter the output as a dataframe artifact if it looks like a dataframe, this will create a new dataset artifact in the provenance graph for this output, and it will link it to the step run and to the input artifacts that were used to produce it.
                        out_ref = self.register_dataframe(
                            output_id,
                            output_obj,
                            role=output_roles.get(output_id, "derived"),
                            record_id_col=record_id_col,
                            source=f"step:{name}",
                        )
                    elif self._looks_like_model(output_obj): # register the output as a model artifact if it looks like a model, this will create a new model artifact in the provenance graph for this output, and it will link it to the step run and to the input artifacts that were used to produce it.
                        out_ref = self.register_model(output_id, output_obj, source=f"step:{name}")
                    elif isinstance(output_obj, (int, float)): # register the output as a metric artifact if it looks like a metric, this will create a new metric artifact in the provenance graph for this output, and it will link it to the step run and to the input artifacts that were used to produce it.
                        out_ref = self.register_metric(output_id, output_id, float(output_obj), source=f"step:{name}")
                    else:
                        out_ref = self._register_generic_artifact(output_id, output_obj, source=f"step:{name}")

                    self.graph.add_rel("wasGeneratedBy", out_ref.label, out_ref.key, "StepRun", step_run_id)
                    for input_id in inputs:
                        input_ref = self.artifacts[input_id]
                        self.graph.add_rel("wasDerivedFrom", out_ref.label, out_ref.key, input_ref.label, input_ref.key)

                duration = time.time() - start
                self.graph.get_or_create_node( # it updates the retrospective StepRun node with the execution duration and status, this will allow us to track the performance of each step execution in the provenance graph.
                    "StepRun",
                    step_run_id,
                    duration_seconds=duration,
                    status="success",
                )
                return result

            return wrapper
        return decorator

    def _normalise_outputs(self, outputs: Sequence[str], result: Any) -> Dict[str, Any]:
        if isinstance(result, dict):
            missing = [o for o in outputs if o not in result]
            if missing:
                raise ValueError(f"Result dict is missing outputs: {missing}")
            return {o: result[o] for o in outputs}
        if len(outputs) == 1:
            return {outputs[0]: result}
        if not isinstance(result, (list, tuple)) or len(result) != len(outputs):
            raise ValueError("Function must return a tuple/list matching outputs")
        return dict(zip(outputs, result))

    def _looks_like_model(self, obj: Any) -> bool:
        return hasattr(obj, "fit") or hasattr(obj, "predict") or obj.__class__.__module__.startswith("sklearn")

    def _register_generic_artifact(self, artifact_id: str, value: Any, *, source: str) -> ArtifactRef:
        props = {
            "name": artifact_id,
            "value_repr": repr(value)[:500],
            "source": source,
            "artifact_kind": ArtifactType.GENERIC.value,
        }
        self.graph.get_or_create_node("Artifact", artifact_id, **props)
        ref = ArtifactRef(
            key=artifact_id,
            label="Artifact",
            name=artifact_id,
            artifact_type=ArtifactType.GENERIC,
            props=props,
        )
        self.artifacts[artifact_id] = ref
        return ref

    # ------------------------------------------------------------------
    # Export helpers
    # ------------------------------------------------------------------
    def export_json(self, path: str | Path) -> None:
        self.graph.export_json(path)

    def export_neo4j_csv(self, nodes_path: str | Path, rels_path: str | Path) -> None:
        self.graph.export_neo4j_csv(nodes_path, rels_path)

    def summary(self) -> Dict[str, Dict[str, int]]:
        return self.graph.summary()
