#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import time
from threading import Thread
import script_header as sh
import argparse

#arg parser
parser=argparse.ArgumentParser()
parser.add_argument("config",help="config file")
parser.add_argument("-l","--logfile",help="potential logfile")
args=parser.parse_args()

#read configfile
config_devices = sh.read_testbeamDCS_config(args.config)

#create setting query
sh.show_testbeamDCS_device_list(config_devices)

#connection
devices = sh.connect_testbeamDCS_devices(config_devices)

#logfile
if args.logfile:
    checktxtfile = (args.logfile + ".txt")
    if os.path.isfile(checktxtfile):
        sys.exit("logfile " + args.logfile + " already exists!")
    fw = sh.new_txt_file(args.logfile)
    header = ["time"]
    d_names = []
    for i in config_devices:
        #d_names = d_names + ["|"]
        #d_names = d_names + i
        #d_names = d_names + ["|"]
        d_names.append("|")
        d_names.append(i[0])
        d_names.append(i[1])
        d_names.append("|")
    for i in devices:
        header = header + (i.output(show=False)[0])
    sh.write_line(fw,d_names)
    sh.write_line(fw,header)

cont = 1
cont2 = 1
def getKey(threadname):
    global cont
    global cont2
    cont = 1
    cont2 = 1
    while True:
        x = raw_input()
        if x == "q":
            cont = 0
            print("Quit")
            break
        elif x == "c":
            cont2 = 0
            #print("Change")
            break
        else:
            print("Nooooooo")

starttime = time.time()

while cont == 1:
    cont2 = 1
    threadKey = Thread( target=getKey, args=("Thread-1",) )
    threadKey.start()
    while cont == 1 and cont2 == 1:
        values = [str(time.time())]
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        timestamp = (time.time()-starttime) /60
        h,s = divmod(timestamp,1)
        #timestamp = time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())
        print(" \033[35m CONTROL CENTER \t " + "runtime: %.0f min %.0f s \033[0m"%(h,s*60))
        print("-----------------------------------------------------")
        for d in devices:
            h,v = d.output()
            values += v
            print("-----------------------------------------------------")
        print("press c (=CHANGE PARAMETER) or q (=QUIT) and ENTER")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("")
        if args.logfile:
            sh.write_line(fw,values)
        if cont == 1 and cont2 == 1:
            time.sleep(5)
    threadKey.join()
    if cont == 1:
        print("List of active Devices:")
        for i in range(len(config_devices)):
            print("%i: %s"%(i+1,config_devices[i][1]))
        x = raw_input("Choose the number of a Device:")
        try:
            x = int(x)
        except:
            x = 100
        if (x-1) in range(len(config_devices)):
            devices[int(x)-1].interaction()
        #print(d)

#print(threadKey.is_alive())
for d in devices:
    d.close()
if args.logfile:
    sh.close_txt_file(fw)
