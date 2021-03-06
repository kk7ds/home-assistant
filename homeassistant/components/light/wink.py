"""
homeassistant.components.light.wink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support for Wink lights.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.wink/
"""
import logging

from homeassistant.components.light import ATTR_BRIGHTNESS, Light
from homeassistant.const import CONF_ACCESS_TOKEN

REQUIREMENTS = ['python-wink==0.6.0']


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return Wink lights. """
    import pywink

    token = config.get(CONF_ACCESS_TOKEN)

    if not pywink.is_token_set() and token is None:
        logging.getLogger(__name__).error(
            "Missing wink access_token - "
            "get one at https://winkbearertoken.appspot.com/")
        return

    elif token is not None:
        pywink.set_bearer_token(token)

    add_devices_callback(
        WinkLight(light) for light in pywink.get_bulbs())


class WinkLight(Light):
    """ Represents a Wink light. """

    def __init__(self, wink):
        self.wink = wink

    @property
    def unique_id(self):
        """ Returns the id of this Wink switch. """
        return "{}.{}".format(self.__class__, self.wink.device_id())

    @property
    def name(self):
        """ Returns the name of the light if any. """
        return self.wink.name()

    @property
    def is_on(self):
        """ True if light is on. """
        return self.wink.state()

    @property
    def brightness(self):
        """Brightness of the light."""
        return int(self.wink.brightness() * 255)

    # pylint: disable=too-few-public-methods
    def turn_on(self, **kwargs):
        """ Turns the switch on. """
        brightness = kwargs.get(ATTR_BRIGHTNESS)

        if brightness is not None:
            self.wink.set_state(True, brightness=brightness / 255)

        else:
            self.wink.set_state(True)

    def turn_off(self):
        """ Turns the switch off. """
        self.wink.set_state(False)

    def update(self):
        """ Update state of the light. """
        self.wink.update_state()
