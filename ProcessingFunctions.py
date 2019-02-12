from enum import Enum
import numpy as np
import scipy
import math
import scipy.io.wavfile
import scipy.signal
import pyaudio
import resampy
import wx
import os
import sys
import traceback
import logging
import wave
import matplotlib.pyplot as plt

#some weird legacy libraries
#import pyvst
from pyvst.vstplugin import *

MIDI_KEY = {
    'C-2':0, 'C#-2':1, 'D-2':2, 'D#-2':3, 'E-2':4, 'F-2':5, 'F#-2':6, 'G-2':7, 'G#-2':8, 'A-2':9, 'A#-2':10,'B-2':11,
    'C-1':12,'C#-1':13,'D-1':14,'D#-1':15,'E-1':16,'F-1':17,'F#-1':18,'G-1':19,'G#-1':20,'A-1':21,'A#-1':22,'B-1':23,
    'C0':24, 'C#0':25, 'D0':26, 'D#0':27, 'E0':28, 'F0':29, 'F#0':30, 'G0':31, 'G#0':32, 'A0':33, 'A#0':34, 'B0':35,
    'C1':36, 'C#1':37, 'D1':38, 'D#1':39, 'E1':40, 'F1':41, 'F#1':42, 'G1':43, 'G#1':44, 'A1':45, 'A#1':46, 'B1':47,
    'C2':48, 'C#2':49, 'D2':50, 'D#2':51, 'E2':52, 'F2':53, 'F#2':54, 'G2':55, 'G#2':56, 'A2':57, 'A#2':58, 'B2':59,
    'C3':60, 'C#3':61, 'D3':62, 'D#3':63, 'E3':64, 'F3':65, 'F#3':66, 'G3':67, 'G#3':68, 'A3':69, 'A#3':70, 'B3':71,
    'C4':72, 'C#4':73, 'D4':74, 'D#4':75, 'E4':76, 'F4':77, 'F#4':78, 'G4':79, 'G#4':80, 'A4':81, 'A#4':82, 'B4':83,
    'C5':84, 'C#5':85, 'D5':86, 'D#5':87, 'E5':88, 'F5':89, 'F#5':90, 'G5':91, 'G#5':92, 'A5':93, 'A#5':94, 'B5':95,
    'C6':96, 'C#6':97, 'D6':98, 'D#6':99, 'E6':100,'F6':101,'F#6':102,'G6':103,'G#6':104,'A6':105,'A#6':106,'B6':107,
    'C7':108,'C#7':109,'D7':110,'D#7':111,'E7':112,'F7':113,'F#7':114,'G7':115,'G#7':116,'A7':117,'A#7':118,'B7':119,
    'C8':120,'C#8':121,'D8':122,'D#8':123,'E8':124,'F8':125,'F#8':126,'G8':127
}

WX_APP = 0
WX_IS_INIT = False
logger = logging.Logger('catch_all')

def initWx():
    WX_APP = wx.App()
    WX_IS_INIT = True
    return WX_APP

def loadVST(path, samplerate, blocksize):
    print("Trying to load VST {} with Samplerate {} and Blocksize {}".format(path,samplerate,blocksize))
    plugin = VSTPlugin(path)
    plugin.open()
    plugin.set_sample_rate(samplerate)
    plugin.set_block_size(blocksize)
    return plugin

def raise_gui(plugin, parent_frame = None):
    if WX_IS_INIT == False:
        initWx()
    frame = wx.Frame(parent_frame, -1, plugin.get_name().decode("utf-8"))
    plugin.open_edit(frame.GetHandle())
    rect = plugin.get_erect()
    frame.SetClientSize((rect.right, rect.bottom))
    frame.Show()
    if parent_frame != None: #If an external app tries to open this as a second window: Don't start a new app loop
        WX_APP.MainLoop()

def getDatatype(plugin):
    if plugin.can_process_double():
        datatype = numpy.float64
    else:
        datatype = numpy.float32
    return datatype

def configVST(plugin, parent_frame = None):
    if plugin.has_editor():
        raise_gui(plugin, parent_frame)
        #The plugin should be open now. Setup your effect and close it again :)
        plugin.resume()
    else:
        print("Cannot find GUI of plugin")

def closePlugin(plugin):
    plugin.suspend()

def processEffect(plugin, inputL, inputR = None, input3 = None, input4 = None, padLength = 0):
    #Init Inputs
    input1 = inputL #L
    if inputR is None and plugin.number_of_inputs > 1:
        input2 = input1 #if we need to fill 2 inputs, take first signal for both
    else:
        input2 = inputR
    
    #Zero Padding after sample
    if padLength > 0:
        input1 = AddZeroPadding(input1, numFront=0, numBack=padLength)
        input2 = AddZeroPadding(input2, numFront=0, numBack=padLength)
    
    if plugin.number_of_inputs > 2:
        if input3 is None:
            input3 = numpy.zeros(input1.shape, dtype=getDatatype(plugin))
        if input4 is None:
            input4 = numpy.zeros(input1.shape, dtype=getDatatype(plugin))
    #Check if we have some data in at least the first two signals
    assertIsNonZero(input1)
    assertIsNonZero(input2)
    numSamples = input1.shape[0] # 'Length' of samples
    output = numpy.zeros((plugin.number_of_outputs, numSamples), dtype=getDatatype(plugin))
    #Test if all samples are of same size
    if input2 is not None:
        if not numSamples == input2.shape[0]:
            raise Exception('Excuse me what the fuck, Code: 1!=2')
    if input3 is not None:
        if not numSamples == input3.shape[0]:
            raise Exception('Excuse me what the fuck, Code: 1!=3')        
    if input4 is not None:
        if not numSamples == input4.shape[0]:
            raise Exception('Excuse me what the fuck, Code: 1!=4')
    block_size = plugin.block_size
    for i in range(int(numSamples/block_size)):
        idx_from = i*block_size
        idx_to = (i+1)*block_size
        if plugin.number_of_inputs == 1:
            input_samples = [input1[idx_from:idx_to]]
        if plugin.number_of_inputs == 2:
            input_samples = [input1[idx_from:idx_to], input2[idx_from:idx_to]]
        if plugin.number_of_inputs == 4:
            input_samples = [input1[idx_from:idx_to], input2[idx_from:idx_to], input3[idx_from:idx_to], input4[idx_from:idx_to]]
        plugin.process(input_samples * int(plugin.number_of_inputs / 2), output[:, idx_from:idx_to])
    if plugin.number_of_outputs == 1:
        return output
    if plugin.number_of_outputs == 2:
        return output[0], output[1]
    if plugin.number_of_outputs == 3:
        return output[0], output[1], output[2]
    if plugin.number_of_outputs == 4:
        return output[0], output[1], output[2], output[3]

def processInstrument(plugin, length=None): #length = integer number of samples
    if length is None:
        length = plugin.sample_rate*5 #default = 5 seconds
    pluginIsSomeWeirdFuck = False
    if plugin.number_of_inputs > 0: #I'm looking at you play engine...
        pluginIsSomeWeirdFuck = True
        inputs = numpy.zeros((plugin.number_of_inputs, length), dtype=getDatatype(plugin))
    outputs = numpy.zeros((plugin.number_of_outputs, length), dtype=getDatatype(plugin))
    block_size = plugin.block_size
    for i in range(int(length/block_size)):
        idx_from = i*block_size
        idx_to = (i+1)*block_size
        if pluginIsSomeWeirdFuck:
            plugin.process(inputs[:, idx_from:idx_to],outputs[:, idx_from:idx_to])
        else:
            plugin.process_output(outputs[:, idx_from:idx_to])

    return outputs #variable size depending on choice of numOutputs parameter !

def getCustomMidiEvent(midiData1, midiData2, midiData3, deltaFrames=0):
    #List of MIDI messages: https://www.midi.org/specifications-old/category/reference-tables
    kVstMidiType = 1
    #kVstMidiEventIsRealTime = 1
    midiEvent = VstMidiEvent()
    midiEvent.type = kVstMidiType
    midiEvent.byteSize = 24 #sizeof(VstMidiEvent)
    midiEvent.deltaFrames = deltaFrames #sample frames related to the current block start sample position
    midiEvent.flags = 0 #@see VstMidiEventFlags (kVstMidiEventIsRealtime = 1 << 0 if realtime, i.e. 000...0010
    midiEvent.noteLength = 0 #(in sample frames) of entire note, if available, else 0
    midiEvent.noteOffset = 0 #offset (in sample frames) into note from note start if available, else 0
    midiEvent.midiData1 = midiData1
    midiEvent.midiData2 = midiData2
    midiEvent.midiData3 = midiData3
    midiEvent.midiData4 = (0x00) # reserved (zero)
    midiEvent.detune = 0 #-64 to +63 cents; for scales other than 'well-tempered' ('microtuning')
    midiEvent.noteOffVelocity = 0 #Note Off Velocity [0, 127]
    midiEvent.reserved1 = 0 #zero 
    midiEvent.reserved2 = 0 #zero
    return midiEvent

def getNoteOnEvent(key, velocity=0xFF, channel=1, deltaFrames=0):
    if channel<0 or channel>15 or key<0 or key>127 or velocity<0 or velocity>127: #valid ranges
        raise Exception('Excuse me what the fuck, Code: 0x00>.<0xFF')
    midiData1 = (0x90+(channel-1)) #NoteOn: 0x90...0x9F
    midiData2 = key
    midiData3 = velocity
    return getCustomMidiEvent(midiData1, midiData2, midiData3, deltaFrames=deltaFrames)

def getNoteOffEvent(key, velocity=0, channel=1, deltaFrames=0, type='Aftertouch'):
    if type == 'NoteOnZero':
        #Other interpretation of NoteOff. which is setting NoteOn velocity to zero.
        #But it doesn't allow a release velocity (which may be useful e.g. for good sample libraries with release samples)
        return getNoteOnEvent(key=key,velocity=0,channel=channel)
    else:
        if channel<0 or channel>15 or key<0 or key>127 or velocity<0 or velocity>127: #valid ranges
            raise Exception('Excuse me what the fuck, Code: 0x00>.<0xFF')
        midiData1 = (0x80+(channel-1)) #NoteOff: 0x80...0x8F
        midiData2 = key
        midiData3 = velocity
        return getCustomMidiEvent(midiData1, midiData2, midiData3, deltaFrames=deltaFrames)

def getMidiCCEvent(cc=1, val=127, channel=1, deltaFrames=0):
    if channel<0 or channel>15 or cc<0 or cc>127 or val<0 or val>127: #valid ranges
        raise Exception('Excuse me what the fuck, Code: 0x00>.<0xFF')
    midiData1 = (0xB0+(channel-1)) #CC: 0xB0...0xBF
    midiData2 = cc #1 Mod, 11 Expr, ...
    midiData3 = val
    return getCustomMidiEvent(midiData1, midiData2, midiData3, deltaFrames=deltaFrames)
    
def mergeMidiEvents(midiEventList):
    vstEvents = VstEvents()
    vstEvents.numEvents = len(midiEventList)
    vstEvents.reserved = 0
    for idx,event in enumerate(midiEventList):
        vstEvents.events[idx] = POINTER(VstMidiEvent)(event)
    return vstEvents

def sendMidiEventsToPlugin(plugin, mergedMidiEvents):
    plugin.processEvents(mergedMidiEvents)
    
def isMono(data):
    if data.ndim == 1:
        return True
    elif data.shape[1] == 2:
        return False
    else:
        raise Exception('Excuse me what the fuck, Code: 0xQWERTY')

def assertIsMono(data):
    if not isMono(data):
        raise Exception('Excuse me what the fuck, Code: -1')

def isNonZero(mono_data):
    assertIsMono(mono_data)
    return mono_data[mono_data!=0].shape[0] != 0

def assertIsNonZero(mono_data):
    if not isNonZero(mono_data):
        raise Exception('Excuse me what the fuck, Code: 0.5!=0')    

def isFloat(mono_data):
    assertIsMono(mono_data)
    if mono_data.dtype == numpy.float32 or mono_data.dtype == numpy.float64:
        return True
    else:
        return False
    
def assertIsFloat(mono_data):
    if not isFloat(mono_data):
        raise Exception('Excuse me what the fuck, Code: NUL')

def convert_to_float(mono_data, destination_type=numpy.float32):
    # From SciPy Docu:
    # WAV format                Min        Max            NumPy dtype
    # 32-bit floating-point    -1.0        +1.0            float32
    # 32-bit PCM            -2147483648    +2147483647    int32
    # 16-bit PCM            -32768            +32767        int16
    # 8-bit PCM                0            255            uint8
    # VST processes floats. Let's convert it first
    assertIsMono(mono_data)
    olddatatype = mono_data.dtype
    if olddatatype == destination_type:
        return mono_data, olddatatype
    elif olddatatype == 'int16':
        mono_data = mono_data/32767
    elif olddatatype == 'int32':
        mono_data = mono_data/2147483647
    elif  olddatatype == 'uint8':
        mono_data = mono_data/255
    mono_data = np.array(mono_data, dtype=destination_type)
    return mono_data, olddatatype

def convert_float_to_other_type(mono_data, datatype):
    assertIsMono(mono_data)
    assertIsFloat(mono_data)
    if datatype == 'int16':
        mono_data = mono_data*32767
    elif datatype == 'int32':
        mono_data = mono_data*2147483647
    elif datatype == 'uint8':
        mono_data = mono_data*255
    mono_data = mono_data.round() #minimal quantization error possible. may need some dithering in the end TODO
    mono_data = mono_data.astype(datatype)
    return mono_data

def plot_stft(mono_data, sample_rate):
    assertIsMono(mono_data)
    assertIsFloat(mono_data)
    f, t, Zxx = scipy.signal.stft(mono_data,sample_rate)
    amp = 2 * np.sqrt(2)
    plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=amp)
    #plt.specgram(Zxx, Fs=SAMPLERATE)
    plt.yscale('log', nonposy='clip')
    axes = plt.gca()
    axes.set_ylim([20,20000])
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

def plot_log(data, dataR=None):
    if dataR is None:
        log =20*np.log10(np.abs(data))
        plt.plot(log)
    else:
        logL=20*np.log10(np.abs(data))
        logR=20*np.log10(np.abs(dataR))
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1)
        ax.plot(logL)
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1)
        ax.plot(logR)
    
def resample(mono_data, old_f, new_f):
    assertIsMono(mono_data)
    return resampy.resample(mono_data, old_f, new_f)
    
def AddZeroPadding(mono_data, numFront = 0, numBack = 0):
    assertIsMono(mono_data)
    if numFront == 0 and numBack == 0:
        print("Excuse me now, seriously.. what the fuck are you trying to do?")
        return mono_data
    return np.pad(mono_data, (numFront,numBack), 'constant')

def gateMonoSample(mono_data, trimFront=False, trimBehind=True, onThreshold=-25, offThreshold=-40, prestartDuration=0.005, sample_rate=44100, mode='dBFSR'): #db,db,sec,'dbFSR'or'belowMax'
    assertIsMono(mono_data)
    assertIsFloat(mono_data)
    #take log/calculate level in dB
    log =20*np.log10(np.abs(mono_data))
    if mode == 'belowMax': #referenced to maximal value
        maxValue = max(log)
        log = log - maxValue
    #Thresholding+Slice Sample
    if trimFront:
        threshLogIdx = np.where(log>onThreshold)
        firstThresh = threshLogLIdx[0][0]
        prestart = prestartDuration * sample_rate
        idx = int(firstThresh-prestart)
        if idx < 0:
            idx = 0
        mono_data = mono_data[idx:]
    if trimBehind:
        OffthreshLogIdx = np.where(log>offThreshold)
        lastThresh  = OffthreshLogIdx[0][-1]
        mono_data = data[:lastThresh]
    return mono_data

def gateStereoSample(dataL, dataR, trimFront=False, trimBehind=True, onThreshold=-25, offThreshold=-40, prestartDuration=0.005, sample_rate=44100, mode='dBFSR'): #db,db,sec,'dbFSR'or'belowMax'
    #Gates to the maximum of both sample durations
    assertIsMono(dataL)
    assertIsMono(dataR)
    assertIsFloat(dataL)
    assertIsFloat(dataR)
    #take log/calculate level in dB
    logL =20*np.log10(np.abs(dataL))
    logR =20*np.log10(np.abs(dataR))
    if mode == 'belowMax': #referenced to maximal value
        maxValueL = max(logL)
        maxValueR = max(logR)
        logL = logL - maxValueL
        logR = logR - maxValueR
    #Thresholding+Slice Sample
    if trimFront == True:
        threshLogLIdx = np.where(logL>onThreshold)
        threshLogRIdx = np.where(logR>onThreshold)
        firstThreshL = threshLogLIdx[0][0]
        firstThreshR = threshLogRIdx[0][0]
        firstThresh = min(firstThreshL,firstThreshR)
        prestart = prestartDuration * sample_rate
        idx = int(firstThresh-prestart)
        if idx < 0:
            idx = 0
        dataL = dataL[idx:]
        dataR = dataR[idx:]
    if trimBehind == True:
        OffthreshLogLIdx = np.where(logL>offThreshold)
        OffthreshLogRIdx = np.where(logR>offThreshold)
        lastThreshL  = OffthreshLogLIdx[0][-1]
        lastThreshR  = OffthreshLogRIdx[0][-1]
        lastThresh = max(lastThreshL,lastThreshR)
        dataL = dataL[:lastThresh]
        dataR = dataR[:lastThresh]
    return dataL,dataR

def limitSample(mono_data, valdB=-0.1): #valdB = limit in dB
    assertIsMono(mono_data)
    assertIsFloat(mono_data)
    #calculate amplitude limit from dB Value
    valFloat = 10**(valdB/20)
    #Hard Limit
    mono_data[mono_data>valFloat] = valFloat
    mono_data[mono_data<-valFloat] = -valFloat
    return mono_data    

def getAllAudioDevices(): #will setup  new PyAudio handle
    PYA = pyaudio.PyAudio()
    pya_audio_devices = []
    for i in range(0, PYA.get_device_count()):
        pya_audio_devices.append("ID {} - {}".format(i,PYA.get_device_info_by_index(i).get('name')))
    PYA.terminate()
    return pya_audio_devices

def openPYA():
    PYA = pyaudio.PyAudio()
    return PYA

def closePYA(PYA):
    PYA.terminate()

def getOutputStream(PYA, output_device_id, numChannels, samplerate):
    output_stream = PYA.open(format=pyaudio.paFloat32,
                             channels=numChannels,
                             rate=samplerate,
                             output=True,
                             output_device_index=output_device_id,
                             start=False
                             )
    return output_stream
def closeOutputStream(output_stream):
    output_stream.close()
    
def getInputStream(PYA, input_device_id, numChannels, samplerate, blocksize):
    try:
        input_stream = PYA.open(
            format=pyaudio.paInt16, #we record in int and convert it later to float because the resulting byte stream is broken af. idk man
            channels=numChannels,
            rate=samplerate,
            input=True,
            frames_per_buffer=blocksize,
            input_device_index=input_device_id,
            start=False
        )
        print("Could successfully open audio device!")
        return input_stream
    except:
        #OSError not available
        raise Exception("Error: Couldn't open audio device")

def closeInputStream(input_stream):
    input_stream.stop_stream()
    input_stream.close()
    
def playAudio(np_audio, output_stream=None, output_device_id=0, numChannels=2, samplerate=44100):    
    # Assuming you have a numpy array called np_audio
    np_audio = np_audio.T #transform to other notation
    bytedata = np_audio.astype(np.float32).tostring()
    if output_stream is None:
        PYA = openPYA()
        output_stream = getOutputStream(PYA, output_device_id, numChannels, samplerate)
        output_stream.start_stream()
        output_stream.write(bytedata)
        closeOutputStream(output_stream)
        closePYA(PYA)
    else:
        output_stream.start_stream()
        output_stream.write(bytedata)
        output_stream.stop_stream()
    
def recordAudio(duration, input_stream=None, input_device_id=0, numChannels=2, samplerate=44100, blocksize=1024): #dur in sec
    ownStream = not input_stream is None
    if not ownStream:
        print("getting device info")
        PYA = pyaudio.PyAudio()
        input_stream = getInputStream(PYA, input_device_id, numChannels, samplerate, blocksize)
        
    input_stream.start_stream()
    
    frames = []
    numBlocks = int(math.ceil(duration * samplerate / blocksize))
    print("recording...")
    for i in range(0, numBlocks):
        data = input_stream.read(blocksize)
        frames.append(data)
        
    if not ownStream:
        closeInputStream(input_stream)
        closePYA(PYA)
    else:
        input_stream.stop_stream()
        
    print("converting...")
    
    framesAll = b''.join(frames) #merged block list
    result = np.fromstring(framesAll, dtype=np.int16) # [CH1 CH2 ...] concatenated
    chunk_length = int(result.shape[0] / numChannels)
    result = np.reshape(result, (chunk_length, numChannels))

    if isMono(result):
        result_float = convert_to_float(result, destination_type=numpy.float32)
    else:
        result_float = np.zeros(result.shape, dtype = numpy.float32);
        for i in range(0,result.shape[1]):
            result_float[:,i] = convert_to_float(result[:,i], destination_type=numpy.float32)[0]
        #result_float = np.array(result_float)
        #result_float = result_float.reshape(result_float.shape,order='A')
        
        #TODO find a fany solution for any amount of channels. indexing gets weird. somehow result_float[1] doesn't results in first channel like the loaded .wav files or the VSTi samples did.... wtf numpy
        #if numChannels == 2:
        #    return np.array([result_float[:,0], result_float[:,1]])
        #if numChannels == 3:
        #    return np.array([result_float[:,0], result_float[:,1], result_float[:,2]])
        #if numChannels == 4:
        #    return np.array([result_float[:,0], result_float[:,1], result_float[:,2], result_float[:,3]])
        #if numChannels == 5:
        #    return np.array([result_float[:,0], result_float[:,1], result_float[:,2], result_float[:,3], result_float[:,4]])
        #if numChannels == 6:
        #    return np.array([result_float[:,0], result_float[:,1], result_float[:,2], result_float[:,3], result_float[:,4], result_float[:,5]])
    print("done...")
    return result_float.T #transpose to numpy notation

#def play_wav_file(filepath, block_size):
#    PYA = pyaudio.PyAudio()
#    wf = wave.open(filepath, 'rb') #read mode
#    stream = PYA.open(format=PYA.get_format_from_width(wf.getsampwidth()),
#                    channels=wf.getnchannels(),
#                    rate=wf.getframerate(),
#                    output=True)
#    dataframes = wf.readframes(block_size)
#    while dataframes != '':
#        stream.write(dataframes)
#        dataframes = wf.readframes(block_size)
#    stream.stop_stream()
#    stream.close()
#    PYA.terminate()



#def zeroTrimStereoSample(dataL, dataR, trimFront = False, trimBack = True):
#    assertIsMono(dataL)
#    assertIsMono(dataR)
#    datatype = numpy.float32 #just assume it here. Doesn't make a big difference here
#    dataL[np.abs(dataL) < 10*np.finfo(datatype).eps] = 0 #set very small values to zero
#    dataR[np.abs(dataR) < 10*np.finfo(datatype).eps] = 0
#    #if trimFront: # fix padding first TODO
#    #    dataL = numpy.trim_zeros(dataL,'f')
#    #    dataR = numpy.trim_zeros(dataR,'f')
#    if trimBack:
#        dataL = numpy.trim_zeros(dataL,'b')
#        dataR = numpy.trim_zeros(dataR,'b')
#    maxlength = max(dataL.shape[0],dataR.shape[0]) #both are not same size not. fill the shorter one with zeros
#    dataL = np.pad(dataL,(0,maxlength-dataL.shape[0]),'constant')
#    dataR = np.pad(dataR,(0,maxlength-dataR.shape[0]),'constant')
#    return dataL, dataR
