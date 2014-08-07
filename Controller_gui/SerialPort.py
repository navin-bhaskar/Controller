#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

#       (c) Navin Bhaskar 2013
"""
@file       SerialPort.py
@author     Navin Bhaskar
@brief      Just a wrapper around pyserial
"""

import serial,sys
import time, re, string
""" This file implements functions required for commmunication with Arduino
over the serial port """

class SerialPort(object):
    """ This class initializes the serial port at 9600 baudrate. optinally,
       pass the comport number other wise, com 1 is taken as default """


    def __init__(self, port = 'COM1'):
        """Constructor for serial port"""
        if type(port) != type(""):
            raise TypeError, "I was expecting string but received %s" %type(port)

        try:
            self.serialPort = serial.Serial(port)
        except IOError:
            #print "***** could not  Open Serial Port %s******" %(port)
            #sys.exit(1)
            raise IOError, "Could not open serial port: %s " %port 
        port = 'COM6'
        baudrate = '9600'
        bytesize = '8'
        parity = 'N'
        stopbits = '1'
        self.serialPort.baudrate = int(baudrate)
        self.serialPort.bytesize = int(bytesize)
        self.serialPort.parity   = parity
        self.serialPort.stopbits = int(stopbits)
        self.serialPort.timeout  = 2
        self.serialPort.XonXoff  = None
        return


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# this is used to close the serial port

    def Close_Port(self):
        """ This method closes the serial port """
        self.serialPort.close()
        return

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# this is used to write to the port

    def Write_To_Port(self,command):
        """ This method reads what the Arduino has to say """
        #command.lstrip("\n")
        self.serialPort.flushOutput()
        #for i in range (0,len(command)):
         #   self.serialPort.write(command[i])
         #   time.sleep(1)
        self.serialPort.writelines(command)
        self.serialPort.flushInput()        # we don't want to read echoed charcters
        #self.serialPort.write("\n")         # new line
        self.serialPort.write("\r")
        time.sleep(0.1)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# this is used to read from the port

    def Read_From_Port(self):
        portBuffer = ""
        returnval = 0
        for i in range(0,500):           
            time.sleep(0.01)
            while (self.serialPort.inWaiting() > 0):
                temp = self.serialPort.read()
                #if (len(temp) >= 1):
                    #sys.stdout.write(temp)
                    #print "%s" %(string.rstrip(temp)),
                portBuffer += temp

            if (re.search("OK",portBuffer)):
                returnval = 1
                break
        res = portBuffer.strip("OK").replace("\r\n", '')
        return (res, returnval)

