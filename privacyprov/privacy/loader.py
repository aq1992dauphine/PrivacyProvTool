from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import PrivacyConfig # to convert loaded data into a structured privacy objects


def _load_raw(path: Path) -> Mapping[str, Any]: # what is Mapping? it is a generic type that represents a dictionary-like object, it is used here to indicate that the function returns a dictionary with string keys and values of any type, this allows us to work with the raw data loaded from JSON/YAML without having to define a specific structure for it, and it also allows us to pass this raw data to the PrivacyConfig.from_mapping method to convert it into a structured PrivacyConfig object. we cann\t use Dict[str, Any] here because it is not guaranteed that the loaded data will be a flat dictionary, it could be a nested dictionary or it could contain lists, so using Mapping[str, Any] allows us to work with any kind of dictionary-like structure that we might encounter in the loaded data.
    suffix = path.suffix.lower() # it checks the file extension of the input path to determine whether it is a JSON or YAML file, and it uses the appropriate library to load the data based on the file extension. if the file extension is not supported, it raises a ValueError to indicate that the input file format is not supported for loading privacy configuration.
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

    @staticmethod # no need for self or cls because this method does not depend on the state of the class or an instance of the class, it is a utility function that can be called directly on the class without needing to create an instance of it, this is appropriate here because the loading of privacy configuration is a stateless operation that does not require any context or state to be maintained within an instance of the class.
    def load(path: str | Path) -> PrivacyConfig:
        path = Path(path)
        data = _load_raw(path)
        return PrivacyConfig.from_mapping(data) # this mehtod converts the raw dictionary int oa structred PrivacyCPnfig object, using the from from the AnnotationSpec class to convert the nested annotation specifications into structured AnnotationSpec objects, this allows us to work with the loaded privacy configuration in a more structured and type-safe way throughout the rest of the codebase, and it also allows us to take advantage of the methods and properties defined in the PrivacyConfig and AnnotationSpec classes to manipulate and access the privacy configuration data more easily.
