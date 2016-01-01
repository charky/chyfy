import time
import os
import xbmc
import xbmcaddon

from bluetooth import Bluetooth
import actions


class Service:
    
    def __init__(self):
        self.monitor = xbmc.Monitor()
        self.player = xbmc.Player()
        self.addon = xbmcaddon.Addon()
        self.blue = Bluetooth()
        self.lightIsON=False
        self.deviceFound=False
        self.discoveryIsOn=False
        self.delayToggle = 0
        
    def run(self):
        while not self.monitor.abortRequested():
            waitForTime = 5
            if self.addon.getSetting("service_enabled") == "true":
                self.startDiscovery()
                waitForTime = int(self.addon.getSetting("waiting_time")) + self.delayToggle
                self.delayToggle = 0
            else:
                self.stopDiscovery()
                #SleepTime in Minutes
                waitForTime = int(self.addon.getSetting("sleep_time")) * 60        
            # Sleep/wait for abort for $waitForTime seconds
            if self.monitor.waitForAbort(waitForTime):
                # Abort was requested while waiting. We should exit
                break
            xbmc.log("ChyFy::service.py - Run after wait for %d seconds" % waitForTime, level=xbmc.LOGDEBUG)
            if self.discoveryIsOn:
                self.scan()
                
    def scan(self):
        dbusDevices = self.blue.get_devices()
        #Check if not None
        if dbusDevices is not None:
            deviceFound=False
            
            rssiSensity = int(self.addon.getSetting("rssi"))
            
            #Get Devices
            device_names = []
            device_names.append(self.addon.getSetting("bt_1_name"))
            
            device_numbers = int(self.addon.getSetting("bt_numbers")) + 1
            if device_numbers > 1:
                for i in range(2,device_numbers):
                    device_names.append(self.addon.getSetting("bt_"+i+"_name"))
            
            for key in dbusDevices:
                 if 'Name' in dbusDevices[key]:
                    devName = dbusDevices[key]['Name']
                    devAddress = dbusDevices[key]['Address']
                    devRSSI = dbusDevices[key]['RSSI']
                    xbmc.log("Bluetooth: %s -> %s (%s)" % (key, devName,devRSSI), level=xbmc.LOGDEBUG)
                    if (devName in device_names or devAddress in device_names) and devRSSI >= rssiSensity:
                        xbmc.log("ChyFy::service.py - Device was found: %s" % devName, level=xbmc.LOGDEBUG)
                        deviceFound=True
                        break
            if deviceFound:
                self.handle_device_found()
            else:
                self.handle_device_notfound()
        else:
            xbmc.log("ChyFy::service.py - dbusDevices is None", level=xbmc.LOGERROR)
            
    def handle_device_found(self):
        if not self.lightIsON:
            for i in range(1,4):
                if self.addon.getSetting("ws_"+str(i)+"_auto_on") == "true":
                    actions.ws_control(str(i), "1")
            if self.addon.getSetting("mc_auto_play") == "true" and not self.player.isPlaying():
                self.player.pause()
            self.delayToggle = 30
            self.lightIsON=True
            
    def handle_device_notfound(self):
        if self.lightIsON:
            for i in range(1,4):
                if self.addon.getSetting("ws_"+str(i)+"_auto_off") == "true":
                    actions.ws_control(str(i), "0")
            if self.addon.getSetting("mc_auto_pause") == "true" and self.player.isPlaying():
                self.player.pause()
            self.lightIsON=False
            
    def startDiscovery(self): 
        if not self.discoveryIsOn:
            self.blue.start_service()
            self.blue.start_discovery() 
            self.discoveryIsOn = True
                    
    def stopDiscovery(self):
        if self.discoveryIsOn:
            self.blue.stop_discovery()
            self.blue.stop_service()
            self.discoveryIsOn = False
            
##
#
#Init Service and Run
#
##
if __name__ == '__main__':
    service = Service()
    service.run()