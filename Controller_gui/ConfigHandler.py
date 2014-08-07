#!/usr/bin/python

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
@file       ConfigHandler.py
@author     Navin Bhaskar
"""

"""
Reads an configuration file and maintains internal data structure that
the appliactaion can query to get info on pins available, the data that
has to be sent to the hardware module and similar othe information.

"""import ConfigParser
import os
import re

class ConfigHandler:
    
    
    def __loadDictionary__(self, dic, pin_info):
        """ Loads the internal dictionaries with the pin name and their
        values """
        for pin in pin_info:
            if (pin[1] != ""):
                dic[pin[0]] = pin[1]


    def __init__(self, configFile):
        """ This is the constructor that reads the config file and fills
        up the required data structures """
        config = ConfigParser.SafeConfigParser()
        
        if os.path.exists(configFile) == False:
            raise IOError, "The file %s does not exist " %configFile
            
        # Load the config file
        try:
            config.read(configFile)
        except ConfigParser.ParsingError:
            raise TypeError, "The file %s has invalid syntax(s) " %configFile
        
        
        self.digiPins = {}
        self.anaInPins = {}
        self.anaOutPins = {}
        self.board = ""
        self.vref = ""
        self.res = ""
        self.AoutMax = ""
        
    
        if config.has_section("Digital") == True:
            pin_info = config.items("Digital")
            self.__loadDictionary__(self.digiPins, pin_info)
            
        if config.has_section("AnIn"):
            pin_info = config.items("AnIn")
            self.__loadDictionary__(self.anaInPins, pin_info)
            
        if config.has_section("AnOut"):
            pin_info = config.items("AnOut")
            self.__loadDictionary__(self.anaOutPins, pin_info)
            
        if config.has_section("Settings"):
            settings = config.items("Settings")
            for setting in settings:
                if (setting[0] == "board"):
                    self.board = setting[1]
                elif (setting[0] == "vref"):
                    self.vref = setting[1]
                elif (setting[0] == "res"):
                    self.res = setting[1]
                elif (setting[0] == "aoutmax"):
                    self.AoutMax = setting[1]
                    
                    
           
    
    def __cmp__(self, a, b):
        """ comapers two alpha numeric string.
        This will be used by sort() method. The method used to compare
        two string is that the first numeric char in the string is 
        considered for sorting. If there is no numeral in the string,
        then it is considered as zero """
        temp1 = re.findall(r'\d+', a)
        temp2 = re.findall(r'\d+', b)
        name1 = re.split(r'[0-9]', a)
        name2 = re.split(r'[0-9]', b)
        if name1 == name2:
            if len(temp1) > 0 and len(temp2) > 0:
                return (int(temp1[0]) - int(temp2[0]))
            else:
                return (int(temp2[0]) - int(temp1[0]))
        else:
            return len(name1) - len(name2)
        
    def getDigiPinNames(self):
        """ Lists all the Digital pins, sorted """
        temp = self.digiPins.keys()
        temp.sort(cmp=self.__cmp__)
        return temp
        
    def getAnaInPinNames(self):
        """ Returns list of sorted analog input pins """
        temp = self.anaInPins.keys()
        temp.sort(cmp=self.__cmp__)
        return temp
        
    def getAnaOutPinNames(self):
        """ Returns a list of sorted analog output pins """
        temp = self.anaOutPins.keys()
        temp.sort(cmp=self.__cmp__)
        return temp
    
    def getDigiPinValue(self, pin_name):
        """ Returns the value associated with the digital pin name """
        try:
            return int(self.digiPins[pin_name])
        except KeyError:
            raise ValueError, "Invalid Digital pin name"
            
    def getAnaOutPinValue(self, pin_name):
        """ Returns the value associated with the analog out pin"""
        try:
            return int(self.anaOutPins[pin_name])
        except KeyError:
            raise ValueError, "Invalid analog out pin"
            
    def getAnaInPinValue(self, pin_name):
        """ Returns the value associated with the analog in pin"""
        try:
            return int(self.anaInPins[pin_name])
        except KeyError:
            raise ValueError, "Invalid analog in pin "
    
            
    def getBoard(self):
        """ Retruns the name of the board """
        return self.board
        
    def getVref(self):
        """ Retruns the reference voltage """
        try:
            temp = float(self.vref.replace(" ", ''))
        except ValueError:
            temp = 5.0
        return (temp/1.0)
        
    def getRes(self):
        """ Returns the resolution used by the MCU for ADC"""
        try:
            temp = int(self.res)
        except ValueError:
            temp = 1024
            
        return temp
        
    def getAoutMax(self):
        """ Returns the maximum value that can be sent to the DAC/PWM
        module """
        
        try:
            temp = int(self.AoutMax)
        except ValueError:
            temp = 255
            
        return temp

if __name__ == "__main__":
    samp = ConfigHandler("cfg/mbed.cfg")
    print "Digital pins :", 
    print samp.getDigiPinNames()
    print "Board name: ",
    print samp.getBoard()
    print "Refrence voltage: ",
    print samp.getVref()
    print "Resolution: ",
    print samp.getRes()
    print "Value of p1 ",
    try:
        print samp.getDigiPinValue("p1")
    except ValueError, e:
        print e
    
    #-ve test
    print "Value of pp",
    
    try:
        print samp.getDigiPinValue("pp")
    except ValueError, e:
        print "[ERROR] " + str(e)
    
    print "Maximum analog out value ", samp.getAoutMax()
    print "Value of analog input pin p0 ", samp.getAnaInPinValue('p0')
    print "VAlue of analog output pin p18 ", samp.getAnaOutPinValue('p18')
    print "Value of analog output pin p1",
    try: 
        samp.getAnaOutPinValue('p1')
    except ValueError, e:
        print "[ERROR] " + str(e)
    
    
    
        
        

