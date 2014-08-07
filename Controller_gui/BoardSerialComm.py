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
@file       BoardSerialComm.py
@author     Navin Bhaskar
@brief      Implements the serial communication interface
"""

from BoardComm import BoardComm
import serial,sys
import time, re, string
import time

class BoardSerialComm(BoardComm):
    
    """ Implements methods required for communication with board over 
    the serial port """
    
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        
        if type(port) != type(""):
            raise TypeError, "Type of port is invalid "
            
        if type(baudrate) != type(1):
            raise TypeError, "Type of baud is invalid "
        
        # Try to open the serial port 
        try:
            self.serialPort = serial.Serial(port)
        except IOError:
            raise IOError, "Could not open serial port: %s " %port 
        
        bytesize = 8
        parity = 'N'
        stopbits = 1
        self.serialPort.baudrate = baudrate
        self.serialPort.bytesize = bytesize
        self.serialPort.parity   = parity
        self.serialPort.stopbits = stopbits
        self.serialPort.timeout  = 2
        self.serialPort.XonXoff  = None
         

    
    def close(self):
        """ Closes the serial port """
        self.serialPort.close()
        
        
    def write(self, cmd):
        """ Writes the serial port """
        
        if (type(cmd) != type("")):
            try:
                cmd = str(cmd)
            except:
                raise TypeError, "Type of argument passed to write is invalid "
        
        self.serialPort.flushOutput()
        self.serialPort.writelines(cmd)
        self.serialPort.flushInput()
        if (cmd.find('\n') < 0):
            self.serialPort.write('\n')
        
        
        time.sleep(0.1)
        
    def read(self):
        """ Reads from the serial port and returns a tuple whose first
        elsment indicates whether any serial data was recived and 
        the second element consists of the result of the operation
        as written by the hardware module if the board had some value 
        to be returnde, it would be present as the third element"""
        portBuffer = ""
        returnval = False
        # 'OK' indicates the end of frame
        for i in range(0,500):           
            time.sleep(0.01)
            while (self.serialPort.inWaiting() > 0):
                temp = self.serialPort.read()
                portBuffer += temp
                
            if (re.search("OK",portBuffer)):
                returnval = True
                break
        res = portBuffer.strip("OK").replace("\r\n", '')
        return (res, returnval)
        
    def __del__(self):
        try:
            self.close()
        except:
            pass
        return
        
         
