import wx
from TransLayer import TransLayer
import time
import ControllerExceptions

class QuickCtl(wx.Frame):
    def __init__(self, serPort, cfg, gpios, adcs, dacs):
        wx.Frame.__init__(self, None, -1, "Quick Controller")
        self.panel = wx.Panel(self)
        self.txtFields=[]
        self.config = cfg
        
        try:
            self.BoardComm = TransLayer(serPort, cfg.getVref(), cfg.getRes())
            time.sleep(1)
        except IOError:
            wx.MessageBox("Could not open serial port %s" %serPort, style=wx.ICON_EXCLAMATION)
            self.Close()
            wx.Exit()
            
        self.ctlDic = {'gpio':{}, 'adc':{}, 'dac':{}}
        gpiobox = self.MakeGpioCluster(gpios)
        adcbox = self.MakeAdcCluster(adcs)
        dacbox = self.MakeDacCluster(dacs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # add the controls only if required
        if gpiobox != None: sizer.Add(gpiobox, 0, wx.ALL, 10)
        if adcbox != None: sizer.Add(adcbox, 0, wx.ALL, 10)
        if dacbox != None: sizer.Add(dacbox, 0, wx.ALL, 10)
        
        self.statusBar = self.CreateStatusBar()
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        
        self.panel.SetSizer(sizer)
        
        sizer.Fit(self)
    
    def HandleException(self, e):
        """ Exception handler """
        wx.MessageBox(e.message)
        self.SetStatusText(e.message)
        
    def MakeGpio(self, portName):
        btn1 = wx.Button(self.panel, wx.ID_ANY, portName + u" read", wx.DefaultPosition, wx.DefaultSize, 0, name = portName )
        btn1.Bind(wx.EVT_BUTTON, self.OnGpioRead)
        btn2 = wx.Button(self.panel, wx.ID_ANY, portName + u" write", wx.DefaultPosition, wx.DefaultSize, 0, name = portName )
        btn2.Bind(wx.EVT_BUTTON, self.OnGpioWrite)
        txt = wx.TextCtrl(self.panel, -1, "", size=(30, -1))
        self.ctlDic['gpio'][portName] = txt
        self.txtFields.append(txt)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(btn1, 0, wx.ALL, 5)
        sizer.Add(btn2, 0, wx.ALL, 5)
        sizer.Add(txt, 0, wx.ALL, 5)
        return sizer
        
    
    def MakeStaticBoxSizer(self, boxlabel):
        box = wx.StaticBox(self.panel, -1, boxlabel)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        return sizer
        
    def MakeGpioCluster(self, gpioList):
        if len(gpioList) == 0: return None
        sizer = self.MakeStaticBoxSizer("GPIOs")
        self.MakeCluster(sizer, gpioList, self.MakeGpio)
        return sizer
        
    def MakeAdc(self, portName):
        btn = wx.Button(self.panel, wx.ID_ANY, portName + u" read", wx.DefaultPosition, wx.DefaultSize, 0 )
        btn.SetName(portName)
        btn.Bind(wx.EVT_BUTTON, self.OnAdcRead)
        txt = wx.TextCtrl(self.panel, -1, "", size=(30, -1))
        self.ctlDic['adc'][portName] = txt
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(btn, 0, wx.ALL, 5)
        sizer.Add(txt, 0, wx.ALL, 5)
        return sizer
        
        
    def MakeAdcCluster(self, adcList):
        if len(adcList) == 0: return None
        sizer = self.MakeStaticBoxSizer("ADCs")
        self.MakeCluster(sizer, adcList, self.MakeAdc)
        return sizer
        
       
    def MakeDac(self, portName):
        stTxt = wx.StaticText(self.panel, -1, portName + ':')
        slider = wx.Slider(
            self.panel, wx.ID_ANY, 0, 0, 100, (30, 60), (250, -1), 
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS, 
            name = portName)
        slider.SetTickFreq(5, 1)
        slider.Bind(wx.EVT_SCROLL_CHANGED, self.OnDacWrite)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(stTxt, 0, wx.ALL | wx.CENTRE, 5)
        sizer.Add(slider, 0, wx.ALL, 5)
        return sizer
        
    def MakeCluster(self, sizer, pinList, adderFunc):
        for pin in pinList:
            ui = adderFunc(pin)
            sizer.Add(ui, 0, wx.ALL)
        
    def MakeDacCluster(self, dacList):
        if len(dacList) == 0 : return None
        sizer = self.MakeStaticBoxSizer("DACs")
        self.MakeCluster(sizer, dacList, self.MakeDac)
        return sizer
        
        
    def OnGpioRead(self, event):
        button = event.GetEventObject()
        btnId = event.GetId()
        btnById = self.FindWindowById(btnId)
        pinName = btnById.GetName()
        pin_no = self.config.getDigiPinValue(pinName)
        try:
            val = self.BoardComm.ReadPin(pin_no)
            self.ctlDic['gpio'][pinName].SetValue(str(val))
            self.SetStatusText("Read logic level " + val + " at pin " + pinName)
        except Exception, e:
            self.HandleException(e)
        
        
        
    def OnGpioWrite(self, event):
        button = event.GetEventObject()
        btnId = event.GetId()
        btnById = self.FindWindowById(btnId)
        pinName = btnById.GetName()
        pin_no = self.config.getDigiPinValue(pinName)
        state = self.ctlDic['gpio'][pinName].GetValue()
        if state == '1':
            pin_st = 1
        elif state == '0':
            pin_st = 0
        else:
            wx.MessageBox("Please specify 1 (logic high) or 0 (logic low)")
            return 
            
        
        try:
            self.BoardComm.SetPinData(pin_no, pin_st)
            # No exception, every thing went smoothly
            self.SetStatusText("Set pin " + pinName + " to " + state)
        except Exception, e:
            self.HandleException(e)

        
    def OnAdcRead(self, event):
        button = event.GetEventObject()
        btnId = event.GetId()
        btnById = self.FindWindowById(btnId)
        pinName = btnById.GetName()
        ana_pin = self.config.getAnaInPinValue(pinName)
        try:
            ana_val = self.BoardComm.ReadAnalogVal(ana_pin)
            self.ctlDic['adc'][pinName].SetValue(ana_val)
            self.SetStatusText("Read voltage " + ana_val  + " at pin " + pinName)
        except Exception, e:
            self.HandleException(e)
            
        
    def OnDacWrite(self, event):
        slider = event.GetEventObject()
        sliderId = event.GetId()
        sliderById = self.FindWindowById(sliderId)
        pinName = sliderById.GetName()
        ana_val = slider.GetValue()
        
        ana_pin = self.config.getAnaOutPinValue(pinName)

        maxAout = self.config.getAoutMax()
        if ana_val < 0 or ana_val > maxAout:
          wx.MessageBox("Analog output value must be in the range 0 and %d" %maxAout)
          return
        frac = float(ana_val)/100
        ana_val = int(frac*maxAout)
        if ana_val == 0:return 
        try:
            self.BoardComm.SetAnalogVal(ana_pin, ana_val)
            self.SetStatusText("Set analog pin " + pinName + " to " + str(ana_val))
        except Exception, e:
            self.HandleException(e)

        
    def __del__( self ):
        try:
            self.BoardComm.Close()
        except:
            pass
            
        wx.Exit()
        return

if __name__ == '__main__':
    app = wx.PySimpleApp()
    from ConfigHandler import ConfigHandler
    import os
    cfgFile = os.path.join('cfg', 'Arduino_Duemilanove.cfg') 
    cfg = ConfigHandler(cfgFile)
    QuickCtl('COM5', cfg, ['p0', 'p1', 'p13'], ['p0', 'p3'], ['p3', 'p6']).Show()
    app.MainLoop()
