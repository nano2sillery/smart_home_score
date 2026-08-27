"""Actionable Recommendations & Simulation Engine for Smart Home Score (v0.5.1)."""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from .calculator import calculate_audit
from .models import (
    ActionType,
    ActionableRecommendation,
    CriterionState,
    CriterionStatus,
    DifficultyLevel,
    SimulationResult,
)

if TYPE_CHECKING:
    from ..criteria.repository import CriteriaRepository

# Full 59 Criteria Taxonomy: (DifficultyLevel, Primary ActionType, Additional ActionTags, RiskLevel)
CRITERIA_TAXONOMY: dict[str, tuple[DifficultyLevel, ActionType, list[ActionType], str]] = {
    # ELEC — Sécurité Électrique
    "ELEC01": (DifficultyLevel.AVANCEE, ActionType.TEST, [ActionType.MATERIEL], "ÉLEVÉ"),
    "ELEC02": (DifficultyLevel.AVANCEE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "ÉLEVÉ"),
    "ELEC03": (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "FAIBLE"),
    "ELEC04": (DifficultyLevel.AVANCEE, ActionType.MATERIEL, [ActionType.TEST], "ÉLEVÉ"),
    "ELEC05": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.TEST], "MOYEN"),

    # CYBER — Cybersécurité
    "CYBER01": (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "MOYEN"),
    "CYBER02": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "FAIBLE"), # Quick Win
    "CYBER03": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.ORGANISATION], "FAIBLE"), # Quick Win
    "CYBER04": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.ORGANISATION], "FAIBLE"), # Quick Win
    "CYBER05": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.ORGANISATION], "FAIBLE"), # Quick Win
    "CYBER06": (DifficultyLevel.FACILE, ActionType.HABITUDE, [ActionType.DOCUMENTATION], "FAIBLE"),     # Quick Win
    "CYBER07": (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [ActionType.MATERIEL], "MOYEN"),
    "CYBER08": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.AUTOMATISATION], "FAIBLE"), # Quick Win

    # RES — Résilience & Continuité
    "RES01": (DifficultyLevel.MOYENNE, ActionType.TEST, [ActionType.CONFIGURATION], "MOYEN"),
    "RES02": (DifficultyLevel.AVANCEE, ActionType.MATERIEL, [ActionType.TEST], "ÉLEVÉ"),
    "RES03": (DifficultyLevel.FACILE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win
    "RES04": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "FAIBLE"),
    "RES05": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "FAIBLE"),       # Quick Win
    "RES06": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "FAIBLE"),       # Quick Win
    "RES07": (DifficultyLevel.AVANCEE, ActionType.TEST, [ActionType.DOCUMENTATION], "MOYEN"),          # ADVANCED TEST (NOT Quick Win!)
    "RES08": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "MOYEN"),

    # AUTO — Intelligence & Automatisations
    "AUTO01": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),
    "AUTO02": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),
    "AUTO03": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),
    "AUTO04": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),
    "AUTO05": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.MATERIEL], "MOYEN"),
    "AUTO06": (DifficultyLevel.FACILE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win
    "AUTO07": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),
    "AUTO08": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.AUTOMATISATION], "FAIBLE"), # Quick Win
    "AUTO09": (DifficultyLevel.FACILE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win

    # ENER — Énergie & Ressources
    "ENER01": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "MOYEN"),
    "ENER02": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.ORGANISATION], "FAIBLE"),   # Quick Win
    "ENER03": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "FAIBLE"),
    "ENER04": (DifficultyLevel.AVANCEE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "ÉLEVÉ"),
    "ENER05": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.AUTOMATISATION], "FAIBLE"), # Quick Win
    "ENER06": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),
    "ENER07": (DifficultyLevel.MOYENNE, ActionType.AUTOMATISATION, [ActionType.MATERIEL], "FAIBLE"),
    "ENER08": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "MOYEN"),
    "ENER09": (DifficultyLevel.FACILE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win

    # INTER — Interopérabilité & Fonctionnement Local
    "INTER01": (DifficultyLevel.AVANCEE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "MOYEN"),
    "INTER02": (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [ActionType.MATERIEL], "FAIBLE"),
    "INTER03": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"),  # Quick Win
    "INTER04": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"),  # Quick Win
    "INTER05": (DifficultyLevel.AVANCEE, ActionType.MATERIEL, [ActionType.CONFIGURATION], "MOYEN"),
    "INTER06": (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "FAIBLE"),

    # UX — Confort & Expérience Utilisateur
    "UX01": (DifficultyLevel.MOYENNE, ActionType.MATERIEL, [ActionType.ORGANISATION], "FAIBLE"),
    "UX02": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"),    # Quick Win
    "UX03": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"),    # Quick Win
    "UX04": (DifficultyLevel.FACILE, ActionType.CONFIGURATION, [ActionType.HABITUDE], "FAIBLE"),        # Quick Win
    "UX05": (DifficultyLevel.FACILE, ActionType.HABITUDE, [ActionType.ORGANISATION], "FAIBLE"),         # Quick Win
    "UX06": (DifficultyLevel.FACILE, ActionType.AUTOMATISATION, [ActionType.CONFIGURATION], "FAIBLE"),  # Quick Win
    "UX07": (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [ActionType.MATERIEL], "FAIBLE"),

    # MAINT — Maintenance & Documentation
    "MAINT01": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win
    "MAINT02": (DifficultyLevel.FACILE, ActionType.DOCUMENTATION, [ActionType.HABITUDE], "FAIBLE"),     # Quick Win
    "MAINT03": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win
    "MAINT04": (DifficultyLevel.FACILE, ActionType.HABITUDE, [ActionType.ORGANISATION], "FAIBLE"),      # Quick Win
    "MAINT05": (DifficultyLevel.FACILE, ActionType.ORGANISATION, [ActionType.CONFIGURATION], "FAIBLE"), # Quick Win
    "MAINT06": (DifficultyLevel.FACILE, ActionType.DOCUMENTATION, [ActionType.HABITUDE], "FAIBLE"),     # Quick Win
    "MAINT07": (DifficultyLevel.FACILE, ActionType.DOCUMENTATION, [ActionType.HABITUDE], "FAIBLE"),     # Quick Win
}


class SmartHomeAdvisor:
    """Produces prioritized recommendations, simulations and real gain calculations."""

    def __init__(self, repository: CriteriaRepository) -> None:
        """Initialize the advisor."""
        self.repository = repository

    def simulate_improvement(
        self,
        criteria_states: dict[str, CriterionState],
        criterion_id: str,
        simulated_score: int,
    ) -> SimulationResult:
        """Pure simulation of an improvement without mutating criteria_states or store."""
        c_def = self.repository.get_criterion(criterion_id)
        if not c_def:
            raise ValueError(f"Unknown criterion: {criterion_id}")

        # Current baseline audit
        current_audit = calculate_audit(self.repository, criteria_states)
        current_global = current_audit.global_score
        current_dom_score = current_audit.domains[c_def.domain].score

        # Deepcopy states for pure isolation
        simulated_states = copy.deepcopy(criteria_states)
        sim_state = simulated_states.get(criterion_id)
        if not sim_state:
            sim_state = CriterionState(criterion_id=criterion_id)
            simulated_states[criterion_id] = sim_state

        sim_state.effective_score = simulated_score
        sim_state.status = CriterionStatus.CONFIRMED

        # Recalculate audit with the exact same calculator
        sim_audit = calculate_audit(self.repository, simulated_states)
        sim_global = sim_audit.global_score
        sim_dom_score = sim_audit.domains[c_def.domain].score

        exact_gain = round(max(0.0, sim_global - current_global), 2)
        domain_gain = round(max(0.0, sim_dom_score - current_dom_score), 1)

        return SimulationResult(
            criterion_id=criterion_id,
            simulated_score=simulated_score,
            current_global_score=current_global,
            simulated_global_score=sim_global,
            exact_gain=exact_gain,
            domain_code=c_def.domain,
            current_domain_score=current_dom_score,
            simulated_domain_score=sim_dom_score,
            domain_gain=domain_gain,
        )

    def generate_recommendations(
        self,
        criteria_states: dict[str, CriterionState],
        filter_quick_wins: bool = False,
    ) -> list[ActionableRecommendation]:
        """Generate fully prioritized list of actionable recommendations with exact gains."""
        recommendations: list[ActionableRecommendation] = []
        
        for cid, c_def in self.repository.criteria.items():
            st = criteria_states.get(cid)
            if not st or not st.applicable or st.status == CriterionStatus.NOT_APPLICABLE:
                continue

            current_score = st.effective_score if st.effective_score is not None else 0
            if current_score >= 4:
                continue

            target_score = 4
            next_step_score = current_score + 1

            # Compute real gain for target 4
            sim_res = self.simulate_improvement(criteria_states, cid, target_score)
            if sim_res.exact_gain <= 0.0 and current_score > 0:
                continue

            # Recommendation text for the next step
            rec_key = f"{current_score}_to_{next_step_score}"
            rec_text = c_def.recommendations.get(rec_key, c_def.description)

            # Metadata from official taxonomy
            meta = CRITERIA_TAXONOMY.get(cid, (DifficultyLevel.MOYENNE, ActionType.CONFIGURATION, [], "FAIBLE"))
            difficulty, primary_action, action_tags, risk_level = meta

            # Formal Quick Win Rule:
            # 1. Difficulty == FACILE (< 15 min)
            # 2. Risk level == "FAIBLE" (no heavy network, electrical or destructive actions)
            # 3. ActionType NOT in [MATERIEL, TEST]
            # 4. Interesting gain (exact_gain >= 0.3)
            is_quick_win = (
                difficulty == DifficultyLevel.FACILE
                and risk_level == "FAIBLE"
                and primary_action not in [ActionType.MATERIEL, ActionType.TEST]
                and sim_res.exact_gain >= 0.3
            )

            # Prioritization hierarchy:
            # 1 = Critical risk at score 0
            # 2 = Security & Cybersecurity (domain in ["ELEC", "CYBER"] or critical)
            # 3 = Quick wins (high efficiency, fast)
            # 4 = Resilience
            # 5 = Other gains
            if c_def.critical and current_score == 0:
                priority = 1
                priority_label = "CRITIQUE"
            elif c_def.domain in ["ELEC", "CYBER"] or c_def.critical:
                priority = 2
                priority_label = "SÉCURITÉ"
            elif is_quick_win:
                priority = 3
                priority_label = "QUICK WIN"
            elif c_def.domain == "RES":
                priority = 4
                priority_label = "RÉSILIENCE"
            else:
                priority = 5
                priority_label = "AMÉLIORATION"

            dom_name = self.repository.domains.get(c_def.domain, {}).get("name", c_def.domain)

            rec = ActionableRecommendation(
                criterion_id=c_def.id,
                domain=c_def.domain,
                domain_name=dom_name,
                criterion_name=c_def.name,
                current_score=current_score,
                target_score=target_score,
                recommendation_text=rec_text,
                priority=priority,
                priority_label=priority_label,
                difficulty=difficulty,
                action_type=primary_action,
                action_tags=action_tags,
                risk_level=risk_level,
                is_quick_win=is_quick_win,
                is_critical=c_def.critical,
                exact_gain=sim_res.exact_gain,
                domain_gain=sim_res.domain_gain,
            )

            if filter_quick_wins and not is_quick_win:
                continue

            recommendations.append(rec)

        # Sorting: Priority (1 to 5), then highest exact_gain descending
        recommendations.sort(key=lambda r: r.exact_gain, reverse=True)
        recommendations.sort(key=lambda r: r.priority)

        return recommendations
