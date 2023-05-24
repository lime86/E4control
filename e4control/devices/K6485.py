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
        self.trm = '\n' ## K6485 message response terminator is LF and EOI (End or Identify)

    def initialize(self, iChannel='all'):
        self.reset()
        self.write(":INIT")

    def identify(self, iChannel="all"):
        return self.ask('*IDN?')

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
        return self.ask(":SENS:CURR:RANG:AUTO?")
        
    def setCurrentRange(self, sRange, iChannel=-1):
        self.write(":SENS:CURR:RANG {}".format(sRange))
    def getCurrentRange(self, iChannel=-1):
        return self.ask(":SENS:CURR:RANG:ULIM?")

    ## NPLC: Number of power line cycles;
    ## 1 PLC for 60Hz is 16.67msec (1/60) and 1 PLC for 50Hz (and 400Hz) is 20msec (1/50)
    ## default is 5 or 6, optimum is 1--10, range is 0.01--50/60

    def setNPLC(self, iChannel=-1, n=5):
        self.write(":SENS:CURR:NPLC {}".format(n))

    def setIntegrationRate(self, iChannel=-1, speed="slow"):
        n = 5
        if speed == "fast":
            n = 0.1
        elif speed == "med" or speed == "medium":
            n = 1
        elif speed == "slow":
            n = 5
        self.write(":SENS:CURR:NPLC {}".format(n))


    def getCurrent(self, iChannel=-1):
        try:
            sValue = self.ask("READ?").split("A")[0]
            return float(sValue.lower())
        except Exception as e:
            print(e)
            raise
        return None
        
    def getAutoZeroStatus(self, iChannel=-1):
        return self.ask(":SYST:AZER?")
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
        return self.ask(":SYST:ZCH:STAT?")
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
        return self.ask(":SYST:ZCOR?")
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
