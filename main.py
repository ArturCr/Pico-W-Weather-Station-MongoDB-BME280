##_Pico W weather sation with Mongodb and BMP280 sensor
##_by ArturCr
##_10/09/2022

##_Libraries
import machine
import urequests as requests
import network
import rp2
import time
##_Library required for bme280
import bme280

##_A file called secrets.py is required with the following data...
from secrets import secrets as s
SSID = s['ssid']
PSK = s['pw']
COUNTRY = s['country']
API_KEY = s['api-key']
URL_ENDPOINT = s['url-endpoint']
CLUSTER = s['cluster']
DATABASE = s['database']
COLLECTION = s['collection']
STATION_NAME  = "Pico_Station_0"


##_Led pattern on powerup
led = machine.Pin('LED', machine.Pin.OUT)
led.toggle()
time.sleep(.75)
led.off()

##_Provides time to avoid reset loops but allows for clean network reconnection
def reset_protocol():
    for x in range(50):
        led.toggle()
        time.sleep(.2)
    led.on()
    time.sleep(1)
    machine.reset()

##_Configure the Wifi card to use the frequencies available for that geography
rp2.country(COUNTRY)

##_Connects to wifi using the provided credentials otherwise reboot pico
def connect_to_wifi(ssid, psk):
    ##_Enable Wifi in Client Mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ##_Connect to Wifi, keep trying until failure or success
    wlan.connect(ssid, psk)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to Connect")
        time.sleep(5)
    if not wlan.isconnected():
        #raise Exception("Wifi not available")
        print("Wifi not available")
        reset_protocol()
    print("Connected to WiFi")

##_Discconect from wifi to safe on power
def disconnect_to_wifi():
    ##_Stop the Wifi
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)
    except Exception as e:
        print('try 2: ',e)

##_Get weather data from bme280 sensor
Data_to_send=[]
def get_bme280_readings():
    data_to_send=[]
    
    ##_Power on sensor
    power = machine.Pin(2, machine.Pin.OUT)
    power.on()
    time.sleep(1)
    
    ##_Commuticate over I2C 
    i2c = machine.I2C(0,scl=machine.Pin(1), sda=machine.Pin(0))
    bme = bme280.BME280(i2c=i2c)

    for x in range (6):
        print(bme.values)
        ##Temperature(C) Pressure(-1000) and Humidity(%)
        data_to_send.append({'Temperature':float(bme.values[0][:-1]),'Pressure':float(bme.values[1][:-3])-1000.0,'Humidity':float(bme.values[2][:-1]),'timestamp':formated_datetime()})
        time.sleep(2)

    print(data_to_send)
    return data_to_send

##_Real time clock
rtc = machine.RTC()
def set_RTC():
    #connect_to_wifi(SSID, PSK)
    ##_Make GET request to server with time data
    while True:
        try:
            ##Getting time data from "http://date.jsontest.com"
            r = requests.get("http://date.jsontest.com", timeout=10) 
            break
        except:
            print('.',end='')
            time.sleep(1)
            
    date_and_time = r.json()
    r.close()

    print(date_and_time)

    H24_clock_offset=0
    if date_and_time['time'][9:]=='PM':
        H24_clock_offset=12
    hour=int(date_and_time['time'][:2])+H24_clock_offset

    rtc.datetime((int(date_and_time['date'][6:]),
                  int(date_and_time['date'][:2]),
                  int(date_and_time['date'][3:5]),
                  0,
                  int(hour),
                  int(date_and_time['time'][3:5]),
                  int(date_and_time['time'][6:8]),
                  1))
    #disconnect_to_wifi()

##_Reformat data for the database to be able to read it
def formated_datetime():
    a=rtc.datetime()
    return str(a[0])+'-'+str(a[1])+'-'+str(a[2])+'T'+str(a[4])+':'+str(a[5])+':'+str(a[6])

def send_data_out():
    #connect_to_wifi(SSID, PSK)
        
    url = URL_ENDPOINT + "/action/insertOne"
    headers = { "api-key": API_KEY}

    documentToAdd = {"device": STATION_NAME , "v": Data_to_send}

    insertPayload = {
        "dataSource": CLUSTER,
        "database": DATABASE,
        "collection": COLLECTION,
        "document": documentToAdd,
    }

    print("sending...")

    response = requests.post(url, headers=headers, json=insertPayload, timeout=10)

    print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))

    if response.status_code == 201:
        print("Added Successfully")
        led.toggle()
        time.sleep(.25)
        led.toggle()
    else:
        print("Error")

    ##_Always close response objects so we don't leak memory
    response.close()
    time.sleep(.01)


##_Main Loop
try:
    connect_to_wifi(SSID, PSK)
    
    set_RTC()
    
    print(formated_datetime())
    
    Data_to_send=get_bme280_readings()
    
    send_data_out()
    
    disconnect_to_wifi()

except Exception as e:
    print('Main code loop error: ',e)

disconnect_to_wifi()
print("Entering deepsleep 60 sec")
machine.deepsleep(60*1000)#Deepsleep for x secounds


