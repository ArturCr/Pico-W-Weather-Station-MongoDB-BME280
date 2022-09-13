# Pico-W-Weather-Station-MongoDB-BME280
Small Pico W based weather station written with micropython using the BME280 sensor for data collection and storing the data collected on a MongoDB database

<!-- Logo Here? -->

<!-- TABLE OF CONTENTS -->

## Table of Contents
  <ol>
    <li><a href="#setup-mongodb">Setup MongoDB</a></li>
    <li><a href="#configure-pico-w-with-micropython">Configure Pico W with micropython</a></li>
    <li><a href="#hardware">Hardware</a></li>
    <li><a href="#code">Code</a></li>  
    <li><a href="#modify-secretspy">Modify secrets.py</a></li>
    <li><a href="#success-or-likely-debugging-"> Success (or likely debugging 😅)</a></li>
  </ol>
<br />

<!-- MAIN CONTENTS -->
## Setup MongoDB
Setup database:
* <a href="https://www.mongodb.com/cloud/atlas/register">
  Register/Sign in to 
  <img src="https://webimages.mongodb.com/_com_assets/cms/kuyj3d95v5vbmm2f4-horizontal_white.svg?auto=format%252Ccompress" alt="mongodb.com" width="80" height="18"      style="vertical-align:middle"> 
  </a>
  
* Create a project
* Inside the project create a Cluster (**The Shared Cluster is Free without term limits and does not require a credit card 💳**)
* Inside the cluster create a database
* and Inside the database create collection
  - (This video by Patrick does the previous steps well from min 7 to 12 https://youtu.be/qWYx5neOh2s?t=440) 
  <br />
  
Setup API:
* Then go to the Api Section  
![Mongodb_DataAPI]
* Enable it, making sure the cluster is set to "Read and Write" and get a copy of the "URL Endpoint" for later
* Finally click on "Create API Key" and safe it somewhere safe
<br />

## Configure Pico W with micropython
A great resource for this can be found at the <a href="https://www.raspberrypi.com/documentation/microcontrollers/micropython.html"> Raspberry Pi</a>
If this is your first project make sure to get [Thonny](https://thonny.org/) to interface with the pico
<br />

## Hardware
![squematic]
<br />

## Code
...
<br />

## Modify secrets.py
Open the secret.py file and replace the placeholder data with your Wi-Fi and Database data
<br />

##  Success (or likely debugging 😅)
By now the system should be working but there is a chace something is wrong. If so please feel free to raise an issue and I wish you the best of luck debugging and hacking the server to do more
<br />

## Roadmap:
- [x] Get data from BME280
- [x] Upload data to a Mongodb database
- [ ] Power the system with battery
- [ ] charge the battery with a solar panel
<br />

## Extra Resources:
BME code source used (12/09/2022):
https://github.com/catdog2/mpy_bme280_esp8266/tree/d7e052b28281942996a8f0e1bbdbef87f87bbb8e

Getting MongoDB to work helpful resource:
https://medium.com/@johnlpage/introduction-to-microcontrollers-and-the-pi-pico-w-f7a2d9ad1394
