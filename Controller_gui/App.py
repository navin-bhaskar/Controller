# -*- coding: utf-8 -*-
###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

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
@file       App.py
@author     Navin Bhaskar
@brief      The main app, displays the configuration files and lets user
            start the rest of the app based on the config file 
"""



import wx
from ControllerFrame import ControllerFrame
from QuickCtlConfig import QuickCtlConfig
import os

###########################################################################
## Class CtrlConfig
###########################################################################

class CtrlConfig ( wx.Dialog ):

    def __init__( self, parent, size):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select Config File", pos = wx.DefaultPosition, size=size, style = wx.DEFAULT_DIALOG_STYLE )
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizerMain = wx.BoxSizer( wx.HORIZONTAL )



        self.m_staticTextSelBoard = wx.StaticText( self, wx.ID_ANY, u"Select your hardware module:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticTextSelBoard.Wrap( -1 )
        bSizerMain.Add( self.m_staticTextSelBoard, 0, wx.ALL, 5 )

        m_choiceSelFileChoices = []
        self.m_choiceSelFile = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceSelFileChoices, 0 )
        self.m_choiceSelFile.SetSelection( 0 )
        bSizerMain.Add( self.m_choiceSelFile, 0, wx.ALL, 5 )
        
        self.m_selQuickWin = wx.CheckBox(self, wx.ID_ANY, u"Quick Ctl", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerMain.Add( self.m_selQuickWin, 0, wx.ALL, 5 ) 

        self.m_buttonStart = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerMain.Add( self.m_buttonStart, 0, wx.ALL, 5 )

        self.m_buttonCancel = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerMain.Add( self.m_buttonCancel, 0, wx.ALL, 5 )

        self.SetSizer( bSizerMain )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_buttonStart.Bind( wx.EVT_BUTTON, self.OnStart )
        self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnStop )
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        cfgFiles = self.listCfgFiles()


        for cfgFile in cfgFiles:
            self.m_choiceSelFile.Append(cfgFile)

    def __del__( self ):
        wx.Exit()


    def OnStart( self, event ):
        cfgFileChoice = self.m_choiceSelFile.GetSelection()

        if cfgFileChoice == -1:
            return
        cfgFile = self.cfgFiles[cfgFileChoice]
        cfgFile = os.path.join('cfg', cfgFile)

        self.Show(False)
        if self.m_selQuickWin.GetValue() == False:
            self.AppFrame = ControllerFrame(self, cfgFile)
            self.AppFrame.Show(True)
        else:
            self.AppFrame = QuickCtlConfig(self, cfgFile)
            self.AppFrame.Show(True)

    def OnStop( self, event ):
        self.Close(True)
        
    def OnClose(self, event):
        self.Destroy()


    def listCfgFiles(self):
        import os, os.path
        import re

        def __populate_list__(self):
            self.cfgFiles = []

            def matchFiles(arg, dir, files):
                for file in files:
                    if re.search(r".*\.cfg", file):
                        self.cfgFiles.append(file)

            os.path.walk('cfg', matchFiles, 0)

        __populate_list__(self)

        cfgNames = []
        self.cfgFiles.sort()
        for cfgFile in self.cfgFiles:
            cfgNames.append(os.path.splitext(cfgFile)[0])

        return cfgNames


class App(wx.App):
    def OnInit(self):
        self.SetExitOnFrameDelete(True)
        # Don't know why this is required :(
        if os.name == 'posix':
            size = wx.Size( 600,60 )
        else:
            size = wx.Size( 550,60 )

        self.main = CtrlConfig(None, size )
        self.main.Show()
        return True

    def OnExit(self):
        try:
          self.main.Close()
        except :
            pass


def main():
    application = App(0)
    application.MainLoop()


if __name__ == '__main__':
    main()
