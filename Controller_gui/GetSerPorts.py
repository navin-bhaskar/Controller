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
@file       GetSerPorts.py
@author     Navin Bhaskar
@brief      Lists out the serial ports that are available on the 
            system. Tested on Linux(Ubuntu, Open suse) and win env.
            Only virtual com ports (serial port emulation by USB devs)
            are supported only those device names that start with
            ttyUSB are listed. Change 'port_name' to suit 
            your needs.
"""

import os

class GetSerPorts:
	""" This class tries to scan all the ports and lists them """
	def __init__(self):
		""" Initializer, determines the os and tries to select a prefix name 
		for serial port """
		if os.name == 'nt':
			self.port_name = 'COM'
			self.port_name1 = ''         # Secondary port name 
			self.offset = 1
		elif os.name == 'posix':
			self.port_name = '/dev/ttyUSB'
			self.port_name1 = '/dev/ttyACM'   # Secondary port name 
			self.offset = 0
		else:
			self.port_name = ''
			self.offset = 0
		
	
	def get_ports(self):
		""" This method returns a list of all the available serial ports """
		ports  = []
		import serial
		
		for i in range(0, 70):
			try:
				if self.port_name == 'COM':
					ser = serial.Serial(i)
					ports.append(self.port_name + str(i+self.offset))
					ser.close()
				elif self.port_name == '/dev/ttyUSB':
					ser = serial.Serial(self.port_name + str(i))
					ports.append(self.port_name + str(i+self.offset))	
			except serial.SerialException:
				pass
				
			if self.port_name == '/dev/ttyUSB':
			# Try to open by the other name
				try:
					ser = serial.Serial(self.port_name1 + str(i))
					ports.append(self.port_name1 + str(i+self.offset))
				except serial.SerialException:
					pass
		return ports
		

if __name__ == "__main__":
	ports = GetSerPorts()
	print ports.get_ports()
