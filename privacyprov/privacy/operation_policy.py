from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional
import json
import re

from privacyprov.core.graph import ProvenanceGraph, Node


def _as_list(value: Any) -> List[str]:
    """Normalise a config value into a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, tuple) or isinstance(value, set):
        return [str(v) for v in value]
    return [str(value)]


def _unique(values: Iterable[str]) -> List[str]:
    return list(dict.fromkeys(str(v) for v in values if v is not None and str(v) != ""))


def _safe_key(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_:\-.]+", "_", text)


@dataclass
class OperationPolicySpec:
    """Declarative privacy propagation policy for one workflow step.

    The policy is deliberately permissive: operator-specific fields are stored in
    ``raw`` so the later propagation engine can interpret only the fields it
    understands. This keeps the policy dictionary extensible for new workflows.
    """
    policy_id: str
    step: Optional[str] = None
    operatorType: str = "UNKNOWN"
    contributorGranularity: str = "artifact"
    inputArtifacts: List[str] = field(default_factory=list)
    outputArtifacts: List[str] = field(default_factory=list)
    selectedAttributes: List[str] = field(default_factory=list)
    removedAttributes: List[str] = field(default_factory=list)
    joinKeys: List[str] = field(default_factory=list)
    target: Optional[str] = None
    features: List[str] = field(default_factory=list)
    excludedAttributes: List[str] = field(default_factory=list)
    transformations: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    globalParameters: Dict[str, Any] = field(default_factory=dict)
    mintingRules: List[Dict[str, Any]] = field(default_factory=list)
    attenuationRules: List[Dict[str, Any]] = field(default_factory=list)
    riskRemovalRules: List[Dict[str, Any]] = field(default_factory=list)
    modelExposureMapping: Dict[str, str] = field(default_factory=dict)
    erasureRewrite: Dict[str, str] = field(default_factory=dict)
    modelAccessRoles: List[str] = field(default_factory=list)
    note: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, policy_id: str, data: Mapping[str, Any]) -> "OperationPolicySpec":
        return cls(
            policy_id=str(policy_id),
            step=data.get("step") or data.get("step_name") or data.get("stepName"),
            operatorType=str(data.get("operatorType", "UNKNOWN")),
            contributorGranularity=str(data.get("contributorGranularity", "artifact")),
            inputArtifacts=_as_list(data.get("inputArtifacts")),
            outputArtifacts=_as_list(data.get("outputArtifacts")),
            selectedAttributes=_as_list(data.get("selectedAttributes")),
            removedAttributes=_as_list(data.get("removedAttributes")),
            joinKeys=_as_list(data.get("joinKeys")),
            target=data.get("target"),
            features=_as_list(data.get("features")),
            excludedAttributes=_as_list(data.get("excludedAttributes")),
            transformations={str(k): dict(v) for k, v in data.get("transformations", {}).items()},
            globalParameters=dict(data.get("globalParameters", {})),
            mintingRules=[dict(r) for r in data.get("mintingRules", [])],
            attenuationRules=[dict(r) for r in data.get("attenuationRules", [])],
            riskRemovalRules=[dict(r) for r in data.get("riskRemovalRules", [])],
            modelExposureMapping={str(k): str(v) for k, v in data.get("modelExposureMapping", {}).items()},
            erasureRewrite={str(k): str(v) for k, v in data.get("erasureRewrite", {}).items()},
            modelAccessRoles=_as_list(data.get("modelAccessRoles")),
            note=data.get("note"),
            raw=dict(data),
        )

    def to_node_props(self) -> Dict[str, Any]:
        """Return compact properties to materialise on an OperationPolicy node."""
        return {
            "policy_id": self.policy_id,
            "step": self.step,
            "operatorType": self.operatorType,
            "contributorGranularity": self.contributorGranularity,
            "inputArtifacts": self.inputArtifacts,
            "outputArtifacts": self.outputArtifacts,
            "selectedAttributes": self.selectedAttributes,
            "removedAttributes": self.removedAttributes,
            "joinKeys": self.joinKeys,
            "target": self.target,
            "features": self.features,
            "excludedAttributes": self.excludedAttributes,
            "modelAccessRoles": self.modelAccessRoles,
            "note": self.note,
            "raw_json": json.dumps(self.raw, ensure_ascii=False, default=str),
        }


@dataclass
class OperationPolicyConfig:
    """Collection of operation policies loaded from JSON/YAML."""
    operation_policies: Dict[str, OperationPolicySpec] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "OperationPolicyConfig":
        policies = {
            str(policy_id): OperationPolicySpec.from_mapping(str(policy_id), spec)
            for policy_id, spec in data.get("operation_policies", {}).items()
        }
        return cls(operation_policies=policies, raw=dict(data))


class OperationPolicyConfigLoader:
    """Load operation policies from JSON or YAML."""

    @staticmethod
    def load(path: str | Path) -> OperationPolicyConfig:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() in {".yaml", ".yml"}:
            try:
                import yaml  # type: ignore
            except Exception as exc:  # pragma: no cover
                raise RuntimeError("PyYAML is required to read YAML policy files") from exc
            data = yaml.safe_load(text)
        else:
            data = json.loads(text)
        if not isinstance(data, Mapping):
            raise ValueError("Operation policy file must contain a JSON/YAML object")
        return OperationPolicyConfig.from_mapping(data)


class OperationPolicyMaterializer:
    """Materialise operation policies into the provenance graph.

    This component does not run privacy propagation. It stores the policies in
    graph form and links them to the corresponding design-time Steps and runtime
    StepRuns, so the next component can consume them.
    """

    def __init__(self, graph: ProvenanceGraph, config: OperationPolicyConfig) -> None:
        self.graph = graph
        self.config = config

    def apply(self) -> Dict[str, int]:
        policy_count = 0
        transform_rule_count = 0
        minting_rule_count = 0
        attenuation_rule_count = 0
        risk_removal_rule_count = 0
        exposure_mapping_count = 0
        erasure_rewrite_count = 0
        step_links = 0
        step_run_links = 0

        for policy in self.config.operation_policies.values():
            self._materialise_policy_node(policy)
            policy_count += 1
            step_links += self._link_policy_to_step(policy)
            step_run_links += self._link_policy_to_step_runs(policy)
            transform_rule_count += self._materialise_transformations(policy)
            minting_rule_count += self._materialise_rule_list(policy, "MintingRule", "hasMintingRule", policy.mintingRules)
            attenuation_rule_count += self._materialise_rule_list(policy, "AttenuationRule", "hasAttenuationRule", policy.attenuationRules)
            risk_removal_rule_count += self._materialise_rule_list(policy, "RiskRemovalRule", "hasRiskRemovalRule", policy.riskRemovalRules)
            exposure_mapping_count += self._materialise_model_exposure_mappings(policy)
            erasure_rewrite_count += self._materialise_erasure_rewrites(policy)

        return {
            "operation_policies": policy_count,
            "step_policy_links": step_links,
            "step_run_policy_links": step_run_links,
            "transformation_rules": transform_rule_count,
            "minting_rules": minting_rule_count,
            "attenuation_rules": attenuation_rule_count,
            "risk_removal_rules": risk_removal_rule_count,
            "model_exposure_mappings": exposure_mapping_count,
            "erasure_rewrite_rules": erasure_rewrite_count,
        }

    # ------------------------------------------------------------------
    # Materialisation helpers
    # ------------------------------------------------------------------
    def _materialise_policy_node(self, policy: OperationPolicySpec) -> Node:
        node = self.graph.get_or_create_node(
            "OperationPolicy",
            policy.policy_id,
            **policy.to_node_props(),
        )
        self.graph.get_or_create_node("OperatorType", policy.operatorType, name=policy.operatorType)
        self.graph.add_rel(
            "hasOperatorType",
            "OperationPolicy", policy.policy_id,
            "OperatorType", policy.operatorType,
        )
        return node

    def _link_policy_to_step(self, policy: OperationPolicySpec) -> int:
        count = 0
        for node in self.graph.nodes.values():
            if node.label != "Step":
                continue
            if node.props.get("policy_id") == policy.policy_id or node.key == policy.step:
                self.graph.add_rel(
                    "hasPolicy",
                    "Step", node.key,
                    "OperationPolicy", policy.policy_id,
                )
                # Also materialise the richer policy fields on the Step node for fast lookup.
                node.props["operation_policy_id"] = policy.policy_id
                node.props["contributorGranularity"] = policy.contributorGranularity
                node.props["selectedAttributes"] = policy.selectedAttributes
                node.props["removedAttributes"] = policy.removedAttributes
                node.props["features"] = policy.features
                node.props["target"] = policy.target
                count += 1
        return count

    def _link_policy_to_step_runs(self, policy: OperationPolicySpec) -> int:
        count = 0
        for node in self.graph.nodes.values():
            if node.label != "StepRun":
                continue
            if node.props.get("policy_id") == policy.policy_id or node.props.get("step_id") == policy.step:
                self.graph.add_rel(
                    "usesPolicy",
                    "StepRun", node.key,
                    "OperationPolicy", policy.policy_id,
                )
                node.props["operation_policy_id"] = policy.policy_id
                node.props["contributorGranularity"] = policy.contributorGranularity
                count += 1
        return count

    def _materialise_transformations(self, policy: OperationPolicySpec) -> int:
        count = 0
        for output_attr, spec in policy.transformations.items():
            rule_key = _safe_key(f"{policy.policy_id}::transformation::{output_attr}")
            derived_from = _as_list(spec.get("derivedFrom"))
            preserve_categories = bool(spec.get("preserveCategories", False))
            self.graph.get_or_create_node(
                "TransformationRule",
                rule_key,
                policy_id=policy.policy_id,
                outputAttribute=str(output_attr),
                derivedFrom=derived_from,
                preserveCategories=preserve_categories,
                raw_json=json.dumps(spec, ensure_ascii=False, default=str),
            )
            self.graph.add_rel(
                "hasTransformationRule",
                "OperationPolicy", policy.policy_id,
                "TransformationRule", rule_key,
            )
            count += 1
        return count

    def _materialise_rule_list(
        self,
        policy: OperationPolicySpec,
        label: str,
        rel_type: str,
        rules: List[Dict[str, Any]],
    ) -> int:
        count = 0
        for idx, rule in enumerate(rules, start=1):
            rule_key = _safe_key(f"{policy.policy_id}::{label}::{idx:03d}")
            self.graph.get_or_create_node(
                label,
                rule_key,
                policy_id=policy.policy_id,
                order=idx,
                condition=rule.get("condition"),
                addCategories=_as_list(rule.get("addCategories") or rule.get("add")),
                restrictRolesTo=_as_list(rule.get("restrictRolesTo")),
                removeCategories=_as_list(rule.get("removeCategories") or rule.get("remove")),
                raw_json=json.dumps(rule, ensure_ascii=False, default=str),
            )
            self.graph.add_rel(
                rel_type,
                "OperationPolicy", policy.policy_id,
                label, rule_key,
            )
            # Link category/rule terms when available.
            for cat in _as_list(rule.get("addCategories") or rule.get("add")):
                self.graph.get_or_create_node("SensitivityCategory", cat, name=cat)
                self.graph.add_rel("addsCategory", label, rule_key, "SensitivityCategory", cat)
            for cat in _as_list(rule.get("removeCategories") or rule.get("remove")):
                self.graph.get_or_create_node("SensitivityCategory", cat, name=cat)
                self.graph.add_rel("removesCategory", label, rule_key, "SensitivityCategory", cat)
            for role in _as_list(rule.get("restrictRolesTo")):
                self.graph.get_or_create_node("AccessRole", role, name=role)
                self.graph.add_rel("restrictsToRole", label, rule_key, "AccessRole", role)
            count += 1
        return count

    def _materialise_model_exposure_mappings(self, policy: OperationPolicySpec) -> int:
        count = 0
        for source_cat, target_cat in policy.modelExposureMapping.items():
            mapping_key = _safe_key(f"{policy.policy_id}::modelExposure::{source_cat}::{target_cat}")
            self.graph.get_or_create_node(
                "ModelExposureMapping",
                mapping_key,
                policy_id=policy.policy_id,
                sourceCategory=source_cat,
                targetCategory=target_cat,
            )
            self.graph.add_rel(
                "hasModelExposureMapping",
                "OperationPolicy", policy.policy_id,
                "ModelExposureMapping", mapping_key,
            )
            self.graph.get_or_create_node("SensitivityCategory", source_cat, name=source_cat)
            self.graph.get_or_create_node("SensitivityCategory", target_cat, name=target_cat)
            self.graph.add_rel("mapsFromCategory", "ModelExposureMapping", mapping_key, "SensitivityCategory", source_cat)
            self.graph.add_rel("mapsToCategory", "ModelExposureMapping", mapping_key, "SensitivityCategory", target_cat)
            count += 1
        return count

    def _materialise_erasure_rewrites(self, policy: OperationPolicySpec) -> int:
        count = 0
        for source_obligation, target_obligation in policy.erasureRewrite.items():
            rule_key = _safe_key(f"{policy.policy_id}::erasureRewrite::{source_obligation}::{target_obligation}")
            self.graph.get_or_create_node(
                "ErasureRewriteRule",
                rule_key,
                policy_id=policy.policy_id,
                sourceObligation=source_obligation,
                targetObligation=target_obligation,
            )
            self.graph.add_rel(
                "hasErasureRewriteRule",
                "OperationPolicy", policy.policy_id,
                "ErasureRewriteRule", rule_key,
            )
            self.graph.get_or_create_node("ErasureConstraint", source_obligation, name=source_obligation)
            self.graph.get_or_create_node("ErasureConstraint", target_obligation, name=target_obligation)
            self.graph.add_rel("rewritesFromErasure", "ErasureRewriteRule", rule_key, "ErasureConstraint", source_obligation)
            self.graph.add_rel("rewritesToErasure", "ErasureRewriteRule", rule_key, "ErasureConstraint", target_obligation)
            count += 1
        return count
