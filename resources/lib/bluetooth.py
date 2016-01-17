import dbus
import os
import xbmc

class Bluetooth:

    def __init__(self):
        try:
	    self.dbusSystemBus = dbus.SystemBus()
            self.dbusBluezAdapter = None
            xbmc.log('bluetooth::__init__ exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::__init__ ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)


    def start_service(self):
        try:
            xbmc.log('bluetooth::start_service enter_function', level=xbmc.LOGDEBUG)
            if 'org.bluez' in self.dbusSystemBus.list_names():
                self.init_adapter()
            xbmc.log('bluetooth::start_service exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::start_service ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    def stop_service(self):
        try:
            xbmc.log('bluetooth::stop_service enter_function', level=xbmc.LOGDEBUG)
            if hasattr(self, 'discovery_thread'):
                self.discovery_thread.stop()
                del self.discovery_thread
            if hasattr(self, 'dbusBluezAdapter'):
                self.dbusBluezAdapter = None
            xbmc.log('bluetooth::stop_service exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::stop_service ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    def exit(self):
        try:
            xbmc.log('bluetooth::exit enter_function', level=xbmc.LOGDEBUG)
            if hasattr(self, 'discovery_thread'):
                self.discovery_thread.stop()
                del self.discovery_thread
            xbmc.log('bluetooth::exit exit_function', level=xbmc.LOGDEBUG)
            pass
        except Exception, e:
            xbmc.log('bluetooth::exit ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    # ###################################################################
    # # Bluetooth Adapter
    # ###################################################################

    def init_adapter(self):
        try:
            xbmc.log('bluetooth::init_adapter enter_function', level=xbmc.LOGDEBUG)
            dbusBluezManager = dbus.Interface(self.dbusSystemBus.get_object('org.bluez', '/'), 'org.freedesktop.DBus.ObjectManager')
            dbusManagedObjects = dbusBluezManager.GetManagedObjects()
            for (path, ifaces) in dbusManagedObjects.iteritems():
                self.dbusBluezAdapter = ifaces.get('org.bluez.Adapter1')
                if self.dbusBluezAdapter != None:
                    self.dbusBluezAdapter = dbus.Interface(self.dbusSystemBus.get_object('org.bluez', path), 'org.bluez.Adapter1')
                    break
            dbusBluezManager = None
            dbusManagedObjects = None
            if self.dbusBluezAdapter != None:
                self.adapter_powered(self.dbusBluezAdapter)
            xbmc.log('bluetooth::init_adapter exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::init_adapter ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    def adapter_powered(self, adapter, state=1):
        try:
            xbmc.log('bluetooth::adapter_powered enter_function', level=xbmc.LOGDEBUG)
            if int(self.adapter_info(self.dbusBluezAdapter, 'Powered')) != state:
                xbmc.log('bluetooth::adapter_powered set state (' + unicode(state) + ')', level=xbmc.LOGDEBUG)
                adapter_interface = dbus.Interface(self.dbusSystemBus.get_object('org.bluez', adapter.object_path),
                                                   'org.freedesktop.DBus.Properties')
                adapter_interface.Set('org.bluez.Adapter1', 'Alias', dbus.String(os.environ.get('HOSTNAME', 'openelec')))
                adapter_interface.Set('org.bluez.Adapter1', 'Powered', dbus.Boolean(state))
            xbmc.log('bluetooth::adapter_powered exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::adapter_powered ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    def adapter_info(self, adapter, name):
        try:
            xbmc.log('bluetooth::adapter_info enter_function', level=xbmc.LOGDEBUG)
            adapter_interface = dbus.Interface(self.dbusSystemBus.get_object('org.bluez', adapter.object_path),
                                               'org.freedesktop.DBus.Properties')
            xbmc.log('bluetooth::adapter_info exit_function', level=xbmc.LOGDEBUG)
            return adapter_interface.Get('org.bluez.Adapter1', name)
        except Exception, e:
            xbmc.log('bluetooth::adapter_info ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    def start_discovery(self):
        try:
            xbmc.log('bluetooth::start_discovery enter_function', level=xbmc.LOGDEBUG)
            self.dbusBluezAdapter.StartDiscovery()
            self.discovering = True
            xbmc.log('bluetooth::start_discovery exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::start_discovery ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    def stop_discovery(self):
        try:
            xbmc.log('bluetooth::stop_discovery enter_function', level=xbmc.LOGDEBUG)
            if hasattr(self, 'discovering'):
                del self.discovering
                self.dbusBluezAdapter.StopDiscovery()
            xbmc.log('bluetooth::stop_discovery exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::stop_discovery ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)

    # ###################################################################
    # # Bluetooth Device
    # ###################################################################

    def get_devices(self):
        try:
            xbmc.log('bluetooth::get_devices enter_function', level=xbmc.LOGDEBUG)
            devices = {}
            dbusBluezManager = dbus.Interface(self.dbusSystemBus.get_object('org.bluez', '/'), 'org.freedesktop.DBus.ObjectManager')
            managedObjects = dbusBluezManager.GetManagedObjects()
            for (path, interfaces) in managedObjects.iteritems():
                if 'org.bluez.Device1' in interfaces:
                    devices[path] = interfaces['org.bluez.Device1']
            managedObjects = None
            dbusBluezManager = None
            return devices
            xbmc.log('bluetooth::get_devices exit_function', level=xbmc.LOGDEBUG)
        except Exception, e:
            xbmc.log('bluetooth::get_devices::__init__ ERROR: (' + repr(e) + ')', level=xbmc.LOGERROR)
            