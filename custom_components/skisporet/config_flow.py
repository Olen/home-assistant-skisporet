"""Config flow for Skisporet integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries, data_entry_flow
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_DOMAIN,
    ATTR_ENTITY_PICTURE,
    CONF_NAME,
    CONF_URL,
)
from homeassistant.helpers import config_validation as cv

from .const import (
    ATTR_SEGMENT_ID,
    ATTR_TRACK_ID,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class SkipsoretConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Skisporet."""

    VERSION = 1

    def __init__(self) -> None:
        self.error = {}

    async def async_step_import(self, import_input):
        """Importing config from configuration.yaml"""
        _LOGGER.debug(import_input)
        return self.async_create_entry(
            title=import_input[CONF_NAME],
            data={
                CONF_URL: f"https://www.skisporet.no/map/segment/{import_input[ATTR_TRACK_ID]}",
                CONF_NAME: import_input[CONF_NAME],
            },
        )

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.debug("Setup skisporet")
        if user_input is not None:
            _LOGGER.debug("User Input %s", user_input)
            # Validate user input
            valid = await self.validate_step_1(user_input)
            if valid:
                return self.async_create_entry(
                    title=valid[CONF_NAME],
                    data={CONF_NAME: valid[CONF_NAME], CONF_URL: valid[CONF_URL]},
                )

        data_schema = {
            vol.Required(CONF_NAME): cv.string,
            # vol.Required(CONF_URL): cv.url,
            vol.Required(CONF_URL): cv.string,
        }
        _LOGGER.debug("Schema: %s", data_schema)
        return self.async_show_form(
            step_id="user",
            errors=self.error,
            data_schema=vol.Schema(data_schema),
        )

    async def validate_step_1(self, user_input):
        """Validate step one"""
        _LOGGER.debug("Validating step 1: %s", user_input)
        # https://www.skisporet.no/map/segment/47897
        if not user_input[CONF_URL].startswith("https"):
            self.error[CONF_URL] = "Feil i URL (ikke https)"
            return False
        if not "skisporet" in user_input[CONF_URL]:
            self.error[CONF_URL] = "Feil i URL (ikke skisporet)"
            return False
        if not "segment" in user_input[CONF_URL]:
            self.error[CONF_URL] = "Feil i URL (ikke segment)"
            return False
        if len(user_input[CONF_NAME]) < 3:
            # TODO: More validation of name
            # Maybe get name from url and segment ID or something
            self.error[CONF_NAME] = "Feil i navn"
            return False

        return user_input
