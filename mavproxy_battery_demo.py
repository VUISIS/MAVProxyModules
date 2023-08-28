#!/usr/bin/env python
'''battery demo command'''

from pymavlink import mavutil

from MAVProxy.modules.lib import mp_module

import re

class BatteryDemoModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(BatteryDemoModule, self).__init__(mpstate, "battery_demo", "battery demo command")
        self.add_command('batdemo', self.cmd_bat_demo, "run battery demo")
        self.armed = False
        self.arm_module = self.module('arm')
        self.mode_module = self.module('mode')
        self.wp_module = self.module('wp')
        self.formula_module = self.module('formula')

    def cmd_bat_demo(self, args):
        self.formula_module.cmd_formula(['load', 'battery.4ml'])
        self.formula_module.cmd_formula(['solve', 'pm 1 Battery.conforms'])
        output = self.formula_module.cmd_formula(['extract', '0 0 demo'])
        if re.search("Model\s+not\s+solvable\.", output):
            print("Model returned not solvable. Stopping run.")
            return
        elif re.search("Solution\s+number", output):
            print("Solution found. Starting run.")
            if not self.armed:
                self.arm_module.cmd_arm(['throttle'])

            self.wp_module.cmd_wp(['load', 'mission.txt'])

            self.wp_module.wp_add_takeoff([20])

            self.wp_module.wp_add_RTL()

            self.mode_module.cmd_mode(['auto'])

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        if mtype == 'HEARTBEAT' and m.type != mavutil.mavlink.MAV_TYPE_GCS:
            self.armed = self.master.motors_armed()
        elif mtype == "BATTERY_STATUS":
            print(m.BATTERY_STATUS.battery_remaining)

def init(mpstate):
    '''initialise module'''
    return BatteryDemoModule(mpstate)
