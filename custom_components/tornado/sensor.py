"""Sensor platform for Tornado AC."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = {
    "envtemp": ("Current Temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer"),
    "temp": ("Target Temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer"),
    "pwrlimit": ("Power Limit", PERCENTAGE, "mdi:gauge"),
    "ac_mode": ("Raw Mode", None, "mdi:air-conditioner"),
    "ac_mark": ("Raw Fan Mode", None, "mdi:fan"),
}


async def async_setup_entry(
    hass,
    config_entry,
    async_add_entities: AddEntitiesCallback,
):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    coordinator = entry_data["coordinator"]

    devices = coordinator.data.values()

    async_add_entities(
        TornadoSensorEntity(
            coordinator,
            device,
            parameter,
            name,
            unit,
            icon,
        )
        for device in devices
        for parameter, (name, unit, icon) in SENSORS.items()
    )


class TornadoSensorEntity(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device, parameter, name, unit, icon):
        super().__init__(coordinator)

        self._parameter = parameter
        self._device_id = device["endpointId"]

        friendly_name = device.get("friendlyName") or self._device_id

        self._attr_unique_id = f"{self._device_id}_sensor_{parameter}"
        self._attr_name = f"{friendly_name} {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

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
        if not self._device:
            return None

        value = self._device.get("params", {}).get(self._parameter)

        if value is None:
            return None

        if self._parameter in ("envtemp", "temp"):
            return value / 10

        return value