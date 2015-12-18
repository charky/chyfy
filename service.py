import time
import os
import xbmc
import xbmcaddon
from bluetooth import Bluetooth
 
if __name__ == '__main__':
    monitor = xbmc.Monitor()
    
    settings = xbmcaddon.Addon()
        
    blue = Bluetooth()
    lightIsON=False
    deviceFound=False
    discoveryIsOn=False
    
    while not monitor.abortRequested():
        
        if settings.getSetting("service_enabled") == "true":
            #Start Services
            if not discoveryIsOn:
                    blue.start_service()
                    blue.start_discovery()
                    discoveryIsOn = True
            
            # Sleep/wait for abort for 5 seconds
            if monitor.waitForAbort(5):
                # Abort was requested while waiting. We should exit
                break
            #Do the Action
            dbusDevices = blue.get_devices()
            deviceFound=False
            for key in dbusDevices:
                 if 'Name' in dbusDevices[key]:
                    apName = dbusDevices[key]['Name']
                    address = dbusDevices[key]['Address']
                    xbmc.log("Bluetooth: %s -> %s" % (key, apName), level=xbmc.LOGDEBUG)
                    if address == "88:0F:10:64:55:FA":
                        deviceFound=True
                        break
            if deviceFound:
                if not lightIsON:
                    os.system("sh /storage/sendWS.sh 11101 3 1")
                    lightIsON=True
            else:
                if lightIsON:
                    os.system("sh /storage/sendWS.sh 11101 3 0")
                    lightIsON=False
        else:
            if discoveryIsOn:
                blue.stop_discovery()
                blue.stop_service()
                discoveryIsOn = False
            break
    #CleanUp before exit
    if discoveryIsOn:
        os.system("sh /storage/sendWS.sh 11101 3 0")
        blue.stop_discovery()
        blue.stop_service()