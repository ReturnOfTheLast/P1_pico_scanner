# Import Modules
from scanner import scan
from transmitter import ap_connect, ap_mac_address, transmit

import network
from machine import Pin
from time import sleep_ms

# Instantiate wlan object and bring the network interface up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Instantiate led object
led = Pin("LED", Pin.OUT)
led.off()

# C2 AP
C2_SSID = "C2 AP"
C2_PASSWD = "thisisaverygoodandverylongpassword"

# COLLECTOR HOST AND PORT
COLLECTOR_HOST = "10.10.0.50"
COLLECTOR_PORT = 62222

# Constants
LED_BLINK_SCAN = 1
LED_BLINK_TRANSMIT = 2
DELAY = 1000
FILTERTYPE = 'b'
FILTERMODE = 0

# Variables
filterlist = []

# Connect to the C2 AP
ap_connect(wlan, C2_SSID, C2_PASSWD)
led.on()

# Add C2 AP Mac Address to Blacklist
filterlist.append(ap_mac_address(wlan))
# Alternatively Filter by SSID
#filterlist.append(C2_SSID)

def blinker(times):
    time = int(200/(times*2))
    for i in times:
        led.off()
        sleep_ms(time)
        led.on()
        sleep_ms(time)

while True:
    # Make Scan
    blinker(LED_BLINK_SCAN)
    scandata = scan(wlan, filterlist=filterlist, filtertype=FILTERTYPE, filtermode=FILTERMODE)
    
    # Setup Data Package
    data = {
        "scan": scandata,
        "location": [0, 0, 0],
        "time": 0
    }
    print(data)

    # Transmit Data
    blinker(LED_BLINK_TRANSMIT)
    transmit(COLLECTOR_HOST, COLLECTOR_PORT, data)

    # Sleep Delay
    sleep_ms(DELAY)