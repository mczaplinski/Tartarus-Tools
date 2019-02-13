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
## Class LibRecorderGUI
###########################################################################

class LibRecorderGUI ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Tartarus Tools - Sample Library Recorder", pos = wx.DefaultPosition, size = wx.Size( 1400,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu3 = wx.Menu()
        self.m_menuItem2 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Audio Device Settings", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu3.AppendItem( self.m_menuItem2 )

        self.m_menubar1.Append( self.m_menu3, u"File" ) 

        self.SetMenuBar( self.m_menubar1 )

        gSizer1 = wx.GridSizer( 3, 1, 0, 0 )

        gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

        gSizer6 = wx.GridSizer( 5, 2, 0, 0 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Library Name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer6.Add( self.m_staticText7, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxLibName = wx.TextCtrl( self, wx.ID_ANY, u"MyStupidLibrary", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer6.Add( self.wxLibName, 0, wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Folder to save samples to", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        self.m_staticText8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer6.Add( self.m_staticText8, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxSavePath = wx.DirPickerCtrl( self, wx.ID_ANY, u"X:\\_SAMPLING_\\TestLib", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        gSizer6.Add( self.wxSavePath, 0, wx.ALL, 5 )

        self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"SamplesPrefix", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        self.m_staticText9.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer6.Add( self.m_staticText9, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxSamplePrefix = wx.TextCtrl( self, wx.ID_ANY, u"MyLibStacc", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer6.Add( self.wxSamplePrefix, 0, wx.ALL, 5 )

        self.wxSaveButton = wx.Button( self, wx.ID_ANY, u"Accept changes", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer6.Add( self.wxSaveButton, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxRecordButton = wx.Button( self, wx.ID_ANY, u"Start Recording", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        self.wxRecordButton.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.wxRecordButton.SetBackgroundColour( wx.Colour( 223, 223, 223 ) )

        gSizer6.Add( self.wxRecordButton, 0, wx.ALL, 5 )

        self.wxPreviewDryButton = wx.Button( self, wx.ID_ANY, u"Preview Dry 5 sec", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer6.Add( self.wxPreviewDryButton, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxPreviewWetButton = wx.Button( self, wx.ID_ANY, u"Preview Wet 5 sec", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer6.Add( self.wxPreviewWetButton, 0, wx.ALL, 5 )


        gSizer2.Add( gSizer6, 1, wx.EXPAND, 5 )

        gSizer7 = wx.GridSizer( 5, 2, 0, 0 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Samplerate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer7.Add( self.m_staticText2, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        wxSamplerateChoices = [ u"6000", u"8000", u"11025", u"16000", u"22050", u"32000", u"44100", u"48000", u"64000", u"88200", u"96000", u"176400", u"192000" ]
        self.wxSamplerate = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), wxSamplerateChoices, 0 )
        self.wxSamplerate.SetSelection( 6 )
        gSizer7.Add( self.wxSamplerate, 0, wx.ALL, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Blocksize (for processing)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer7.Add( self.m_staticText3, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        wxBlocksizeChoices = [ u"32", u"64", u"128", u"256", u"512", u"1024", u"2048", u"4096", u"8192", u"16384", u"32768", u"1024" ]
        self.wxBlocksize = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), wxBlocksizeChoices, 0 )
        self.wxBlocksize.SetSelection( 5 )
        gSizer7.Add( self.wxBlocksize, 0, wx.ALL, 5 )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Sample Duration (in sec)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        self.m_staticText4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer7.Add( self.m_staticText4, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxSampleDuration = wx.TextCtrl( self, wx.ID_ANY, u"5.0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer7.Add( self.wxSampleDuration, 0, wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Zero Padding Length (in sec)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        self.m_staticText5.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer7.Add( self.m_staticText5, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxZeroPadding = wx.TextCtrl( self, wx.ID_ANY, u"5.0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer7.Add( self.wxZeroPadding, 0, wx.ALL, 5 )

        self.wxPreStartText = wx.StaticText( self, wx.ID_ANY, u"Pre Start Duration (time before live rec in sec)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxPreStartText.Wrap( -1 )
        self.wxPreStartText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer7.Add( self.wxPreStartText, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxPreStartDuration = wx.TextCtrl( self, wx.ID_ANY, u"3.0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer7.Add( self.wxPreStartDuration, 0, wx.ALL, 5 )


        gSizer2.Add( gSizer7, 1, wx.EXPAND, 5 )


        gSizer1.Add( gSizer2, 1, wx.EXPAND, 5 )

        gSizer3 = wx.GridSizer( 0, 3, 0, 0 )

        gSizer9 = wx.GridSizer( 7, 2, 0, 0 )

        self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Input Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        self.m_staticText10.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText10, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        wxInputModeChoices = [ u"VSTi", u"Live Recording", u"MIDI Out -> Rec" ]
        self.wxInputMode = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), wxInputModeChoices, 0 )
        self.wxInputMode.SetSelection( 0 )
        gSizer9.Add( self.wxInputMode, 0, wx.ALL, 5 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"From Note (C-2 ... G8).", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText11, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxFromNote = wx.TextCtrl( self, wx.ID_ANY, u"C-2", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer9.Add( self.wxFromNote, 0, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"To Note (use # not b)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        self.m_staticText12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText12, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxToNote = wx.TextCtrl( self, wx.ID_ANY, u"G8", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer9.Add( self.wxToNote, 0, wx.ALL, 5 )

        self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Velocity Steps (recording)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )
        self.m_staticText13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText13, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVelSteps = wx.TextCtrl( self, wx.ID_ANY, u"[127]", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer9.Add( self.wxVelSteps, 0, wx.ALL, 5 )

        self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Velocity Ranges (Kontakt assignments)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        self.m_staticText14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText14, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVelRanges = wx.TextCtrl( self, wx.ID_ANY, u"[[0,27]]", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer9.Add( self.wxVelRanges, 0, wx.ALL, 5 )

        self.m_staticText241 = wx.StaticText( self, wx.ID_ANY, u"Mod Wheel Steps", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText241.Wrap( -1 )
        self.m_staticText241.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText241, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxMWSteps = wx.TextCtrl( self, wx.ID_ANY, u"[127]", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer9.Add( self.wxMWSteps, 0, wx.ALL, 5 )

        self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Num Round Robins", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText25.Wrap( -1 )
        self.m_staticText25.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer9.Add( self.m_staticText25, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxNumRRs = wx.TextCtrl( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer9.Add( self.wxNumRRs, 0, wx.ALL, 5 )


        gSizer3.Add( gSizer9, 1, wx.EXPAND, 5 )

        gSizer10 = wx.GridSizer( 5, 2, 0, 0 )

        gSizer19 = wx.GridSizer( 0, 2, 0, 0 )

        self.wxTuningTarget = wx.CheckBox( self, wx.ID_ANY, u"VSTi Tuning Target", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        gSizer19.Add( self.wxTuningTarget, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVSTiName = wx.StaticText( self, wx.ID_ANY, u"VSTi DLL", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxVSTiName.Wrap( -1 )
        self.wxVSTiName.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer19.Add( self.wxVSTiName, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


        gSizer10.Add( gSizer19, 1, wx.EXPAND, 5 )

        gSizer12 = wx.GridSizer( 0, 4, 0, 0 )

        self.wxVSTiPath = wx.FilePickerCtrl( self, wx.ID_ANY, u"D:\\VST64", u"Select the VST Instrument .dll", u"*.dll", wx.DefaultPosition, wx.Size( 50,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        gSizer12.Add( self.wxVSTiPath, 0, wx.ALL, 5 )

        self.wxVSTiOpenButton = wx.Button( self, wx.ID_ANY, u"Open", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        gSizer12.Add( self.wxVSTiOpenButton, 0, wx.ALL, 5 )


        gSizer10.Add( gSizer12, 1, wx.EXPAND, 5 )

        self.wxOnThreshText = wx.StaticText( self, wx.ID_ANY, u"On Threshold Gating (dB)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxOnThreshText.Wrap( -1 )
        self.wxOnThreshText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer10.Add( self.wxOnThreshText, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxOnThresh = wx.TextCtrl( self, wx.ID_ANY, u"-40.0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer10.Add( self.wxOnThresh, 0, wx.ALL, 5 )

        self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Off Threshold Gating (dB)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )
        self.m_staticText17.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer10.Add( self.m_staticText17, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxOffThresh = wx.TextCtrl( self, wx.ID_ANY, u"-80.0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer10.Add( self.wxOffThresh, 0, wx.ALL, 5 )

        self.wxMidiOutDeviceText = wx.StaticText( self, wx.ID_ANY, u"MIDI Out Device ID", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxMidiOutDeviceText.Wrap( -1 )
        self.wxMidiOutDeviceText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer10.Add( self.wxMidiOutDeviceText, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxMIDIOutDevice = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer10.Add( self.wxMIDIOutDevice, 0, wx.ALL, 5 )

        self.wxMidiInDeviceText = wx.StaticText( self, wx.ID_ANY, u"MIDI In Device ID (for Playback/Preview)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxMidiInDeviceText.Wrap( -1 )
        self.wxMidiInDeviceText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer10.Add( self.wxMidiInDeviceText, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxMIDIInDevice = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        gSizer10.Add( self.wxMIDIInDevice, 0, wx.ALL, 5 )


        gSizer3.Add( gSizer10, 1, wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 5, 4, 0, 0 )

        self.wxVST1Name = wx.StaticText( self, wx.ID_ANY, u"PostFX VST1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxVST1Name.Wrap( -1 )
        self.wxVST1Name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVST1Name, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVst1Path = wx.FilePickerCtrl( self, wx.ID_ANY, u"D:\\VST64", u"Select the VST FX1 .dll", u"*.dll", wx.DefaultPosition, wx.Size( 80,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        gSizer11.Add( self.wxVst1Path, 0, wx.ALL, 5 )

        self.wxVst1isActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.wxVst1isActive.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVst1isActive, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.wxVst1openButton = wx.Button( self, wx.ID_ANY, u"Open GUI", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.wxVst1openButton, 0, wx.ALL, 5 )

        self.wxVST2Name = wx.StaticText( self, wx.ID_ANY, u"PostFX VST2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxVST2Name.Wrap( -1 )
        self.wxVST2Name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVST2Name, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVst2Path = wx.FilePickerCtrl( self, wx.ID_ANY, u"D:\\VST64", u"Select the VST FX2 .dll", u"*.dll", wx.DefaultPosition, wx.Size( 80,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        gSizer11.Add( self.wxVst2Path, 0, wx.ALL, 5 )

        self.wxVst2isActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.wxVst2isActive.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVst2isActive, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.wxVst2openButton = wx.Button( self, wx.ID_ANY, u"Open GUI", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.wxVst2openButton, 0, wx.ALL, 5 )

        self.wxVST3Name = wx.StaticText( self, wx.ID_ANY, u"PostFX VST3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxVST3Name.Wrap( -1 )
        self.wxVST3Name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVST3Name, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVst3Path = wx.FilePickerCtrl( self, wx.ID_ANY, u"D:\\VST64", u"Select the VST FX3 .dll", u"*.dll", wx.DefaultPosition, wx.Size( 80,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        gSizer11.Add( self.wxVst3Path, 0, wx.ALL, 5 )

        self.wxVst3isActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.wxVst3isActive.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVst3isActive, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.wxVst3openButton = wx.Button( self, wx.ID_ANY, u"Open GUI", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.wxVst3openButton, 0, wx.ALL, 5 )

        self.wxVST4Name = wx.StaticText( self, wx.ID_ANY, u"PostFX VST4", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxVST4Name.Wrap( -1 )
        self.wxVST4Name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVST4Name, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVst4Path = wx.FilePickerCtrl( self, wx.ID_ANY, u"D:\\VST64", u"Select the VST FX4 .dll", u"*.dll", wx.DefaultPosition, wx.Size( 80,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        gSizer11.Add( self.wxVst4Path, 0, wx.ALL, 5 )

        self.wxVst4isActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.wxVst4isActive.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVst4isActive, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.wxVst4openButton4 = wx.Button( self, wx.ID_ANY, u"Open GUI", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.wxVst4openButton4, 0, wx.ALL, 5 )

        self.wxVST5Name = wx.StaticText( self, wx.ID_ANY, u"PostFX VST5", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxVST5Name.Wrap( -1 )
        self.wxVST5Name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVST5Name, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.wxVst5Path = wx.FilePickerCtrl( self, wx.ID_ANY, u"D:\\VST64", u"Select the VST FX5 .dll", u"*.dll", wx.DefaultPosition, wx.Size( 80,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        gSizer11.Add( self.wxVst5Path, 0, wx.ALL, 5 )

        self.wxVst5isActive = wx.CheckBox( self, wx.ID_ANY, u"isActive", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.wxVst5isActive.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        gSizer11.Add( self.wxVst5isActive, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.wxVst5openButton = wx.Button( self, wx.ID_ANY, u"Open GUI", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.wxVst5openButton, 0, wx.ALL, 5 )


        gSizer3.Add( gSizer11, 1, wx.EXPAND, 5 )


        gSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )

        gSizer5 = wx.GridSizer( 2, 1, 0, 0 )

        gSizer101 = wx.GridSizer( 0, 4, 0, 0 )

        self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"ModWheel", wx.Point( -1,-1 ), wx.Size( -1,-1 ), 0 )
        self.m_staticText26.Wrap( -1 )
        self.m_staticText26.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )

        gSizer101.Add( self.m_staticText26, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Velocity", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText27.Wrap( -1 )
        self.m_staticText27.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )

        gSizer101.Add( self.m_staticText27, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"Note", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText28.Wrap( -1 )
        self.m_staticText28.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )

        gSizer101.Add( self.m_staticText28, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, u"Round Robin", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText29.Wrap( -1 )
        self.m_staticText29.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )

        gSizer101.Add( self.m_staticText29, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        gSizer5.Add( gSizer101, 1, wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 0, 4, 0, 0 )

        self.wxCurMWValue = wx.StaticText( self, wx.ID_ANY, u".", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxCurMWValue.Wrap( -1 )
        self.wxCurMWValue.SetFont( wx.Font( 50, 70, 90, 92, False, wx.EmptyString ) )

        gSizer111.Add( self.wxCurMWValue, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )

        self.wxCurVelValue = wx.StaticText( self, wx.ID_ANY, u".", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxCurVelValue.Wrap( -1 )
        self.wxCurVelValue.SetFont( wx.Font( 50, 70, 90, 92, False, wx.EmptyString ) )

        gSizer111.Add( self.wxCurVelValue, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )

        self.wxCurNoteValue = wx.StaticText( self, wx.ID_ANY, u".", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxCurNoteValue.Wrap( -1 )
        self.wxCurNoteValue.SetFont( wx.Font( 50, 70, 90, 92, False, wx.EmptyString ) )

        gSizer111.Add( self.wxCurNoteValue, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )

        self.wxCurRRValue = wx.StaticText( self, wx.ID_ANY, u".", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.wxCurRRValue.Wrap( -1 )
        self.wxCurRRValue.SetFont( wx.Font( 50, 70, 90, 92, False, wx.EmptyString ) )

        gSizer111.Add( self.wxCurRRValue, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )


        gSizer5.Add( gSizer111, 1, wx.EXPAND, 5 )


        gSizer1.Add( gSizer5, 1, wx.EXPAND, 5 )


        self.SetSizer( gSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.onMenuAudioDeviceSettings, id = self.m_menuItem2.GetId() )
        self.wxSaveButton.Bind( wx.EVT_BUTTON, self.saveChangesFromGUI )
        self.wxRecordButton.Bind( wx.EVT_BUTTON, self.startRecording )
        self.wxPreviewDryButton.Bind( wx.EVT_BUTTON, self.previewDry )
        self.wxPreviewWetButton.Bind( wx.EVT_BUTTON, self.previewWet )
        self.wxSamplerate.Bind( wx.EVT_CHOICE, self.onSamplerateChange )
        self.wxBlocksize.Bind( wx.EVT_CHOICE, self.onBlockSizeChange )
        self.wxInputMode.Bind( wx.EVT_CHOICE, self.onInputeModeChange )
        self.wxTuningTarget.Bind( wx.EVT_CHECKBOX, self.onVSTiTuningTargetChange )
        self.wxVSTiPath.Bind( wx.EVT_FILEPICKER_CHANGED, self.onVSTiBrowse )
        self.wxVSTiOpenButton.Bind( wx.EVT_BUTTON, self.open_VST_instrument )
        self.wxVst1Path.Bind( wx.EVT_FILEPICKER_CHANGED, self.onVST1Browse )
        self.wxVst1openButton.Bind( wx.EVT_BUTTON, self.open_VST_fx_1 )
        self.wxVst2Path.Bind( wx.EVT_FILEPICKER_CHANGED, self.onVST2Browse )
        self.wxVst2openButton.Bind( wx.EVT_BUTTON, self.open_VST_fx_2 )
        self.wxVst3Path.Bind( wx.EVT_FILEPICKER_CHANGED, self.onVST3Browse )
        self.wxVst3openButton.Bind( wx.EVT_BUTTON, self.open_VST_fx_3 )
        self.wxVst4Path.Bind( wx.EVT_FILEPICKER_CHANGED, self.onVST4Browse )
        self.wxVst4openButton4.Bind( wx.EVT_BUTTON, self.open_VST_fx_4 )
        self.wxVst5Path.Bind( wx.EVT_FILEPICKER_CHANGED, self.onVST5Browse )
        self.wxVst5openButton.Bind( wx.EVT_BUTTON, self.open_VST_fx_5 )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def onMenuAudioDeviceSettings( self, event ):
        event.Skip()

    def saveChangesFromGUI( self, event ):
        event.Skip()

    def startRecording( self, event ):
        event.Skip()

    def previewDry( self, event ):
        event.Skip()

    def previewWet( self, event ):
        event.Skip()

    def onSamplerateChange( self, event ):
        event.Skip()

    def onBlockSizeChange( self, event ):
        event.Skip()

    def onInputeModeChange( self, event ):
        event.Skip()

    def onVSTiTuningTargetChange( self, event ):
        event.Skip()

    def onVSTiBrowse( self, event ):
        event.Skip()

    def open_VST_instrument( self, event ):
        event.Skip()

    def onVST1Browse( self, event ):
        event.Skip()

    def open_VST_fx_1( self, event ):
        event.Skip()

    def onVST2Browse( self, event ):
        event.Skip()

    def open_VST_fx_2( self, event ):
        event.Skip()

    def onVST3Browse( self, event ):
        event.Skip()

    def open_VST_fx_3( self, event ):
        event.Skip()

    def onVST4Browse( self, event ):
        event.Skip()

    def open_VST_fx_4( self, event ):
        event.Skip()

    def onVST5Browse( self, event ):
        event.Skip()

    def open_VST_fx_5( self, event ):
        event.Skip()


