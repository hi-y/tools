#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import *
import re
import time
import subprocess
import shlex
import argparse

def main(cmd_line, items, interval=1, outputformat="table"):
    i = ItemController(cmd_line, items, outputformat)
    if outputformat=="table":
        print i.header()
    i.continuous_output(interval)

class Item():
    """tuple including Label and Pattern

    Label  : String - Name of the item.
    Pattern: String - Describe target counter with regular expression. Target counter must be number.

    Option:
        diff: whether output incremental difference or itself.
        width: width of column. 
   """

    def __init__(self, label, pattern, diff=False, width=None):
        self.label = label
        self.pattern = pattern
        self.diff = diff
        self.initial_value = None
        self.value = None
        self.last_value = None
        if type(width) is int:
            self.width = max(len(self.label) + 2, width + 2, 10)
        else:
            self.width = max(len(self.label) + 2, 10)

    def output(self):
        if type(self.value) is int and type(self.last_value) is int:
            if self.diff == True:
                output = self.value - self.last_value
            else:
                output = self.value
        else:
            output = self.value
        return output

class ItemController():
    def __init__(self, cmd, items, outputformat="table"):
        self.cmd_line = cmd
        self.cmd_result = None
        self.cmd_lastupdate = None
        self.items = items
        self.outputformat = outputformat

    def run_cmd(self, initial=False):
        if initial:
            s = subprocess.Popen(shlex.split(self.cmd_line),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,)
            self.cmd_lastupdate = datetime.now()
            self.cmd_result = s.communicate()
            self.update_items()
            for item in self.items:
                item.initial_value = item.value
        else:
            s = subprocess.Popen(shlex.split(self.cmd_line),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,)
            self.cmd_lastupdate = datetime.now()
            self.cmd_result = s.communicate()
            self.update_items()
    
    def update_items(self,):
        for item in self.items:
            item.last_value = item.value
            for line in self.cmd_result:
                r = re.compile(item.pattern).search(line)
                if r:
                    if r.group(1).isdigit() == True:
                        item.value = int(r.group(1))
                    else:
                        item.value = str(r.group(1))

    def header(self,):
        header_line = 'DATE'.ljust(11,' ') + 'TIME'.ljust(15,' ')
        for item in self.items:
            header_line = header_line + item.label.rjust(item.width, ' ')
        top = '=' * len(header_line) + "\n" + self.cmd_line + "\n" + '=' * len(header_line) 
        btm = '-' * len(header_line)
        header_line = top + "\n"\
            + header_line + "\n"\
            + btm
        return header_line            

    def edited_result_line(self, initial=False):
        """
        To do: need to support "csv,tsv" format.
        """
        if self.outputformat == "table":
            if initial:
                line = str(self.cmd_lastupdate)
                for item in self.items:
                    if item.diff:
                        line += str(None).rjust(item.width, ' ')
                    else:
                        line += str(item.output()).rjust(item.width, ' ')
                return line
            else:
                line = str(self.cmd_lastupdate)
                for item in self.items:
                    line += str(item.output()).rjust(item.width, ' ')
                return line
        elif self.outputformat == "json":
            if initial:
                line = '{"timestamp" : "' + str(self.cmd_lastupdate.strftime("%Y-%m-%dT%H:%M:%S%z")) + '"'
                for item in self.items:
                    if item.diff:
                        line += ', "' + item.label + '" : null'
                    elif item.output() is None:
                        line += ', "' + item.label + '" : null'
                    else:
                        if type(item.output())==int:
                            line += ', "' + item.label + '" : ' + str(item.output())
                        elif type(item.output())==str:
                            if item.output().lower()=="true" or "false":
                                line += ', "' + item.label + '" : ' + str(item.output())
                            else:
                                line += ', "' + item.label + '" : "' + str(item.output()) + '"'
                        else:
                            line += ', "' + item.label + '" : "' + str(item.output()) + '"'
                line += '}'
                return line
            else:
                line = '{"timestamp" : "' + self.cmd_lastupdate.isoformat() + '"'
                for item in self.items:
                    if type(item.output()) is int:
                        line += ', "' + item.label + '" : ' + str(item.output())
                    elif type(item.output()) is str:
                        if item.output().lower()=="true" or "false":
                            line += ', "' + item.label + '" : ' + str(item.output())
                        else:
                            line += ', "' + item.label + '" : "' + str(item.output()) + '"'
                    elif type(item.output()) is None:
                        line += ', "' + item.label + '" : null'
                    else:
                        line += ', "' + item.label + '" : "' + str(item.output()) + '"'
                line += '}'
                return line
        elif self.outputformat == "csv" or "tsv":
            return "not implemented"
        
    def continuous_output(self, interval=1, count=None):
        """
        To do: need to implement "count" feature.
        """
        cmd_firstupdate = datetime.now()
        self.run_cmd(initial=True)
        print self.edited_result_line(initial=True)
        try:
            elapse = 0
            while True:
                if interval > elapse:
                    time.sleep(interval - elapse)
                t = time.time()
                self.run_cmd()
                print self.edited_result_line()
                elapse = time.time() - t
        except KeyboardInterrupt:
            if self.outputformat == "table":
                elapsed_time = self.cmd_lastupdate - cmd_firstupdate
                print "\n" + '--- ' + self.cmd_line + ' statistics ---'
                print 'time ' + str(elapsed_time)
                for item in self.items:
                    if type(item.value) is int and type(item.initial_value) is int:
                        print item.label.ljust(item.width, ' ') + ': ' + str(item.value - item.initial_value)
            

##########################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='repeatedly output command result')
    parser.add_argument("ofp", help="Openflow port. ex) OFP22")
    parser.add_argument("-i", "--interval", type=int, default=1,
                        help="command execution interval")
    parser.add_argument("-a", "--allitem", action="store_true",
                        help="output all items")
                        
    args = parser.parse_args()

    cmd_line = 'ifconfig ' + args.ofp 

    if args.allitem:
        print_items = [
            Item('RxPackets_statistic', 'RX\spackets:(\d+)', diff=False),
            Item('RxPackets', 'RX\spackets:(\d+)', diff=True),
            Item('TxPackets', 'TX\spackets:(\d+)', diff=True),
            Item('NoPacket', 'DD\spets:(\d+)', diff=True),
        ]
    else:
        print_items = [
            Item('RxPackets_statistic', 'RX\spackets:(\d+)', diff=False),
            Item('RxPackets', 'RX\spackets:(\d+)', diff=True),
            Item('TxPackets', 'TX\spackets:(\d+)', diff=True),
            Item('NoPacket', 'DD\spets:(\d+)', diff=True),
        ]

    main(cmd_line, print_items, args.interval)
