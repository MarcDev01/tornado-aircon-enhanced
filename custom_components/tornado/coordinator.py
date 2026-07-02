from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .aux_cloud import AuxCloudAPI

_LOGGER = logging.getLogger(__name__)


class AuxCloudDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator that fetches all AUX devices."""

    def __init__(self, hass: HomeAssistant, api: AuxCloudAPI) -> None:
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name="AuxCloud",
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self) -> dict:
        """Fetch all devices from the AUX cloud."""

        try:
            if not hasattr(self.api, "loginsession") or not self.api.loginsession:
                _LOGGER.info("No valid login session, attempting to login")
                await self.api.login()

            devices = await self.api.get_devices()

            return {
                device["endpointId"]: device
                for device in devices
            }

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err