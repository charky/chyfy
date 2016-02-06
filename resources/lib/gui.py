import sys
import xbmc
import xbmcaddon
from xbmcgui import Dialog

from actions import Actions
from settings import Settings

settings = Settings()

##### Variables #####
addon     = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

class GUI:
    
    def __init__(self):
       self.wsControlLabels = []
       self.wsControlLabels.append(settings.wireless_switch["ws_1_name"] + " On")
       self.wsControlLabels.append(settings.wireless_switch["ws_1_name"] + " Off")
       self.wsControlLabels.append(settings.wireless_switch["ws_2_name"] + " On")
       self.wsControlLabels.append(settings.wireless_switch["ws_2_name"] + " Off")
       self.wsControlLabels.append(settings.wireless_switch["ws_3_name"] + " On")
       self.wsControlLabels.append(settings.wireless_switch["ws_3_name"] + " Off")
       self.wsControlLabels.append("- - -")
       self.wsControlLabels.append("Toggle Service on/off")
       self.actions = Actions()
     
    def toggleService(self):
        settings.update_general()
        if settings.general["service_enabled"]:
            settings.set("service_enabled", "false")
        else:
            settings.set("service_enabled", "true")
        settings.update_general()    
       
    def show(self):    
        ## main loop ##
        while True:
            if settings.general["service_enabled"]:
                self.wsControlLabels[7] = "Disable Service"
            else:
                self.wsControlLabels[7] = "Enable Service"
                
            idx = Dialog().select(addonname, self.wsControlLabels)
            xbmc.log(msg=self.wsControlLabels[idx], level=xbmc.LOGDEBUG)  
            if idx >= 0 and idx <= 5:
                wsID = str(idx / 2 + 1)
                powerState = "0"
                if idx % 2 == 0:
                    powerState = "1"
                self.actions.ws_control(wsID,powerState)
            elif idx == 7:
                self.toggleService()
            elif idx == 8:
                self.actions.start_settings_server()
            elif idx == -1:
                break
            else:
                break   
        sys.modules.clear()
    