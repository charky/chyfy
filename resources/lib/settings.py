import time
import xbmcaddon

class Settings:
    
    def __init__( self, *args, **kwargs ):
        self.addon = xbmcaddon.Addon()
        self.general = {}
        self.wireless_switch = {}
        self.media_control = {}
        self.bt_devices = {}
        self.update()
        
    def update(self):
        self.addon = xbmcaddon.Addon()
        self.update_general()
        self.update_wireless_switch()
        self.update_media_control()
        self.update_bt_devices()
        
    def update_general(self):
        self.general.update({
            "service_enabled": self.string2bool("service_enabled"),
            "ws_code": self.addon.getSetting("ws_code"),
            "waiting_time": int(self.addon.getSetting("waiting_time")),
            "sleep_time": int(self.addon.getSetting("sleep_time")) * 60,
            "rssi": int(self.addon.getSetting("rssi")),
            "use_time_interval": self.string2bool("use_time_interval"),
            "start_time": time.strptime(self.addon.getSetting("start_time"), '%H:%M'),
            "end_time": time.strptime(self.addon.getSetting("end_time"), '%H:%M') })
        
    def update_wireless_switch(self):
        self.wireless_switch.update({
            "ws_1_name": self.addon.getSetting("ws_1_name").strip(),
            "ws_2_name": self.addon.getSetting("ws_2_name").strip(),
            "ws_3_name": self.addon.getSetting("ws_3_name").strip(),
            "ws_1_auto_on": self.string2bool("ws_1_auto_on"),
            "ws_2_auto_on": self.string2bool("ws_2_auto_on"),
            "ws_3_auto_on": self.string2bool("ws_3_auto_on"),
            "ws_1_auto_off": self.string2bool("ws_1_auto_off"),
            "ws_2_auto_off": self.string2bool("ws_2_auto_off"),
            "ws_3_auto_off": self.string2bool("ws_3_auto_off") })
        
    def update_media_control(self):
        self.media_control.update({
            "mc_auto_play": self.string2bool("mc_auto_play"),
            "mc_auto_pause": self.string2bool("mc_auto_pause") })
        
    def update_bt_devices(self):
        self.bt_devices.update({
            "bt_numbers": int(self.addon.getSetting("bt_numbers")) + 1,
            "bt_1_name": self.addon.getSetting("bt_1_name"),
            "bt_2_name": self.addon.getSetting("bt_2_name"),
            "bt_3_name": self.addon.getSetting("bt_3_name"),
            "bt_4_name": self.addon.getSetting("bt_4_name"),
            "bt_5_name": self.addon.getSetting("bt_5_name") })
    
    def set(self,key,value):
        self.addon.setSetting(key, value)
        
    def getJSON(self):
        retStr = '{ "general": { "init": "1"'
        for key in self.general:
            retStr += ', "' + key + '": "' + self.general[key] +'"'
        retStr += '}, "wireless_switch": { "init": "1"'
        for key in self.wireless_switch:
            retStr += ', "' + key + '": "' + self.general[key] +'"'
        retStr += '}, "media_control": { "init": "1"'
        for key in self.media_control:
            retStr += ', "' + key + '": "' + self.general[key] +'"'
        retStr += '}, "bt_devices": { "init": "1"'
        for key in self.bt_devices:
            retStr += ', "' + key + '": "' + self.general[key] +'"'
        retStr += " } }"
        
        return retStr
        
    def string2bool(self, idname):
        return (str(self.addon.getSetting(idname)).lower() == "true")
    