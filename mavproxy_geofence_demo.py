#!/usr/bin/env python
'''geofence demo command'''

from pymavlink import mavutil

from MAVProxy.modules.lib import mp_module

class GeofenceDemoModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(GeofenceDemoModule, self).__init__(mpstate, "geofence_demo", "geofence demo command")
        self.add_command('gfdemo', self.cmd_gf_demo, "run geofence demo")
        self.fence_module = self.module('fence')

    def cmd_gf_demo(self, args):
        print(args)

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        if mtype == "BATTERY_STATUS":
            print(m.BATTERY_STATUS.battery_remaining)

def init(mpstate):
    '''initialise module'''
    return GeofenceDemoModule(mpstate)
