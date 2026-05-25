from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, List, Set


class PrivacyOntology: # it stores category implicaiton rules
    """Small in-memory category ontology supporting implication closure."""

    def __init__(self, implications: Dict[str, Iterable[str]] | None = None) -> None:
        self.implications: Dict[str, Set[str]] = defaultdict(set)
        for source, targets in (implications or {}).items():
            self.implications[str(source)].update(str(t) for t in targets)

    def add_implication(self, source: str, target: str) -> None:
        self.implications[str(source)].add(str(target))

    def categories(self) -> Set[str]:
        cats: Set[str] = set(self.implications.keys())
        for targets in self.implications.values():
            cats.update(targets)
        return cats

    def closure(self, categories: Iterable[str]) -> List[str]:
        """Return the transitive implication closure of the supplied categories.

        The original categories are included in the result. The order is stable
        enough for display: explicit categories appear first, then implied terms.
        """
        explicit = [str(c) for c in categories]
        seen: Set[str] = set(explicit)
        ordered: List[str] = list(dict.fromkeys(explicit))
        queue: deque[str] = deque(ordered)

        while queue:
            current = queue.popleft()
            for implied in sorted(self.implications.get(current, [])):
                if implied not in seen:
                    seen.add(implied)
                    ordered.append(implied)
                    queue.append(implied)
        return ordered
