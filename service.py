import time, os
import xbmc, xbmcaddon

# Load Libs
__addon__    = xbmcaddon.Addon()
__cwd__      = __addon__.getAddonInfo('path').decode("utf-8")
__resource__ = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
sys.path.append(__resource__)

from actions import Actions
from bluetooth import Bluetooth
from settings import Settings


settings = Settings()

class Service:
    
    def __init__(self):
        self.monitor = CE_Monitor(self)
        self.player = xbmc.Player()
        self.actions = Actions()
        self.blue = Bluetooth()
        self.lightIsON=False
        self.deviceFound=False
        self.discoveryIsOn=False
        self.delayToggle = 0

    def run(self):
        while not self.monitor.abortRequested():
            waitForTime = 5
            
            timeIntervalHit = True
            
            if settings.general["use_time_interval"]:
                startTime = settings.general["start_time"]   
                endTime = settings.general["end_time"]
                currentTime = time.localtime()
                if currentTime >= startTime and currentTime <= endTime:
                    timeIntervalHit = True
                    xbmc.log("ChyFy::service.py - Time Interval Hit", level=xbmc.LOGDEBUG)
                else:
                    timeIntervalHit = False
                    xbmc.log("ChyFy::service.py - Current Time not in Time Interval", level=xbmc.LOGDEBUG)
                
            if settings.general["service_enabled"] and timeIntervalHit:
                self.startDiscovery()
                waitForTime = settings.general["waiting_time"] + self.delayToggle
                self.delayToggle = 0
            else:
                self.stopDiscovery()
                #SleepTime in Minutes
                waitForTime = settings.general["sleep_time"]        
            # Sleep/wait for abort for $waitForTime seconds
            xbmc.log("ChyFy::service.py - Start waiting for %d seconds" % waitForTime, level=xbmc.LOGDEBUG)
            if self.monitor.waitForAbort(waitForTime):
                # Abort was requested while waiting. We should exit
                break
            xbmc.log("ChyFy::service.py - Run after wait", level=xbmc.LOGDEBUG)
            if self.discoveryIsOn:
                self.scan()
                xbmc.log("ChyFy::service.py - discovery is on", level=xbmc.LOGDEBUG)
            else:
                xbmc.log("ChyFy::service.py - discovery is off", level=xbmc.LOGDEBUG)
                
    def scan(self):
        dbusDevices = self.blue.get_devices()
        #Check if not None
        if dbusDevices is not None:
            deviceFound=False
            
            rssiSensity = settings.general["rssi"]
            
            #Get Devices
            device_names = []
            device_names.append(settings.bt_devices["bt_1_name"])
            
            device_numbers = settings.bt_devices["bt_numbers"]
            if device_numbers > 1:
                for i in range(2,device_numbers):
                    device_names.append(settings.bt_devices["bt_"+i+"_name"])
            
            for key in dbusDevices:
                 if 'Name' in dbusDevices[key]:
                    devName = dbusDevices[key]['Name']
                    devAddress = dbusDevices[key]['Address']
                    devRSSI = int(dbusDevices[key]['RSSI'])
                    xbmc.log("ChyFy::service.py - Device: %s -> %s (%s >= %s)" % (key, devName, devRSSI, rssiSensity), level=xbmc.LOGDEBUG)
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
                if settings.wireless_switch["ws_"+str(i)+"_auto_on"]:
                    self.actions.ws_control(str(i), "1")
            if settings.media_control["mc_auto_play"] and not self.player.isPlaying():
                self.player.pause()
            self.delayToggle = 30
            self.lightIsON=True
            
    def handle_device_notfound(self):
        if self.lightIsON:
            for i in range(1,4):
                if settings.wireless_switch["ws_"+str(i)+"_auto_off"]:
                    self.actions.ws_control(str(i), "0")
            if settings.media_control["mc_auto_pause"] and self.player.isPlaying():
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

class CE_Monitor( xbmc.Monitor ):
    def __init__(self, service):
        xbmc.Monitor.__init__(self)
        self.service = service
    def onSettingsChanged(self):
        settings.update()
        xbmc.log("ChyFy::service.py - onSettingsChanged - ServiceEnabled = %s" % settings.general["service_enabled"], level=xbmc.LOGNOTICE)
        
        
##
#
#Init Service and Run
#
##
if __name__ == '__main__':
    xbmc.log("ChyFy::service.py - Main Service starting", level=xbmc.LOGNOTICE)
    Service().run()
    xbmc.log("ChyFy::service.py - Main Service stopped", level=xbmc.LOGNOTICE)
    