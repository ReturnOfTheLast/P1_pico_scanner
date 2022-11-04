# Import Modules
from scanner import scan
from transmitter import ap_connect, transmit 
import network
from machine import Pin
from time import sleep_ms, time as unix_time
import socket

# Instantiate wlan object and bring the network interface up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Instantiate led object
led = Pin("LED", Pin.OUT)
led.off()

# C2 AP
C2_SSID = "C152 AP"
C2_PASSWD = "thisisaverygoodandverylongpassword"

# IP Negotiation HOST and PORT
NEGOTIATION_HOST = "192.168.4.100"
NEGOTIATION_PORT = 61111

# COLLECTOR HOST AND PORT
collector_host = "0.0.0.0"
COLLECTOR_PORT = 62222

# Constants
LED_BLINK_SCAN = 1
LED_BLINK_TRANSMIT = 2
DELAY = 100
FILTERTYPE = 'b'    # '' = no filter, 'w' = whitelist, 'b' = blacklist
FILTERMODE = 1      # 0 = bssid, 1 = ssid

# Variables
filterlist = []

# Set static IP Address
wlan.ifconfig((NEGOTIATION_HOST, "255.255.255.0", "192.168.4.1", "0.0.0.0"))

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

# Get collector ip
neg_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
neg_sock.bind(NEGOTIATION_HOST, NEGOTIATION_PORT)
neg_sock.listen()
conn, addr = neg_sock.accept()

collector_host = addr[0]
conn.send(b"\x01")
conn.close()

sleep_ms(1000)

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
    transmit(collector_host, COLLECTOR_PORT, data)

    # Sleep Delay
    sleep_ms(DELAY)
