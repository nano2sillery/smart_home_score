"""Criteria repository loader and manager."""
from __future__ import annotations

import json
import os
from typing import Any

from ..engine.models import CriterionDefinition

DOMAINS_CONFIG: dict[str, dict[str, Any]] = {
    "ELEC": {"name": "Sécurité électrique et sûreté", "weight": 15, "icon": "mdi:flash-alert"},
    "CYBER": {"name": "Cybersécurité", "weight": 15, "icon": "mdi:shield-lock"},
    "RES": {"name": "Résilience et continuité", "weight": 15, "icon": "mdi:server-network"},
    "AUTO": {"name": "Intelligence et automatisations", "weight": 15, "icon": "mdi:robot-industrial"},
    "ENER": {"name": "Énergie et ressources", "weight": 15, "icon": "mdi:leaf"},
    "INTER": {"name": "Interopérabilité et fonctionnement local", "weight": 10, "icon": "mdi:swap-horizontal-circle"},
    "UX": {"name": "Confort et expérience utilisateur", "weight": 10, "icon": "mdi:account-group"},
    "MAINT": {"name": "Maintenance et documentation", "weight": 5, "icon": "mdi:wrench"},
}


class CriteriaRepository:
    """Repository managing criterion definitions for a given model version."""

    def __init__(self, model_version: str = "1.0") -> None:
        """Initialize the repository."""
        self.model_version = model_version
        self._criteria: dict[str, CriterionDefinition] = {}
        self._load_criteria()

    def _load_criteria(self) -> None:
        """Load JSON criteria definitions for current model version."""
        version_dir_name = f"v{self.model_version.replace('.', '_')}"
        base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), version_dir_name)
        if not os.path.exists(base_path):
            raise FileNotFoundError(f"Criteria version directory not found: {base_path}")

        for filename in sorted(os.listdir(base_path)):
            if filename.endswith(".json") and not filename.startswith("."):
                fpath = os.path.join(base_path, filename)
                with open(fpath, "r", encoding="utf-8") as f:
                    crits_data = json.load(f)
                    for c_dict in crits_data:
                        definition = CriterionDefinition(
                            id=c_dict["id"],
                            domain=c_dict["domain"],
                            name=c_dict["name"],
                            description=c_dict["description"],
                            weight=c_dict["weight"],
                            critical=c_dict["critical"],
                            default_evaluation_type=c_dict["default_evaluation_type"],
                            levels=c_dict["levels"],
                            question=c_dict["question"],
                            test_procedure=c_dict["test_procedure"],
                            recommendations=c_dict["recommendations"],
                            auto_requirements=c_dict.get("auto_requirements", {}),
                            model_version=c_dict.get("model_version", self.model_version),
                        )
                        self._criteria[definition.id] = definition

    @property
    def criteria(self) -> dict[str, CriterionDefinition]:
        """Return all criteria definitions."""
        return self._criteria

    def get_criterion(self, criterion_id: str) -> CriterionDefinition | None:
        """Get a specific criterion definition."""
        return self._criteria.get(criterion_id.upper())

    def get_domain_criteria(self, domain_code: str) -> list[CriterionDefinition]:
        """Get criteria belonging to a domain."""
        return [c for c in self._criteria.values() if c.domain == domain_code.upper()]

    @property
    def domains(self) -> dict[str, dict[str, Any]]:
        """Return the domains configuration."""
        return DOMAINS_CONFIG
