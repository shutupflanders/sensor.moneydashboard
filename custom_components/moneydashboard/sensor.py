"""
Support for MoneyDashboard sensors.

For more details about this platform, please refer to the documentation at
https://github.com/custom-components/sensor.moneydashboard
"""

import logging
import voluptuous as vol
import json
from datetime import timedelta
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

__version__ = '0.1.1'

CONF_EMAIL = 'email'
CONF_PASSWORD = 'password'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
CONF_CATEGORIES = 'monitored_categories'

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

ATTR_POSITIVEBALANCE = "Positive Balance"
ATTR_NEGATIVEBALANCE = "Negative Balance"

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Money Dashboard component."""
    from moneydashboard import MoneyDashboard, LoginFailedException, GetAccountsListFailedException
    md = MoneyDashboard(email=config[CONF_EMAIL], password=config[CONF_PASSWORD])
    add_entities([MoneyDashboardBalances(md=md, unit_of_measurement="GBP")])


class MoneyDashboardBalances(Entity):
    """Representation of a moneydashboard.com net worth sensor."""

    def __init__(self, md, unit_of_measurement):
        """Initialize the sensor."""
        self._md = md
        self._unit_of_measurement = unit_of_measurement
        self._state = None
        self._positive_balance = None
        self._negative_balance = None
        self.update()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest state of the sensor."""
        try:
            data = json.loads(self._md.get_balances())
            self._state = data['net_balance']
            self._positive_balance = data['positive_balance']
            self._negative_balance = data['negative_balance']
        except GetAccountsListFailedException:
            try:
                self._md.login()
            except LoginFailedException:
                _LOGGER.error('Unable to login, please check your credentials.')



    @property
    def name(self):
        """Return the name of the sensor."""
        return 'MoneyDashboard Net Balance'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measure this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return 'mdi:cash-multiple'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        attributes = {
            ATTR_POSITIVEBALANCE: self._positive_balance,
            ATTR_NEGATIVEBALANCE: self._negative_balance
        }
        return attributes
