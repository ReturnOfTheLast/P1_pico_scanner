import network

# Instantiate wlan object and bring the network interface up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)