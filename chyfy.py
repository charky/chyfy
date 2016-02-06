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

import os, sys, urlparse
import xbmc, xbmcaddon

# Load Libs
__addon__    = xbmcaddon.Addon()
__cwd__      = __addon__.getAddonInfo('path').decode("utf-8")
__resource__ = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
sys.path.append(__resource__)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Import Actions
        from actions import Actions
        Actions().doAction(sys.argv)
    else:
        # Import GUI
        from gui import GUI
        GUI().show()
