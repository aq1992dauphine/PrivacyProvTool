########## this script is import to modify the csv files into clean versions by splittign the props_json into the correspoding columns
import base64
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


def encode_props(value: Any) -> str:
    """Encode nested properties as Base64 JSON so CSV quoting cannot break."""
    raw = json.dumps(value or {}, ensure_ascii=False, sort_keys=True)
    return base64.b64encode(raw.encode("utf-8")).decode("ascii")


def stringify(value: Any) -> str:
    """Flatten simple values for CSV."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return "|".join(str(v) for v in value)
    if isinstance(value, dict):
        return encode_props(value)
    return str(value)


def load_graph(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def node_id(node: Dict[str, Any]) -> str:
    return str(
        node.get("id")
        or node.get("key")
        or node.get("uid")
        or node.get("local_id")
    )


def node_label(node: Dict[str, Any]) -> str:
    label = node.get("label") or node.get("type") or "ProvNode"
    if isinstance(label, list):
        return str(label[0]) if label else "ProvNode"
    return str(label)


def node_props(node: Dict[str, Any]) -> Dict[str, Any]:
    props = dict(node.get("props") or {})
    for k, v in node.items():
        if k not in {"props", "id", "key", "uid", "label"}:
            props.setdefault(k, v)
    return props


def rel_source(rel: Dict[str, Any]) -> str:
    return str(
        rel.get("source")
        or rel.get("start")
        or rel.get("start_key")
        or rel.get("startKey")
    )


def rel_target(rel: Dict[str, Any]) -> str:
    return str(
        rel.get("target")
        or rel.get("end")
        or rel.get("end_key")
        or rel.get("endKey")
    )


def rel_type(rel: Dict[str, Any]) -> str:
    return str(
        rel.get("type")
        or rel.get("rel_type")
        or rel.get("relationship")
        or "RELATED_TO"
    )


def rel_props(rel: Dict[str, Any]) -> Dict[str, Any]:
    props = dict(rel.get("props") or {})
    for k, v in rel.items():
        if k not in {
            "props",
            "source",
            "target",
            "start",
            "end",
            "start_key",
            "end_key",
            "startKey",
            "endKey",
            "type",
            "rel_type",
            "relationship",
        }:
            props.setdefault(k, v)
    return props


def write_nodes(graph: Dict[str, Any], pipeline: str, out_path: Path) -> None:
    nodes = graph.get("nodes", [])

    fields = [
        "id",
        "label",
        "pipeline",
        "name",
        "type",
        "privacy_categories",
        "privacy_usages",
        "privacy_erasures",
        "privacy_roles",
        "props_b64",
    ]

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
            quoting=csv.QUOTE_ALL,
            doublequote=True,
            lineterminator="\n",
        )
        writer.writeheader()

        for n in nodes:
            props = node_props(n)
            row = {
                "id": node_id(n),
                "label": node_label(n),
                "pipeline": pipeline,
                "name": stringify(props.get("name") or props.get("label") or node_id(n)),
                "type": stringify(props.get("type") or node_label(n)),
                "privacy_categories": stringify(props.get("privacy_categories")),
                "privacy_usages": stringify(props.get("privacy_usages")),
                "privacy_erasures": stringify(props.get("privacy_erasures")),
                "privacy_roles": stringify(props.get("privacy_roles")),
                "props_b64": encode_props(props),
            }
            writer.writerow(row)


def write_relationships(graph: Dict[str, Any], pipeline: str, out_path: Path) -> None:
    relationships = graph.get("relationships", graph.get("rels", []))

    fields = [
        "source",
        "target",
        "type",
        "pipeline",
        "props_b64",
    ]

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
            quoting=csv.QUOTE_ALL,
            doublequote=True,
            lineterminator="\n",
        )
        writer.writeheader()

        for r in relationships:
            row = {
                "source": rel_source(r),
                "target": rel_target(r),
                "type": rel_type(r),
                "pipeline": pipeline,
                "props_b64": encode_props(rel_props(r)),
            }
            writer.writerow(row)


def convert(graph_json: str, pipeline: str, out_dir: str) -> Tuple[Path, Path]:
    graph_path = Path(graph_json)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    graph = load_graph(graph_path)

    nodes_out = out / f"{pipeline}_nodes_clean.csv"
    rels_out = out / f"{pipeline}_relationships_clean.csv"

    write_nodes(graph, pipeline, nodes_out)
    write_relationships(graph, pipeline, rels_out)

    return nodes_out, rels_out


if __name__ == "__main__":
    # Edit these paths as needed.
    jobs = [
        ("census/census_graph.json", "census"),
        ("compas/compas_graph.json", "compas"),
        ("german/german_graph.json", "german"),
        ("asd/asd_graph.json", "asd"),
    ]

    for graph_json, pipeline in jobs:
        graph_path = Path(graph_json)
        if not graph_path.exists():
            print(f"Skipping missing file: {graph_path}")
            continue

        nodes_csv, rels_csv = convert(graph_json, pipeline, "neo4j_import")
        print(f"{pipeline}:")
        print(f"  nodes -> {nodes_csv}")
        print(f"  rels  -> {rels_csv}")