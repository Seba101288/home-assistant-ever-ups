"""Ever UPS coordinator."""

from __future__ import annotations

from datetime import timedelta
import logging

from pysnmp.hlapi.asyncio import SnmpEngine

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SnmpApi
from .const import (
    DOMAIN,
    SNMP_OID_BATTERY_STATUS,
    SNMP_OID_BATTERY_CAPACITY,
    SNMP_OID_BATTERY_LAST_REPLACED,
    SNMP_OID_BATTERY_REMAINING,
    SNMP_OID_BATTERY_TEST_STATUS,
    SNMP_OID_BATTERY_VOLTAGE,
    SNMP_OID_IDENT_FIRMWARE_VERSION,
    SNMP_OID_IDENT_FIRMWARE_VERSION_XUPS,
    SNMP_OID_IDENT_PART_NUMBER,
    SNMP_OID_IDENT_PRODUCT_NAME,
    SNMP_OID_IDENT_PRODUCT_NAME_XUPS,
    SNMP_OID_IDENT_SERIAL_NUMBER,
    SNMP_OID_INPUT_NUM_PHASES,
    SNMP_OID_INPUT_PHASE,
    SNMP_OID_INPUT_VOLTAGE,
    SNMP_OID_OUTPUT_LOAD,
    SNMP_OID_OUTPUT_NUM_PHASES,
    SNMP_OID_OUTPUT_PHASE,
    SNMP_OID_OUTPUT_VOLTAGE,
    SNMP_OID_SYSTEM_STATUS,
    SNMP_OID_OUTPUT_SOURCE,

)

_LOGGER = logging.getLogger(__name__)


class SnmpCoordinator(DataUpdateCoordinator):
    """Data update coordinator."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, snmpEngine: SnmpEngine
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )
        self._api = SnmpApi(entry.data, snmpEngine)

        self._baseOIDs = [
            SNMP_OID_IDENT_PRODUCT_NAME,
            SNMP_OID_IDENT_PRODUCT_NAME_XUPS,
            SNMP_OID_IDENT_PART_NUMBER,
            SNMP_OID_IDENT_SERIAL_NUMBER,
            SNMP_OID_IDENT_FIRMWARE_VERSION,
            SNMP_OID_IDENT_FIRMWARE_VERSION_XUPS,
            SNMP_OID_INPUT_NUM_PHASES,
            SNMP_OID_OUTPUT_NUM_PHASES,
            SNMP_OID_BATTERY_REMAINING,
            SNMP_OID_BATTERY_VOLTAGE,
            SNMP_OID_BATTERY_CAPACITY,
            SNMP_OID_BATTERY_STATUS,
            SNMP_OID_BATTERY_LAST_REPLACED,
            SNMP_OID_BATTERY_TEST_STATUS,
            SNMP_OID_SYSTEM_STATUS,
            SNMP_OID_OUTPUT_SOURCE,
        ]

    async def _update_data(self) -> dict:
        """Fetch the latest data from the source."""
        try:
            data = await self._api.get(self._baseOIDs)

            if self.data is None:
                self.data = data
            else:
                self.data.update(data)

            input_count = self.data.get(SNMP_OID_INPUT_NUM_PHASES, 0)
            if input_count > 0:
                for result in await self._api.get_bulk(
                    [
                        SNMP_OID_INPUT_PHASE.replace("index", ""),
                        SNMP_OID_INPUT_VOLTAGE.replace("index", ""),
                    ],
                    input_count,
                ):
                    self.data.update(result)

            output_count = self.data.get(SNMP_OID_OUTPUT_NUM_PHASES, 0)
            if output_count > 0:
                for result in await self._api.get_bulk(
                    [
                        SNMP_OID_OUTPUT_PHASE.replace("index", ""),
                        SNMP_OID_OUTPUT_VOLTAGE.replace("index", ""),
                        SNMP_OID_OUTPUT_LOAD.replace("index", ""),
                    ],
                    output_count,
                ):
                    self.data.update(result)

            return self.data  # noqa: TRY300

        except RuntimeError as err:
            raise UpdateFailed(err) from err

    async def _async_update_data(self) -> dict:
        """Fetch the latest data from the source."""
        return await self._update_data()
