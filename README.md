# home-assistant-skisporet

Adds a sensor to get the last time a ski track was prepared according to skisporet.no

![image](https://user-images.githubusercontent.com/203184/219651567-db1f47df-bc0f-4988-8dc6-f3260c86f33c.png)


# BREAKING CHANGE

> **Warning**
>
> Due to changes at skisporet.no some attributes are no longer available, and others have appeared.
> 
> You also need to set this integration up from scratch again from the UI.  Old yaml-config is no longer supported.

## Install

This can be installed manually or through HACS

### Via HACS
* Open HACS
* Click "Integrations"
* Click the three dots in the upper right corner and select "Custom Repositiories"
* Add the link to this repo with type "Integration"
* Click "Download this repository with HACS" in the new "Skisporet" card in HACS
* Restart Home Assistant

### Manual installation
* Create a new folder under config/custom_components called "skisporet"
* Copy all the files from this repo to the new folder

## Config
The integration is set up from the GUI in HA

First, you need the share-link from skisporet.no
* Open the map in a browser https://skisporet.no/
* Click on the track you want the sensor to follow
* Click the "Share" icon at the upper left corner of the popup
* Click "Kopier lenke"

Then go to HomeAssistant, Settings, Devices and Services.
* Click "Add integration"
* Search for "Skisporet"
* Add the URL you copied, and give this track a name
* Click "Submit"

> **Note**
>
> Skisporet reports last preparation as something like "X days and Y hours ago".  To try to keep a consistent sensor value, this "timestamp" is converted to a datetime-object with minutes and seconds set to zero.  
>
> If last prep was more than 14 days ago, skipsoret only reports it as "More than 14 days ago".  This integration will the always set the timestamp to Jan. 1. 2000. when it receives that update.


<a href="https://www.buymeacoffee.com/olatho" target="_blank">
<img src="https://user-images.githubusercontent.com/203184/184674974-db7b9e53-8c5a-40a0-bf71-c01311b36b0a.png" style="height: 50px !important;"> 
</a>
