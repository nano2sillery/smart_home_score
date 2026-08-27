"""Home Assistant Environment Analyzer for Smart Home Score.

Collects an objective, non-sensitive snapshot of the installation using exclusively
public Home Assistant registries and APIs (entity_registry, device_registry, area_registry, states).
"""
from __future__ import annotations

import logging
import re
import time
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import (
    area_registry as ar,
    device_registry as dr,
    entity_registry as er,
)

from .models import InstallationSnapshot

_LOGGER = logging.getLogger(__name__)

# Known protocol and integration categories
LOCAL_INTEGRATIONS_SET = {
    "zha", "zigbee2mqtt", "mqtt", "esphome", "matter", "zwave_js",
    "shelly", "wled", "tasmota", "homematicip_local", "freebox",
    "modbus", "snmp", "systemmonitor", "local_tuya", "tuya_local",
    "nut", "apcupsd", "keba", "tibber_pulse", "lixee", "zlinky_tic"
}

CLOUD_INTEGRATIONS_SET = {
    "tuya", "smartthings", "somfy", "overkiz", "netatmo", "withings",
    "ecobee", "nest", "tado", "meross_cloud", "ewelink"
}


class HomeAssistantAnalyzer:
    """Analyzer extracting objective observations from Home Assistant."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the analyzer."""
        self.hass = hass

    async def async_collect_snapshot(self) -> InstallationSnapshot:
        """Collect the installation snapshot asynchronously."""
        start_time = time.perf_counter()
        snapshot = InstallationSnapshot()
        snapshot.snapshot_time = datetime.now().isoformat()

        # 1. Entity Registry
        ent_reg = er.async_get(self.hass)
        dev_reg = dr.async_get(self.hass)
        area_reg = ar.async_get(self.hass)

        all_entries = list(ent_reg.entities.values())
        all_devices = list(dev_reg.devices.values())
        all_areas = list(area_reg.areas.values())

        snapshot.total_entities = len(all_entries)
        snapshot.total_devices = len(all_devices)
        snapshot.total_areas = len(all_areas)

        # Count devices with area
        snapshot.devices_with_area_count = sum(1 for d in all_devices if d.area_id)

        # 2. Config Entries / Integrations
        if hasattr(self.hass, "config_entries") and self.hass.config_entries:
            for entry in self.hass.config_entries.async_entries():
                dom = entry.domain
                snapshot.integrations_present.add(dom)
                if dom in LOCAL_INTEGRATIONS_SET:
                    snapshot.local_integrations.add(dom)
                elif dom in CLOUD_INTEGRATIONS_SET:
                    snapshot.cloud_integrations.add(dom)

        # Check key protocols
        snapshot.has_zigbee = bool("zha" in snapshot.integrations_present or "zigbee2mqtt" in snapshot.integrations_present)
        snapshot.has_matter = "matter" in snapshot.integrations_present
        snapshot.has_mqtt = "mqtt" in snapshot.integrations_present
        snapshot.has_esphome = "esphome" in snapshot.integrations_present
        snapshot.has_zwave = "zwave_js" in snapshot.integrations_present
        snapshot.has_ups_monitoring = bool({"nut", "apcupsd", "snmp"}.intersection(snapshot.integrations_present))

        # Count Zigbee devices if available
        if snapshot.has_zigbee:
            for d in all_devices:
                for ident in d.identifiers:
                    if ident[0] in ("zha", "zigbee2mqtt"):
                        snapshot.zigbee_devices_count += 1
                        break

        # 3. States & Entity attributes analysis
        all_states = self.hass.states.async_all()
        proper_name_pattern = re.compile(r"^[a-z_]+[0-9]*\.[a-z0-9]+_[a-z0-9_]+$")
        raw_hex_pattern = re.compile(r"(0x[0-9a-fA-F]{8,}|[0-9a-fA-F]{16})")

        for state in all_states:
            domain = state.domain
            snapshot.domains_present.add(domain)
            snapshot.domain_counts[domain] = snapshot.domain_counts.get(domain, 0) + 1

            eid = state.entity_id
            attrs = state.attributes or {}
            device_class = attrs.get("device_class", "")
            unit = str(attrs.get("unit_of_measurement", "")).lower()

            if state.state in ("unavailable", "unknown"):
                snapshot.unavailable_count += 1

            # Check naming conventions (no raw IEEE hex IDs)
            if not raw_hex_pattern.search(eid):
                snapshot.entities_with_proper_naming_count += 1

            # Domain specific classification
            if domain == "light":
                snapshot.lights_count += 1
            elif domain == "cover":
                snapshot.covers_count += 1
            elif domain == "climate":
                snapshot.climates_count += 1
            elif domain == "fan":
                snapshot.fans_count += 1
            elif domain == "switch":
                snapshot.switches_count += 1
            elif domain == "binary_sensor":
                snapshot.binary_sensors_count += 1
                if device_class in ("moisture", "water") or "fuite" in eid or "water" in eid:
                    snapshot.has_water_leak_sensors = True
                    snapshot.water_leak_sensors_count += 1
                if device_class in ("motion", "occupancy", "presence") or "motion" in eid or "presence" in eid:
                    snapshot.has_motion_presence_sensors = True
                if device_class in ("door", "window", "opening") or "fenetre" in eid or "porte" in eid:
                    snapshot.has_window_door_sensors = True
            elif domain == "sensor":
                snapshot.sensors_count += 1
                if device_class == "battery" or unit == "%" and "battery" in eid or "pile" in eid:
                    snapshot.batteries_count += 1
                if device_class == "humidity" or unit == "%" and ("humidity" in eid or "humidite" in eid):
                    snapshot.has_humidity_sensors = True

                # Realtime power & energy detection
                if device_class == "power" or unit in ("w", "kw", "va"):
                    if any(k in eid for k in ("grid", "linky", "total", "reseau", "general", "maison", "puissance_active")):
                        snapshot.has_grid_power_realtime = True
                    if any(k in eid for k in ("solar", "photovoltaic", "production", "solaire", "inverter")):
                        snapshot.has_solar_production = True
                        snapshot.solar_power_entity = eid

                if device_class == "energy" or unit in ("kwh", "mwh", "wh"):
                    if any(k in eid for k in ("grid", "linky", "total", "reseau", "general", "index", "hchp", "hchc")):
                        snapshot.has_grid_energy_total = True
                    if any(k in eid for k in ("solar", "photovoltaic", "production", "solaire")):
                        snapshot.has_solar_production = True
                    # Individual submetering candidate
                    if not any(k in eid for k in ("grid", "total", "general", "reseau")):
                        snapshot.individual_energy_devices_count += 1

                # Water detection
                if device_class == "water" or unit in ("l", "m³", "m3", "gal", "l/min", "l/h") or "water" in eid or "eau" in eid:
                    if unit in ("m³", "m3", "l", "gal") or "compteur" in eid or "conso" in eid:
                        snapshot.has_water_meter = True

            elif domain == "valve":
                snapshot.has_connected_valve = True
            elif domain == "automation":
                snapshot.automations_count += 1
                if attrs.get("description"):
                    snapshot.automations_with_description_count += 1
            elif domain == "script":
                snapshot.scripts_count += 1
            elif domain in ("input_boolean", "input_select", "input_number", "input_text", "input_datetime", "timer", "counter"):
                snapshot.helpers_count += 1
            elif domain == "person":
                snapshot.persons_count += 1

        # Check entity area assignment
        for ent in all_entries:
            if ent.area_id:
                snapshot.entities_with_area_count += 1
            elif ent.device_id:
                dev = dev_reg.async_get(ent.device_id)
                if dev and dev.area_id:
                    snapshot.entities_with_area_count += 1

        # Dashboards count
        if hasattr(self.hass, "data") and "frontend" in self.hass.data:
            snapshot.has_custom_dashboards = True
            snapshot.dashboards_count = 2

        elapsed = (time.perf_counter() - start_time) * 1000.0
        _LOGGER.debug("Installation snapshot collected in %.2f ms (entities: %d, devices: %d)", elapsed, snapshot.total_entities, snapshot.total_devices)
        return snapshot
