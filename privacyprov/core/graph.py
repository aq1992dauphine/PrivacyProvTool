from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
import csv
import json


@dataclass
class Node:
    label: str
    key: str
    props: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    rel_type: str
    start_label: str
    start_key: str
    end_label: str
    end_key: str
    props: Dict[str, Any] = field(default_factory=dict)


class ProvenanceGraph:
    """Small in-memory graph compatible with the user's current MetaModel style."""

    def __init__(self) -> None:
        self.nodes: Dict[Tuple[str, str], Node] = {}
        self.relationships: List[Relationship] = []

    def get_or_create_node(self, label: str, key: str, **props: Any) -> Node:
        node_key = (label, str(key))
        if node_key not in self.nodes:
            all_props = {"key": str(key), **props}
            self.nodes[node_key] = Node(label=label, key=str(key), props=all_props)
        else:
            self.nodes[node_key].props.update(props)
        return self.nodes[node_key]

    def add_rel(
        self,
        rel_type: str,
        start_label: str,
        start_key: str,
        end_label: str,
        end_key: str,
        **props: Any,
    ) -> None:
        self.relationships.append(
            Relationship(
                rel_type=rel_type,
                start_label=start_label,
                start_key=str(start_key),
                end_label=end_label,
                end_key=str(end_key),
                props=props,
            )
        )

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {"label": n.label, "key": n.key, **n.props}
                for n in self.nodes.values()
            ],
            "relationships": [
                {
                    "type": r.rel_type,
                    "start_label": r.start_label,
                    "start_key": r.start_key,
                    "end_label": r.end_label,
                    "end_key": r.end_key,
                    **r.props,
                }
                for r in self.relationships
            ],
        }

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_json_dict(), f, indent=2, ensure_ascii=False)

    def export_neo4j_csv(self, nodes_path: str | Path, rels_path: str | Path) -> None:
        nodes_path = Path(nodes_path)
        rels_path = Path(rels_path)
        nodes_path.parent.mkdir(parents=True, exist_ok=True)
        rels_path.parent.mkdir(parents=True, exist_ok=True)

        with nodes_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["ID", "LABEL", "key", "props_json"])
            for node in self.nodes.values():
                node_id = f"{node.label}|{node.key}"
                writer.writerow([
                    node_id,
                    node.label,
                    node.key,
                    json.dumps(node.props, ensure_ascii=False, default=str),
                ])

        with rels_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["START_ID", "END_ID", "TYPE", "props_json"])
            for rel in self.relationships:
                writer.writerow([
                    f"{rel.start_label}|{rel.start_key}",
                    f"{rel.end_label}|{rel.end_key}",
                    rel.rel_type,
                    json.dumps(rel.props, ensure_ascii=False, default=str),
                ])

    def summary(self) -> Dict[str, Dict[str, int]]:
        from collections import Counter
        return {
            "nodes": dict(Counter(n.label for n in self.nodes.values())),
            "relationships": dict(Counter(r.rel_type for r in self.relationships)),
        }
