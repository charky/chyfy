'''
Copyright 2015 Charky

This file is part of ChyFy.

ChyFy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ChyFy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ChyFy.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
import xbmc
import urlparse
from xbmcgui import Dialog

_appName = "ChyFy"
_wsControlLabels = ["WS A On","WS A Off","WS B On","WS B Off","WS C On","WS C Off"]

def ws_control(wsID,powerState):
    #os.system("bash /home/charky/runIt.sh 11101 "+wsID+" "+powerState)
    os.system("sh /storage/sendWS.sh 11101 "+wsID+" "+powerState)
    xbmc.log(msg="wsID="+wsID+" powerState="+powerState, level=xbmc.LOGDEBUG)

def main():
    ## main loop ##
    confirm_discard = False
    while True:
        idx = Dialog().select(_appName, _wsControlLabels)
        xbmc.log(msg=_wsControlLabels[idx], level=xbmc.LOGDEBUG)  
        if idx >= 0 and idx <= 5:
            wsID = str(idx / 2 + 1)
            powerState = "0"
            if idx % 2 == 0:
                powerState = "1"
            ws_control(wsID,powerState)
        elif idx == -1 and confirm_discard:
            if Dialog().yesno(_appName, "Quit?") == 1:
                break
        else:
            break
        
    sys.modules.clear()

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        params = urlparse.parse_qs('&'.join(sys.argv[1:]))
        if params.has_key("wsID") and params.has_key("powerState"):
            ws_control(params["wsID"][0], params["powerState"][0])
        
    else:
        main()