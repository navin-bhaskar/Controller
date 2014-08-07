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

import wx
class VwXtaskBar(wx.TaskBarIcon):
    def __init__(self,win):
        self.win=win
        wx.TaskBarIcon.__init__(self)
        self.Bind(wx.EVT_TASKBAR_MOVE,self.VwXAllEvents)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN,self.VwXAllEvents)
        self.Bind(wx.EVT_TASKBAR_LEFT_UP,self.VwXAllEvents)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN,self.VwXAllEvents)
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP,self.VwXAllEvents)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK,self.VwXAllEvents)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DCLICK,self.VwXAllEvents)
        self.Bind(wx.EVT_MENU,self.OnMenu,id=-1)
        
    def VwXAllEvents(self,event):
        self.win.GetEventHandler().ProcessEvent(event)
        if(event.GetEventType()==wx.wxEVT_TASKBAR_RIGHT_DOWN):
            event.Skip(True)

    def CreatePopupMenu(self):
        return self.win.VwXGetTaskBarMenu()

    def OnMenu(self,event):
        self.win.GetEventHandler().ProcessEvent(event)
