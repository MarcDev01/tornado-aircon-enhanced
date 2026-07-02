"""Switch platform for Tornado AC."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SWITCHES = {
    "scrdisp": ("Display", "mdi:monitor"),
    "ac_clean": ("Clean", "mdi:spray-bottle"),
    "ac_health": ("Health", "mdi:heart"),
    "ac_slp": ("Sleep", "mdi:sleep"),
    "ecomode": ("Eco", "mdi:sprout"),
    "pwrlimitswitch": ("Power Limit", "mdi:lightning-bolt"),
    "comfwind": ("Comfort Wind", "mdi:waves"),
    "ac_astheat": ("Aux Heat", "mdi:heat-wave"),
    "mldprf": ("Anti Fungus", "mdi:bacteria-outline"),
    "sleepdiy": ("Sleep DIY", "mdi:chart-bell-curve"),
    "childlock": ("Child Lock", "mdi:lock"),
}


async def async_setup_entry(hass, config_entry, async_add_entities: AddEntitiesCallback):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    
    client = entry_data["client"]
    coordinator = entry_data["coordinator"]
    
    devices = coordinator.data.values()

    async_add_entities(
        TornadoSwitchEntity(
            coordinator,
            client,
            device,
            parameter,
            name,
            icon,
        )
        for device in devices
        for parameter, (name, icon) in SWITCHES.items()
    )


class TornadoSwitchEntity(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, client, device, parameter, name, icon):
        super().__init__(coordinator)

        self._client = client
        self._parameter = parameter
        self._device_id = device["endpointId"]

        friendly_name = device.get("friendlyName") or self._device_id

        self._attr_unique_id = f"{self._device_id}_{parameter}"
        self._attr_name = f"{friendly_name} {name}"
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
    def is_on(self):
        return self._device.get("params", {}).get(self._parameter, 0) == 1

    async def async_turn_on(self, **kwargs):
        params = {self._parameter: 1}
    
        if self._parameter == "pwrlimitswitch":
            limit = self._device.get("params", {}).get("pwrlimit", 50)
            params["pwrlimit"] = int(limit)
    
        await self._client.set_device_params(self._device, params)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self._client.set_device_params(
            self._device,
            {self._parameter: 0},
        )
        await self.coordinator.async_request_refresh()
