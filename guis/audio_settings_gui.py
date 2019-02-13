# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class AudioDeviceSettingsGUI
###########################################################################

class AudioDeviceSettingsGUI ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Tartarus Tools - Audio Device Settings", pos = wx.DefaultPosition, size = wx.Size( 800,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        gSizer13 = wx.GridSizer( 5, 1, 0, 0 )

        gSizer14 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_staticText38 = wx.StaticText( self, wx.ID_ANY, u"Input Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText38.Wrap( -1 )
        self.m_staticText38.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )

        gSizer14.Add( self.m_staticText38, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticText39 = wx.StaticText( self, wx.ID_ANY, u"Output Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText39.Wrap( -1 )
        self.m_staticText39.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )

        gSizer14.Add( self.m_staticText39, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        gSizer13.Add( gSizer14, 1, wx.EXPAND, 5 )

        gSizer16 = wx.GridSizer( 0, 2, 0, 0 )

        wxListInputDevicesChoices = []
        self.wxListInputDevices = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 380,100 ), wxListInputDevicesChoices, wx.LB_HSCROLL )
        gSizer16.Add( self.wxListInputDevices, 0, wx.ALL, 5 )

        wxListOutputDevicesChoices = []
        self.wxListOutputDevices = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 380,100 ), wxListOutputDevicesChoices, wx.LB_HSCROLL )
        gSizer16.Add( self.wxListOutputDevices, 0, wx.ALL, 5 )


        gSizer13.Add( gSizer16, 1, wx.EXPAND, 5 )

        gSizer17 = wx.GridSizer( 0, 4, 0, 0 )


        gSizer13.Add( gSizer17, 1, wx.EXPAND, 5 )

        gSizer18 = wx.GridSizer( 0, 6, 0, 0 )

        self.m_staticText37 = wx.StaticText( self, wx.ID_ANY, u"Number of Channels", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText37.Wrap( -1 )
        gSizer18.Add( self.m_staticText37, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxNumInputChannels = wx.TextCtrl( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
        gSizer18.Add( self.wxNumInputChannels, 0, wx.ALL, 5 )

        self.wxIsInputActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxIsInputActive.SetValue(True) 
        gSizer18.Add( self.wxIsInputActive, 0, wx.ALL, 5 )

        self.m_staticText35 = wx.StaticText( self, wx.ID_ANY, u"Number of Channels", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText35.Wrap( -1 )
        gSizer18.Add( self.m_staticText35, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxNumOutputChannels = wx.TextCtrl( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
        gSizer18.Add( self.wxNumOutputChannels, 0, wx.ALL, 5 )

        self.wxIsOutputActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxIsOutputActive.SetValue(True) 
        gSizer18.Add( self.wxIsOutputActive, 0, wx.ALL, 5 )


        gSizer13.Add( gSizer18, 1, wx.EXPAND, 5 )

        gSizer19 = wx.GridSizer( 0, 2, 0, 0 )

        self.wxAcceptButton = wx.Button( self, wx.ID_ANY, u"Start Devices", wx.DefaultPosition, wx.Size( 200,50 ), 0 )
        gSizer19.Add( self.wxAcceptButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_button12 = wx.Button( self, wx.ID_ANY, u"Kill Devices", wx.DefaultPosition, wx.Size( 200,50 ), 0 )
        gSizer19.Add( self.m_button12, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        gSizer13.Add( gSizer19, 1, wx.EXPAND, 5 )


        self.SetSizer( gSizer13 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.wxAcceptButton.Bind( wx.EVT_BUTTON, self.onAccept )
        self.m_button12.Bind( wx.EVT_BUTTON, self.onKillAudioDevices )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def onAccept( self, event ):
        event.Skip()

    def onKillAudioDevices( self, event ):
        event.Skip()


