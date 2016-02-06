import os, sys, platform, urlparse, BaseHTTPServer
import xbmc, xbmcaddon

runningOnRaspberry = False
if platform.machine().startswith("armv7"):
    from remoteswitch import RemoteSwitch
    runningOnRaspberry = True

from settings import Settings

settings = Settings()

class Actions:
    def __init__(self):
        self.HOST_NAME = ''
        self.PORT_NUMBER = 9000
    
    def doAction(self, argv):
        params = {}
        for i in sys.argv:
            args = i
            if(args.startswith('?')):
                args = args[1:]
            params.update(dict(urlparse.parse_qsl(args)))
            
        if params.has_key("wsID") and params.has_key("powerState"):
            self.ws_control(params["wsID"][0], params["powerState"][0])

    def start_settings_server(self):
        server_class = BaseHTTPServer.HTTPServer
        server_class.timeout = 10
        httpd = server_class((self.HOST_NAME, self.PORT_NUMBER), RequestHandler)
        httpd.handle_request()
        httpd.server_close()
    
    def ws_control(self,wsID,powerState):
        ## Load Config RemoteSwitch Key
        ws_code = settings.general["ws_code"]
        
        # devices: A = 1, B = 2, C = 4, D = 8, E = 16
        # Corrections  
        if wsID == "3" :
            wsID = "4"
        
        # change the pin according to your wiring (Raspberry)
        default_pin = 17
        # Only do some Actions on Raspberry
        if runningOnRaspberry:
            device = RemoteSwitch(  
                device= int(wsID), 
                key=map(int, list(ws_code)), 
                pin=default_pin
            )
        
            if int(powerState):
                device.switchOn()
            else: 
                device.switchOff()
            xbmc.log(msg="ChyFy::action.py - ws_control() - wsID="+wsID+" powerState="+powerState, level=xbmc.LOGDEBUG)
        else:
            xbmc.log(msg="ChyFy::action.py - ws_control() - NOT on Raspberry wsID="+wsID+" powerState="+powerState, level=xbmc.LOGDEBUG)
    
    def app_enable_leaving_room(value):
        if (value):
            settings.set("enable_leaving", "true")
        else:
            settings.set("enable_leaving", "false")
            
    def app_enable_service(value):
        if (value):
            settings.set("service_enabled", "true")
        else:
            settings.set("service_enabled", "false")
    
    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
            """Respond to a GET request."""
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(settings.getJSON())
            