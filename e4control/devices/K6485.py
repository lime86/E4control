# -*- coding: utf-8 -*-

from time import sleep

from .device import Device
import warnings
import inspect


class K6485(Device):
    rampSpeed_step = 10
    rampSpeed_delay = 1  # s

    def __init__(self, connection_type, host, port):
        super(K6485, self).__init__(
            connection_type=connection_type, host=host, port=port)
        self.trm = '\r\n'

    def initialize(self, iChannel='all'):
        self.reset()
        self.write(":INIT")
        # self.ask('*IDN?')
        # print("Initialize", self.ask('*IDN?'))

    def convert_iChannel(self, iChannel):
        one = [1, '1', 'one']
        two = [2, '2', 'two']
        if iChannel in one:
            iChannel = 'a'
        elif iChannel in two:
            iChannel = 'b'
        return iChannel

    def setAutoRangeOn(self, iChannel=-1):
        self.write(":SENS:CURR:RANG:AUTO ON")
    def setAutoRangeOff(self, iChannel=-1):
        self.write(":SENS:CURR:RANG:AUTO OFF")
        
    def setAutoRange(self, opt=0, iChannel=-1):
        if opt:
            setCurrentAutoRangeOn()
        else:
            setCurrentAutoRangeOff()
    def getAutoRangeStatus(self, iChannel=-1):
        self.ask(":SENS:CURR:RANG:AUTO?")
        
    def setCurrentRange(self, sRange, iChannel=-1):
        self.write(":SENS:CURR:RANG {}".format(sRange))
        
    def getCurrentRange(self, iChannel=-1):
        self.ask(":SENS:CURR:RANG:ULIM?")

    def getCurrent(self, iChannel=-1):
        sValue = self.ask("READ?").split("A")[0]
        print("getCurrent", sValue)
        return float(sValue.lower())
        
        
    def getAutoZeroStatus(self, iChannel=-1):
        self.ask(":SYST:AZER?")
    def setAutoZeroOn(self, iChannel=-1):
        self.write(":SYST:AZER:STAT ON")
    def setAutoZeroOff(self, iChannel=-1):
        self.write(":SYST:AZER:STAT OFF")
    def setAutoZero(self, opt=0, iChannel=-1):
        if opt:
            setAutoZeroOn()
        else:
            setAutoZeroOff()
            
    def getZeroCheckStatus(self, iChannel=-1):
        self.ask(":SYST:ZCH:STAT?")
    def setZeroCheckOn(self, iChannel=-1):
        self.write(":SYST:ZCH:STAT ON")
    def setZeroCheckOff(self, iChannel=-1):
        self.write(":SYST:ZCH:STAT OFF")
    def setZeroCheck(self, opt=0, iChannel=-1):
        if opt:
            setZeroCheckOn()
        else:
            setZeroCheckOff()
            
    def getZeroCorrectStatus(self, iChannel=-1):
        self.ask(":SYST:ZCOR?")
    def setCheckOn(self, iChannel=-1):
        self.write(":SYST:ZCOR:STAT ON")
    def setCheckOff(self, iChannel=-1):
        self.write(":SYST:ZCOR:STAT OFF")
    def setCheck(self, opt=0, iChannel=-1):
        if opt:
            setZeroCorrectOn()
        else:
            setZeroCorrectOff()

    def resetTS(self):
        try:
            self.write(":SYST:TIME:RES")
        except Exception as e:
            print(inspect.current_frame(), e)
        
    def reset(self):
        self.write("*RST")
    
    def selfTest(self):
        self.ask("*TST?")
