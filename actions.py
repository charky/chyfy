import os
import xbmc

def ws_control(wsID,powerState):
    #os.system("bash /home/charky/runIt.sh 11101 "+wsID+" "+powerState)
    if os.path.exists("/storage/sendWS.sh"):
        os.system("sh /storage/sendWS.sh 11101 "+wsID+" "+powerState)
        xbmc.log(msg="ChyFy::action.py::ws_control() - wsID="+wsID+" powerState="+powerState, level=xbmc.LOGDEBUG)
    else:
        xbmc.log(msg="aChyFy::action.py::ws_control() - Script not found; Params: wsID="+wsID+" powerState="+powerState, level=xbmc.LOGERROR)
    