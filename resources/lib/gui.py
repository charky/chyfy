import sys
import xbmc
import xbmcaddon
from xbmcgui import Dialog

import actions

##### Variables #####
addon     = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

class GUI:
    
    def __init__(self):
       self.wsControlLabels = []
       self.wsControlLabels.append(addon.getSetting("ws_1_name").strip() + " On")
       self.wsControlLabels.append(addon.getSetting("ws_1_name").strip() + " Off")
       self.wsControlLabels.append(addon.getSetting("ws_2_name").strip() + " On")
       self.wsControlLabels.append(addon.getSetting("ws_2_name").strip() + " Off")
       self.wsControlLabels.append(addon.getSetting("ws_3_name").strip() + " On")
       self.wsControlLabels.append(addon.getSetting("ws_3_name").strip() + " Off")
       self.wsControlLabels.append("- - -")
       self.wsControlLabels.append("Toggle Service on/off")
     
    def toggleService(self):
        if addon.getSetting("service_enabled") == "true":
            addon.setSetting("service_enabled", "false")
        else:
            addon.setSetting("service_enabled", "true")
       
    def show(self):    
        ## main loop ##
        while True:
            if addon.getSetting("service_enabled") == "true":
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
                actions.ws_control(wsID,powerState)
            elif idx == 7:
                self.toggleService()
            elif idx == -1:
                break
            else:
                break   
        sys.modules.clear()
    