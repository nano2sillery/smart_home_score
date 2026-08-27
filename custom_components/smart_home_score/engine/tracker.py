"""Observable State Change Tracker & Drift Detection for Smart Home Score (v0.5.1)."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from .models import (
    ChangeCategory,
    CriterionState,
    CriterionStatus,
    InstallationSnapshot,
    RuleEvaluationResult,
)

if TYPE_CHECKING:
    from .rules import RuleEngine

_LOGGER = logging.getLogger(__name__)


class ChangeTracker:
    """Compares observable Home Assistant state and detects STRUCTURAL drift on confirmed scores.

    Strictly separates MATURITY (durable capability) from HEALTH (transient availability).
    Transient entity unavailabilities do NOT degrade maturity or trigger NEEDS_REVIEW.
    """

    def __init__(self, rule_engine: RuleEngine) -> None:
        """Initialize the change tracker."""
        self.rule_engine = rule_engine

    def detect_changes_and_update(
        self,
        current_states: dict[str, CriterionState],
        new_snapshot: InstallationSnapshot,
        is_transient_outage: bool = False,
    ) -> tuple[dict[str, CriterionState], list[str]]:
        """Evaluate new snapshot against existing confirmed scores without overwriting them.

        Only STRUCTURAL changes (e.g. integration removed, device deleted) can trigger NEEDS_REVIEW.
        Transient entity unavailability leaves maturity score strictly unchanged.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flagged_review_ids: list[str] = []

        if is_transient_outage:
            _LOGGER.debug("Transient outage detected: maturity scores preserved without change.")
            return current_states, []

        new_evaluations = self.rule_engine.evaluate_all(new_snapshot)

        for cid, new_eval in new_evaluations.items():
            current_state = current_states.get(cid)
            if not current_state:
                continue

            # If criterion was confirmed by user
            if current_state.user_confirmed or current_state.status == CriterionStatus.CONFIRMED:
                has_structural_conflict = False
                if new_eval.proposed_score is not None and new_eval.proposed_score != current_state.effective_score:
                    has_structural_conflict = True
                elif current_state.effective_score is not None and current_state.effective_score > 0 and new_eval.proposed_score is None and new_eval.confidence < 70.0:
                    has_structural_conflict = True

                if has_structural_conflict:
                    current_state.status = CriterionStatus.NEEDS_REVIEW
                    current_state.needs_review = True
                    current_state.previous_score = current_state.effective_score
                    current_state.previous_evidence = current_state.evidence
                    current_state.auto_score = new_eval.proposed_score
                    current_state.evidence = new_eval.evidence
                    current_state.needs_review_reason = (
                        f"Changement structurel détecté le {now_str} : nouvelle observation ({new_eval.proposed_score or 'non détecté'}/4) "
                        f"diffère de votre note confirmée ({current_state.effective_score}/4). "
                        f"Preuve : {new_eval.evidence}"
                    )
                    flagged_review_ids.append(cid)
                    _LOGGER.info("Criterion %s flagged for review due to structural change", cid)
            else:
                # Criterion not confirmed by human: apply scan evaluation
                is_auto = new_eval.confidence >= 90.0 and new_eval.proposed_score is not None
                if is_auto:
                    current_state.status = CriterionStatus.AUTO_EVALUATED
                    current_state.auto_score = new_eval.proposed_score
                    current_state.effective_score = new_eval.proposed_score
                    current_state.evaluation_source = EvaluationSource.AUTO
                    current_state.confidence = new_eval.confidence
                    current_state.evidence = new_eval.evidence
                    current_state.applicable = new_eval.applicable
                else:
                    current_state.auto_score = new_eval.proposed_score
                    current_state.confidence = new_eval.confidence
                    current_state.evidence = new_eval.evidence
                    current_state.reason_if_not_auto = new_eval.reason_if_not_auto
                    current_state.applicable = new_eval.applicable
                    if new_eval.evidence and new_eval.proposed_score is not None:
                        current_state.status = CriterionStatus.CAPABILITY_EVIDENCE

        return current_states, flagged_review_ids
