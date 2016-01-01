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

import sys
import urlparse

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Import Actions
        import actions
         
        params = urlparse.parse_qs('&'.join(sys.argv[1:]))
        if params.has_key("wsID") and params.has_key("powerState"):
            actions.ws_control(params["wsID"][0], params["powerState"][0])
    else:
        # Import GUI
        from gui import GUI
        GUI().show()
