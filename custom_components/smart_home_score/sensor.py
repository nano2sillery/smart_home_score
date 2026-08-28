"""Sensor platform for Smart Home Score."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    AUTHOR,
    DOMAIN,
    MODEL_VERSION,
    NAME,
    SENSOR_COMPLETENESS,
    SENSOR_CRITICAL_RISKS,
    SENSOR_DOMAIN_AUTO,
    SENSOR_DOMAIN_CYBER,
    SENSOR_DOMAIN_ELEC,
    SENSOR_DOMAIN_ENER,
    SENSOR_DOMAIN_INTER,
    SENSOR_DOMAIN_MAINT,
    SENSOR_DOMAIN_RES,
    SENSOR_DOMAIN_UX,
    SENSOR_ENGINE_VERSION,
    SENSOR_EVALUATED_CRITERIA,
    SENSOR_GLOBAL_SCORE,
    SENSOR_MATURITY_LEVEL,
    SENSOR_POTENTIAL_GAIN,
    VERSION,
)
from .coordinator import SmartHomeScoreCoordinator
from .engine.models import AuditResult


@dataclass(frozen=True, kw_only=True)
class SmartHomeScoreSensorEntityDescription(SensorEntityDescription):
    """Describes Smart Home Score sensor entity."""

    value_fn: Callable[[AuditResult], Any]
    extra_attrs_fn: Callable[[AuditResult], dict[str, Any]] | None = None


SENSOR_DESCRIPTIONS: tuple[SmartHomeScoreSensorEntityDescription, ...] = (
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_GLOBAL_SCORE,
        translation_key=SENSOR_GLOBAL_SCORE,
        icon="mdi:shield-star",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.global_score,
        extra_attrs_fn=lambda result, coordinator=None: {
            "maturity_level": result.maturity_level,
            "is_provisional": result.is_provisional,
            "completeness": result.completeness,
            "critical_count": result.critical_count,
            "potential_gain": result.potential_gain,
            "model_version": result.model_version,
            "auto_evaluated_count": result.auto_evaluated_count,
            "evaluated_count": result.evaluated_count,
            "applicable_count": result.applicable_count,
            "total_count": result.total_count,
            "domain_scores": {
                dom_key: dom_res.score
                for dom_key, dom_res in result.domains.items()
            } if result.domains else {},
            "installation_stats": {
                "devices_count": coordinator.last_snapshot.total_devices if (coordinator and coordinator.last_snapshot) else 0,
                "entities_count": coordinator.last_snapshot.total_entities if (coordinator and coordinator.last_snapshot) else 0,
                "integrations_count": len(coordinator.last_snapshot.integrations_present) if (coordinator and coordinator.last_snapshot) else 0,
                "automations_count": coordinator.last_snapshot.automations_count if (coordinator and coordinator.last_snapshot) else 0,
                "scripts_count": coordinator.last_snapshot.scripts_count if (coordinator and coordinator.last_snapshot) else 0,
                "areas_count": coordinator.last_snapshot.total_areas if (coordinator and coordinator.last_snapshot) else 0,
                "zigbee_devices_count": coordinator.last_snapshot.zigbee_devices_count if (coordinator and coordinator.last_snapshot and coordinator.last_snapshot.has_zigbee) else 0,
                "has_zigbee": coordinator.last_snapshot.has_zigbee if (coordinator and coordinator.last_snapshot) else False,
                "has_matter": coordinator.last_snapshot.has_matter if (coordinator and coordinator.last_snapshot) else False,
                "has_zwave": coordinator.last_snapshot.has_zwave if (coordinator and coordinator.last_snapshot) else False,
            } if (coordinator and coordinator.last_snapshot) else {},
            "recommendations": [
                rec.to_dict()
                for rec in (coordinator.advisor.generate_recommendations(result.criteria_states) if coordinator else [])
            ] if coordinator else [],
            "evolution": (
                coordinator.history_mgr.get_evolution_summary().to_dict()
                if (coordinator and coordinator.history_mgr)
                else {}
            ),
            "criteria_states": {
                cid: {
                    "effective_score": st.effective_score,
                    "auto_score": st.auto_score,
                    "status": st.status.value if hasattr(st.status, "value") else str(st.status),
                    "source": st.evaluation_source.value if hasattr(st.evaluation_source, "value") else str(st.evaluation_source),
                    "confidence": st.confidence,
                    "evidence": st.evidence,
                    "applicable": st.applicable,
                    "user_confirmed": st.user_confirmed,
                }
                for cid, st in result.criteria_states.items()
            } if result.criteria_states else {},
        },
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_COMPLETENESS,
        translation_key=SENSOR_COMPLETENESS,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:progress-check",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.completeness,
        extra_attrs_fn=lambda result: {
            "evaluated_count": result.evaluated_count,
            "applicable_count": result.applicable_count,
            "total_count": result.total_count,
        },
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_EVALUATED_CRITERIA,
        translation_key=SENSOR_EVALUATED_CRITERIA,
        icon="mdi:checkbox-marked-circle-outline",
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda result: result.evaluated_count,
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_ENGINE_VERSION,
        translation_key=SENSOR_ENGINE_VERSION,
        icon="mdi:information-outline",
        value_fn=lambda result: VERSION,
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_MATURITY_LEVEL,
        translation_key=SENSOR_MATURITY_LEVEL,
        icon="mdi:medal-outline",
        value_fn=lambda result: result.maturity_level,
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_CRITICAL_RISKS,
        translation_key=SENSOR_CRITICAL_RISKS,
        icon="mdi:alert-circle-outline",
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda result: result.critical_count,
        extra_attrs_fn=lambda result: {"critical_items": result.critical_items},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_POTENTIAL_GAIN,
        translation_key=SENSOR_POTENTIAL_GAIN,
        icon="mdi:trending-up",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.potential_gain,
    ),
    # 8 Domain Sensors
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_ELEC,
        translation_key=SENSOR_DOMAIN_ELEC,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:flash-alert",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["ELEC"].score if "ELEC" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["ELEC"].contribution,
            "max_weight": result.domains["ELEC"].weight,
            "evaluated_count": result.domains["ELEC"].evaluated_count,
            "applicable_count": result.domains["ELEC"].applicable_count,
        } if "ELEC" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_CYBER,
        translation_key=SENSOR_DOMAIN_CYBER,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:shield-lock",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["CYBER"].score if "CYBER" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["CYBER"].contribution,
            "max_weight": result.domains["CYBER"].weight,
            "evaluated_count": result.domains["CYBER"].evaluated_count,
            "applicable_count": result.domains["CYBER"].applicable_count,
        } if "CYBER" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_RES,
        translation_key=SENSOR_DOMAIN_RES,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:server-network",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["RES"].score if "RES" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["RES"].contribution,
            "max_weight": result.domains["RES"].weight,
            "evaluated_count": result.domains["RES"].evaluated_count,
            "applicable_count": result.domains["RES"].applicable_count,
        } if "RES" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_AUTO,
        translation_key=SENSOR_DOMAIN_AUTO,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:robot-industrial",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["AUTO"].score if "AUTO" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["AUTO"].contribution,
            "max_weight": result.domains["AUTO"].weight,
            "evaluated_count": result.domains["AUTO"].evaluated_count,
            "applicable_count": result.domains["AUTO"].applicable_count,
        } if "AUTO" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_ENER,
        translation_key=SENSOR_DOMAIN_ENER,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:leaf",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["ENER"].score if "ENER" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["ENER"].contribution,
            "max_weight": result.domains["ENER"].weight,
            "evaluated_count": result.domains["ENER"].evaluated_count,
            "applicable_count": result.domains["ENER"].applicable_count,
        } if "ENER" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_INTER,
        translation_key=SENSOR_DOMAIN_INTER,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:swap-horizontal-circle",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["INTER"].score if "INTER" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["INTER"].contribution,
            "max_weight": result.domains["INTER"].weight,
            "evaluated_count": result.domains["INTER"].evaluated_count,
            "applicable_count": result.domains["INTER"].applicable_count,
        } if "INTER" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_UX,
        translation_key=SENSOR_DOMAIN_UX,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:account-group",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["UX"].score if "UX" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["UX"].contribution,
            "max_weight": result.domains["UX"].weight,
            "evaluated_count": result.domains["UX"].evaluated_count,
            "applicable_count": result.domains["UX"].applicable_count,
        } if "UX" in result.domains else {},
    ),
    SmartHomeScoreSensorEntityDescription(
        key=SENSOR_DOMAIN_MAINT,
        translation_key=SENSOR_DOMAIN_MAINT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:wrench",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda result: result.domains["MAINT"].score if "MAINT" in result.domains else 0.0,
        extra_attrs_fn=lambda result: {
            "contribution": result.domains["MAINT"].contribution,
            "max_weight": result.domains["MAINT"].weight,
            "evaluated_count": result.domains["MAINT"].evaluated_count,
            "applicable_count": result.domains["MAINT"].applicable_count,
        } if "MAINT" in result.domains else {},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Smart Home Score sensors based on config_entry."""
    coordinator: SmartHomeScoreCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        SmartHomeScoreSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class SmartHomeScoreSensor(CoordinatorEntity[SmartHomeScoreCoordinator], SensorEntity):
    """Representation of a Smart Home Score Sensor."""

    entity_description: SmartHomeScoreSensorEntityDescription

    def __init__(
        self,
        coordinator: SmartHomeScoreCoordinator,
        entry: ConfigEntry,
        description: SmartHomeScoreSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=NAME,
            manufacturer=AUTHOR,
            model=f"Audit Engine v{MODEL_VERSION}",
            sw_version=VERSION,
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes."""
        if not self.coordinator.data or not self.entity_description.extra_attrs_fn:
            return None
        import inspect
        sig = inspect.signature(self.entity_description.extra_attrs_fn)
        if len(sig.parameters) > 1:
            return self.entity_description.extra_attrs_fn(self.coordinator.data, self.coordinator)
        return self.entity_description.extra_attrs_fn(self.coordinator.data)
