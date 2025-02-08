
# World's Saddest BluOS(tm) (compatible) Media Controller

This is distributed under the Modified "shit-ware" license (see LICENSE.md).

## Prerequisitez

1. Python 3.10 or better (I refused to use python until they implemented a switch/case equivalent, and I waited a LONG time)
2. You need "requests" so invoke 'pip3 install requests' if you don't have it!

## Instructionz

1. Modify wsbmc.py with the IP address of your BluOS hardware.
     (I haven't implemented auto-discovery yet)
2. Open a terminal and invoke python3 ./wsbmc.py
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

1. The player may abort under certain conditions, like, say if you change away
   from BluOS mode to another device input. My gift to you!
2. The API used by WSBMC may be found here:
     https://bluos.io/wp-content/uploads/2023/09/BluOS-Custom-Integration-API-v1.5.pdf

