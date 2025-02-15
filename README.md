
# World's Saddest BluOS(tm) (compatible) Media Controller

This is distributed under the Modified "shit-ware" license (see LICENSE.md).

## Prerequisitez

1. Python 3.10 or better (I refused to use python until they implemented a switch/case equivalent, and I waited a LONG time)
2. You need "requests" so invoke 'pip3 install requests' if you don't have it!
3. For auto-discovery to work you might need to allow broadcasts from your firewall,
    if it doesn't work try the following: "sudo ufw allow 11430/udp"
4. Note that auto-discovery is optional if you already know the IP of your BluOS device.

## Instructionz

1. Open a terminal and invoke "python3 ./wsbmc.py".
2. Or, if you already know the IP address of the BluOS device, invoke "python ./wsbmc.py IPADDR", where IPADDR is your device's IP (e.g.: 192.168.1.110).
3. The following key commands are supported by the player:

- u - volume up (and unmute)
- d - volume down
- m - mute
- p - toggle pause
- s - skip track
- b - back track
- q - quit WSBMC
- r - refresh display

## Known Featurez / Notez

1. The API used by WSBMC may be found here:
     https://bluos.io/wp-content/uploads/2023/09/BluOS-Custom-Integration-API-v1.5.pdf

