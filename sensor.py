"""Support for weather service."""
import asyncio
import logging
import re
from datetime import datetime, timedelta
import pandas as pd

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_URL,
    DEVICE_CLASS_TIMESTAMP,
    HTTP_BAD_REQUEST,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt as dt_util
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

ATTR_DISTANCE = "distance"
ATTR_PROPERTIES = "properties"
ATTR_LAST_PREP = "last_prep"

DEFAULT_NAME = "skisporet"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_URL): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Weather sensor."""
    name = config.get(CONF_NAME)
    url = config.get(CONF_URL)

    _LOGGER.info(f"Setting up skisporet-sensor for {name}")
    dev = SkisporetSensor(hass, name, url)
    async_add_entities([dev], True)


class SkisporetSensor(Entity):
    """A sensor for a track"""
    def __init__(self, hass, name, url):
        """Initialize the sensor."""
        self._name = name
        self._url = url
        self._state = None
        self._distance = None
        self._properties = None
        self._last_prep = None
        self.hass = hass
        self.entity_slug = "Skisporet {}".format(self._name)
        self.entity_id = ENTITY_ID_FORMAT.format(
            slugify(self.entity_slug.replace(' ', '_')))
        _LOGGER.info(f"Added skisporet-sensor {self.entity_id}")

    @property
    def unique_id(self):
        return self.entity_slug.replace(' ', '_')

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        if self._state:
            return self._state.astimezone().isoformat()
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
                ATTR_DISTANCE: self._distance,
                ATTR_PROPERTIES: self._properties,
                ATTR_LAST_PREP: self._last_prep,
                }


    @property
    def device_class(self):
        """Return the device class of this entity, if any."""
        return DEVICE_CLASS_TIMESTAMP


    async def async_update(self):
        """Fetch status from skisporet."""
        _LOGGER.debug(f"Updating skisporet-sensor for {self._name}")

        d = (int(datetime.now().astimezone().strftime("%s")) - (datetime.now()-datetime.utcnow()).seconds) * 1000
        # d = int(datetime.now().strftime('%s')) * 1000
        data = f't%3Azoneid=TmpId_{d}' 

        url = self._url.split("/")
        url[6] = str(d)
        self._url="/".join(url)

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        try:
            websession = async_get_clientsession(self.hass)
            with async_timeout.timeout(10):
                resp = await websession.post(self._url, headers=headers, data=data)
            skisporet = await resp.json()

        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            return
    
        parsed = pd.read_html(skisporet['_tapestry']['content'][0][1])
        _LOGGER.debug(f"Got data from skisporet-sensor for {self._name}, {parsed}")
    
        i=0
        o = {}
        while i < len(parsed[0][0]):
            key = str(parsed[0][0][i]).replace(":", "").strip()
            val = str(parsed[0][1][i]).replace("Smøretips", "").strip()
            if key == "Oppdatert":
                self._last_prep = val
                self._state = self._parse_timestamp(val)
            if key == "Lengde":
                self._distance = val
            if key == "Egenskaper":
                self._properties = val
            i = i + 1
    
    
    def _parse_timestamp(self, ts):
        days = 0
        hours = 0
        minutes = 0
        parts = ts.split(" og ")
        
    
        for part in parts:
            if "uke" in part:
                part = int(re.sub('\D', '', part))
                days = days + (part * 7)
                precision = '0'
            elif 'dag' in part:
                part = int(re.sub('\D', '', part))
                days = days + part
                precision = 'D'
            elif 'time' in part:
                part = int(re.sub('\D', '', part))
                hours = hours + part
                precision = 'T'
            elif 'minutt' in part:
                part = int(re.sub('\D', '', part))
                minutes = minutes + part
                precision = 'M'

        dt = datetime.now() - timedelta(days=days, hours=hours, minutes=minutes)
        # Dont bother with rounding errors
        if precision == '0':
            last = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            if self._state and (last - self._state).seconds < (60 * 60 * 24):
                last = self._state
        if precision == 'D':
            last = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            if self._state and (last - self._state).seconds < (60 * 60 * 24):
                last = self._state
        if precision == 'T':
            last = dt.replace(minute=0, second=0, microsecond=0)
            if self._state and (last - self._state).seconds < (60 * 60):
                last = self._state
        if precision == 'M':
            last = dt.replace(second=0, microsecond=0)
            if self._state and (last - self._state).seconds < 60:
                last = self._state
        return last



