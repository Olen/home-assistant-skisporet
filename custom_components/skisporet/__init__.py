"""The skisporet component."""

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

PLATFORMS = ["sensor"]


def setup(hass: HomeAssistant, config: ConfigEntry):
    """Set up this using config flow."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up skiporet from config entry"""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True
