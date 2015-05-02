'''
Copyright 2015 Andre Zaske

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

import xbmcaddon
import xbmcgui
import sys

#Set global addon information first
__addon_id__ = 'script.audio.chyfy'
addon_cfg = xbmcaddon.Addon(__addon_id__)
__addon_path__ = addon_cfg.getAddonInfo('path')
__addon_version__ = addon_cfg.getAddonInfo('version')
DEFAULT_FOLDER_IMG = 'DefaultFolder.png'


addon_handle = int(sys.argv[1])
url_path = sys.argv[0] + '?' + 'Inbox'

#Hello Wolrd 
addonname   = addon_cfg.getAddonInfo('name')
 
line1 = "Hello World!"
line2 = "We can write anything we want here"
line3 = "Using Python"
 
xbmcgui.Dialog().ok(addonname, line1, line2, line3) 

item = xbmcgui.ListItem("FolderItem1", iconImage = DEFAULT_FOLDER_IMG)
xbmcplugin.addDirectoryItem(handle = addon_handle, 
                                    url = url_path, listitem = item, 
                                    isFolder = True) 

 