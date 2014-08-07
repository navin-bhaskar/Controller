# -*- coding: iso-8859-1 -*-
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
@brief      Implements the controller frame
"""

# Don't modify comment

import wx
import wx.gizmos
#[inc]add your include files here
from TransLayer import TransLayer
import ControllerExceptions
import sys
from ConfigHandler import ConfigHandler
#[inc]end your include

class ControllerFrame(wx.Frame):
    def __init__(self,parent,conf_file='conf.txt',id = -1,title = '',pos = wx.Point(0,0),size = wx.Size(530,520),style = wx.DEFAULT_DIALOG_STYLE,name = 'dialogBox'):
        #pre=wx.PreDialog()
        self.OnPreCreate()

        try:
            self.conf = ConfigHandler(conf_file)
        except IOError:
            wx.MessageBox("Could not find the config file, %s" %conf_file)
            self.__del__()
            sys.exit(1)

        board = self.conf.getBoard()
        wx.Frame.__init__(self, parent, id,title + ' ' + board,pos,size,wx.CAPTION|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.MINIMIZE_BOX,name)
        self.statusBar = self.CreateStatusBar()
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        self.initBefore()
        self.VwXinit()
        self.initAfter()

    def __del__(self):
        self.Ddel()
        wx.Exit()
        return


    def VwXinit(self):
        self.main_pannel = wx.Panel(self,-1,wx.Point(-5,0),wx.Size(609,493))
        self.DigiOpPin = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,100),wx.Size(500,70))
        self.DigiOpPin.SetLabel('Digital output pins')
        digi_pins = self.conf.getDigiPinNames()
        self.cmbDigiOpPins = wx.ComboBox(self.main_pannel,-1,"",wx.Point(160,125),wx.Size(80,25),digi_pins,wx.CB_READONLY)
        self.cmbDigiOpPins.SetLabel("Select Pin")
        self.stDigitalOut = wx.StaticText(self.main_pannel,-1,"",wx.Point(25,125),wx.Size(125,20),wx.ST_NO_AUTORESIZE)
        self.stDigitalOut.SetLabel("Select a Digital Pin")
        self.btDigiOutSet = wx.Button(self.main_pannel,-1,"",wx.Point(420,120),wx.Size(85,30))
        self.btDigiOutSet.SetLabel("Set")
        self.Bind(wx.EVT_BUTTON,self.OnDigiSet,self.btDigiOutSet)
        self.stDigiOpSelState = wx.StaticText(self.main_pannel,-1,"",wx.Point(250,125),wx.Size(80,20),wx.ST_NO_AUTORESIZE)
        self.stDigiOpSelState.SetLabel("Select State")
        self.cmbHighLow = wx.ComboBox(self.main_pannel,-1,"",wx.Point(340,125),wx.Size(65,25),[r'High',r'Low'],wx.CB_READONLY)
        self.cmbHighLow.SetLabel("State")
        self.sbDigigInpPins = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,190),wx.Size(500,76))
        self.sbDigigInpPins.SetLabel('Digital Input Pins')
        self.stDigiOutPin = wx.StaticText(self.main_pannel,-1,"",wx.Point(25,215),wx.Size(125,20),wx.ST_NO_AUTORESIZE)
        self.stDigiOutPin.SetLabel("Select a Digital Pin")
        self.cmbSerPort = wx.ComboBox(self.main_pannel,-1,"",wx.Point(160,35),wx.Size(120,25),[],wx.CB_READONLY)
        self.cmbSerPort.SetLabel("Select Pin")
        self.btOpenPrt = wx.Button(self.main_pannel,-1,"",wx.Point(285,30),wx.Size(85,30))
        self.btOpenPrt.SetLabel("Open")
        self.Bind(wx.EVT_BUTTON,self.OnOpenPrt,self.btOpenPrt)
        self.ledPinState = wx.gizmos.LEDNumberCtrl(self.main_pannel,-1,wx.Point(350,215),wx.Size(70,40))
        self.sbAnalogOut = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,285),wx.Size(500,70))
        self.sbAnalogOut.SetLabel('Analog Out')
        self.stAnIn = wx.StaticText(self.main_pannel,-1,"",wx.Point(20,400),wx.Size(140,20),wx.ST_NO_AUTORESIZE)
        self.stAnIn.SetLabel("Select an Analog pin")
        self.cmbAnalogOut = wx.ComboBox(self.main_pannel,-1,"",wx.Point(160,310),wx.Size(80,25),self.conf.getAnaOutPinNames(),wx.CB_READONLY)
        self.cmbAnalogOut.SetLabel("Select pin")
        self.txAnalogOut = wx.TextCtrl(self.main_pannel,-1,"",wx.Point(345,310),wx.Size(60,25))
        self.stAnoutVal = wx.StaticText(self.main_pannel,-1,"",wx.Point(250,310),wx.Size(100,20),wx.ST_NO_AUTORESIZE)
        self.stAnoutVal.SetLabel("Enter a value")
        self.btAnalogOut = wx.Button(self.main_pannel,-1,"",wx.Point(420,310),wx.Size(85,30))
        self.btAnalogOut.SetLabel("Set")
        self.Bind(wx.EVT_BUTTON,self.OnAnaSet,self.btAnalogOut)
        self.sbAnalogIn = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,375),wx.Size(500,80))
        self.sbAnalogIn.SetLabel('Analog In')
        self.stSelAnOut = wx.StaticText(self.main_pannel,-1,"",wx.Point(20,310),wx.Size(140,20),wx.ST_NO_AUTORESIZE)
        self.stSelAnOut.SetLabel("Select an Analog pin")
        self.cmbAnalogIn = wx.ComboBox(self.main_pannel,-1,"",wx.Point(160,400),wx.Size(80,25),self.conf.getAnaInPinNames(),wx.CB_READONLY)
        self.cmbAnalogIn.SetLabel("Select pin")
        self.btAnalogRead = wx.Button(self.main_pannel,-1,"",wx.Point(250,400),wx.Size(85,30))
        self.btAnalogRead.SetLabel("Read")
        self.Bind(wx.EVT_BUTTON,self.OnAnaRead,self.btAnalogRead)
        self.ledAnalogRead = wx.gizmos.LEDNumberCtrl(self.main_pannel,-1,wx.Point(350,400),wx.Size(75,40))
        self.SerPort = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,10),wx.Size(500,71))
        self.SerPort.SetLabel('Serial port selection')
        self.stSelPort = wx.StaticText(self.main_pannel,-1,"",wx.Point(20,35),wx.Size(140,20),wx.ST_NO_AUTORESIZE)
        self.stSelPort.SetLabel("Select a serial port")
        self.cmbDigiRead = wx.ComboBox(self.main_pannel,-1,"",wx.Point(160,215),wx.Size(80,25),digi_pins,wx.CB_READONLY)
        self.cmbDigiRead.SetLabel("Select Pin")
        self.btClosePrt = wx.Button(self.main_pannel,-1,"",wx.Point(385,30),wx.Size(85,30))
        self.btClosePrt.SetLabel("Close")
        self.Bind(wx.EVT_BUTTON,self.OnClosePrt,self.btClosePrt)
        self.btDigiRead = wx.Button(self.main_pannel,-1,"",wx.Point(250,215),wx.Size(85,30))
        self.btDigiRead.SetLabel("Read")
        self.Bind(wx.EVT_BUTTON,self.OnDigiRead,self.btDigiRead)
        self.Refresh()

        return
    def VwXDelComp(self):
        return

#[win]add your code here

    def OnOpenPrt(self,event): #init function
        #[51e]Code event VwX...Don't modify[51e]#
        #add your code here

        ser_prt = self.cmbSerPort.GetValue().encode('ASCII')
        if (ser_prt == ""):
            return
        # lets try and create a TransLayer object
        try:
          self.ArdCtrl = TransLayer(ser_prt, self.conf.getVref(), self.conf.getRes())
          print self.conf.getVref();
          self.btOpenPrt.Enable(False)
          self.btClosePrt.Enable(True)
          self.btDigiOutSet.Enable(True)
          self.btDigiRead.Enable(True)
          self.btAnalogOut.Enable(True)
          self.btAnalogRead.Enable(True)
        except IOError, error:
          err = str(error)
          wx.MessageBox(err+"\n Application exiting...")
          sys.exit(1)

        return #end function

    def OnClosePrt(self,event): #init function
        #[521]Code event VwX...Don't modify[521]#
        #add your code here

        self.ArdCtrl.Stop()
        self.btOpenPrt.Enable(True)
        self.btClosePrt.Enable(False)
        self.btDigiOutSet.Enable(False)
        self.btDigiRead.Enable(False)
        self.btAnalogOut.Enable(False)
        self.btAnalogRead.Enable(False)
        return #end function


    def HandleException(self, e):
        """ Exception handler """
        wx.MessageBox(e.message)
        self.SetStatusText(e.message)

    def OnDigiRead(self,event): #init function
        #[174]Code event VwX...Don't modify[174]#
        #add your code here

        pin = self.cmbDigiRead.GetValue()

        if pin == "" :
          return

        pin_no = self.conf.getDigiPinValue(pin)

        try:
            val = self.ArdCtrl.ReadPin(pin_no)
            self.ledPinState.SetValue(val)
            self.SetStatusText("Read logic level " + val + " at pin " + pin)
        except Exception, e:
            self.HandleException(e)

        return #end function

    def OnAnaSet(self,event): #init function
        #[175]Code event VwX...Don't modify[175]#
        #add your code here

        ana = self.cmbAnalogOut.GetValue()
        ana_val = self.txAnalogOut.GetValue()

        if ana == '' or ana_val == '':
          return

        ana_pin = self.conf.getAnaOutPinValue(ana)
        ana_val = int(ana_val)

        maxAout = self.conf.getAoutMax()
        if ana_val < 0 or ana_val > maxAout-1:
          wx.MessageBox("Analog output value must be in the range 0 and %d" %maxAout)
          return

        try:
            self.ArdCtrl.SetAnalogVal(ana_pin, ana_val)
            self.SetStatusText("Set analog pin " + ana + " to " + str(ana_val))
        except Exception, e:
            self.HandleException(e)

        return #end function

    def OnAnaRead(self,event): #init function
        #[176]Code event VwX...Don't modify[176]#
        #add your code here

        ana = self.cmbAnalogIn.GetValue()

        if ana == '':
          return

        ana_pin = self.conf.getAnaInPinValue(ana)

        try:
            ana_val = self.ArdCtrl.ReadAnalogVal(ana_pin)
            self.ledAnalogRead.SetValue(ana_val)
            self.SetStatusText("Read voltage " + ana_val  + " at pin " + ana)
        except Exception, e:
            self.HandleException(e)

        return #end function


    def OnDigiSet(self,event): #init function
        #[234]Code event VwX...Don't modify[234]#
        #add your code here

        pin = self.cmbDigiOpPins.GetValue()
        state = self.cmbHighLow.GetValue()

        if pin == "" or state == "":
          return

        pin_no = self.conf.getDigiPinValue(pin)

        if state == 'High':
          pin_st = 1
        else:
          pin_st = 0

        try:
            self.ArdCtrl.SetPinData(pin_no, pin_st)
            # No exception, every thing went smoothly
            self.SetStatusText("Set pin " + pin + " to " + state)
        except Exception, e:
            self.HandleException(e)


        return #end function


    def initBefore(self):
        #add your code here

        return

    def initAfter(self):
        #add your code here
        from GetSerPorts import GetSerPorts
        serPrtsLister = GetSerPorts()
        serPrts = serPrtsLister.get_ports()
        for prt in serPrts:
            self.cmbSerPort.Append(prt)

        self.btOpenPrt.Enable(True)
        self.btClosePrt.Enable(False)
        self.btDigiOutSet.Enable(False)
        self.btDigiRead.Enable(False)
        self.btAnalogOut.Enable(False)
        self.btAnalogRead.Enable(False)
        self.Centre()
        return

    def OnPreCreate(self):
        #add your code here

        return

    def Ddel(self): #init function
        #[158]Code VwX...Don't modify[157]#
        #add your code here

        try:
            self.ArdCtrl.Stop()
        except:
            pass


        return #end function

#[win]end your code

import os
class App(wx.App):
    
    def OnInit(self):
        self.main = ControllerFrame(None, os.path.join('cfg', 'mbed.cfg'))
        self.main.Show()
        return True

    def OnExit(self):
        try:
            self.main.Close()
        except:
            pass


def main():
    application = App(0)
    application.MainLoop()


if __name__ == '__main__':
    main()
