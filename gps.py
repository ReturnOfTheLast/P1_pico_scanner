from machine import Pin, UART
from time import sleep_ms

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

TIMEOUT = False

def getGPS() -> tuple[str, str, str]:
    """Get the GPS location.

    Returns:
        tuple[str, str, str]: latitude, longitude, satellites
    """
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(",")
        #print(buff)

        if parts[0] == "b'$GPGGA" and len(parts) == 15:
            if parts[2] and parts[3] and parts[4] and parts[5] and parts[6]:
                latitude = convertToDegree(parts[2])
                if (parts[3] == "S"):
                    latitude = f"-{latitude}"
                longitude = convertToDegree(parts[4])
                if (parts[5] == "W"):
                    longitude = f"-{longitude}"
                satellites = parts[7]
                break
        sleep_ms(200)
    return latitude, longitude, satellites

def convertToDegree(rawdegrees: str) -> str:
    """Convert raw degrees into formatted degrees.

    Args:
        rawdegrees (str): Raw Degrees

    Returns:
        str: Formatted degrees
    """
    rawasfloat = float(rawdegrees)
    firstdigits = int(rawasfloat/100)
    nexttwodigits = rawasfloat - float(firstdigits*100)

    converted = float(firstdigits + nexttwodigits/60.0)
    converted = f"{converted:.6f}"
    return str(converted)
