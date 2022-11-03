# Import Modules
from scanner import scan
from transmitter import ap_connect, transmit 
import network
from machine import Pin
from time import sleep_ms, time as unix_time

# Instantiate wlan object and bring the network interface up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Instantiate led object
led = Pin("LED", Pin.OUT)
led.off()

# C2 AP
C2_SSID = "C152 AP"
C2_PASSWD = "thisisaverygoodandverylongpassword"

# COLLECTOR HOST AND PORT
# IDEA: Make the collector transmit its ip
# and set it on the pico.
# wlan.ifconfig(("192.168.4.100", "255.255.255.0", "192.168.4.1", "192.168.4.1"))
# (after wifi connect) will set the pico's ip to 192.168.4.100 so we can transmit
# to it at the start. By doing this we do not need to set a static ip on the
# collector side
COLLECTOR_HOST = "192.168.4.50"
COLLECTOR_PORT = 62222

# Constants
LED_BLINK_SCAN = 1
LED_BLINK_TRANSMIT = 2
DELAY = 100
FILTERTYPE = 'b'    # '' = no filter, 'w' = whitelist, 'b' = blacklist
FILTERMODE = 1      # 0 = bssid, 1 = ssid

# Variables
filterlist = []

# Connect to the C2 AP
ap_connect(wlan, C2_SSID, C2_PASSWD)
led.on()

# Filter C2 SSID from the scan list
filterlist.append(C2_SSID)

def blinker(times):
    time = int(200/(times*2))
    for i in range(times):
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
        "time": unix_time()
    }
    print(data)

    # Transmit Data
    blinker(LED_BLINK_TRANSMIT)
    transmit(COLLECTOR_HOST, COLLECTOR_PORT, data)

    # Sleep Delay
    sleep_ms(DELAY)
