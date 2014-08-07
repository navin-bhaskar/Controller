# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import os
from collections import namedtuple
from ConfigHandler import ConfigHandler
import pickle
from GetSerPorts import GetSerPorts
from QuickCtl import QuickCtl
import time
###########################################################################
## Class QuickCtl
###########################################################################

class QuickCtlConfig ( wx.Frame ):

    def __init__( self, parent, cfgFile="Arduino_Duemilanove.cfg" ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 373,507 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # This named tuple acts like the group holder for GUI controls
        # that we need to control
        self.ctls = namedtuple("ctls", 'availableLstCtl selectedLstCtl')
        self.ctlDic = {}
        self.serPort = ""
        self.cfgFile = cfgFile

        # Try to open the config file and load the values
        try:
            self.cfg = ConfigHandler(self.cfgFile)
        except:
            wx.MessageBox(cfgFile + " was not found ")
            wx.Exit()

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        frameSizer = wx.BoxSizer( wx.VERTICAL )

        self.mainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        mainSizer = wx.BoxSizer( wx.VERTICAL )


        #mainSizer.Add( gpioBox, 1, wx.EXPAND, 5 )
        sizer = self.addPerBox('GPIOs', 'gpio')
        mainSizer.Add( sizer, 1, wx.EXPAND, 5 )
        sizer = self.addPerBox('DACs', 'dac')
        mainSizer.Add( sizer, 1, wx.EXPAND, 5 )
        sizer = self.addPerBox('ADCs', 'adc')
        mainSizer.Add( sizer, 1, wx.EXPAND, 5 )


        # Let's popuate the list box with the pins that are available
        # first read the pickle file associated with the config file
        # and populate appropriately
        try:
            pick = os.path.splitext(self.cfgFile)[0]+'.pickle'
            pick = file(pick)
            self.selectedCtlDic = pickle.load(pick)
        except:
            self.selectedCtlDic = {'gpio':[], 'dac':[], 'adc':[]}

        self.selectedCtlDic['gpio'].sort(self.cfg.__cmp__)
        self.selectedCtlDic['adc'].sort(self.cfg.__cmp__)
        self.selectedCtlDic['dac'].sort(self.cfg.__cmp__)

        gpios = self.cfg.getDigiPinNames()
        gpios = self.__reomove_dups__(gpios, self.selectedCtlDic['gpio'])
        self.ctlDic['gpio'].availableLstCtl.InsertItems(gpios, 0)
        self.ctlDic['gpio'].selectedLstCtl.InsertItems(self.selectedCtlDic['gpio'], 0)


        dacs = self.cfg.getAnaOutPinNames()
        dacs = self.__reomove_dups__(dacs, self.selectedCtlDic['dac'])
        self.ctlDic['dac'].availableLstCtl.InsertItems(dacs, 0)
        self.ctlDic['dac'].selectedLstCtl.InsertItems(self.selectedCtlDic['dac'], 0)


        adcs = self.cfg.getAnaInPinNames()
        adcs = self.__reomove_dups__(adcs, self.selectedCtlDic['adc'])
        self.ctlDic['adc'].availableLstCtl.InsertItems(adcs, 0)
        self.ctlDic['adc'].selectedLstCtl.InsertItems(self.selectedCtlDic['adc'], 0)



        self.availbleCtlDic = {'gpio':gpios, 'dac':dacs, 'adc':adcs}

        self.prts = GetSerPorts()
        self.ports = self.prts.get_ports();

        sdbSizer = wx.StdDialogButtonSizer()
        self.sdbSizerOK = wx.Button( self.mainPanel, wx.ID_OK )
        self.sdbSizerOK.Bind( wx.EVT_BUTTON, self.onOk )
        sdbSizer.AddButton( self.sdbSizerOK )
        self.sdbSizerCancel = wx.Button( self.mainPanel, wx.ID_CANCEL )
        self.sdbSizerCancel.Bind( wx.EVT_BUTTON, self.onCancel )
        sdbSizer.AddButton( self.sdbSizerCancel )
        sdbSizer.Realize();
        self.stPortName = wx.StaticText(self.mainPanel, -1, " Select the serial port name")
        self.cmbSerPort = wx.ComboBox(self.mainPanel,-1,"",wx.Point(120,35),wx.Size(15,21), self.ports,wx.CB_READONLY)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.stPortName, 1, wx.EXPAND, 10)
        sizer.Add(self.cmbSerPort, 1, wx.EXPAND, 1)

        mainSizer.Add((0, 20))
        mainSizer.Add(sizer, .9, wx.EXPAND, 5 )
        mainSizer.Add((0, 10))
        mainSizer.Add( sdbSizer, .8, wx.EXPAND, 5 )
        mainSizer.Add((0, 20))

        self.mainPanel.SetSizer( mainSizer )
        self.mainPanel.Layout()
        mainSizer.Fit( self.mainPanel )
        frameSizer.Add( self.mainPanel, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( frameSizer )
        # Now that all the GUI controls are laid out, let us now populate the lists

        self.Layout()


        self.Centre( wx.BOTH )


    def __reomove_dups__(self, origList, copyList):
        """ Removes entries from origList that are present in origList
        """

        if len(origList) == 0:return
        for cp in copyList:
            if cp in origList: origList.remove(cp)

        return origList

    def onL2r(self, event):
        button = event.GetEventObject()

        btnId = event.GetId()
        btnById = self.FindWindowById(btnId)
        name = btnById.GetName().replace('l2r', '')
        selection = self.ctlDic[name].availableLstCtl.GetStringSelection()
        if selection == '': return
        self.ctlDic[name].selectedLstCtl.Append(selection)
        self.selectedCtlDic[name].append(selection)
        n = self.ctlDic[name].availableLstCtl.FindString(selection)
        self.ctlDic[name].availableLstCtl.Delete(n)
        #print self.selectedCtlDic[name]

    def onR2l(self, event):
        button = event.GetEventObject()

        btnId = event.GetId()
        btnById = self.FindWindowById(btnId)
        name = btnById.GetName().replace('r2l', '')

        selection = self.ctlDic[name].selectedLstCtl.GetStringSelection()
        if selection == '': return
        self.ctlDic[name].availableLstCtl.Append(selection)
        self.selectedCtlDic[name].remove(selection)
        n = self.ctlDic[name].selectedLstCtl.FindString(selection)
        self.ctlDic[name].selectedLstCtl.Delete(n)
        #print self.selectedCtlDic[name]

    def onOk(self, event):
        # Let us store the user selections
        cfgFile = os.path.splitext(self.cfgFile)[0]
        # serialize
        pick = file(cfgFile + '.pickle', 'w')
        self.selectedCtlDic['gpio'].sort(self.cfg.__cmp__)
        self.selectedCtlDic['adc'].sort(self.cfg.__cmp__)
        self.selectedCtlDic['dac'].sort(self.cfg.__cmp__)
        pickle.dump(self.selectedCtlDic, pick)
        serPort = self.cmbSerPort.GetValue().encode('ASCII')
        try:
            quickCtlFrame = QuickCtl(serPort, self.cfg, self.selectedCtlDic['gpio'], self.selectedCtlDic['adc'], self.selectedCtlDic['dac'])
            self.Show(False)
        except:
            wx.MessageBox("Oops, there was a problem", style=wx.ICON_EXCLAMATION)
            wx.Exit()

        quickCtlFrame.Show(True)

    def onCancel(self, event):
        self.Close()

    def addPerBox(self, title='GPIOs', name='gpio'):

        # We will use a dictionary to hold all the info required to
        # control the list item


        boxSizer = wx.StaticBoxSizer( wx.StaticBox( self.mainPanel, wx.ID_ANY, title), wx.VERTICAL )

        vSizer = wx.BoxSizer( wx.HORIZONTAL )

        leftVSizer = wx.BoxSizer( wx.VERTICAL )

        self.stAvailablePorts = wx.StaticText( self.mainPanel, wx.ID_ANY, u"Available port(s)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stAvailablePorts.Wrap( -1 )
        leftVSizer.Add( self.stAvailablePorts, 0, wx.ALL, 5 )

        self.lstAvailablePorts = wx.ListBox( self.mainPanel, wx.ID_ANY, wx.DefaultPosition, (100, 75), style = wx.LB_SORT)
        leftVSizer.Add( self.lstAvailablePorts, 0, wx.ALL, 5 )


        vSizer.Add( leftVSizer, 1, wx.EXPAND, 5 )

        midVSizer = wx.BoxSizer( wx.VERTICAL )

        midVSizer.Add((0, 30))
        self.btnLeftToRight = wx.Button( self.mainPanel, wx.ID_ANY, u">>", wx.DefaultPosition, wx.DefaultSize, 0, name = name+'l2r' )
        self.btnLeftToRight.Bind( wx.EVT_BUTTON, self.onL2r )
        midVSizer.Add( self.btnLeftToRight, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.btnRightToLeft = wx.Button( self.mainPanel, wx.ID_ANY, u"<<", wx.DefaultPosition, wx.DefaultSize, 0, name = name+'r2l' )
        self.btnRightToLeft.Bind( wx.EVT_BUTTON, self.onR2l )

        midVSizer.Add( self.btnRightToLeft, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        vSizer.Add( midVSizer, 1, wx.EXPAND, 10 )


        rightVSizer = wx.BoxSizer( wx.VERTICAL )

        self.stSelectedPorts = wx.StaticText( self.mainPanel, wx.ID_ANY, u"Selected port(s)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSelectedPorts.Wrap( -1 )
        rightVSizer.Add( self.stSelectedPorts, 0, wx.ALL, 5 )

        self.lstSelectedPorts = wx.ListBox( self.mainPanel, wx.ID_ANY, wx.DefaultPosition, (100, 75), style = wx.LB_SORT)
        rightVSizer.Add( self.lstSelectedPorts, 0, wx.ALL, 5 )

        temp = self.ctls(self.lstAvailablePorts, self.lstSelectedPorts)
        vSizer.Add( rightVSizer, 1, wx.EXPAND, 5 )

        boxSizer.Add( vSizer, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )
        self.ctlDic[name] = temp

        return boxSizer

    def __del__( self ):
        wx.Exit()
        return


class App(wx.App):
    def OnInit(self):
        self.main = QuickCtlConfig(None, cfgFile = os.path.join('cfg', "Arduino_Duemilanove.cfg"))
        self.main.Show()
        return True

def main():
    application = App(0)
    application.MainLoop()


if __name__ == '__main__':
    main()
