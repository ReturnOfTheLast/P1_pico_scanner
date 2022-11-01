import network
import socket
from machine import Pin, Timer
import time

led = Pin("LED", Pin.OUT)

timer = Timer()


def blink(timer):
    led.toggle()

#timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)


def wlan_setup():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

def wlan_connect(ssid, key):
    global wlan, timer, pico_config
    for i in range(5):
        if wlan.isconnected() == False:
            wlan.connect(ssid, key)
            pico_config = wlan.ifconfig()
            if wlan.isconnected() == True:  
                print(f"Connected to {ssid}")
                break
            else:
                print("Not connected")


def wlan_scan():
    global read, wlan
    wlan.active()
    wlan.scan()
    read = wlan.scan()

"""
pico_config = wlan.ifconfig()
pico_ip = pico_config[0]
pico_addr = (str(pico_ip),138)
"""

"""
time.sleep(1)
wlan.active()
wlan.scan()
read = wlan.scan()
print(reading)
#print(wlan.scan())

"""


def data_filter():
    global data, read, mellemled, wlan
    for i in range(len(read)):
        #data.append([bytes(reading[i][0])])
        data.append([(read[i][0])])
        tekst = read[i][3]
        tekst = str(tekst)
        tekst = tekst.replace("-","")
        tekst = int(tekst)
        #tekst = bytes(tekst)
        mellemled.append(tekst)
        data[i].append(tekst)
        print(data)



def socket_send():
    pico_socket = socket.socket()
    pico_socket.connect((client_ssid, client_port))
    print("\nconnected")
    for i in range(len(data)):
        sending = str(data[i])
        print(sending)
        #pico_socket.sendall(sending)
        pico_socket.write(sending)
    pico_socket.close()
    print("\nsent")

def toggle():
    global led
    for i in range(4):
        led.toggle()
        time.sleep_ms(200)
        

#pico_socket.write("end")
#pico_socket.sendall(data)


ssid="C2 AP"
key="thisisaverygoodandverylongpassword"
wlan_setup()
wlan_connect(ssid, key)
led.toggle()


client_ssid = "10.10.0.226"
client_port = 65432

for i in range(4):
    read = []
    wlan_scan()

    data = []
    mellemled = []
    print(len(read))
    data_filter()
    toggle()
    socket_send()
    toggle()
    time.sleep(4)
    print(f"#{i+1}")

led.toggle()