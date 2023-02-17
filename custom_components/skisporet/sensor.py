"""Support for weather service."""
import asyncio
import logging
import re
from datetime import datetime, timedelta

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA


from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import (
    CONF_NAME,
    CONF_URL,
)
from homeassistant.components.sensor.const import (
    SensorDeviceClass,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.util import dt as dt_util
from homeassistant.util import slugify

from .const import DOMAIN, ATTR_DISTANCE, ATTR_TRAIL_NAME, ATTR_TRAIL_TYPE, ICON

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "skisporet"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup skisporet sensor."""
    config = config_entry.data
    name = config.get(CONF_NAME)
    url = config.get(CONF_URL)

    async_add_entities([SkisporetSensor(hass, name, url)])


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


class SkisporetSensor(Entity):
    """A sensor for a track"""

    def __init__(self, hass, name, url) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._name = name
        self._url = url
        self.native_value = None
        self._distance = None
        self._properties = None
        self._last_update = None
        self._trail_name = None
        self._trail_type = None
        self.entity_slug = "Skisporet {}".format(self._name)
        self.entity_id = ENTITY_ID_FORMAT.format(
            slugify(self.entity_slug.replace(" ", "_"))
        )
        _LOGGER.info(f"Added skisporet-sensor {self.entity_id}")

    @property
    def unique_id(self):
        return self.entity_slug.replace(" ", "_")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the name of the sensor."""
        return ICON

    @property
    def state(self):
        """Return the state of the device."""
        return self.native_value

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_TRAIL_NAME: self._trail_name,
            ATTR_TRAIL_TYPE: self._trail_type,
            ATTR_DISTANCE: self._distance,
        }

    @property
    def device_class(self):
        """Return the device class of this entity, if any."""
        return SensorDeviceClass.TIMESTAMP

    @property
    def segment_id(self):
        """Return segment_id from url"""
        return self._url.split("/")[5]

    async def async_update(self):
        """Fetch status from skisporet."""
        _LOGGER.debug(f"Updating skisporet-sensor for {self._name}")

        websession = async_get_clientsession(self.hass)
        json_url = self._url + "?_data=routes%2Fmap%2Fsegment.%24segmentId"
        try:
            with async_timeout.timeout(10):
                resp = await websession.get(json_url)
            segment = await resp.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            _LOGGER.error(f"No data from skisporet: {err}")
            return
        except Exception as err:
            _LOGGER.error(err)
            return

        features = segment["segment"]["geoJson"]["features"][0]["properties"]
        trails = segment["segment"]["trails"]

        if features["newest_prep_days"] > 14:
            self.native_value = datetime(2000, 1, 1)
        else:
            dt = datetime.now() - timedelta(
                days=int(features["newest_prep_days"]),
                hours=int(features["newest_prep_hours"]),
            )
            self.native_value = dt.replace(minute=0, second=0, microsecond=0)

        if trails:
            self._distance = trails[0]["totalLengthOfAllSegments"]
            self._trail_name = trails[0]["name"]
            self._trail_type = trails[0]["trailType"]
