#!/usr/bin/env python
'''battery demo command'''

from pymavlink import mavutil

from MAVProxy.modules.lib import mp_module

import re

from pythonnet import load
load("coreclr")
import clr
clr.AddReference("/home/stephen/git/formula/Src/CommandLine/bin/Release/Linux/x64/net6.0/CommandLine.dll")

from Microsoft.Formula.CommandLine import CommandInterface, CommandLineProgram
from System.IO import StringWriter
from System import Console 

class BatteryDemoModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(BatteryDemoModule, self).__init__(mpstate, "battery_demo", "battery demo command", public=True)
        self.add_command('batdemo', self.cmd_bat_demo, "run battery demo")
        self.arm_module = self.module('arm')
        self.mode_module = self.module('mode')
        self.wp_module = self.module('wp')
        self.cmdlong_module = self.module('cmdlong')
        self.armed = False
        self.battery_cap = 11.4*1.1*3600
        self.rate = 116.67
        self.consumed_cap = 0.0
        self.battery_period = mavutil.periodic_event(1)
        self.print_period = mavutil.periodic_event(0.25)
        self.sw = StringWriter()
        Console.SetOut(self.sw)
        Console.SetError(self.sw)

        sink = CommandLineProgram.ConsoleSink()
        chooser = CommandLineProgram.ConsoleChooser()
        self.ci = CommandInterface(sink, chooser)

        if not self.ci.DoCommand('wait on'):
            print("Wait command failed.")
            return

    def cmd_bat_demo(self, args):
        if len(args) != 1:
             return
        
        if not self.ci.DoCommand('unload *'):
            print("Solve command failed.")
            return
        
        if not self.ci.DoCommand('tunload *'):
            print("Solve command failed.")
            return
        
        self.sw.GetStringBuilder().Clear()
        
        file = ""
        if args[0] == 'valid':
            file = '/home/stephen/git/MAVProxyModules/ValidBatteryChecker.4ml'
        elif args[0] == 'invalid':
            file = '/home/stephen/git/MAVProxyModules/InvalidBatteryChecker.4ml'
        elif args[0] == 'fixed':
            file = '/home/stephen/git/MAVProxyModules/FixedBatteryChecker.4ml'

        if not self.ci.DoCommand('load ' + file):
            print("Load command failed.")
            return
        
        output = self.sw.ToString()
        self.sw.GetStringBuilder().Clear()
        print(output)
        
        mission = ""
        if args[0] == 'valid':
            mission = '/home/stephen/git/MAVProxyModules/ValidMission.txt'
            if not self.ci.DoCommand('solve validBatteryPartialModel 1 BatteryChecker.conforms'):
                print("Solve command failed.")
                return
        elif args[0] == 'invalid':
            if not self.ci.DoCommand('solve invalidBatteryPartialModel 1 BatteryChecker.conforms'):
                print("Solve command failed.")
                return
        elif args[0] == 'fixed':
            mission = '/home/stephen/git/MAVProxyModules/FixedMission.txt';
            if not self.ci.DoCommand('solve fixedBatteryPartialModel 1 BatteryChecker.conforms'):
                print("Solve command failed.")
                return

        output = self.sw.ToString()
        self.sw.GetStringBuilder().Clear()
        print(output)

        if not self.ci.DoCommand('extract 0 0 0'):
                print("Extract command failed.")
                return
            
        output = self.sw.ToString()
        self.sw.GetStringBuilder().Clear()

        if re.search("Model\s+not\s+solvable\.", output):
            print("Model returned not solvable. Stopping run.")
            return
        elif re.search("Solution\s+number", output):
            match = re.search("batteryCapacity\((\d+)\/(\d+)\)", output)
            if match != None:
                top = match.group(1)
                bot = match.group(2)

                calc = float(top)/float(bot)

                per = (calc/self.battery_cap)*100.0

                print("Calculated battery capacity: {:.2f} Joules".format(calc))
                print("Drone battery capacity: {:.2f} Joules".format(self.battery_cap))

                if calc < self.battery_cap:
                    print("Battery capacity sufficient. Loading waypoints...")
                    self.wp_module.cmd_wp(['load', mission])
                    self.wp_module.wp_add_landing()
                else:
                    print("Battery capacity exceeded. Stopping run.")
                    return
                
            match = re.search("rate\((\d+)\/(\d+)\)", output)
            if match != None:
                top = match.group(1)
                bot = match.group(2)

                calc = float(top)/float(bot)
                print("Rate: {:.2f} Joules".format(calc))

    def update_capacity(self):
        self.consumed_cap += self.rate*0.4497
    
    def print_capacity(self):
        print("Consumed battery capacity: {:.2f} Joules".format(self.consumed_cap))

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        if self.master.flightmode == 'AUTO' and self.battery_period.trigger():
            self.update_capacity()
        if  self.master.flightmode == 'AUTO' and self.print_period.trigger():
            self.print_capacity()

def init(mpstate):
    '''initialise module'''
    return BatteryDemoModule(mpstate)
