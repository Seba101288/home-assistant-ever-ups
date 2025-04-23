"""Support for Ever UPS sensors."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import get_time_zone

from .const import (
    SNMP_OID_BATTERY_STATUS,
    SNMP_OID_BATTERY_CAPACITY,
    SNMP_OID_BATTERY_LAST_REPLACED,
    SNMP_OID_BATTERY_REMAINING,
    SNMP_OID_BATTERY_TEST_STATUS,
    SNMP_OID_BATTERY_VOLTAGE,
    SNMP_OID_INPUT_NUM_PHASES,
    SNMP_OID_INPUT_VOLTAGE,
    SNMP_OID_OUTPUT_LOAD,
    SNMP_OID_OUTPUT_NUM_PHASES,
    SNMP_OID_OUTPUT_VOLTAGE,
    SNMP_OID_SYSTEM_STATUS,
    SNMP_OID_OUTPUT_SOURCE,

    SysStatus,
    BatStatus,
    BatteryTestStatus,
    OutputSource,

)
from .coordinator import SnmpCoordinator
from .entity import SnmpEntity

PARALLEL_UPDATES = 0
SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensors."""

    coordinator = entry.runtime_data
    entities: list[SensorEntity] = [
        SnmpBatteryVoltageSensorEntity(coordinator),
        SnmpBatteryCapacitySensorEntity(coordinator),
        SnmpBatteryStatusSensorEntity(coordinator),
        SnmpBatteryLastReplacedSensorEntity(coordinator),
        SnmpBatteryRemainingSensorEntity(coordinator),
        SnmpBatteryTestStatusSensorEntity(coordinator),
        SnmpSystemStatusSensorEntity(coordinator),
        SnmpOutputSourceSensorEntity(coordinator),
    ]

    for index in range(
        1,
        coordinator.data.get(SNMP_OID_INPUT_NUM_PHASES, 0) + 1,
    ):
        entities.append(SnmpInputVoltageSensorEntity(coordinator, index))

    for index in range(
        1,
        coordinator.data.get(SNMP_OID_OUTPUT_NUM_PHASES, 0) + 1,
    ):
        entities.append(SnmpOutputVoltageSensorEntity(coordinator, index))
        entities.append(SnmpOutputLoadSensorEntity(coordinator, index))

    async_add_entities(entities)


class SnmpSensorEntity(SnmpEntity, SensorEntity):
    """Representation of a Ever UPS sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    _multiplier: float | None = None

    _default_value: float = 0.0

    def __init__(self, coordinator: SnmpCoordinator, index: str = "") -> None:
        """Initialize a Ever UPS sensor."""
        super().__init__(coordinator, index)
        self._attr_native_value = self.coordinator.data.get(
            self._value_oid, self._default_value
        )
        if self._multiplier is not None:
            self._attr_native_value *= self._multiplier

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.get(
            self._value_oid, self._default_value
        )
        if self._multiplier is not None:
            self._attr_native_value *= self._multiplier

        super().async_write_ha_state()


class SnmpBatterySensorEntity(SnmpSensorEntity):
    """Representation of a Ever UPS battery sensor."""

    _name_prefix = "Battery"

class SnmpSystemSensorEntity(SnmpSensorEntity):
    """Representation of a Ever UPS system sensor."""

    _name_prefix = "System"    


class SnmpBatteryVoltageSensorEntity(SnmpBatterySensorEntity):
    """Representation of a Ever UPS battery voltage sensor."""

    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _multiplier = 0.1

    _name_suffix = "Voltage"
    _value_oid = SNMP_OID_BATTERY_VOLTAGE




class SnmpBatteryCapacitySensorEntity(SnmpBatterySensorEntity):
    """Representation of a Ever UPS battery watts sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE

    _name_suffix = "Capacity"
    _value_oid = SNMP_OID_BATTERY_CAPACITY


class SnmpBatteryStatusSensorEntity(SnmpBatterySensorEntity):
    """Representation of a Ever UPS battery status sensor."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_state_class = None
    _attr_translation_key = "bat_status"
    _attr_options = [bat_status.value for bat_status in BatStatus]

    _name_suffix = "Status"
    _value_oid = SNMP_OID_BATTERY_STATUS


class SnmpBatteryLastReplacedSensorEntity(SnmpBatterySensorEntity):
    """Representation of a Ever UPS battery last replaced sensor."""

    _attr_device_class = SensorDeviceClass.DATE
    _attr_state_class = None

    _name_suffix = "Last Replaced"
    _value_oid = SNMP_OID_BATTERY_LAST_REPLACED

    @property
    def native_value(self) -> date | None:
        """Return the value reported by the sensor."""
        try:
            return (
                datetime.strptime(self._attr_native_value, "%Y/%m/%d")
                .replace(tzinfo=get_time_zone(self.coordinator.hass.config.time_zone))
                .date()
            )
        except ValueError:
            return None


class SnmpBatteryRemainingSensorEntity(SnmpBatterySensorEntity):
    """Representation of a Ever UPS battery last replaced sensor."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES

    _name_suffix = "Remaining"
    _value_oid = SNMP_OID_BATTERY_REMAINING 


class SnmpBatteryTestStatusSensorEntity(SnmpBatterySensorEntity):
    """Representation of a Ever UPS battery test status sensor."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_state_class = None
    _attr_translation_key = "battery_test_status"
    _attr_options = [
        battery_test_status.value for battery_test_status in BatteryTestStatus
    ]

    _name_suffix = "Test Status"
    _value_oid = SNMP_OID_BATTERY_TEST_STATUS

class SnmpSystemStatusSensorEntity(SnmpSystemSensorEntity):
    """Representation of a Ever UPS system status status sensor."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_state_class = None
    _attr_translation_key = "system_status"
    _attr_options = [system_status.value for system_status in SysStatus]

    _name_suffix = "Status"
    _value_oid = SNMP_OID_SYSTEM_STATUS


class SnmpInputSensorEntity(SnmpSensorEntity):
    """Representation of a Ever UPS input sensor."""

    _name_oid = "1"
    _name_prefix = "Input"


class SnmpInputVoltageSensorEntity(SnmpInputSensorEntity):
    """Representation of a Ever UPS input voltage sensor."""

    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_entity_registry_visible_default = False

    _name_suffix = "Voltage"
    _multiplier = 0.1
    _value_oid = SNMP_OID_INPUT_VOLTAGE




class SnmpOutputSensorEntity(SnmpSensorEntity):
    """Representation of a Ever UPS output sensor."""

    _name_oid = "1"
    _name_prefix = "Output"


class SnmpOutputVoltageSensorEntity(SnmpOutputSensorEntity):
    """Representation of a Ever UPS output voltage sensor."""

    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_entity_registry_visible_default = False
    _multiplier = 0.1
    _name_suffix = "Voltage"
    _value_oid = SNMP_OID_OUTPUT_VOLTAGE


class SnmpOutputLoadSensorEntity(SnmpOutputSensorEntity):
    """Representation of a Ever UPS output watts sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE

    _name_suffix = "Load"
    _value_oid = SNMP_OID_OUTPUT_LOAD


class SnmpOutputSourceSensorEntity(SnmpOutputSensorEntity):
    """Representation of a Eaton UPS output source sensor."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_state_class = None
    _attr_translation_key = "output_source"
    _attr_options = [output_source.value for output_source in OutputSource]

    _name_suffix = "Source"
    _value_oid = SNMP_OID_OUTPUT_SOURCE



