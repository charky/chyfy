import xbmcgui

KEY_BUTTON_BACK = 275
KEY_KEYBOARD_ESC = 61467

class UIWindow( xbmcgui.WindowXML ):


    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXML.__init__( self, *args, **kwargs )
    
    
    def onInit(self):
        pass

    def onAction(self, action):
        buttonCode =  action.getButtonCode()
        actionID   =  action.getId()
        print "onAction(): actionID=%i buttonCode=%i" % (actionID,buttonCode)
        if (buttonCode == KEY_BUTTON_BACK or buttonCode == KEY_KEYBOARD_ESC):
            self.close()

    def onClick(self, controlID):
        if (controlID == 2):
            print "Some Control with id 2 was pressed"

    def onFocus(self, controlID):
        if (controlID == 5):
            print 'The control with id="5" just got focus'
