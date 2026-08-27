"""Mock configuration and test setup for Smart Home Score unit tests (v0.6.2)."""
import sys
import types
from unittest.mock import AsyncMock, MagicMock

# 1. Mock Voluptuous
if "voluptuous" not in sys.modules:
    vol = types.ModuleType("voluptuous")
    vol.Schema = lambda schema, *args, **kwargs: MagicMock(side_effect=lambda data: data)
    vol.Required = lambda key, *args, **kwargs: key
    vol.Optional = lambda key, *args, **kwargs: key
    vol.Coerce = lambda typ: typ
    vol.All = lambda *args: args[0]
    vol.Range = lambda *args, **kwargs: lambda x: x
    sys.modules["voluptuous"] = vol

# 2. Mock HomeAssistant
if "homeassistant" not in sys.modules:
    ha = types.ModuleType("homeassistant")
    sys.modules["homeassistant"] = ha

if "homeassistant.core" not in sys.modules:
    ha_core = types.ModuleType("homeassistant.core")
    ha_core.HomeAssistant = MagicMock
    ha_core.ServiceCall = MagicMock
    ha_core.callback = lambda f: f
    sys.modules["homeassistant.core"] = ha_core

if "homeassistant.const" not in sys.modules:
    ha_const = types.ModuleType("homeassistant.const")
    ha_const.Platform = types.SimpleNamespace(SENSOR="sensor")
    sys.modules["homeassistant.const"] = ha_const

if "homeassistant.config_entries" not in sys.modules:
    ha_ce = types.ModuleType("homeassistant.config_entries")
    ha_ce.ConfigEntry = MagicMock
    class MockConfigFlow:
        def __init_subclass__(cls, domain=None, **kwargs):
            cls.domain = domain
        def async_show_form(self, step_id=None, errors=None, data_schema=None):
            return {"type": "form", "step_id": step_id, "errors": errors or {}, "data_schema": data_schema}
        def async_create_entry(self, title=None, data=None):
            return {"type": "create_entry", "title": title, "data": data or {}}
        def _async_current_entries(self):
            return []
    ha_ce.ConfigFlow = MockConfigFlow
    sys.modules["homeassistant.config_entries"] = ha_ce

if "homeassistant.data_entry_flow" not in sys.modules:
    ha_def = types.ModuleType("homeassistant.data_entry_flow")
    ha_def.FlowResult = dict
    sys.modules["homeassistant.data_entry_flow"] = ha_def

ha_helpers = types.ModuleType("homeassistant.helpers")
sys.modules["homeassistant.helpers"] = ha_helpers

area_reg = types.ModuleType("homeassistant.helpers.area_registry")
area_reg.async_get = MagicMock(return_value=MagicMock(areas={}))
sys.modules["homeassistant.helpers.area_registry"] = area_reg
ha_helpers.area_registry = area_reg

device_reg = types.ModuleType("homeassistant.helpers.device_registry")
device_reg.async_get = MagicMock(return_value=MagicMock(devices={}))
sys.modules["homeassistant.helpers.device_registry"] = device_reg
ha_helpers.device_registry = device_reg

entity_reg = types.ModuleType("homeassistant.helpers.entity_registry")
entity_reg.async_get = MagicMock(return_value=MagicMock(entities={}))
sys.modules["homeassistant.helpers.entity_registry"] = entity_reg
ha_helpers.entity_registry = entity_reg

integ_plat = types.ModuleType("homeassistant.helpers.integration_platform")
integ_plat.async_process_integration_platforms = AsyncMock()
sys.modules["homeassistant.helpers.integration_platform"] = integ_plat
ha_helpers.integration_platform = integ_plat

cv_mod = types.ModuleType("homeassistant.helpers.config_validation")
cv_mod.string = lambda v: str(v)
cv_mod.boolean = lambda v: bool(v)
sys.modules["homeassistant.helpers.config_validation"] = cv_mod
ha_helpers.config_validation = cv_mod

ha_coord = types.ModuleType("homeassistant.helpers.update_coordinator")
class MockDataUpdateCoordinator:
    def __class_getitem__(cls, item):
        return cls
    def __init__(self, hass, logger, name, update_interval=None):
        self.hass = hass
        self.logger = logger
        self.name = name
        self.update_interval = update_interval
        self.data = None
    async def async_config_entry_first_refresh(self):
        self.data = await self._async_update_data()
    async def async_refresh(self):
        self.data = await self._async_update_data()
    async def _async_update_data(self):
        return None
ha_coord.DataUpdateCoordinator = MockDataUpdateCoordinator
ha_coord.UpdateFailed = Exception
sys.modules["homeassistant.helpers.update_coordinator"] = ha_coord
ha_helpers.update_coordinator = ha_coord

ha_store = types.ModuleType("homeassistant.helpers.storage")
class MockStore:
    def __class_getitem__(cls, item):
        return cls
    def __init__(self, hass, version, key):
        self.hass = hass
        self.version = version
        self.key = key
        self._data = None
    async def async_load(self):
        return self._data
    async def async_save(self, data):
        self._data = data
ha_store.Store = MockStore
sys.modules["homeassistant.helpers.storage"] = ha_store
ha_helpers.storage = ha_store

if "homeassistant.components" not in sys.modules:
    ha_comp = types.ModuleType("homeassistant.components")
    sys.modules["homeassistant.components"] = ha_comp

# 3. Mock homeassistant.components.frontend with add_extra_js_url and remove_extra_js_url
active_frontend_urls = set()

def mock_add_extra_js_url(hass, url, es5=False):
    active_frontend_urls.add(url)

def mock_remove_extra_js_url(hass, url):
    active_frontend_urls.discard(url)

ha_frontend = types.ModuleType("homeassistant.components.frontend")
ha_frontend.add_extra_js_url = mock_add_extra_js_url
ha_frontend.remove_extra_js_url = mock_remove_extra_js_url
ha_frontend.active_frontend_urls = active_frontend_urls
sys.modules["homeassistant.components.frontend"] = ha_frontend

# 4. Mock homeassistant.components.http with StaticPathConfig
ha_http = types.ModuleType("homeassistant.components.http")
class StaticPathConfig:
    def __init__(self, url_path, path, cache_headers=True):
        self.url_path = url_path
        self.path = path
        self.cache_headers = cache_headers
ha_http.StaticPathConfig = StaticPathConfig
sys.modules["homeassistant.components.http"] = ha_http

ha_sensor = types.ModuleType("homeassistant.components.sensor")
class SensorEntity:
    pass
class SensorStateClass:
    MEASUREMENT = "measurement"
    TOTAL = "total"
class SensorDeviceClass:
    pass
ha_sensor.SensorEntity = SensorEntity
ha_sensor.SensorStateClass = SensorStateClass
ha_sensor.SensorDeviceClass = SensorDeviceClass
sys.modules["homeassistant.components.sensor"] = ha_sensor

ha_entity = types.ModuleType("homeassistant.helpers.entity")
class Entity:
    pass
class DeviceInfo:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
ha_entity.Entity = Entity
ha_entity.DeviceInfo = DeviceInfo
sys.modules["homeassistant.helpers.entity"] = ha_entity
ha_helpers.entity = ha_entity
