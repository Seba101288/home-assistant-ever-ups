# ever UPS integration for Home Assistant

![GitHub Release](https://img.shields.io/github/v/release/Seba101288/home-assistant-ever-ups)
[![Validate for HACS](https://github.com/Seba101288/home-assistant-ever-ups/workflows/Validate%20for%20HACS/badge.svg)](https://github.com/Seba101288/home-assistant-ever-ups/actions/workflows/hacs.yaml)
[![Validate% with hassfest](https://github.com/Seba101288/home-assistant-ever-ups/workflows/Validate%20with%20hassfest/badge.svg)](https://github.com/Seba101288/home-assistant-ever-ups/actions/workflows/hassfest.yaml)

Thanks to jaroschek for sharing the code for integrating UPS Eoton

Custom Home Assistant integration for Ever UPS devices and sensors through SNMP.

Testing on NMC Ever powerline RT3000


![alt text](/.github/images/sensor.JPG) 

## Install
### HACS
The easiest way to install this component is by clicking the badge below, which adds this repo as a custom repo in your HASS instance.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Seba101288&repository=https%3A%2F%2Fgithub.com%2FSeba101288%2Fhome-assistant-ever-ups&category=Integration)

You can also add the integration manually by copying `custom_components/ever_ups` into `<HASS config directory>/custom_components`


## Configuration

* Browse to your Home Assistant instance.
* Go to  Settings > Devices & Services.
* In the bottom right corner, select the  Add Integration button.
* From the list, select Ever Ups.
* Follow the instructions on screen to complete the setup.

![alt text](/.github/images/config-1.JPG) 

1. Name   
   * your device name
2. Host
   * ip UPS addres
3. Port 
   * port for comunication (default: 161)
4. SNMP Version
   * version snmp V1 or V2

* SNMP V1:

![alt text](/.github/images/config-2.JPG) 

* SNMP V3:

![alt text](/.github/images/config-3.JPG) 
