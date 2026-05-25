from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple
import re

from privacyprov.core.graph import ProvenanceGraph, Node

from .models import AnnotationSpec, PrivacyConfig
from .ontology import PrivacyOntology


ARTIFACT_LABELS = {
    "DatasetArtifact",
    "DataRecordArtifact",
    "DataCellArtifact",
    "ModelArtifact",
    "EvaluationMetric",
    "Artifact",
}


def _unique(values: Iterable[str]) -> List[str]: # removes duplicates while preserving order
    return list(dict.fromkeys(str(v) for v in values if v is not None and str(v) != ""))


def _safe_key(text: str) -> str: # creates a safe graph key for privacy annotaiotns modes by replacing unusal charachters
    return re.sub(r"[^A-Za-z0-9_:\-.]+", "_", text)


class InitialPrivacyAnnotator:
    """Materialises initial privacy annotations into a provenance graph.

    This component only seeds manual privacy annotations. It does not propagate
    annotations to derived artifacts. Propagation is handled by the next module.
    """

    def __init__(self, graph: ProvenanceGraph, config: PrivacyConfig) -> None:
        self.graph = graph
        self.config = config
        self.ontology = PrivacyOntology(config.category_implications) # this creates a privacy ontology based on the category implications defined in the privacy configuration, this will allow us to understand the relationships between different sensitivity categories and to perform implication closure when applying annotations to the graph, which means that if an artifact is annotated with a certain category, it will also be implicitly annotated with all categories that are implied by that category according to the ontology.
        self.annotation_counter = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def apply(self) -> Dict[str, int]:
        """Apply ontology and all manual annotations to the graph."""
        self._materialise_ontology_terms() # creates graph nodes for privacy vocabulary terms (sensitivity categories, roles, usage and erasure constraints) and creates "implies" relationships between sensitivity categories based on the implication rules defined in the privacy ontology, this will allow us to have a structured representation of the privacy vocabulary in the graph, and it will also allow us to perform reasoning based on the implication rules when we apply annotations to the artifacts in the graph.

        dataset_count = 0
        for dataset_id, spec in self.config.dataset_annotations.items(): # it apppies daatset level annotaiton
            target = self._find_artifact(dataset_id)
            if target is not None:
                self._annotate_node(target, spec, target_level="dataset")
                dataset_count += 1

        record_count = 0
        for dataset_id, spec in self.config.record_default_annotations.items():
            for record_node in self._records_for_dataset(dataset_id):
                self._annotate_node(record_node, spec, target_level="record")
                record_count += 1

        cell_count = 0
        for dataset_id, attr_specs in self.config.attribute_annotations.items():
            for attr, spec in attr_specs.items():
                for cell_node in self._cells_for_dataset_attribute(dataset_id, attr):
                    self._annotate_node(cell_node, spec, target_level="cell")
                    cell_count += 1

        return {
            "dataset_annotations": dataset_count,
            "record_annotations": record_count,
            "cell_annotations": cell_count,
            "privacy_annotation_nodes": len([n for n in self.graph.nodes.values() if n.label == "PrivacyAnnotation"]),
        }

    # ------------------------------------------------------------------
    # Ontology/materialisation helpers
    # ------------------------------------------------------------------
    def _materialise_ontology_terms(self) -> None:
        categories = set(self.ontology.categories())
        for spec in self.config.dataset_annotations.values():
            categories.update(spec.C)
        for spec in self.config.record_default_annotations.values():
            categories.update(spec.C)
        for attr_specs in self.config.attribute_annotations.values():
            for spec in attr_specs.values():
                categories.update(spec.C)

        for category in sorted(categories):
            self.graph.get_or_create_node("SensitivityCategory", category, name=category)

        for source, targets in self.config.category_implications.items():
            self.graph.get_or_create_node("SensitivityCategory", source, name=source)
            for target in targets:
                self.graph.get_or_create_node("SensitivityCategory", target, name=target)
                self.graph.add_rel(
                    "implies",
                    "SensitivityCategory", source,
                    "SensitivityCategory", target,
                )

        for role in sorted(set(self.config.roles)):
            self.graph.get_or_create_node("AccessRole", role, name=role)
        for usage in sorted(set(self.config.usages)):
            self.graph.get_or_create_node("UsageConstraint", usage, name=usage)
        for erasure in sorted(set(self.config.erasures)):
            self.graph.get_or_create_node("ErasureConstraint", erasure, name=erasure)

    def _annotate_node(self, target: Node, spec: AnnotationSpec, *, target_level: str) -> None:# this creates a privacyAnnotaiton node for one target artifact
        self.annotation_counter += 1
        ann_key = _safe_key(f"PA::{target.label}::{target.key}::{self.annotation_counter:04d}")
        explicit_categories = _unique(spec.C)
        closed_categories = self.ontology.closure(explicit_categories)

        # If a lower-level annotation omits U/R/A, inherit those facets from
        # the nearest containing record/dataset when available. This represents
        # the conceptual tables where cells often define C locally but inherit
        # usage and erasure constraints from their record or dataset container.
        inherited = self._container_privacy_props(target)
        usages = _unique(spec.U or inherited.get("privacy_usages", []))
        erasures = _unique(spec.R or inherited.get("privacy_erasures", []))
        roles = _unique(spec.A or inherited.get("privacy_roles", []))

        ann_node = self.graph.get_or_create_node(
            "PrivacyAnnotation",
            ann_key,
            annotationId=ann_key,
            target_label=target.label,
            target_key=target.key,
            granularity=spec.granularity or target_level,
            source=spec.source,
            note=spec.note,
            C_explicit=explicit_categories,
            C=closed_categories,
            U=usages,
            R=erasures,
            A=roles,
        )
        self.graph.add_rel("annotates", "PrivacyAnnotation", ann_node.key, target.label, target.key)

        for category in closed_categories:
            self.graph.get_or_create_node("SensitivityCategory", category, name=category)
            rel_props = {"explicit": category in explicit_categories}
            self.graph.add_rel(
                "hasCategory",
                "PrivacyAnnotation", ann_node.key,
                "SensitivityCategory", category,
                **rel_props,
            )
        for usage in usages:
            self.graph.get_or_create_node("UsageConstraint", usage, name=usage)
            self.graph.add_rel("hasUsage", "PrivacyAnnotation", ann_node.key, "UsageConstraint", usage)
        for erasure in erasures:
            self.graph.get_or_create_node("ErasureConstraint", erasure, name=erasure)
            self.graph.add_rel("hasErasure", "PrivacyAnnotation", ann_node.key, "ErasureConstraint", erasure)
        for role in roles:
            self.graph.get_or_create_node("AccessRole", role, name=role)
            self.graph.add_rel("allowsRole", "PrivacyAnnotation", ann_node.key, "AccessRole", role)

        # Materialise for fast access in later propagation/query layers.
        self._merge_privacy_props( # it stores privacy data directly on the target artifact node for fast access in later propagation and query layers, this is a denormalised representation of the privacy annotations that allows us to quickly understand the privacy properties of an artifact without having to traverse the annotation nodes and their relationships, it also allows us to perform efficient propagation of privacy properties in the workflow based on the annotations applied to the artifacts.
            target,
            categories=closed_categories,
            explicit_categories=explicit_categories,
            usages=usages,
            erasures=erasures,
            roles=roles,
            annotation_sources=[spec.source],
        )

    def _merge_privacy_props(
        self,
        node: Node,
        *,
        categories: List[str],
        explicit_categories: List[str],
        usages: List[str],
        erasures: List[str],
        roles: List[str],
        annotation_sources: List[str],
    ) -> None:
        props = node.props
        props["privacy_categories"] = _unique(props.get("privacy_categories", []) + categories)
        props["privacy_categories_explicit"] = _unique(props.get("privacy_categories_explicit", []) + explicit_categories)
        props["privacy_usages"] = _unique(props.get("privacy_usages", []) + usages)
        props["privacy_erasures"] = _unique(props.get("privacy_erasures", []) + erasures)
        props["privacy_roles"] = _unique(props.get("privacy_roles", []) + roles)
        props["privacy_annotation_sources"] = _unique(props.get("privacy_annotation_sources", []) + annotation_sources)

    # ------------------------------------------------------------------
    # Graph navigation helpers
    # ------------------------------------------------------------------
    def _find_artifact(self, artifact_id: str) -> Optional[Node]:
        for (label, key), node in self.graph.nodes.items():
            if key == artifact_id and label in ARTIFACT_LABELS:
                return node
        return None

    def _records_for_dataset(self, dataset_id: str) -> List[Node]:
        nodes: List[Node] = []
        for rel in self.graph.relationships:
            if (
                rel.rel_type == "containsDR"
                and rel.start_label == "DatasetArtifact"
                and rel.start_key == dataset_id
                and rel.end_label == "DataRecordArtifact"
            ):
                node = self.graph.nodes.get((rel.end_label, rel.end_key))
                if node is not None:
                    nodes.append(node)
        return nodes

    def _cells_for_dataset_attribute(self, dataset_id: str, attribute: str) -> List[Node]:
        nodes: List[Node] = []
        for node in self.graph.nodes.values():
            if node.label != "DataCellArtifact":
                continue
            if node.props.get("dataset_id") == dataset_id and node.props.get("attribute") == attribute:
                nodes.append(node)
        return nodes

    def _container_privacy_props(self, node: Node) -> Dict[str, List[str]]: # find privacy properties from a paretn record or dataset so lower-level annotaitons can inhereit them
        """Return inherited privacy properties from a cell/record container.

        The lookup is intentionally simple and local: cell -> record -> dataset,
        or record -> dataset. It is used only to materialise initial inherited
        U/R/A facets, not to perform end-to-end propagation.
        """
        if node.label == "DataCellArtifact":
            record_key = f"{node.props.get('dataset_id')}::record::{node.props.get('record_id')}"
            record_node = self.graph.nodes.get(("DataRecordArtifact", record_key))
            if record_node is not None:
                return {
                    "privacy_usages": record_node.props.get("privacy_usages", []),
                    "privacy_erasures": record_node.props.get("privacy_erasures", []),
                    "privacy_roles": record_node.props.get("privacy_roles", []),
                }
        if node.label in {"DataCellArtifact", "DataRecordArtifact"}:
            dataset_id = node.props.get("dataset_id")
            if dataset_id:
                dataset_node = self.graph.nodes.get(("DatasetArtifact", str(dataset_id)))
                if dataset_node is not None:
                    return {
                        "privacy_usages": dataset_node.props.get("privacy_usages", []),
                        "privacy_erasures": dataset_node.props.get("privacy_erasures", []),
                        "privacy_roles": dataset_node.props.get("privacy_roles", []),
                    }
        return {}
