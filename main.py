# Import Modules
from scanner import scan
from transmitter import connect
from time import sleep_ms

# Constants
DELAY = 1000
FILTERLIST = ['0ac5e1a99ea8']
FILTERTYPE = 'w'
FILTERMODE = 0

# C2 AP
C2_SSID = ""
C2_PASSWD = ""

while True:
    # Make Scan
    data = scan(filterlist=FILTERLIST, filtertype=FILTERTYPE, filtermode=FILTERMODE)
    print(data)
    
    # TODO: Transmit Data
    
    # Sleep Delay
    sleep_ms(DELAY)