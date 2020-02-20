# MoneyDashboard Net Worth Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

This component will scrape your [MoneyDashboard](https://moneydashboard.com) account for the following attributes: 
 
    * Net Balance  
    * Positive Balance
    * Negative Balance
    * Individual Account Balances (coming soon)
    
The Base state for the component will use your **Net Balance**  

### Installation
#### HACS
This card is available in [HACS](https://github.com/custom-components/hacs) (Home Assistant Community Store)

#### Manual
Copy this folder to `<config_dir>/custom_components/moneydashboard/`.

### Configuration
Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: moneydashboard
    email: me@example.com
    password: password
```

Restart HomeAssistant and look for your new shiny `sensor.moneydashboard_net_balance` sensor!

##Formatting
After receiving advice from a user regarding the formatting "breaking" the history of the sensor, the thousands 
separator (,) has been removed in place of just standard floats, if you would like it back for your lovelace display
you can use the following value template

```mustache
{{ ‘{0:,.0f}’.format(states.sensor.moneydashboard_net_balance) }}
```


[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/IcV9egW
