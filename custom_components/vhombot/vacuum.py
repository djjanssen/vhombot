"""Support for Neato Connected Vacuums."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.vacuum import (
    ATTR_STATUS,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_ERROR,
    STATE_RETURNING,
    SUPPORT_BATTERY,
    SUPPORT_CLEAN_SPOT,
    SUPPORT_LOCATE,
    SUPPORT_MAP,
    SUPPORT_PAUSE,
    SUPPORT_RETURN_HOME,
    SUPPORT_START,
    SUPPORT_STATE,
    SUPPORT_STOP,
    StateVacuumEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_MODE, STATE_IDLE, STATE_PAUSED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SCAN_INTERVAL_MINUTES,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=SCAN_INTERVAL_MINUTES)


SUPPORT_VHOMBOT = (
    SUPPORT_BATTERY
    | SUPPORT_PAUSE
    | SUPPORT_RETURN_HOME
    | SUPPORT_STOP
    | SUPPORT_START
    | SUPPORT_STATE
    | SUPPORT_LOCATE
)


ATTR_CLEAN_START = "clean_start"
ATTR_CLEAN_STOP = "clean_stop"
ATTR_CLEAN_AREA = "clean_area"
ATTR_CLEAN_BATTERY_START = "battery_level_at_clean_start"
ATTR_CLEAN_BATTERY_END = "battery_level_at_clean_end"
ATTR_CLEAN_SUSP_COUNT = "clean_suspension_count"
ATTR_CLEAN_SUSP_TIME = "clean_suspension_time"
ATTR_CLEAN_PAUSE_TIME = "clean_pause_time"
ATTR_CLEAN_ERROR_TIME = "clean_error_time"
ATTR_LAUNCHED_FROM = "launched_from"

ATTR_NAVIGATION = "navigation"
ATTR_CATEGORY = "category"
ATTR_ZONE = "zone"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Neato vacuum with config entry."""
    dev = []

    # mapdata: dict[str, Any] | None = hass.data.get(NEATO_MAP_DATA)
    platform = entity_platform.async_get_current_platform()
    assert platform is not None


class VHomBotConnectedVacuum(StateVacuumEntity):
    """Representation of a LG VHombot Connected Vacuum."""

    def __init__(self) -> None:
        """Initialize the Vhombot Connected Vacuum."""
        self._name: str | None = None
        self._serial: str | None = None
        self._status_state: str | None = None
        self._clean_state: str | None = None
        self._state: dict[str, Any] | None = None
        self._clean_time_start: str | None = None
        self._clean_time_stop: str | None = None
        self._clean_area: float | None = None
        self._clean_battery_start: int | None = None
        self._clean_battery_end: int | None = None
        self._clean_susp_charge_count: int | None = None
        self._clean_susp_time: int | None = None
        self._clean_pause_time: int | None = None
        self._clean_error_time: int | None = None
        self._launched_from: str | None = None
        self._battery_level: int | None = None
        self._robot_boundaries: list = []
        self._robot_stats: dict[str, Any] | None = None

    def update(self) -> None:
        """Update the states of Neato Vacuums."""
        _LOGGER.debug("Running Neato Vacuums update for '%s'", self.entity_id)

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._name

    @property
    def supported_features(self) -> int:
        """Flag vacuum cleaner robot features that are supported."""
        return SUPPORT_VHOMBOT

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the vacuum cleaner."""
        return self._battery_level

    @property
    def available(self) -> bool:
        """Return if the robot is available."""
        return True

    @property
    def icon(self) -> str:
        """Return neato specific icon."""
        return "mdi:robot-vacuum-variant"

    @property
    def state(self) -> str | None:
        """Return the status of the vacuum cleaner."""
        return self._clean_state

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._serial

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the vacuum cleaner."""
        data: dict[str, Any] = {}

        if self._status_state is not None:
            data[ATTR_STATUS] = self._status_state
        if self._clean_time_start is not None:
            data[ATTR_CLEAN_START] = self._clean_time_start
        if self._clean_time_stop is not None:
            data[ATTR_CLEAN_STOP] = self._clean_time_stop
        if self._clean_area is not None:
            data[ATTR_CLEAN_AREA] = self._clean_area
        if self._clean_susp_charge_count is not None:
            data[ATTR_CLEAN_SUSP_COUNT] = self._clean_susp_charge_count
        if self._clean_susp_time is not None:
            data[ATTR_CLEAN_SUSP_TIME] = self._clean_susp_time
        if self._clean_pause_time is not None:
            data[ATTR_CLEAN_PAUSE_TIME] = self._clean_pause_time
        if self._clean_error_time is not None:
            data[ATTR_CLEAN_ERROR_TIME] = self._clean_error_time
        if self._clean_battery_start is not None:
            data[ATTR_CLEAN_BATTERY_START] = self._clean_battery_start
        if self._clean_battery_end is not None:
            data[ATTR_CLEAN_BATTERY_END] = self._clean_battery_end
        if self._launched_from is not None:
            data[ATTR_LAUNCHED_FROM] = self._launched_from

        return data

    @property
    def device_info(self) -> DeviceInfo:
        """Device info for vhombot robot."""
        stats = self._robot_stats
        return DeviceInfo(
            identifiers={(DOMAIN, self._serial)},
            manufacturer=stats["battery"]["vendor"] if stats else None,
            model=stats["model"] if stats else None,
            name=self._name,
            sw_version=stats["firmware"] if stats else None,
        )

    def start(self) -> None:
        """Start cleaning or resume cleaning."""
        if self._state:
            try:
                if self._state["state"] == 1:
                    _LOGGER.info("Implement starting")
                    # self.robot.start_cleaning()
                elif self._state["state"] == 3:
                    _LOGGER.info("Implement Continue")
            except Exception as ex:
                _LOGGER.error(
                    "VHombot vacuum connection error for '%s': %s", self.entity_id, ex
                )

    def pause(self) -> None:
        """Pause the vacuum."""
        try:
            _LOGGER.info("Implement pause")
        except Exception as ex:
            _LOGGER.error(
                "VHombot vacuum connection error for '%s': %s", self.entity_id, ex
            )

    def return_to_base(self, **kwargs: Any) -> None:
        """Set the vacuum cleaner to return to the dock."""
        try:
            if self._clean_state == STATE_CLEANING:
                _LOGGER.info("Implement return to base")

            self._clean_state = STATE_RETURNING
            _LOGGER.info("Implement return to base")

        except Exception as ex:
            _LOGGER.error(
                "VHomeBot vacuum connection error for '%s': %s", self.entity_id, ex
            )

    def stop(self, **kwargs: Any) -> None:
        """Stop the vacuum cleaner."""
        try:
            _LOGGER.info("Implement stopping")

        except Exception as ex:
            _LOGGER.error(
                "VHombot vacuum connection error for '%s': %s", self.entity_id, ex
            )

    def locate(self, **kwargs: Any) -> None:
        """Locate the robot by making it emit a sound."""
        try:
            _LOGGER.info("Implement make some noice")

        except Exception as ex:
            _LOGGER.error(
                "VHombot vacuum connection error for '%s': %s", self.entity_id, ex
            )

    def clean_spot(self, **kwargs: Any) -> None:
        """Run a spot cleaning starting from the base."""
        try:
            _LOGGER.info("Implement spot cleaning")

        except Exception as ex:
            _LOGGER.error(
                "VHombot vacuum connection error for '%s': %s", self.entity_id, ex
            )
