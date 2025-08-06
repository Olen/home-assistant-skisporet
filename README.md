# home-assistant-skisporet

> **Warning**
>
> Skisporet og iMarka blir Sporet
>
> Før skisesongen 2025-2026 vil iMarka (Skiforeningen) og Skisporet (Swix) gå sammen i en felles, landsdekkende tjeneste: Sporet.
>
> Siden denne tjenesten ikke er operativ enda, og ting tyder på at det vil bli en betaltjeneste, er det mulig at dette prosjektet må legges ned,
> litt avhengig av hvordan APIer osv vil se ut og kunne brukes.
>
> https://www.skiforeningen.no/nyheter/landsdekkende-foremelding/
>
> 


Adds a sensor to get the last time a ski track was prepared according to skisporet.no

![image](https://user-images.githubusercontent.com/203184/219651567-db1f47df-bc0f-4988-8dc6-f3260c86f33c.png)


[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=skisporet)

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

If you have set up "My Homeassistant", you can use this link:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=skisporet)

> **Note**
>
> Skisporet reports last preparation as something like "X days and Y hours ago".  To try to keep a consistent sensor value, this "timestamp" is converted to a datetime-object with minutes and seconds set to zero.  
>
> If last prep was more than 14 days ago, skipsoret only reports it as "More than 14 days ago".  This integration will the always set the timestamp to Jan. 1. 2000. when it receives that update.


<a href="https://www.buymeacoffee.com/olatho" target="_blank">
<img src="https://user-images.githubusercontent.com/203184/184674974-db7b9e53-8c5a-40a0-bf71-c01311b36b0a.png" style="height: 50px !important;"> 
</a>
