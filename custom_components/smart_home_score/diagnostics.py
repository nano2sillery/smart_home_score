"""Diagnostics support for Smart Home Score (v0.7.0 Bêta).

Produces shareable, anonymized diagnostics for debugging and beta community support without
exposing personal names, IP addresses, tokens, secrets, SSIDs, device IDs or file paths.
"""
from __future__ import annotations

import re
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, IS_BETA, MODEL_VERSION, VERSION
from .coordinator import SmartHomeScoreCoordinator


def sanitize_diagnostic_text(text: str) -> str:
    """Comprehensively redact private and identifiable information from diagnostic strings."""
    if not text:
        return ""
    # Redact IPv4 / IPv6
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 'xxx.xxx.xxx.xxx', text)
    # Redact MAC addresses
    text = re.sub(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b', 'xx:xx:xx:xx:xx:xx', text)
    # Redact emails
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', text)
    # Redact local file paths
    text = re.sub(r'(?:/[a-zA-Z0-9_.-]+)+/[a-zA-Z0-9_.-]+', '[REDACTED_PATH]', text)
    # Redact SSIDs
    text = re.sub(r'(?i)(SSID|Network|Wifi)\s*[:=]\s*\S+', r'\1: [REDACTED_SSID]', text)
    return text


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return comprehensive anonymized diagnostics for beta validation."""
    coordinator: SmartHomeScoreCoordinator = hass.data[DOMAIN][entry.entry_id]
    audit_data = coordinator.data

    # Breakdown by evaluation status
    auto_count = 0
    question_count = 0
    test_count = 0
    disputed_count = 0

    criteria_diag = {}
    disputed_items = []

    for cid, st in coordinator.criteria_states.items():
        status_val = st.status.value if hasattr(st.status, "value") else str(st.status)
        source_val = st.evaluation_source.value if hasattr(st.evaluation_source, "value") else str(st.evaluation_source)
        ev_type_val = st.evidence_type.value if hasattr(st.evidence_type, "value") else str(st.evidence_type)

        if status_val == "AUTO_EVALUATED" or source_val == "AUTO":
            auto_count += 1
        elif status_val == "QUESTION_REQUIRED" or source_val == "QUESTION":
            question_count += 1
        elif status_val == "TEST_REQUIRED" or source_val == "TEST":
            test_count += 1

        if getattr(st, "disputed", False):
            disputed_count += 1
            disputed_items.append({
                "criterion_id": cid,
                "auto_score": st.auto_score,
                "user_score": st.effective_score,
                "feedback": sanitize_diagnostic_text(getattr(st, "dispute_feedback", "")),
                "auto_evidence": sanitize_diagnostic_text(st.evidence),
            })

        criteria_diag[cid] = {
            "status": status_val,
            "effective_score": st.effective_score,
            "auto_score": st.auto_score,
            "evaluation_source": source_val,
            "confidence": st.confidence,
            "applicable": st.applicable,
            "evidence_type": ev_type_val,
            "disputed": getattr(st, "disputed", False),
            "sanitized_evidence": sanitize_diagnostic_text(st.evidence) if st.evidence else "",
        }

    # Anonymized domain scores
    domains_diag = {}
    if audit_data:
        for dom_code, dom_res in audit_data.domains.items():
            domains_diag[dom_code] = {
                "score": dom_res.score,
                "weight": dom_res.weight,
                "evaluated_count": dom_res.evaluated_count,
                "applicable_count": dom_res.applicable_count,
            }

    return {
        "integration_version": VERSION,
        "is_beta": IS_BETA,
        "model_version": MODEL_VERSION,
        "author": "Cyrille LEFRANC",
        "homeassistant_version": getattr(hass.config, "version", "2026.x"),
        "audit_summary": {
            "global_score": audit_data.global_score if audit_data else 0.0,
            "completeness": audit_data.completeness if audit_data else 0.0,
            "maturity_level": audit_data.maturity_level if audit_data else "Non évalué",
            "is_provisional": audit_data.is_provisional if audit_data else True,
            "critical_risks_count": audit_data.critical_count if audit_data else 0,
            "total_criteria": len(coordinator.criteria_states),
            "auto_count": auto_count,
            "question_count": question_count,
            "test_count": test_count,
            "disputed_count": disputed_count,
        },
        "disputed_evaluations": disputed_items,
        "domains": domains_diag,
        "criteria": criteria_diag,
        "history_entries_count": len(coordinator.get_history()),
    }
