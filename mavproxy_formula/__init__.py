#!/usr/bin/env python
'''formula command'''

from MAVProxy.modules.lib import mp_module

import os
from pythonnet import load
load("coreclr")
import clr
clr.AddReference(os.path.abspath('./CommandLine/CommandLine.dll'))

from Microsoft.Formula.CommandLine import CommandInterface, CommandLineProgram
from System.IO import StringWriter
from System import Console  

class FormulaModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(FormulaModule, self).__init__(mpstate, "formula", "formula command")
        self.add_command('formula', self.cmd_formula, "run formula",
                         ["<load|solve|extract>"])
        self.cmd_list = ['load', 'solve', 'extract']
        self.sw = StringWriter()
        Console.SetOut(self.sw)
        Console.SetError(self.sw)

        sink = CommandLineProgram.ConsoleSink()
        chooser = CommandLineProgram.ConsoleChooser()
        self.ci = CommandInterface(sink, chooser)

        if not self.ci.DoCommand("wait on"):
            print("Wait on command failed.")
        
    def cmd_formula(self, args):
        if len(args) < 2 and not args[0] in self.cmd_list:
            return
        
        if not self.ci.DoCommand(args[0] + " " + args[1]):
            print(args[0] + " command failed.")
            
        output = self.sw.ToString()
        self.sw.GetStringBuilder().Clear()
        return output

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        if mtype == "BATTERY_STATUS":
            print(m.BATTERY_STATUS.battery_remaining)

def init(mpstate):
    '''initialise module'''
    return FormulaModule(mpstate)
