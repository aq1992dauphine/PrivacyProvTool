from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


FacetMap = Dict[str, List[str]]


def as_list(value: Any) -> List[str]:
    """Normalise a config value into a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, tuple) or isinstance(value, set):
        return [str(v) for v in value]
    return [str(value)]


@dataclass
class AnnotationSpec: #this preresents oen privacy annotaiton declaration
    """A privacy annotation declaration loaded from the policy dictionary.

    The four canonical facets are:
    - C: sensitivity categories;
    - U: authorised usage contexts;
    - R: erasure / retention obligations;
    - A: authorised access roles.
    """
    C: List[str] = field(default_factory=list) # field is used to specify the default value for the list, this is because we want to avoid the mutable default argument issue in python, if we use C: List[str] = [] then all the instances of AnnotationSpec will share the same list object for C, which can lead to unexpected behavior when we modify the list in one instance, by using field(default_factory=list) we ensure that each instance of AnnotationSpec will have its own separate list object for C.
    U: List[str] = field(default_factory=list)
    R: List[str] = field(default_factory=list)
    A: List[str] = field(default_factory=list)
    granularity: str = "artifact" # the granularity of the annotation, it can be "dataset", "record", or "cell", this will help us to understand how the annotation should be applied in the provenance graph and how it should be propagated in the workflow.
    source: str = "manual" # because privacy annotation might be manually, automatically propagated, or inferred from other annotations, this field will help us to track the source of the annotation in the provenance graph, and it will also help us to understand how the annotation was generated and how it was propagated in the workflow.
    note: Optional[str] = None

    @classmethod
    def from_mapping( # creates an annoataionSpec from a dicotnarly loaded from JSON/YAML, it will normalise the values of the facets into lists of strings, and it will set the default values for the granularity and source if they are not provided in the input data.
        cls,
        data: Mapping[str, Any],
        *,
        default_granularity: str = "artifact",
        default_source: str = "manual",
    ) -> "AnnotationSpec": # AnnotationSpec is the class that represents a privacy annotation declaration, it has the four canonical facets C, U, R, A, and it also has the granularity and source fields to track the properties of the annotation. this class will be used to create the privacy annotations for the datasets, records and attributes in the provenance graph, and it will also be used to track the propagation of these annotations in the workflow.
        return cls(
            C=as_list(data.get("C")),
            U=as_list(data.get("U")),
            R=as_list(data.get("R")),
            A=as_list(data.get("A")),
            granularity=str(data.get("granularity", default_granularity)),
            source=str(data.get("source", default_source)),
            note=data.get("note"),
        )

    def explicit_categories(self) -> List[str]: # removes duplicates from the C facet and returns the list of unique sensitivity categories, this will be useful when we want to understand the sensitivity of an artifact or a dataset based on its annotations, and it will also help us to understand how the sensitivity categories are propagated in the workflow.
        return list(dict.fromkeys(self.C))

    def all_terms(self) -> Dict[str, List[str]]: # returns all foru privacy facets as a dictionary of lists of strings, this will be useful when we want to understand the full set of privacy properties associated with an artifact or a dataset based on its annotations, and it will also help us to understand how these properties are propagated in the workflow.
        return {
            "C": list(dict.fromkeys(self.C)),
            "U": list(dict.fromkeys(self.U)),
            "R": list(dict.fromkeys(self.R)),
            "A": list(dict.fromkeys(self.A)),
        }


@dataclass
class PrivacyConfig:
    """Full privacy configuration loaded from JSON/YAML.
    it would store 
    roles
    usages
    erasures
    category implications
    dataset annotations
    record default annotations
    attribute annotations
    """
    roles: List[str] = field(default_factory=list)
    usages: List[str] = field(default_factory=list)
    erasures: List[str] = field(default_factory=list)
    category_implications: Dict[str, List[str]] = field(default_factory=dict)
    dataset_annotations: Dict[str, AnnotationSpec] = field(default_factory=dict)
    record_default_annotations: Dict[str, AnnotationSpec] = field(default_factory=dict) # this is a dictionary where the key is the dataset id and the value is the default annotation spec for the records in that dataset, this will allow us to specify default annotations for all records in a dataset, and it will also allow us to track the propagation of these annotations in the workflow based on the dataset level.
    attribute_annotations: Dict[str, Dict[str, AnnotationSpec]] = field(default_factory=dict) # this is a nested dictionary where the first key is the dataset id, the second key is the attribute name, and the value is the AnnotationSpec for that attribute in that dataset, this will allow us to specify different annotations for the same attribute in different datasets, and it will also allow us to track the propagation of these annotations in the workflow based on the dataset and attribute level.
    raw: Dict[str, Any] = field(default_factory=dict) # keeps the original loaded config dictionary for reference, this can be useful for debugging and for understanding the original structure of the input configuration, especially if we want to compare the loaded configuration with the original JSON/YAML file or if we want to access any additional fields that are not explicitly defined in the PrivacyConfig class.

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PrivacyConfig": # converts the raw json/yaml dictionary into a structred PrivacyConfig object
        dataset_annotations = {
            str(k): AnnotationSpec.from_mapping(v, default_granularity="dataset")
            for k, v in data.get("dataset_annotations", {}).items()
        }
        record_default_annotations = {
            str(k): AnnotationSpec.from_mapping(v, default_granularity="record")
            for k, v in data.get("record_default_annotations", {}).items()
        }

        attribute_annotations: Dict[str, Dict[str, AnnotationSpec]] = {}
        for dataset_id, attrs in data.get("attribute_annotations", {}).items():
            attribute_annotations[str(dataset_id)] = {
                str(attr): AnnotationSpec.from_mapping(spec, default_granularity="cell")
                for attr, spec in attrs.items()
            }

        category_implications = {
            str(k): as_list(v)
            for k, v in data.get("category_implications", {}).items()
        }

        return cls(
            roles=as_list(data.get("roles")),
            usages=as_list(data.get("usages")),
            erasures=as_list(data.get("erasures")),
            category_implications=category_implications,
            dataset_annotations=dataset_annotations,
            record_default_annotations=record_default_annotations,
            attribute_annotations=attribute_annotations,
            raw=dict(data),
        )
