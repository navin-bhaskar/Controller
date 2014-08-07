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
@file       ControllerException.py
@author     Navin Bhaskar
"""


"""
All the exceptions that might be encountered while using the TransLayer
object are listed here 
"""


# Let there be exceptions

class InvalidPinException(Exception):
    """ Raise this is the board responded with an "invalid pin" message 
    """
    pass 

class ResponseTimedOutException(Exception):
    """ To let the user know that board went into stealth mode  :p """
    pass 

class InvalidParameterException(Exception):
    """ Board says invalid parameter """
    pass 
    
