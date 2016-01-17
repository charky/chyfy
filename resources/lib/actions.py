import os, sys
import xbmc, xbmcaddon


addon     = xbmcaddon.Addon()
# Load Libs
__resource__ = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
sys.path.append(__resource__)

from remoteSwitch import RemoteSwitch

def ws_control(wsID,powerState):
    ## Load Config RemoteSwitch Key
    ws_code = addon.getSetting("ws_code")
    
    # change the pin according to your wiring (Raspberry)
    default_pin = 17
    
    device = RemoteSwitch(  
        device= int(wsID), 
        key=map(int, list(ws_code)), 
        pin=default_pin
    )

    if int(powerState):
        device.switchOn()
    else: 
        device.switchOff()
    xbmc.log(msg="ChyFy::action.py::ws_control() - wsID="+wsID+" powerState="+powerState, level=xbmc.LOGDEBUG)

def app_enable_leaving_room(value):
    if (value):
        addon.setSetting("enable_leaving", "true")
    else:
        addon.setSetting("enable_leaving", "false")
        
def app_enable_service(value):
    if (value):
        addon.setSetting("service_enabled", "true")
    else:
        addon.setSetting("service_enabled", "false")
        