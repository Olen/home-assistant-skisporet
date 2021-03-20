# home-assistant-skisporet

Adds a sensor to get the last time a ski track was prepared according to skisporet.no

## Install
* create a new folder under config/custom_components called "skisporet"
* copy all the files from this repo to the new folder

## Config
To set up a new sensor, you need the URL to the popup window on the map from skisporet.no
* Open the map in a browser
* Open developer mode in the browser
* Click on the track you want the sensor to follow
* Find the URL of the opened modal window in the developer tools

The url should be something like `https://skisporet.no/trackstatus/trackstatuspopup:StatusWithRouteInTabsHtml/20067/1616262206395/37125573/60.676331341445966/7.995042800903321`
- Of course the numbers will be different for different tracks

* Add the following to your sensor-config in HA:

```
- platform: skisporet
  name: My track
  url: https://skisporet.no/trackstatus/trackstatuspopup:StatusWithRouteInTabsHtml/20067/1616262206395/37125573/60.676331341445966/7.995042800903321
```

* Restart Home Assistant


