from enum import Enum


class OperatorType(str, Enum): # this represent the operator types, which are used to classify the operators in the privacy propagation model.
    """Operator classes used by the privacy propagation model."""
    RED = "RED"       # filtering, projection, split
    TR = "TR"         # value transformation, encoding, normalisation
    AGG = "AGG"       # aggregation, summarisation
    FUS = "FUS"       # join/fusion of sources
    LEARN = "LEARN"   # model training
    EVAL = "EVAL"     # evaluation artifact generation; optional extension
    UNKNOWN = "UNKNOWN"


class ArtifactType(str, Enum):
    DATASET = "DatasetArtifact"
    RECORD = "DataRecordArtifact"
    CELL = "DataCellArtifact"
    MODEL = "ModelArtifact"
    METRIC = "EvaluationMetric"
    GENERIC = "Artifact"
