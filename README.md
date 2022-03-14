# home-assistant-skisporet

Adds a sensor to get the last time a ski track was prepared according to skisporet.no

## Install

This can be installed manually or through HACS

### Via HACS
* Add this repo as a "Custom repository" with type "Integration"
* Click "Install" in the new "Skisporet" card in HACS
* Restart Home Assistant

### Manual installation
* Create a new folder under config/custom_components called "skisporet"
* Copy all the files from this repo to the new folder

## Config
To set up a new sensor, you need the track-id from skisporet.no
* Open the map in a browser https://skisporet.no/
* Click on the track you want the sensor to follow
* Click "Del løype" at the upper right corner of the popup
* Find the track id in the URL to copy: e.g. skisporet.no/?fitTs2Id=**12345**&highlightTs2Id=**12345**&map=norges_grunnkart
- Of course the numbers will be different for different tracks

* Add the following to your sensor-config in HA:

```
- platform: skisporet
  name: My track
  track_id: 12345
```

* Restart Home Assistant


