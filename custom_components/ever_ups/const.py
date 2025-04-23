"""Constants for the Ever UPS integration."""

from __future__ import annotations

from enum import Enum, StrEnum

from homeassistant.const import Platform

DOMAIN = "ever_ups"

MANUFACTURER = "Ever"

PLATFORMS = [
    Platform.SENSOR,
]

ATTR_NAME = "name"
ATTR_HOST = "host"
ATTR_PORT = "port"
ATTR_VERSION = "version"
ATTR_COMMUNITY = "community"
ATTR_USERNAME = "username"
ATTR_AUTH_PROTOCOL = "auth_protocol"
ATTR_AUTH_KEY = "auth_key"
ATTR_PRIV_PROTOCOL = "priv_protocol"
ATTR_PRIV_KEY = "priv_key"


class SnmpVersion(StrEnum):
    """Enum with snmp versions."""

    V1 = "1"
    V3 = "3"


class AuthProtocol(StrEnum):
    """Enum with snmp auth protocol options."""

    NO_AUTH = "no auth"
    SHA = "sha"
    SHA_256 = "sha256"
    SHA_384 = "sha384"
    SHA_512 = "sha512"


class PrivProtocol(StrEnum):
    """Enum with snmp priv protocol options."""

    NO_PRIV = "no priv"
    AES = "aes"
    AES_192 = "aes192"
    AES_256 = "aes256"


SNMP_API_CLIENT = "snmp_api_client"

SNMP_PORT_DEFAULT = 161

SNMP_OID_IDENT_PRODUCT_NAME = "1.3.6.1.4.1.935.10.1.1.1.2.0"
SNMP_OID_IDENT_PRODUCT_NAME_XUPS = "1.3.6.1.2.1.33.1.1.2.0"
SNMP_OID_IDENT_FIRMWARE_VERSION = "1.3.6.1.4.1.935.10.1.1.1.3.0"
SNMP_OID_IDENT_FIRMWARE_VERSION_XUPS = "1.3.6.1.2.1.33.1.1.3.0"
SNMP_OID_IDENT_PART_NUMBER = "1.3.6.1.2.1.33.1.1.5.0"
SNMP_OID_IDENT_SERIAL_NUMBER = "1.3.6.1.4.1.935.10.1.1.1.4.0"

SNMP_OID_SYSTEM_STATUS = "1.3.6.1.4.1.935.10.1.1.2.1.0"

SNMP_OID_BATTERY_REMAINING = "1.3.6.1.4.1.935.10.1.1.3.3.0"
SNMP_OID_BATTERY_VOLTAGE = "1.3.6.1.4.1.935.10.1.1.3.5.0"
SNMP_OID_BATTERY_CAPACITY = "1.3.6.1.4.1.935.10.1.1.3.4.0"
SNMP_OID_BATTERY_STATUS = "1.3.6.1.4.1.935.10.1.1.3.1.0"
SNMP_OID_BATTERY_LAST_REPLACED = "1.3.6.1.4.1.935.10.1.1.3.9.0"
SNMP_OID_BATTERY_TEST_STATUS = "1.3.6.1.4.1.935.10.1.1.7.3.0"

SNMP_OID_INPUT_NUM_PHASES = "1.3.6.1.4.1.935.10.1.1.2.15.0"
SNMP_OID_INPUT_PHASE = "1.3.6.1.4.1.935.10.1.1.2.16.1.1.index"
SNMP_OID_INPUT_VOLTAGE = "1.3.6.1.4.1.935.10.1.1.2.16.1.3.index"

SNMP_OID_OUTPUT_NUM_PHASES = "1.3.6.1.4.1.935.10.1.1.2.17.0"
SNMP_OID_OUTPUT_PHASE = "1.3.6.1.4.1.935.10.1.1.2.18.1.1.index"
SNMP_OID_OUTPUT_VOLTAGE = "1.3.6.1.4.1.935.10.1.1.2.18.1.3.index"
SNMP_OID_OUTPUT_LOAD = "1.3.6.1.4.1.935.10.1.1.2.18.1.7.index"
SNMP_OID_OUTPUT_SOURCE = "1.3.6.1.2.1.33.1.4.1.0"



class YesNo(Enum):
    """Mapping for yes/no."""

    yes = 1
    no = 2


class BatStatus(Enum):
    """Values for Batery Status."""

    unknown = 1
    Normal = 2
    Low = 3
    Depleted = 4
    Discharging = 5
    Failure = 5   

class SysStatus(Enum):
    """Values for System Status."""
 
    Power_on = 1
    Standby = 2
    Bypass = 3
    Line = 4
    Battery = 5
    Battery_Test = 6
    Fault = 7
    Converter = 8
    Eco = 9
    Shutdown = 10
    On_booster = 11
    Other = 12



class BatteryTestStatus(Enum):
    """Values for Battery Test Status."""

    unknow = 1
    in_progress = 2
    passed = 3
    failed = 4
    not_supported = 5
    annulled = 6


class OutputSource(Enum):
    """Values for Output Source."""

    other = 1
    none = 2
    normal = 3
    bypass = 4
    battery = 5
    booster = 6
    reducer = 7
    parallel_capacity = 8
    parallel_redundant = 9
    high_efficiency_mode = 10
    maintenance_bypass = 11
    ess_mode = 12

