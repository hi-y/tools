#!/usr/bin/python
# -*- coding: utf-8 -*-
import statsmonitor
import argparse

def main(cmd_line, items, interval=1):
    i = statsmonitor.ItemController(cmd_line, items)
    print i.header()
    i.continuous_output(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='repeatedly output command result')
    parser.add_argument("interface", help="interface ex) eth0")
    parser.add_argument("-i", "--interval", type=int, default=1,
                        help="command execution interval")
    parser.add_argument("-a", "--allitem", action="store_true",
                        help="output all items")

    args = parser.parse_args()

    cmd_line = 'ifconfig ' + args.interface

    """
    $ ifconfig eth0
    eth0      Link encap:Ethernet  HWaddr 08:00:27:88:0c:a6
              inet addr:10.0.2.15  Bcast:10.0.2.255  Mask:255.255.255.0
              inet6 addr: fe80::a00:27ff:fe88:ca6/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:27663 errors:0 dropped:0 overruns:0 frame:0
              TX packets:13928 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:21883121 (21.8 MB)  TX bytes:911816 (911.8 KB)
    """

    if args.allitem:
        print_items = [
            statsmonitor.Item('RxPackets', 'RX\spackets:(\d+)\serrors:\d+\sdropped:\d+\soverruns:\d+\sframe:\d+', diff=True),
            statsmonitor.Item('RxErrors', 'RX\spackets:\d+\serrors:(\d+)\sdropped:\d+\soverruns:\d+\sframe:\d+', diff=True),
            statsmonitor.Item('RxDropped', 'RX\spackets:\d+\serrors:\d+\sdropped:(\d+)\soverruns:\d+\sframe:\d+', diff=True),
            statsmonitor.Item('RxOverruns', 'RX\spackets:\d+\serrors:\d+\sdropped:\d+\soverruns:(\d+)\sframe:\d+', diff=True),
            statsmonitor.Item('RxFrame', 'RX\spackets:\d+\serrors:\d+\sdropped:\d+\soverruns:\d+\sframe:(\d+)', diff=True),
            statsmonitor.Item('TxPackets', 'TX\spackets:(\d+)\serrors:\d+\sdropped:\d+\soverruns:\d+\scarrier:\d+', diff=True),
            statsmonitor.Item('TxErrors', 'TX\spackets:\d+\serrors:(\d+)\sdropped:\d+\soverruns:\d+\scarrier:\d+', diff=True),
            statsmonitor.Item('TxDropped', 'TX\spackets:\d+\serrors:\d+\sdropped:(\d+)\soverruns:\d+\scarrier:\d+', diff=True),
            statsmonitor.Item('TxOverruns', 'TX\spackets:\d+\serrors:\d+\sdropped:\d+\soverruns:(\d+)\scarrier:\d+', diff=True),
            statsmonitor.Item('TxFrame', 'TX\spackets:\d+\serrors:\d+\sdropped:\d+\soverruns:\d+\scarrier:(\d+)', diff=True),
        ]
    else:
        print_items = [
            statsmonitor.Item('RxPackets', 'RX\spackets:(\d+)\serrors:\d+\sdropped:\d+\soverruns:\d+\sframe:\d+', diff=True),
            statsmonitor.Item('RxErrors', 'RX\spackets:\d+\serrors:(\d+)\sdropped:\d+\soverruns:\d+\sframe:\d+', diff=True),
            statsmonitor.Item('RxDropped', 'RX\spackets:\d+\serrors:\d+\sdropped:(\d+)\soverruns:\d+\sframe:\d+', diff=True),
            statsmonitor.Item('TxPackets', 'TX\spackets:(\d+)\serrors:\d+\sdropped:\d+\soverruns:\d+\scarrier:\d+', diff=True),
            statsmonitor.Item('TxErrors', 'TX\spackets:\d+\serrors:(\d+)\sdropped:\d+\soverruns:\d+\scarrier:\d+', diff=True),
            statsmonitor.Item('TxDropped', 'TX\spackets:\d+\serrors:\d+\sdropped:(\d+)\soverruns:\d+\scarrier:\d+', diff=True),
        ]

    main(cmd_line, print_items, args.interval)
