# Import Modules
from scanner import scan
from transmitter import ap_connect, ap_mac_address, socketconnect, transmit

import network
from time import sleep_ms

# Instantiate wlan object and bring the network interface up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# C2 AP
C2_SSID = "C2 AP"
C2_PASSWD = "thisisaverygoodandverylongpassword"

# COLLECTOR HOST AND PORT
COLLECTOR_HOST = "10.10.0.50"
COLLECTOR_PORT = 62222

# Constants
DELAY = 1000
FILTERTYPE = 'b'
FILTERMODE = 0

# Variables
filterlist = []

# Connect to the C2 AP
ap_connect(wlan, C2_SSID, C2_PASSWD)

# Add C2 AP Mac Address to Blacklist
filterlist.append(ap_mac_address(wlan))
# Alternatively Filter by SSID
#filterlist.append(C2_SSID)

while True:
    # Make Scan
    data = scan(wlan, filterlist=filterlist, filtertype=FILTERTYPE, filtermode=FILTERMODE)
    print(data)
    print(ap_mac_address(wlan))
    
    # TODO: Transmit Data
    transmit(COLLECTOR_HOST, COLLECTOR_PORT, data)
    
    # Sleep Delay
    sleep_ms(DELAY)