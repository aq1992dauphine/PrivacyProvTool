from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enums import ArtifactType, OperatorType


@dataclass  
# these classes represent the artifacts that will be stored in the provenance graph, they will be used to track the execution of the steps and the artifacts that are produced and consumed by each step.
class ArtifactRef: # reference to an artifact already registered in the graph
    """Reference to a runtime artifact registered in the provenance graph."""
    key: str # example "dataset_1234"
    label: str # example "dataset.csv"
    name: str # example "dataset.csv"
    artifact_type: ArtifactType
    props: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StepSpec: # what the workflow step is
    """Design-time step specification."""
    name: str
    operator_type: OperatorType
    phase: str = ""
    policy_id: Optional[str] = None
    props: Dict[str, Any] = field(default_factory=dict)


@dataclass # one actual execution of that step
class StepRunRecord:
    """Retrospective execution record for one step invocation."""
    key: str
    step_name: str
    operator_type: OperatorType
    input_artifacts: List[str]
    output_artifacts: List[str]
    props: Dict[str, Any] = field(default_factory=dict)
