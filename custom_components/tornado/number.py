"""Number platform for Tornado AC."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities: AddEntitiesCallback):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    client = entry_data["client"]
    coordinator = entry_data["coordinator"]

    devices = coordinator.data.values()

    async_add_entities(
        TornadoPowerLimitNumber(coordinator, client, device)
        for device in devices
    )


class TornadoPowerLimitNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, client, device):
        super().__init__(coordinator)

        self._client = client
        self._device_id = device["endpointId"]

        friendly_name = device.get("friendlyName") or self._device_id

        self._attr_unique_id = f"{self._device_id}_pwrlimit"
        self._attr_name = f"{friendly_name} Power Limit Value"
        self._attr_native_min_value = 30
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_icon = "mdi:gauge"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": f"Tornado AC {friendly_name}",
            "manufacturer": "Tornado",
            "model": "AUX Cloud",
        }

    @property
    def _device(self):
        return self.coordinator.data.get(self._device_id)

    @property
    def native_value(self):
        return int(self._device.get("params", {}).get("pwrlimit", 50))

    async def async_set_native_value(self, value: float):
        params = {
            "pwrlimitswitch": 1,
            "pwrlimit": int(value),
        }

        await self._client.set_device_params(self._device, params)
        await self.coordinator.async_request_refresh()