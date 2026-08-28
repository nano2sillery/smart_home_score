"""DataUpdateCoordinator for Smart Home Score v0.5.0."""
from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, MODEL_VERSION, VERSION
from .criteria.repository import CriteriaRepository
from .engine.advisor import SmartHomeAdvisor
from .engine.analyzer import HomeAssistantAnalyzer
from .engine.assistant import AssistantQuestionCard, AuditAssistant
from .engine.calculator import calculate_audit
from .engine.history import AuditHistoryManager
from .engine.models import (
    ActionableRecommendation,
    AuditHistoryEntry,
    AuditResult,
    CriterionState,
    CriterionStatus,
    EvaluationSource,
    EvolutionSummary,
    SimulationResult,
)
from .engine.rules import CONFIDENCE_AUTO_THRESHOLD, RuleEngine
from .engine.store import SmartHomeScoreStore
from .engine.tracker import ChangeTracker

_LOGGER = logging.getLogger(__name__)


class SmartHomeScoreCoordinator(DataUpdateCoordinator[AuditResult]):
    """Coordinator to manage Smart Home Score state, interactive audit, advisor and history."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )
        self.model_version: str = MODEL_VERSION
        self.engine_version: str = VERSION
        self.repository = CriteriaRepository(model_version=self.model_version)
        self.analyzer = HomeAssistantAnalyzer(hass)
        self.rule_engine = RuleEngine(self.repository)
        self.assistant = AuditAssistant(self.repository)
        self.advisor = SmartHomeAdvisor(self.repository)
        self.history_mgr = AuditHistoryManager(hass, model_version=self.model_version)
        self.tracker = ChangeTracker(self.rule_engine)
        self.store = SmartHomeScoreStore(hass, model_version=self.model_version)
        self.criteria_states: dict[str, CriterionState] = {}
        self.last_snapshot: InstallationSnapshot | None = None
        self.last_audit_date: str | None = None
        self.last_analysis_duration_ms: float = 0.0

    async def async_init_store(self) -> None:
        """Load stored criteria states and history."""
        await self.history_mgr.async_load()
        self.last_snapshot = await self.analyzer.async_collect_snapshot()
        stored_states = await self.store.async_load()
        if stored_states:
            self.criteria_states = stored_states
        else:
            await self.async_run_analysis(save_on_complete=False)

    async def async_run_analysis(self, save_on_complete: bool = True) -> AuditResult:
        """Execute on-demand local environment analysis with change tracking."""
        start_time = time.perf_counter()
        _LOGGER.info("Starting Smart Home Score automated analysis (v0.5.0)...")

        # 1. Collect non-sensitive snapshot
        snapshot = await self.analyzer.async_collect_snapshot()
        self.last_snapshot = snapshot

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_audit_date = now_str

        # 2. If existing states exist, run change tracker to detect drift without overwriting
        if self.criteria_states:
            self.criteria_states, flagged_ids = self.tracker.detect_changes_and_update(
                self.criteria_states, snapshot
            )
            if flagged_ids:
                _LOGGER.info("Identified %d criteria requiring review after environment changes", len(flagged_ids))
        else:
            # First initialization
            evaluations = self.rule_engine.evaluate_all(snapshot)
            for cid, eval_res in evaluations.items():
                is_auto = eval_res.confidence >= CONFIDENCE_AUTO_THRESHOLD and eval_res.proposed_score is not None
                status = CriterionStatus.AUTO_EVALUATED if is_auto else eval_res.status
                self.criteria_states[cid] = CriterionState(
                    criterion_id=cid,
                    status=status,
                    auto_score=eval_res.proposed_score,
                    effective_score=eval_res.proposed_score if is_auto else None,
                    evaluation_source=EvaluationSource.AUTO if is_auto else EvaluationSource.MANUAL,
                    confidence=eval_res.confidence,
                    user_confirmed=False,
                    needs_review=False,
                    evidence=eval_res.evidence,
                    evidence_type=eval_res.evidence_type,
                    last_evaluated=now_str,
                    applicable=eval_res.applicable,
                    reason_if_not_auto=eval_res.reason_if_not_auto,
                )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        self.last_analysis_duration_ms = elapsed_ms
        _LOGGER.info("Smart Home Score analysis completed in %.2f ms", elapsed_ms)

        if save_on_complete:
            await self.store.async_save(self.criteria_states, last_audit_date=self.last_audit_date)

        res = self._calculate_current_result()
        if hasattr(self, "async_set_updated_data"):
            self.async_set_updated_data(res)
        else:
            self.data = res
        return res

    def _calculate_current_result(self) -> AuditResult:
        """Calculate audit result from current states."""
        return calculate_audit(
            repository=self.repository,
            criteria_states=self.criteria_states,
            last_audit_date=self.last_audit_date,
            analysis_duration_ms=self.last_analysis_duration_ms,
        )

    async def _async_update_data(self) -> AuditResult:
        """Coordinator update method."""
        if not self.criteria_states:
            await self.async_init_store()
        return self._calculate_current_result()

    async def async_submit_answer(self, criterion_id: str, answer_key: str) -> None:
        """Apply user answer via Assistant and recalculate."""
        self.assistant.apply_answer(criterion_id, answer_key, self.criteria_states)
        self.last_audit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.store.async_save(self.criteria_states, last_audit_date=self.last_audit_date)
        
        # If audit reached 100% completeness, record history entry
        current_res = self._calculate_current_result()
        if not current_res.is_provisional:
            await self.history_mgr.async_record_audit(current_res, note="Audit complet finalisé")

        await self.async_refresh()

    async def async_skip_question(self, criterion_id: str) -> None:
        """Skip question with 'Je ne sais pas' / 'Faire plus tard' (no score assigned)."""
        self.assistant.apply_answer(criterion_id, "unknown", self.criteria_states)
        self.last_audit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.store.async_save(self.criteria_states, last_audit_date=self.last_audit_date)
        await self.async_refresh()


    async def async_dispute_auto_evaluation(
        self,
        criterion_id: str,
        user_score: int,
        feedback: str = "",
    ) -> None:
        """User disputes an automated evaluation, providing manual score & feedback for beta diagnostics."""
        st = self.criteria_states.get(criterion_id)
        if not st:
            st = CriterionState(criterion_id=criterion_id)
            self.criteria_states[criterion_id] = st

        st.effective_score = user_score
        st.status = CriterionStatus.CONFIRMED
        st.evaluation_source = EvaluationSource.MANUAL
        st.user_confirmed = True
        st.disputed = True
        st.dispute_feedback = feedback
        st.last_evaluated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        await self.store.async_save(self.criteria_states, last_audit_date=self.last_audit_date)
        await self.async_refresh()

    async def async_reset_audit(self) -> None:
        """Archive completed audit (completeness == 100%), clear user answers and re-execute clean automatic analysis from scratch."""
        current_res = self._calculate_current_result()
        if current_res.completeness >= 100.0 and not current_res.is_provisional:
            await self.history_mgr.async_record_audit(
                current_res,
                note=f"Audit précédent archivé ({current_res.global_score:.1f}/100)",
            )

        self.criteria_states.clear()
        await self.async_run_analysis(save_on_complete=True)
        await self.async_refresh()

    async def async_restart_audit(self) -> None:
        """Alias for async_reset_audit to start a new audit from scratch."""
        await self.async_reset_audit()

    # --- v0.5 Advisor & Simulation Methods ---

    def get_recommendations(self, filter_quick_wins: bool = False) -> list[ActionableRecommendation]:
        """Get prioritized actionable recommendations."""
        return self.advisor.generate_recommendations(self.criteria_states, filter_quick_wins=filter_quick_wins)

    def simulate_improvement(self, criterion_id: str, simulated_score: int) -> SimulationResult:
        """Pure simulation of an improvement without mutating state or store."""
        return self.advisor.simulate_improvement(self.criteria_states, criterion_id, simulated_score)

    async def async_reevaluate_criterion(self, criterion_id: str) -> AssistantQuestionCard | None:
        """Trigger targeted re-evaluation of a specific criterion ('J'ai effectué cette amélioration').

        Does NOT grant points automatically. Checks snapshot evidence and presents the question/test.
        """
        snapshot = await self.analyzer.async_collect_snapshot()
        eval_res = self.rule_engine.evaluate_criterion(criterion_id, snapshot)

        st = self.criteria_states.get(criterion_id)
        if not st:
            st = CriterionState(criterion_id=criterion_id)
            self.criteria_states[criterion_id] = st

        # If direct evidence is available now with >= 90% confidence -> update auto
        if eval_res.confidence >= CONFIDENCE_AUTO_THRESHOLD and eval_res.proposed_score is not None:
            st.auto_score = eval_res.proposed_score
            st.effective_score = eval_res.proposed_score
            st.status = CriterionStatus.AUTO_EVALUATED
            st.evidence = eval_res.evidence
            st.needs_review = False
            await self.store.async_save(self.criteria_states, last_audit_date=self.last_audit_date)
            await self.async_refresh()
            return None

        # Otherwise, present the interactive question card for user confirmation/test
        st.auto_score = eval_res.proposed_score
        st.evidence = eval_res.evidence
        st.status = eval_res.status
        return self.assistant.build_question_card(criterion_id, self.criteria_states)

    # --- v0.5 History & Evolution Methods ---

    async def async_record_history(self, note: str = "") -> AuditHistoryEntry:
        """Explicitly record a history snapshot."""
        current_res = self._calculate_current_result()
        entry = await self.history_mgr.async_record_audit(current_res, note=note)
        return entry

    def get_history(self) -> list[AuditHistoryEntry]:
        """Get history entries for MODEL_VERSION = '1.0'."""
        return self.history_mgr.get_history(self.model_version)

    def get_evolution_summary(self) -> EvolutionSummary:
        """Get score evolution summary."""
        return self.history_mgr.get_evolution_summary(self.model_version)
