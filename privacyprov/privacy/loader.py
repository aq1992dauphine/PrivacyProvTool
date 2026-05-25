from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import PrivacyConfig # to convert loaded data int a strcutred privacy objects


def _load_raw(path: Path) -> Mapping[str, Any]:
    suffix = path.suffix.lower()
    with path.open("r", encoding="utf-8") as f:
        if suffix in {".json", ".jsn"}:
            return json.load(f)
        if suffix in {".yaml", ".yml"}:
            try:
                import yaml  # type: ignore
            except Exception as exc:  # pragma: no cover
                raise RuntimeError(
                    "YAML configuration requires PyYAML. Use JSON or install pyyaml."
                ) from exc
            return yaml.safe_load(f)
    raise ValueError(f"Unsupported privacy configuration file extension: {suffix}")


class PrivacyConfigLoader:
    """Loads initial privacy annotations and ontology terms from JSON/YAML."""

    @staticmethod
    def load(path: str | Path) -> PrivacyConfig:
        path = Path(path)
        data = _load_raw(path)
        return PrivacyConfig.from_mapping(data)
