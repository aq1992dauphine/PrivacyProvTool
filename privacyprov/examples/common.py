from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from privacyprov import (
    InitialPrivacyAnnotator,
    OperationPolicyConfigLoader,
    OperationPolicyMaterializer,
    PrivacyConfigLoader,
    PrivacyPropagationEngine,
)


def load_dataset_or_sample(dataset_path: str | None, sample_factory: Callable[[], pd.DataFrame]) -> pd.DataFrame:
    """Load a CSV dataset if supplied; otherwise return the built-in toy sample."""
    if dataset_path and Path(dataset_path).exists():
        return pd.read_csv(dataset_path)
    return sample_factory()


def finalise_privacyprov_run(
    ctx: Any, # ctx is the WorkflowContext object that contains the graph and other information about the workflow execution, it is used here to export the graph and other outputs of the PrivacyProv run, and to generate a summary of the run that includes information about the seed annotations, policies, propagation results, and the final graph structure, this allows us to capture and save all relevant information about the PrivacyProv run in a structured way that can be easily accessed and analyzed later.
    *,
    privacy_config_path: str | Path,
    operation_policy_path: str | Path,
    out_dir: str | Path,
    prefix: str,
) -> dict[str, Any]:
    """Apply the real PrivacyProv loader/materializer/propagation sequence.

    This replaces the older placeholder PrivacyFramework API.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    privacy_config = PrivacyConfigLoader.load(privacy_config_path) # this loads the privacy configuration from the specified path, it uses the PrivacyConfigLoader class to read the JSON/YAML file and convert it into a structured PrivacyConfig object that contains all the initial privacy annotations and ontology terms defined in the configuration file, this allows us to work with the privacy configuration in a more structured and type-safe way throughout the rest of the codebase, and it also allows us to take advantage of the methods and properties defined in the PrivacyConfig class to manipulate and access the privacy configuration data more easily.
    seed_summary = InitialPrivacyAnnotator(ctx.graph, privacy_config).apply() # this applies the initial privacy annotations to the graph based on the loaded privacy configuration, it uses the InitialPrivacyAnnotator class to traverse the graph and apply the initial annotations to the relevant nodes and edges according to the rules defined in the privacy configuration, this allows us to establish the initial privacy properties of the artifacts and datasets in the graph before we apply any operation policies or propagate these annotations through the workflow, and it also allows us to capture a summary of the seed annotations that were applied to the graph for later analysis and reference.

    policy_config = OperationPolicyConfigLoader.load(operation_policy_path) # this loads the operation policy configuration from the specified path, it uses the OperationPolicyConfigLoader class to read the JSON/YAML file and convert it into a structured OperationPolicyConfig object that contains all the operation policies defined in the configuration file, this allows us to work with the operation policies in a more structured and type-safe way throughout the rest of the codebase, and it also allows us to take advantage of the methods and properties defined in the OperationPolicyConfig class to manipulate and access the operation policy data more easily.
    policy_summary = OperationPolicyMaterializer(ctx.graph, policy_config).apply() # this applies the operation policies to the graph based on the loaded operation policy configuration, it uses the OperationPolicyMaterializer class to traverse the graph and apply the operation policies to the relevant nodes and edges according to the rules defined in the operation policy configuration, this allows us to establish the privacy implications of the operations performed in the workflow based on the defined policies, and it also allows us to capture a summary of the policies that were applied to the graph for later analysis and reference.

    propagation_summary = PrivacyPropagationEngine(ctx.graph, privacy_config, policy_config).apply()

    graph_path = out_dir / f"{prefix}_graph.json"
    nodes_path = out_dir / f"{prefix}_nodes.csv"
    rels_path = out_dir / f"{prefix}_relationships.csv"
    ctx.export_json(graph_path)
    ctx.export_neo4j_csv(nodes_path, rels_path)

    summary = {
        "seed": seed_summary,
        "policies": policy_summary,
        "propagation": propagation_summary,
        "graph": ctx.summary(),
        "outputs": {
            "graph_json": str(graph_path),
            "nodes_csv": str(nodes_path),
            "relationships_csv": str(rels_path),
        },
    }
    (out_dir / f"{prefix}_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return summary


def print_artifact_privacy(ctx: Any, artifact_ids: list[str]) -> None:
    """Print compact C/U/R/A values for selected artifacts."""
    for artifact_id in artifact_ids:
        node = None
        for label in ["DatasetArtifact", "ModelArtifact", "EvaluationMetric", "Artifact"]:
            node = ctx.graph.nodes.get((label, artifact_id))
            if node is not None:
                break
        if node is None:
            print(f"\n{artifact_id}: <missing>")
            continue
        print(f"\n{artifact_id} ({node.label})")
        print("  C=", node.props.get("privacy_categories", []))
        print("  U=", node.props.get("privacy_usages", []))
        print("  R=", node.props.get("privacy_erasures", []))
        print("  A=", node.props.get("privacy_roles", []))
