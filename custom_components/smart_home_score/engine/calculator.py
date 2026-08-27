"""Independent mathematical scoring calculator for Smart Home Score."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .models import (
    AuditResult,
    CriterionStatus,
    DomainResult,
    ImprovementRecommendation,
)

if TYPE_CHECKING:
    from ..criteria.repository import CriteriaRepository
    from .models import CriterionState


def get_maturity_level(score: float) -> str:
    """Determine the maturity level based on the global score."""
    if score >= 90.0:
        return "Exceptionnel"
    if score >= 80.0:
        return "Très avancé"
    if score >= 65.0:
        return "Avancé"
    if score >= 50.0:
        return "Intermédiaire"
    return "Insuffisant"


def calculate_audit(
    repository: CriteriaRepository,
    criteria_states: dict[str, CriterionState],
    last_audit_date: str | None = None,
    analysis_duration_ms: float = 0.0,
) -> AuditResult:
    """Calculate the complete audit result deterministically."""
    domain_results: dict[str, DomainResult] = {}
    recommendations: list[ImprovementRecommendation] = []
    
    total_criteria_count = len(repository.criteria)
    total_evaluated_count = 0
    total_applicable_count = 0
    total_critical_count = 0
    critical_items: list[str] = []
    total_potential_gain = 0.0

    auto_evaluated_count = 0
    question_required_count = 0
    test_required_count = 0
    not_applicable_count = 0

    global_pts_sum = 0.0
    global_max_weight_sum = 0.0

    for dom_code, dom_cfg in repository.domains.items():
        dom_crits = repository.get_domain_criteria(dom_code)
        dom_weight = dom_cfg["weight"]
        dom_name = dom_cfg["name"]

        dom_pts = 0.0
        dom_max_w = 0.0
        dom_evaluated = 0
        dom_applicable = 0
        dom_total = len(dom_crits)

        for c_def in dom_crits:
            state = criteria_states.get(c_def.id)
            if state is None:
                continue

            if state.status == CriterionStatus.NOT_APPLICABLE or not state.applicable:
                not_applicable_count += 1
                continue

            dom_applicable += 1
            total_applicable_count += 1
            dom_max_w += c_def.weight

            if state.status == CriterionStatus.AUTO_EVALUATED:
                auto_evaluated_count += 1
            elif state.status == CriterionStatus.QUESTION_REQUIRED:
                question_required_count += 1
            elif state.status == CriterionStatus.TEST_REQUIRED:
                test_required_count += 1

            score_val = state.effective_score
            if score_val is not None and score_val in [0, 1, 2, 3, 4]:
                dom_evaluated += 1
                total_evaluated_count += 1
                dom_pts += c_def.weight * (score_val / 4.0)

                # Check critical risk
                if c_def.critical and score_val == 0:
                    total_critical_count += 1
                    critical_items.append(c_def.id)

                # Calculate potential gain if < 4
                if score_val < 4:
                    crit_gain = (c_def.weight / 100.0) * dom_weight * ((4 - score_val) / 4.0)
                    crit_gain_rounded = round(crit_gain, 2)
                    total_potential_gain += crit_gain

                    # Recommendation text
                    next_lvl_key = f"{score_val}_to_{score_val + 1}"
                    rec_text = c_def.recommendations.get(next_lvl_key, c_def.description)

                    prio = 1 if (c_def.critical and score_val == 0) else (2 if c_def.critical else (3 if crit_gain_rounded >= 1.0 else 4))
                    recommendations.append(
                        ImprovementRecommendation(
                            criterion_id=c_def.id,
                            domain=c_def.domain,
                            name=c_def.name,
                            current_score=score_val,
                            target_score=4,
                            potential_gain=crit_gain_rounded,
                            recommendation_text=rec_text,
                            is_critical=c_def.critical,
                            priority=prio,
                        )
                    )

        # Domain score with renormalisation
        if dom_max_w > 0:
            dom_score = (dom_pts / dom_max_w) * 100.0
            dom_score_rounded = round(dom_score, 1)
            dom_contrib = round((dom_score * dom_weight) / 100.0, 2)
            global_pts_sum += (dom_score * dom_weight) / 100.0
            global_max_weight_sum += dom_weight
        else:
            dom_score_rounded = 0.0
            dom_contrib = 0.0

        # Progress bar
        filled = min(10, max(0, int(round(dom_score_rounded / 10.0))))
        empty = 10 - filled
        progress_str = "█" * filled + "░" * empty

        domain_results[dom_code] = DomainResult(
            code=dom_code,
            name=dom_name,
            weight=dom_weight,
            score=dom_score_rounded,
            contribution=dom_contrib,
            max_applicable_weight=dom_max_w,
            evaluated_count=dom_evaluated,
            applicable_count=dom_applicable,
            total_count=dom_total,
            progress_bar=progress_str,
        )

    # Global Score calculation with renormalisation
    if global_max_weight_sum > 0:
        global_score = (global_pts_sum / global_max_weight_sum) * 100.0
        global_score_rounded = round(global_score, 1)
    else:
        global_score_rounded = 0.0

    # Ensure score bounds [0.0, 100.0]
    global_score_rounded = max(0.0, min(100.0, global_score_rounded))

    # Completeness calculation
    if total_applicable_count > 0:
        completeness = (total_evaluated_count / total_applicable_count) * 100.0
        completeness_rounded = round(completeness, 1)
    else:
        completeness_rounded = 0.0

    is_provisional = total_evaluated_count < total_applicable_count
    maturity_level = get_maturity_level(global_score_rounded)

    # Sort recommendations: priority first, then highest gain
    recommendations.sort(key=lambda r: r.potential_gain, reverse=True)
    recommendations.sort(key=lambda r: r.priority)

    return AuditResult(
        global_score=global_score_rounded,
        completeness=completeness_rounded,
        maturity_level=maturity_level,
        is_provisional=is_provisional,
        domains=domain_results,
        criteria_states=criteria_states,
        critical_count=total_critical_count,
        critical_items=critical_items,
        potential_gain=round(total_potential_gain, 1),
        recommendations=recommendations,
        evaluated_count=total_evaluated_count,
        applicable_count=total_applicable_count,
        total_count=total_criteria_count,
        model_version=repository.model_version,
        last_audit_date=last_audit_date,
        analysis_duration_ms=round(analysis_duration_ms, 2),
        auto_evaluated_count=auto_evaluated_count,
        question_required_count=question_required_count,
        test_required_count=test_required_count,
        not_applicable_count=not_applicable_count,
    )
