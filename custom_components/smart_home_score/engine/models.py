"""Data models for Smart Home Score engine (v0.5.1)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CriterionStatus(str, Enum):
    """Lifecycle status of a criterion."""

    NOT_EVALUATED = "NOT_EVALUATED"
    AUTO_EVALUATED = "AUTO_EVALUATED"
    QUESTION_REQUIRED = "QUESTION_REQUIRED"
    TEST_REQUIRED = "TEST_REQUIRED"
    CONFIRMED = "CONFIRMED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvaluationSource(str, Enum):
    """Evaluation source of a criterion."""

    AUTO = "AUTO"
    QUESTION = "QUESTION"
    TEST = "TEST"
    MANUAL = "MANUAL"


class EvidenceType(str, Enum):
    """Three-tier evidence categorization."""

    DIRECT_EVIDENCE = "DIRECT_EVIDENCE"
    CAPABILITY_EVIDENCE = "CAPABILITY_EVIDENCE"
    BEHAVIORAL_EVIDENCE = "BEHAVIORAL_EVIDENCE"


class ActionType(str, Enum):
    """Refined action types according to official taxonomy."""

    CONFIGURATION = "CONFIGURATION"    # System configuration / Settings in HA
    AUTOMATISATION = "AUTOMATISATION"  # Automations / Scripts / Blueprints
    ORGANISATION = "ORGANISATION"      # Areas, naming, labels, dashboards
    DOCUMENTATION = "DOCUMENTATION"    # Written procedures, emergency notes, schema
    TEST = "TEST"                      # Practical tests & verification protocols
    MATERIEL = "MATERIEL"              # Physical hardware addition / Cabling / UPS
    HABITUDE = "HABITUDE"              # User routine, maintenance discipline


class DifficultyLevel(str, Enum):
    """Difficulty level to implement recommendation."""

    FACILE = "FACILE"       # < 15 min, software/process
    MOYENNE = "MOYENNE"     # 15-60 min, automations or config
    AVANCEE = "AVANCÉE"     # Hardware purchase, wiring, extensive changes


class ChangeCategory(str, Enum):
    """Category of observable environment change."""

    TRANSIENT_CHANGE = "TRANSIENT_CHANGE"    # Temporary outage / entity unavailable
    STRUCTURAL_CHANGE = "STRUCTURAL_CHANGE"  # Integration/Device added or removed


@dataclass(frozen=True)
class CriterionDefinition:
    """Immuable definition of a criterion in the repository."""

    id: str
    domain: str
    name: str
    description: str
    weight: int
    critical: bool
    default_evaluation_type: str
    levels: dict[str, str]
    question: str
    test_procedure: str
    recommendations: dict[str, str]
    auto_requirements: dict[str, Any] = field(default_factory=dict)
    model_version: str = "1.0"


@dataclass
class CriterionState:
    """State of an audited criterion."""

    criterion_id: str
    status: CriterionStatus = CriterionStatus.NOT_EVALUATED
    auto_score: int | None = None
    effective_score: int | None = None
    evaluation_source: EvaluationSource = EvaluationSource.MANUAL
    confidence: float = 0.0
    user_confirmed: bool = False
    needs_review: bool = False
    needs_review_reason: str = ""
    previous_score: int | None = None
    previous_evidence: str = ""
    evidence: str = ""
    evidence_type: EvidenceType = EvidenceType.BEHAVIORAL_EVIDENCE
    last_evaluated: str | None = None
    applicable: bool = True
    reason_if_not_auto: str = ""
    disputed: bool = False
    dispute_feedback: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for persistence."""
        return {
            "criterion_id": self.criterion_id,
            "status": self.status.value if isinstance(self.status, CriterionStatus) else self.status,
            "auto_score": self.auto_score,
            "effective_score": self.effective_score,
            "evaluation_source": self.evaluation_source.value if isinstance(self.evaluation_source, EvaluationSource) else self.evaluation_source,
            "confidence": self.confidence,
            "user_confirmed": self.user_confirmed,
            "needs_review": self.needs_review,
            "needs_review_reason": self.needs_review_reason,
            "previous_score": self.previous_score,
            "previous_evidence": self.previous_evidence,
            "evidence": self.evidence,
            "evidence_type": self.evidence_type.value if isinstance(self.evidence_type, EvidenceType) else self.evidence_type,
            "last_evaluated": self.last_evaluated,
            "applicable": self.applicable,
            "reason_if_not_auto": self.reason_if_not_auto,
            "disputed": self.disputed,
            "dispute_feedback": self.dispute_feedback,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CriterionState:
        """Create from dictionary."""
        status_raw = data.get("status", CriterionStatus.NOT_EVALUATED.value)
        source_raw = data.get("evaluation_source", EvaluationSource.MANUAL.value)
        ev_type_raw = data.get("evidence_type", EvidenceType.BEHAVIORAL_EVIDENCE.value)
        return cls(
            criterion_id=data["criterion_id"],
            status=CriterionStatus(status_raw) if status_raw in CriterionStatus.__members__ else CriterionStatus.NOT_EVALUATED,
            auto_score=data.get("auto_score"),
            effective_score=data.get("effective_score"),
            evaluation_source=EvaluationSource(source_raw) if source_raw in EvaluationSource.__members__ else EvaluationSource.MANUAL,
            confidence=float(data.get("confidence", 0.0)),
            user_confirmed=bool(data.get("user_confirmed", False)),
            needs_review=bool(data.get("needs_review", False)),
            needs_review_reason=str(data.get("needs_review_reason", "")),
            previous_score=data.get("previous_score"),
            previous_evidence=str(data.get("previous_evidence", "")),
            evidence=str(data.get("evidence", "")),
            evidence_type=EvidenceType(ev_type_raw) if ev_type_raw in EvidenceType.__members__ else EvidenceType.BEHAVIORAL_EVIDENCE,
            last_evaluated=data.get("last_evaluated"),
            applicable=bool(data.get("applicable", True)),
            reason_if_not_auto=str(data.get("reason_if_not_auto", "")),
            disputed=bool(data.get("disputed", False)),
            dispute_feedback=str(data.get("dispute_feedback", "")),
        )


@dataclass
class InstallationSnapshot:
    """Objective, non-sensitive snapshot of a Home Assistant installation."""

    total_entities: int = 0
    total_devices: int = 0
    total_areas: int = 0
    domains_present: set[str] = field(default_factory=set)
    domain_counts: dict[str, int] = field(default_factory=dict)
    integrations_present: set[str] = field(default_factory=set)
    local_integrations: set[str] = field(default_factory=set)
    cloud_integrations: set[str] = field(default_factory=set)

    local_devices_count: int = 0
    cloud_devices_count: int = 0

    lights_count: int = 0
    covers_count: int = 0
    climates_count: int = 0
    fans_count: int = 0
    switches_count: int = 0
    binary_sensors_count: int = 0
    sensors_count: int = 0
    automations_count: int = 0
    scripts_count: int = 0
    helpers_count: int = 0
    persons_count: int = 0
    users_count: int = 0
    admin_users_count: int = 0
    batteries_count: int = 0
    unavailable_count: int = 0

    has_zigbee: bool = False
    zigbee_devices_count: int = 0
    has_matter: bool = False
    has_mqtt: bool = False
    has_esphome: bool = False
    has_zwave: bool = False

    has_grid_power_realtime: bool = False
    has_grid_energy_total: bool = False
    has_solar_production: bool = False
    solar_power_entity: str = ""
    individual_energy_devices_count: int = 0
    has_water_meter: bool = False
    has_water_leak_sensors: bool = False
    water_leak_sensors_count: int = 0
    has_connected_valve: bool = False

    has_humidity_sensors: bool = False
    has_motion_presence_sensors: bool = False
    has_window_door_sensors: bool = False
    has_ups_monitoring: bool = False

    entities_with_area_count: int = 0
    devices_with_area_count: int = 0
    entities_with_proper_naming_count: int = 0
    automations_with_description_count: int = 0
    
    dashboards_count: int = 0
    has_custom_dashboards: bool = False
    snapshot_time: str = ""


@dataclass
class RuleEvaluationResult:
    """Evaluation result for a single criterion by the rules engine."""

    criterion_id: str
    status: CriterionStatus
    proposed_score: int | None
    confidence: float
    evidence: str
    evidence_type: EvidenceType = EvidenceType.BEHAVIORAL_EVIDENCE
    observations_used: list[str] = field(default_factory=list)
    reason_if_not_auto: str = ""
    disputed: bool = False
    dispute_feedback: str = ""
    applicable: bool = True


@dataclass
class DomainResult:
    """Calculation result for a domain."""

    code: str
    name: str
    weight: int
    score: float
    contribution: float
    max_applicable_weight: float
    evaluated_count: int
    applicable_count: int
    total_count: int
    progress_bar: str


@dataclass
class ActionableRecommendation:
    """Full-featured actionable recommendation for the Advisor (v0.5.1)."""

    criterion_id: str
    domain: str
    domain_name: str
    criterion_name: str
    current_score: int
    target_score: int
    recommendation_text: str
    priority: int                   # 1=Critical, 2=Security/Cyber, 3=QuickWin, 4=Resilience, 5=Other
    priority_label: str             # "CRITIQUE", "SÉCURITÉ", "QUICK WIN", "RÉSILIENCE", "AMÉLIORATION"
    difficulty: DifficultyLevel
    action_type: ActionType
    action_tags: list[ActionType] = field(default_factory=list)
    risk_level: str = "FAIBLE"      # "FAIBLE", "MOYEN", "ÉLEVÉ"
    is_quick_win: bool = False
    is_critical: bool = False
    exact_gain: float = 0.0         # Calculated precisely using calculator.py!
    domain_gain: float = 0.0        # Gain inside domain
    current_level_desc: str = ""
    target_level_desc: str = ""
    why_it_matters: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "criterion_id": self.criterion_id,
            "domain": self.domain,
            "domain_name": self.domain_name,
            "criterion_name": self.criterion_name,
            "current_score": self.current_score,
            "target_score": self.target_score,
            "recommendation_text": self.recommendation_text,
            "priority": self.priority,
            "priority_label": self.priority_label,
            "difficulty": self.difficulty.value if hasattr(self.difficulty, "value") else str(self.difficulty),
            "action_type": self.action_type.value if hasattr(self.action_type, "value") else str(self.action_type),
            "action_tags": [t.value if hasattr(t, "value") else str(t) for t in self.action_tags],
            "risk_level": self.risk_level,
            "is_quick_win": self.is_quick_win,
            "is_critical": self.is_critical,
            "exact_gain": self.exact_gain,
            "domain_gain": self.domain_gain,
            "current_level_desc": self.current_level_desc,
            "target_level_desc": self.target_level_desc,
            "why_it_matters": self.why_it_matters,
        }


@dataclass
class ImprovementRecommendation:
    """Legacy lightweight recommendation for backward compatibility."""

    criterion_id: str
    domain: str
    name: str
    current_score: int
    target_score: int
    potential_gain: float
    recommendation_text: str
    is_critical: bool
    priority: int


@dataclass
class SimulationResult:
    """Simulation result without mutating actual state."""

    criterion_id: str
    simulated_score: int
    current_global_score: float
    simulated_global_score: float
    exact_gain: float
    domain_code: str
    current_domain_score: float
    simulated_domain_score: float
    domain_gain: float

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "criterion_id": self.criterion_id,
            "simulated_score": self.simulated_score,
            "current_global_score": self.current_global_score,
            "simulated_global_score": self.simulated_global_score,
            "exact_gain": self.exact_gain,
            "domain_code": self.domain_code,
            "current_domain_score": self.current_domain_score,
            "simulated_domain_score": self.simulated_domain_score,
            "domain_gain": self.domain_gain,
        }


@dataclass
class AuditHistoryEntry:
    """Clean historical audit record (lightweight, no snapshot payload)."""

    audit_id: str
    date: str
    global_score: float
    domain_scores: dict[str, float]
    completeness: float
    critical_count: int
    model_version: str = "1.0"
    note: str = ""
    criteria_count: int = 59
    completed_at: str = ""
    critical_risks: int = 0

    def __post_init__(self) -> None:
        """Ensure alias properties are always synchronized."""
        if not self.completed_at and self.date:
            self.completed_at = self.date
        elif not self.date and self.completed_at:
            self.date = self.completed_at
        if self.critical_risks == 0 and self.critical_count > 0:
            self.critical_risks = self.critical_count
        elif self.critical_count == 0 and self.critical_risks > 0:
            self.critical_count = self.critical_risks

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for persistence."""
        return {
            "audit_id": self.audit_id,
            "date": self.date,
            "completed_at": self.completed_at or self.date,
            "global_score": self.global_score,
            "domain_scores": self.domain_scores,
            "completeness": self.completeness,
            "critical_count": self.critical_count,
            "critical_risks": self.critical_risks or self.critical_count,
            "criteria_count": self.criteria_count,
            "model_version": self.model_version,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuditHistoryEntry:
        """Create from dictionary."""
        date_val = data.get("completed_at") or data.get("date", "")
        crit_val = int(data.get("critical_risks") or data.get("critical_count", 0))
        return cls(
            audit_id=data.get("audit_id", ""),
            date=date_val,
            completed_at=date_val,
            global_score=float(data.get("global_score", 0.0)),
            domain_scores=data.get("domain_scores", {}),
            completeness=float(data.get("completeness", 0.0)),
            critical_count=crit_val,
            critical_risks=crit_val,
            criteria_count=int(data.get("criteria_count", 59)),
            model_version=str(data.get("model_version", "1.0")),
            note=str(data.get("note", "")),
        )


@dataclass
class EvolutionSummary:
    """Historical progression summary."""

    total_audits: int
    first_audit_score: float
    latest_audit_score: float
    total_progression: float
    history_entries: list[AuditHistoryEntry]


@dataclass
class AuditResult:
    """Complete audit result calculated by the engine."""

    global_score: float
    completeness: float
    maturity_level: str
    is_provisional: bool
    domains: dict[str, DomainResult]
    criteria_states: dict[str, CriterionState]
    critical_count: int
    critical_items: list[str]
    potential_gain: float
    recommendations: list[ImprovementRecommendation]
    evaluated_count: int
    applicable_count: int
    total_count: int
    model_version: str
    last_audit_date: str | None = None
    analysis_duration_ms: float = 0.0
    auto_evaluated_count: int = 0
    question_required_count: int = 0
    test_required_count: int = 0
    not_applicable_count: int = 0
