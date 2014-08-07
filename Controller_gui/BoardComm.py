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
@file       BoardComm.py
@author     Navin Bhaskar
@brief      Implements the abstract class for communication with the 
            board 
"""



class BoardComm:
    """ Implements the abstarct class to be used for communication 
    with the hardware module using """
    def __init__(self):
        """ The constructor """
        pass 
        
    def write(self, data):
        """ To send the commands """
        raise NotImplementedError, "Write method is not implemented "
        
    def read(self, data):
        """ To recived the repsonse """
        raise NotImplementedError, "Read method is not implemneted "
        
    def close(self):
        """ Close the communication channel """
        raise NotImplementedError, "Close method is not implemented "

