#!/bin/env python

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
@file       TransLayer.py
@author     Navin Bhaskar
@brief      Trans layer contains object called TransLayer which has some methods
            that frame the message and also have some methods that can query
            data from arduino.
"""

from BoardSerialComm import BoardSerialComm
import ControllerExceptions
class TransLayer:
  """ This class implements the transfer layer for usage with the Ardiuno board
  this class contains methods which frame and send the dat to the arduino """
  def __init__(self, comport='/dev/ttyUSB0', ref=5.0, res=1024):
    """ This constructor initializes this class. Mainly, it opens up a serial 
    port for the communication to happen. If for some reasons, the port could 
    not be opened then this class will rise an IOError """
    try:
      self.comm = BoardSerialComm(comport)
    except IOError:
      raise IOError, "Could not open serial port %s " %comport
    
    # now lets have the flags defined
    self.START_FLAG = 'S'             # this flag has been set as start of frame
    self.PIN_OP     = 'P'             # pin operations flag
    self.ANA_OP     = 'A'             # analog out flag
    self.ANA_IP     = 'I'             # analog read flag
    self.PIN_IP     = 'R'             # read a digital pin
    self.REF_VLTG   =  ref            # reference voltage
    self.RES        =  res            # resolution
    
    # String messages that can be possibly returned by the board 
    self.exceptions = {"ERROR": (IOError, "Unknown error occured "), 
                    "Invalid pin" : (ControllerExceptions.InvalidPinException, "The pin number specified was invalid "),
                    "Invalid arguments" : (ControllerExceptions.InvalidParameterException, "Invalid argument was passed ")
                    }
  def __make_sense_of_the_data__(self, data):
      """ Just a helper that accepts the string returned from the board
      and checks the string and if the operation was succeessful and
      if there were any argument returned by the board, it is returned
      if no argument was received, empty string is returned.
      On the other hand if there were any errors, appropriate 
      exceptions are raised.
      """
      retVal=""     # will hold value returned by the board, if any.
      if data.find("\n") > 0:
          # If we are here then it means that we need to extract the 
          # value returned from the board 
          retVal = data.split("\n")[0]
          data = data.split("\n")[1]
          
      if data.find("SUCCESS") >= 0:
          return retVal
    
      if self.exceptions.has_key(data):
          # else, this is got to be some exception
          raise self.exceptions[data][0], self.exceptions[data][1]
      else:
          raise IOError, "The data received seems to be invalid "


  def SetPinData(self, pin, state):
    """ This function sets or clears a given pin. 
    pin   pin to be set or cleared
    state boolean True-set False-reset """
    
    if type(pin) != type(1) :
      raise TypeError, "TransLayer.SendPinData requires pin to be integer but \
        %s was passed" %(type(pin))
    
    if type(state) != type(1) :
      raise TypeError, "TransLayer.SendPinData requires state to be int "
    
    # let's construct the packet
    if state == 0:
      on = 0
    else :
      on = 1
      
    packet = self.START_FLAG + self.PIN_OP + str(pin) + str(on)
    print "The packet we are sending out is %s " %packet
    
    # send the packet over the serial port
    self.comm.write(packet)
    readTup = self.comm.read()
    print readTup
    if readTup[1] == True:
        return (self.__make_sense_of_the_data__(readTup[0]))
    else:
        raise ControllerExceptions.ResponseTimedOutException, "The board did not respond, we timed out "


  def SetAnalogVal(self, pin, val):
    """ Function to ask Arduino to output analog volatges(PWM) """
    
    if (type(pin) != type(1)) :
      raise TypeError, "SetAnalogValue requires pin number to be integer"
    if (type(val) != type(1)) :
      raise TypeError, "SetAnalogValue requires value to be of integer type "
    
    temp = (val << 8)| pin ;
    
    packet =self.START_FLAG + self.ANA_OP + str(temp)
    
    print "The packet we are sending out is %s " %packet
    self.comm.write(packet)
    readTup = self.comm.read()
    print readTup
    if readTup[1] == True:
        return (self.__make_sense_of_the_data__(readTup[0]))
    else:
        raise ControllerExceptions.ResponseTimedOutException, "The board did not respond, we timed out "
        
    
  def ReadAnalogVal(self, pin):
    """ This fucntion raeds the analog volatge at the given pin.
    This method returns a tuple whose first element is True if the transaction 
    was successfull and the second value is actual read value. If transaction
    was not successfull then this method returns False as first tuple element 
    """
    
    if (type(pin) != type(1)):
      raise TypeError, "Read analog value was expecting integer type argument"
    
    packet = self.START_FLAG + self.ANA_IP+str(pin)
    print "The packet we are sending out is %s " %packet
    self.comm.write(packet)
    val = self.comm.read()
    print val
    if val[1] == True:
      digi_val = self.__make_sense_of_the_data__(val[0])
      if (digi_val == ""):
          raise IOError, "No value received from the board "
      try:
        ana_val = float(self.REF_VLTG/(self.RES-1))* int(digi_val)
      except:
        raise IOError, "The board did not respond with an integer number "
      ana_val = str(ana_val)
      return ana_val
    else :
      raise ControllerExceptions.ResponseTimedOutException, "The board did not respond, we timed out "
    
  def ReadPin(self, pin):
    """ This method reads digital value at a given pin.
    This method returns a tuple whose first element indicates if the transaction
    was successfull. If successful the first element would be True else False.
    If the first element is true then the second element would be the value read
    """
    
    if (type(pin) != type(1)):
      raise TypeError, "This method(ReadPin) expects pin to be of integer type "
    packet = self.START_FLAG + self.PIN_IP+str(pin)
    
    print "The packet we are sending out is %s " %packet
    self.comm.write(packet)
    readTup = self.comm.read()    
    print readTup 
    if readTup[1] == True:
        digiVal = self.__make_sense_of_the_data__(readTup[0])
        if (digiVal == ""):
            raise IOError, "The board did not respond with the message in expected format "
        # Check if this is a numerical value 
        try:
            val = int(digiVal)
        except:
            raise IOError, "The board did not respond with an integer number "
        return digiVal
    else:
        raise ControllerExceptions.ResponseTimedOutException, "The board did not respond, we timed out "
        

  def Stop(self): 
    self.comm.close()
    
  
