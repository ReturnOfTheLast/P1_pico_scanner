# Import Modules
from network import WLAN
import socket
from time import sleep_ms
from binascii import hexlify
import json

# Connect Function
def ap_connect(wlan: WLAN, ssid: str, passwd: str) -> None:
    """Connect to the C2 Access Point

    Args:
        wlan (WLAN): WLAN object for the wifi radio
        ssid (str): SSID of the Access Point
        passwd (str): Password of the Access Point

    Raises:
        RuntimeError: Network Connection Failed
    """
    wlan.connect(ssid, passwd)
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        #print('Waiting for Connection...')
        sleep_ms(1000)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('Network Connection Failed')
    else:
        #print('Connected')
        status = wlan.ifconfig()
        #print("ip = " + status[0])

# Transmit Data
def transmit(host: str, port: int, data: dict) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))
    #print("Socket Connected")
    datadump = bytes(json.dumps(data), "utf-8")
    #print(f"Sending {datadump}")
    sock.send(datadump)
    sock.close()
    #print("Sent")
