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
        
        self._last_data: dict[str, dict] | None = None
        self._failed_updates = 0

        super().__init__(
            hass,
            _LOGGER,
            name="AuxCloud",
            update_interval=timedelta(minutes=3),
            
        )

    async def _async_update_data(self) -> dict:
        """Fetch all devices from the AUX cloud."""
    
        try:
            if not hasattr(self.api, "loginsession") or not self.api.loginsession:
                _LOGGER.info("No valid login session, attempting to login")
                await self.api.login()
    
            devices = await self.api.get_devices()
    
            data = {
                device["endpointId"]: device
                for device in devices
            }
    
            self._last_data = data
            self._failed_updates = 0
    
            return data
    
        except Exception as err:
            self._failed_updates += 1
        
            _LOGGER.warning(
                "Cloud update failed (%d/10): %s",
                self._failed_updates,
                err,
            )
        
            # Gebruik de laatst bekende status zolang de storing kort duurt
            if self._last_data is not None and self._failed_updates < 10:
                _LOGGER.debug("Using cached AUX device data")
                return self._last_data
        
            _LOGGER.info(
                "Resetting login session after %d consecutive failures", 
                self._failed_updates,
            )
            # Reset de sessie zodat de volgende poll opnieuw inlogt
            self.api.loginsession = None
        
            raise UpdateFailed(f"Error fetching data: {err}") from err
