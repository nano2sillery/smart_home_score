"""Constants for the Smart Home Score integration (v0.7.0-beta.1)."""
from typing import Final

DOMAIN: Final = "smart_home_score"
NAME: Final = "Smart Home Score"
VERSION: Final = "0.7.0-beta.8"
MODEL_VERSION: Final = "1.0"
AUTHOR: Final = "Cyrille LEFRANC"
MIN_HA_VERSION: Final = "2024.7.0"
IS_BETA: Final = True
BETA_TAG: Final = "Bêta"

# Sensor Keys
SENSOR_GLOBAL_SCORE: Final = "global_score"
SENSOR_COMPLETENESS: Final = "completeness"
SENSOR_EVALUATED_CRITERIA: Final = "evaluated_criteria"
SENSOR_ENGINE_VERSION: Final = "engine_version"
SENSOR_MATURITY_LEVEL: Final = "maturity_level"
SENSOR_CRITICAL_RISKS: Final = "critical_risks"
SENSOR_POTENTIAL_GAIN: Final = "potential_gain"

# Domain Sensor Keys
SENSOR_DOMAIN_ELEC: Final = "elec_score"
SENSOR_DOMAIN_CYBER: Final = "cyber_score"
SENSOR_DOMAIN_RES: Final = "res_score"
SENSOR_DOMAIN_AUTO: Final = "auto_score"
SENSOR_DOMAIN_ENER: Final = "ener_score"
SENSOR_DOMAIN_INTER: Final = "inter_score"
SENSOR_DOMAIN_UX: Final = "ux_score"
SENSOR_DOMAIN_MAINT: Final = "maint_score"

# Service Names
SERVICE_SUBMIT_ANSWER: Final = "submit_answer"
SERVICE_SKIP_QUESTION: Final = "skip_question"
SERVICE_RESET_AUDIT: Final = "reset_audit"
SERVICE_RUN_ANALYSIS: Final = "run_analysis"
SERVICE_SIMULATE_IMPROVEMENT: Final = "simulate_improvement"
SERVICE_REEVALUATE_CRITERION: Final = "reevaluate_criterion"
SERVICE_RECORD_HISTORY: Final = "record_history"
SERVICE_DISPUTE_AUTO_EVALUATION: Final = "dispute_auto_evaluation"

# Frontend URL with Cache-Busting Version Query Parameter
URL_BASE_STATIC: Final = "/smart_home_score_static"
URL_FRONTEND_CARD: Final = "/smart_home_score_static/smart-home-score-card.js"
URL_FRONTEND_CARD_VERSIONED: Final = f"/smart_home_score_static/smart-home-score-card.js?v={VERSION}"
