"""Config flow for Skisporet integration."""

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class PlantConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Plants."""

    VERSION = 1

    def __init__(self):
        self.plant_info = {}
        self.error = None

    async def async_step_import(self, import_input):
        """Importing config from configuration.yaml"""
        _LOGGER.debug(import_input)
        return self.async_create_entry(
            title=import_input[ATTR_NAME]
            title=import_input[FLOW_PLANT_INFO][ATTR_NAME],
            data=import_input,
        )


