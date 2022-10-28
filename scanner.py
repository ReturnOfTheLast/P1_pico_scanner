# Import Modules
from network import WLAN
from binascii import hexlify

# Scan function
def scan(wlan: WLAN, filterlist: list=[], filtertype: str='', filtermode: int=0) -> list:
    """Scan for networks

    Args:
        wlan (WLAN): WLAN object for the wifi radioS
        filterlist (list, optional): List to filter by. Defaults to [].
        filtertype (str, optional): Type of filter, 'w' = whitelist, 'b' = blacklist, leave empty for no filters. Defaults to ''.
        filtermode (int, optional): Filter by bssid or ssid, 0 = bssid, 1 = ssid. Defaults to 0.

    Raises:
        ValueError: Invalid Values

    Returns:
        list: List of Network Data, (bssid, ssid, rssi)
    """    
    # Make a scan
    scandata = wlan.scan()

    # Extract BSSID,  and RSSI from the scan
    extracted_data = []

    for netw in scandata:
        bssid = hexlify(netw[1]).decode("uft-8")
        ssid = netw[0].decode("uft-8")
        rssi = netw[3]
        extracted_data.append((bssid, ssid, rssi))
    
    # Filter data
    # Check if filtertype is set and filterlist isn't empty
    if len(filtertype) > 0 and len(filterlist) > 0:
        # Make temporary list
        temp_list = []
        
        # Make sure options are valid
        if 0 > filtermode > 1 or not filtertype.lower() in ['w', 'b']:
            raise ValueError("Invalid Values")
        
        # Loop over data and add data to the temp list if it matches
        # with a bssid or ssid (chosen by filtermode) in the filterlist
        for data in extracted_data:
            if data[filtermode] in filterlist:
                temp_list.append(data)
        
        # Overwrite the extracted_data with temp_list if whitelisting
        if filtertype.lower() == 'w':
            extracted_data = temp_list
        # or remove the data from extracted_data if blacklisting
        elif filtertype.lower() == 'b':
            for data in temp_list:
                extracted_data.remove(data)
    
    # Return data
    return extracted_data