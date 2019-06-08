#!/usr/bin/env python
# coding: utf-8

# # TARTARUS TOOLS
#  Exported from Tartarus_Sampling.ipynb. Don't edit Tartarus_Sampling.py

# ### TODO/Ideas
# 
# - Save all variables to save file when start recording
# - Accept changes automatically when preview/record start
# - add audio stream readys to evaluations and logging
# - allow vsti mode without audio output setup
# - Only show Open GUI button after VST loaded
# - checkboxes for thresholds/limiting
# - preview -> add stft plot gui of variable channel/stream number and playback option (https://matplotlib.org/gallery/user_interfaces/embedding_in_wx5_sgskip.html)
# - (try realtime processing -> after recording pass block of stream directly to plugins?)
# - add checkbox to show stft plots in new frames after recording/preview
# - add template string for saving to GUI
# - after round robins: GUI with stft plots and playback options -> happy? yes/no (master solution: adjustable threshold slider but damn that would take too long..)
# - add checkbox for asking if happy about recording
# - quiet beep sound/color change for start of recording/next note
# - display: round robin 3 / 5
# - selection in what order to iterate through sampling query, e.g. as input "vel->mw->rr"
# - allow to give names: vel<30 -> "pp", vel>100 -> "ff"
# - (allow any Midi CC bind. generalize concept to own gui/selection of parameters and mapping)
# - allow different/shifted mappings. e.g. C3 played but saved as C2. Or match velocity to mw  etc..

# In[1]:


from ProcessingFunctions import *
import guis.lib_recorder_gui
import guis.audio_settings_gui
import time
import rtmidi

module = sys.modules[__name__] #current module to save global parameters
WX_APP = initWx() # This will run wx.App() - Only to be run once (in Jupyter)

#Global Variables
module.MY_LIB_NAME = None
module.SAVE_DIR = None
module.MY_SAMPLE_PREFIX = None
module.SAMPLERATE = 44100
PYVST_SAMPLERATE = module.SAMPLERATE
module.BLOCKSIZE = 2048
PYVST_BLOCKSIZE = module.BLOCKSIZE
module.SAMPLE_DURATION = 5.0
module.BEHIND_ZERO_PADDING = 5.0
module.PRE_START = 5.0

#AUDIO DEVICE SETTINGS
module.PYA = None
module.PYA_INPUT_DEVICE_INDEX = 0
module.PYA_INPUT_CHANNELS = 2
module.PYA_OUTPUT_DEVICE_INDEX = 0
module.PYA_OUTPUT_CHANNELS = 2
module.AUDIO_INPUT_IS_ACTIVE = False
module.AUDIO_INPUT_READY = False
module.AUDIO_INPUT_STREAM = None
module.AUDIO_OUTPUT_IS_ACTIVE = False
module.AUDIO_OUTPUT_READY = False
module.AUDIO_OUTPUT_STREAM = None

#GUI Settings
module.GUI_BUTTON_DEFAULT_COLOR = (200,200,200)
module.GUI_BUTTON_RECORDING_COLOR = (255,0,0)

# Input Variables
class INPUT_TYPE(Enum):
    VSTI = 0
    LIVE_REC = 1
    MIDI_REC = 2
module.INPUT_MODE = INPUT_TYPE.VSTI
module.FROM_NOTE = "C-2"
module.TO_NOTE = "G8"
module.VELOCITY_STEPS = [30,90,127]
module.VELOCITY_RANGES = [[0,45],[46,90],[91,127]]
module.MOD_WHEEL_STEPS = [30, 127]
module.ROUND_ROBINS = 3
module.VST_INSTRUMENT = None #where the loaded vst will be stored
module.VST_INSTRUMENT_PATH = ""
module.MIDI_OUT_DEVICE_ID = 0
module.MIDI_IN_DEVICE_ID = 0
module.RR_ERROR_COUNTER = 0
module.KEY_ERROR_COUNTER = 0
module.USE_VSTI_AS_TUNER = False

#Post Processing Variables
module.ON_THRESHOLD = -40 #for recorded input
module.OFF_THRESHOLD = -80 #everytime
module.FX_VST1 = None
module.FX_VST1_PATH = ""
module.FX_VST1_IS_ACTIVE = False
module.FX_VST2 = None
module.FX_VST2_PATH = ""
module.FX_VST2_IS_ACTIVE = False
module.FX_VST3 = None
module.FX_VST3_PATH = ""
module.FX_VST3_IS_ACTIVE = False
module.FX_VST4 = None
module.FX_VST4_PATH = ""
module.FX_VST4_IS_ACTIVE = False
module.FX_VST5 = None
module.FX_VST5_PATH = ""
module.FX_VST5_IS_ACTIVE = False

#Tests if variables are set correctly. See assert_all_important_vars_are_set() (I know this is ugly but it works for now. I don't want some runtime errors because of a typo..)
module.evaluation = False
module.eval_a = False
module.eval_b = False
module.eval_c = False
module.eval_d = False
module.eval_e = False
module.eval_f = False
module.eval_g = False
module.eval_h = False
module.eval_i = False
module.eval_j = False
module.eval_k = False
module.eval_l = False
module.eval_a2 = False
module.eval_b2 = False
module.eval_c2 = False
module.eval_a3 = False
module.eval_b3 = False
module.eval_a4 = False

module.midiout = rtmidi.MidiOut()
available_ports = module.midiout.get_ports()

print("Available MIDI Ports")
print(available_ports)


# In[2]:


def print_all_vars():
    print("###############################")
    print("Printing all accepted variables")
    
    #Global Variables
    print("\nGlobal:\n")
    print("Var name | Value")
    print(" = ".join(["Samplerate",str(module.SAMPLERATE)]))
    print(" = ".join(["Blocksize",str(module.BLOCKSIZE)]))
    print(" = ".join(["InputMode",str(module.INPUT_MODE)]))
    
    print("\nConfiguration:\n")
    print("Var name | Value | Correct Input Type?")
    print(" | ".join(["LibName",module.MY_LIB_NAME,str(module.eval_a)]))
    print(" | ".join(["SaveDir",module.SAVE_DIR,str(module.eval_b)]))
    print(" | ".join(["SamplePrefix",module.MY_SAMPLE_PREFIX,str(module.eval_c)]))
    print(" | ".join(["SampleDuration",str(module.SAMPLE_DURATION),str(module.eval_d)]))
    print(" | ".join(["BehindZeroPadding",str(module.BEHIND_ZERO_PADDING),str(module.eval_e)]))
    print(" | ".join(["FromNote",module.FROM_NOTE,str(module.eval_f)]))
    print(" | ".join(["ToNote",module.TO_NOTE,str(module.eval_g)]))
    print(" | ".join(["VelocitySteps",str(module.VELOCITY_STEPS),str(module.eval_h)]))
    print(" | ".join(["VelocityRanges",str(module.VELOCITY_RANGES),str(module.eval_i)]))
    print(" | ".join(["MWSteps",str(module.MOD_WHEEL_STEPS),str(module.eval_j)]))
    print(" | ".join(["RoundRobins",str(module.ROUND_ROBINS),str(module.eval_k)]))
    print(" | ".join(["OffThresh",str(module.OFF_THRESHOLD),str(module.eval_l)]))
    
    if module.INPUT_MODE == INPUT_TYPE.VSTI:
        print(" | ".join(["VSTiPath",module.VST_INSTRUMENT_PATH,str(module.eval_a2)]))
        print(" | ".join(["VSTi",str(module.VST_INSTRUMENT),str(module.eval_b2)]))
        print(" | ".join(["MidiInDevice",str(module.MIDI_IN_DEVICE_ID),str(module.eval_c2)]))
    
    if module.INPUT_MODE == INPUT_TYPE.LIVE_REC:
        print(" | ".join(["PreStart",str(module.PRE_START),str(module.eval_a3)]))
        print(" | ".join(["OnThresh",str(module.ON_THRESHOLD),str(module.eval_b3)]))
    if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
        print(" | ".join(["MidiOutDevice",str(module.MIDI_OUT_DEVICE_ID),str(module.eval_a4)]))
    
    print("\nPost Processing VSTs:\n")
    print("Var name | Value")
    print(" = ".join(["VST1",str(module.FX_VST1)]))
    print(" = ".join(["VST1Path",str(module.FX_VST1_PATH)]))
    print(" = ".join(["VST1isActive",str(module.FX_VST1_IS_ACTIVE)]))
    print(" = ".join(["VST2",str(module.FX_VST2)]))
    print(" = ".join(["VST2Path",str(module.FX_VST2_PATH)]))
    print(" = ".join(["VST2isActive",str(module.FX_VST2_IS_ACTIVE)]))
    print(" = ".join(["VST3",str(module.FX_VST3)]))
    print(" = ".join(["VST3Path",str(module.FX_VST3_PATH)]))
    print(" = ".join(["VST3isActive",str(module.FX_VST3_IS_ACTIVE)]))
    print(" = ".join(["VST4",str(module.FX_VST4)]))
    print(" = ".join(["VST4Path",str(module.FX_VST4_PATH)]))
    print(" = ".join(["VST4isActive",str(module.FX_VST4_IS_ACTIVE)]))
    print(" = ".join(["VST5",str(module.FX_VST5)]))
    print(" = ".join(["VST5Path",str(module.FX_VST5_PATH)]))
    print(" = ".join(["VST5isActive",str(module.FX_VST5_IS_ACTIVE)]))
    print("###############################")

def assert_all_important_vars_are_set():
    try:
        print("Evaluating global config")
        module.eval_a = type(module.MY_LIB_NAME) == str and module.MY_LIB_NAME != ""
        module.eval_b = type(module.SAVE_DIR) == str and module.SAVE_DIR != "" and os.path.isdir(module.SAVE_DIR)
        module.eval_c = type(module.MY_SAMPLE_PREFIX) == str and module.MY_SAMPLE_PREFIX != ""
        module.eval_d = type(module.SAMPLE_DURATION) == float and module.SAMPLE_DURATION > 1.0
        module.eval_e = type(module.BEHIND_ZERO_PADDING) == float and module.BEHIND_ZERO_PADDING >= 0.0
        
        print("Evaluating global input config")
        module.eval_f = type(module.FROM_NOTE) == str and module.FROM_NOTE != ""
        module.eval_g = type(module.TO_NOTE) == str and module.TO_NOTE != ""
        module.eval_h = type(module.VELOCITY_STEPS) == list and type(module.VELOCITY_STEPS[0]) == int
        module.eval_i = type(module.VELOCITY_RANGES) == list and type(module.VELOCITY_RANGES[0]) == list and type(module.VELOCITY_RANGES[0][0]) == int
        module.eval_j = type(module.MOD_WHEEL_STEPS) == list and type(module.MOD_WHEEL_STEPS[0]) == int
        module.eval_k = type(module.ROUND_ROBINS) == int and module.ROUND_ROBINS >= 1
        
        print("Evaluating global processing config")
        module.eval_l = (type(module.OFF_THRESHOLD) == float or type(module.OFF_THRESHOLD) == int) and module.OFF_THRESHOLD <= 0 
       
        print("Merge evaluations")
        module.evaluation = module.eval_a and module.eval_b and module.eval_c and module.eval_d and module.eval_e and module.eval_f and module.eval_g and module.eval_h
        module.evaluation = module.evaluation and module.eval_i and module.eval_j and module.eval_k and module.eval_l
        
        print(module.evaluation)
        
        print("Input mode switch")
        if module.INPUT_MODE == INPUT_TYPE.VSTI:
            print("Type: VSTi specific config")
            module.eval_a2 = type(module.VST_INSTRUMENT_PATH) == str and module.VST_INSTRUMENT_PATH != ""
            module.eval_b2 = type(module.VST_INSTRUMENT) == VSTPlugin
            module.eval_c2 = type(module.MIDI_IN_DEVICE_ID) == int and module.MIDI_IN_DEVICE_ID >= 0
            print("Merge evaluations")
            module.evaluation = module.evaluation and module.eval_a2 and module.eval_b2
            print(module.evaluation)

        if module.INPUT_MODE == INPUT_TYPE.LIVE_REC:
            print("Type: Live_Rec specific config")
            module.eval_a3 = type(module.PRE_START) == float and module.PRE_START >= 0.0
            module.eval_b3 = (type(module.ON_THRESHOLD) == float or type(module.ON_THRESHOLD) == int) and module.ON_THRESHOLD <= 0 
            print("Merge evaluations")
            module.evaluation = module.evaluation and module.eval_a3 and module.eval_b3
            module.evaluation = module.evaluation and module.AUDIO_INPUT_READY
            print(module.evaluation)
            
        if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
            print("Type: Midi_Rec specific config")
            module.eval_a3 = type(module.PRE_START) == float and module.PRE_START >= 0.0
            module.eval_b3 = (type(module.ON_THRESHOLD) == float or type(module.ON_THRESHOLD) == int) and module.ON_THRESHOLD <= 0 
            module.eval_a4 = type(module.MIDI_OUT_DEVICE_ID) == int and module.MIDI_OUT_DEVICE_ID >= 0
            print("Merge evaluations")
            module.evaluation = module.evaluation and module.eval_a3 and module.eval_b3
            module.evaluation = module.evaluation and module.eval_a4
            module.evaluation = module.evaluation and module.AUDIO_INPUT_READY
            print(module.evaluation)
        
        module.evaluation = module.evaluation and module.AUDIO_OUTPUT_READY
        print(module.evaluation)
        
        print("Evaluations successful")
        return module.evaluation
    except:
        print("Error during evaluation. This may be a e.g. caused by a datatype incompatibility problem")
        return False


# In[3]:


def save_all_vars():
    print("TODO save to file")


# In[4]:


#general helper to add to ProcessingFunction.py
def sendMIDIOut(vars):
    #getLiveRecording
    print("TODO")


# In[5]:


def happyWithResult(libRecordFrame):
    print("TODO")
    return True

def startSampling(libRecordFrame):
    #disable GUI interaction while recording?
    
    #Get subset of notes we want to sample
    key_range = [module.FROM_NOTE, module.TO_NOTE]
    fromIdx = 0
    toIdx = 127
    keys = list(MIDI_KEY.keys())
    for idx,curKey in enumerate(keys):
        if curKey == key_range[0]: #Lowest note we want to sample
            fromIdx = idx
        if curKey == key_range[1]: #Highest note we want to sample
            toIdx = idx+1 #because that's how pythons list index subscripts works bitch (see next line)
    keys = keys[fromIdx:toIdx]
    sub_midi_dict = {k:v for k,v in MIDI_KEY.items() if k in keys}
    
    print("Starting sampling process for following values:")
    print("Key Range:")
    print(key_range,[fromIdx,toIdx])
    print("Velocity Steps:")
    print(module.VELOCITY_STEPS)
    print("Mod Wheel Steps:")
    print(module.MOD_WHEEL_STEPS)
    print("Num Round Robins")
    print(range(1,module.ROUND_ROBINS+1))
    
    #if vsti should do something
    #-> let it play any note of our defined set firstly as initalization
    # because it's sometimes weird for some plugins (Kontakt)
    if module.USE_VSTI_AS_TUNER or module.INPUT_MODE == INPUT_TYPE.VSTI:
        nextMidiInstrumentRecording(next(iter(sub_midi_dict.values())), module.VELOCITY_STEPS[-1], module.MOD_WHEEL_STEPS[-1], rr=0, postprocess = False) #do something
    
    if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
        print("setting up midi out device")
        module.midiout = rtmidi.MidiOut()
        module.midiout.open_port(module.MIDI_OUT_DEVICE_ID)
    
    for key_name, key_value in sub_midi_dict.items():
    #e.g.: key_name,key_value = G2, 55 ...
        for velocity in module.VELOCITY_STEPS:
            for mw in module.MOD_WHEEL_STEPS:
                while True:
                    module.RR_ERROR_COUNTER = 0
                    
                    if module.INPUT_MODE == INPUT_TYPE.LIVE_REC and module.USE_VSTI_AS_TUNER:
                        print("Tuning")
                        libRecordFrame.updateNoteValues(key_name, str(velocity), "Tuner", str(mw))
                        tunerData = nextMidiInstrumentRecording(key_value, velocity, mw, rr=0, postprocess = False)
                        print(tunerData)
                        if tunerData is not None:
                            playAudio(tunerData,module.AUDIO_OUTPUT_STREAM)
                        else:
                            print("Couldn't gather samples from tuner VSTi")
                        
                    
                    for rr in range(1,module.ROUND_ROBINS+1):
                        libRecordFrame.updateNoteValues(key_name, str(velocity), str(rr), str(mw))
                        print("Key:{} Velocity:{} MW:{} RR:{}".format(key_name,str(velocity),str(mw),str(rr)))
                        
                        #GET INPUT
                        data = gatherInputData(key_value, velocity, mw, rr)
                        print(data)
                        if data is None:
                            module.RR_ERROR_COUNTER = module.RR_ERROR_COUNTER + 1
                            print("No output received...")
                            continue
                        
                        #APPLY EFFECTS AND POST PROCESSING
                        data = postProcess(data)
                        print(data)
                        if data is None:
                            module.RR_ERROR_COUNTER = module.RR_ERROR_COUNTER + 1
                            print("FX Chain blocked output...")
                            continue
                        
                        #SAVE
                        saveData(data, key_name, velocity, mw, rr)
                        
                    if module.INPUT_MODE != INPUT_TYPE.LIVE_REC:
                        break
                    else:
                        if happyWithResult(libRecordFrame):
                            break
                        if module.RR_ERROR_COUNTER > 3: #Give it three full runs on one note..
                            module.KEY_ERROR_COUNTER = module.KEY_ERROR_COUNTER + 1 #e.g. missing note in instrument or failure to get any sound of configuration
                            print("KeyError {} during sampling process...".format(key_name))
                            break

def nextMidiInstrumentRecording(key_value, velocity, mw, rr, postprocess = True):
    #Note On Event
    midiEvent1 = getNoteOnEvent(key=key_value, velocity=velocity, deltaFrames=0, channel=1)
    midiEvent2 = getMidiCCEvent(cc=1, val=mw, channel=1, deltaFrames=0)

    #Merge MidiEvents to VstEventList
    midiEventList = []
    midiEventList.append(midiEvent1)
    midiEventList.append(midiEvent2)
    mergedMidiEvents = mergeMidiEvents(midiEventList)

    #Send events to plugin
    sendMidiEventsToPlugin(module.VST_INSTRUMENT, mergedMidiEvents)
    
    sampleDuration = int(round(module.SAMPLE_DURATION*module.SAMPLERATE))
    output = processInstrument(module.VST_INSTRUMENT, length=sampleDuration)
    
    #Send note-off and process (just in case to supress any form of reverb/feedback from previous note)
    midiEvent3 = getNoteOffEvent(key=key_value, velocity=velocity, deltaFrames=0, channel=1)
    midiEvent4 = getNoteOnEvent(key=key_value, velocity=0, deltaFrames=0, channel=1) #Do both types of note-offs
    midiEventList = []
    midiEventList.append(midiEvent3)
    midiEventList.append(midiEvent4)
    mergedMidiEvents = mergeMidiEvents(midiEventList)
    sendMidiEventsToPlugin(module.VST_INSTRUMENT, mergedMidiEvents)
    outputTrash = processInstrument(module.VST_INSTRUMENT, length=sampleDuration) #don't save this output :p
    
    outputdata = np.array([output[0],output[1]])
    
    if isNonZero(output[0]) == False and  isNonZero(output[1]) == False:
        return None #This is wrong/missing data. We set it to zero so it's easier to detect in the upper layer
    
    return np.array([output[0],output[1]])
            
def nextLiveRecording(key_value, velocity, mw, rr):
    sampleDuration = module.PRE_START + module.SAMPLE_DURATION
    dry_recording = recordAudio(sampleDuration,module.AUDIO_INPUT_STREAM)
    
    if isNonZero(dry_recording[0]) == False and  isNonZero(dry_recording[1]) == False:
        return None #This is wrong/missing data. We set it to zero so it's easier to detect in the upper layer
    
    return dry_recording
    
def nextMidiOutRecording(key_value, velocity, mw, rr):
    print("SEND MIDI VALUE THROUGH MIDI PORT")
    sampleDuration = module.PRE_START + module.SAMPLE_DURATION
    note_on = [0x90, key_value, velocity]
    note_off = [0x80, key_value, velocity]
    module.midiout.send_message(note_on)
    
    dry_recording = recordAudio(sampleDuration,module.AUDIO_INPUT_STREAM)
    
    if isNonZero(dry_recording[0]) == False and  isNonZero(dry_recording[1]) == False:
        module.midiout.send_message(note_off)
        return None #This is wrong/missing data. We set it to zero so it's easier to detect in the upper layer
    
    time.sleep(sampleDuration)
    midiout.send_message(note_off)
    
    return dry_recording
    
def gatherInputData(key_value, velocity, mw, rr):
    if module.INPUT_MODE == INPUT_TYPE.VSTI:
        return nextMidiInstrumentRecording(key_value, velocity, mw, rr)
    if module.INPUT_MODE == INPUT_TYPE.LIVE_REC:
        return nextLiveRecording(key_value, velocity, mw, rr)
    if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
        return nextMidiOutRecording(key_value, velocity, mw, rr)
    
def postProcess(data):
    data_L,data_R = data[0],data[1]
    
    #ZeroPadding
    padLength = int(round(module.BEHIND_ZERO_PADDING*module.SAMPLERATE))
    data_L = AddZeroPadding(data_L, numFront=0, numBack=padLength)
    data_R = AddZeroPadding(data_R, numFront=0, numBack=padLength)
    
    #FX1-5
    if module.FX_VST1_IS_ACTIVE:
        if type(module.FX_VST1) == VSTPlugin:
            data_L,data_R = processEffect(module.FX_VST1, inputL = data_L, inputR = data_R, padLength = padLength)
    if module.FX_VST2_IS_ACTIVE:
        if type(module.FX_VST2) == VSTPlugin:
            data_L,data_R = processEffect(module.FX_VST2, inputL = data_L, inputR = data_R, padLength = 0)
    if module.FX_VST3_IS_ACTIVE:
        if type(module.FX_VST3) == VSTPlugin:
            data_L,data_R = processEffect(module.FX_VST3, inputL = data_L, inputR = data_R, padLength = 0)
    if module.FX_VST4_IS_ACTIVE:
        if type(module.FX_VST4) == VSTPlugin:
            data_L,data_R = processEffect(module.FX_VST4, inputL = data_L, inputR = data_R, padLength = 0)
    if module.FX_VST5_IS_ACTIVE:
        if type(module.FX_VST5) == VSTPlugin:
            data_L,data_R = processEffect(module.FX_VST5, inputL = data_L, inputR = data_R, padLength = 0)
    #Outputs should be nonzero (If zero.. well.. tihange will explore and rip the world :( )
    if isNonZero(data_L) == False or isNonZero(data_R) == False:
        return None #This is wrong/missing data. We set it to zero so it's easier to detect in the upper layer
    
    #Gating
    data_L,data_R = gateStereoSample(data_L,data_R,trimFront=False, trimBehind=True, offThreshold=module.OFF_THRESHOLD, mode='dBFSR')
    
    #Some final limiting
    data_L = limitSample(data_L, valdB=-0.1)
    data_R = limitSample(data_R, valdB=-0.1)
    
    return np.array([data_L,data_R])
    
def saveData(data, key_name, velocity, mw, rr):
    velRange = module.VELOCITY_RANGES[module.VELOCITY_STEPS.index(velocity)]
    savefilepath = '_'.join([''.join([module.SAVE_DIR,module.MY_SAMPLE_PREFIX]),key_name,str(velRange[0]),str(velRange[1]),'rr{}mw{}.wav'.format(rr,mw)])
    outputdata = np.array([data[0], data[1]]).T
    scipy.io.wavfile.write(savefilepath, module.SAMPLERATE, outputdata)

def setupAudioStreams():
    #force open new pyaudio instance
    try:
        closePYA(module.PYA)
    except:
        pass
    
    module.PYA = openPYA()
    
    #if both are the same device and should be active:
    if module.PYA_INPUT_DEVICE_INDEX == module.PYA_OUTPUT_DEVICE_INDEX:
        if module.AUDIO_INPUT_IS_ACTIVE and module.AUDIO_OUTPUT_IS_ACTIVE:
            print("Trying to open input+output device {} with {} channels".format(module.PYA_INPUT_DEVICE_INDEX,module.PYA_INPUT_CHANNELS))
            module.AUDIO_INPUT_STREAM = getStream(module.PYA, module.PYA_INPUT_DEVICE_INDEX, module.PYA_INPUT_CHANNELS, module.SAMPLERATE, module.BLOCKSIZE, isInput=True, isOutput=True)
            module.AUDIO_OUTPUT_STREAM = module.AUDIO_INPUT_STREAM #share the same stream
            module.AUDIO_INPUT_READY = True
            module.AUDIO_OUTPUT_READY = True
            return
        
    if module.AUDIO_INPUT_IS_ACTIVE:
        print("Trying to open input device {} with {} channels".format(module.PYA_INPUT_DEVICE_INDEX,module.PYA_INPUT_CHANNELS))
        module.AUDIO_INPUT_STREAM = getStream(module.PYA, module.PYA_INPUT_DEVICE_INDEX, module.PYA_INPUT_CHANNELS, module.SAMPLERATE, module.BLOCKSIZE, isInput=True, isOutput=False)
        module.AUDIO_INPUT_READY = True
        
    if module.AUDIO_OUTPUT_IS_ACTIVE:
        print("Trying to open output device {} with {} channels".format(module.PYA_OUTPUT_DEVICE_INDEX,module.PYA_OUTPUT_CHANNELS))
        module.AUDIO_OUTPUT_STREAM = getStream(module.PYA, module.PYA_OUTPUT_DEVICE_INDEX, module.PYA_OUTPUT_CHANNELS, module.SAMPLERATE, module.BLOCKSIZE, isInput=False, isOutput=True)
        module.AUDIO_OUTPUT_READY = True
        
def previewDry(frame):
    print("TODO switch input mode case")
    if module.AUDIO_INPUT_READY and module.AUDIO_OUTPUT_READY:
        duration = 5 #sec
        
        if module.INPUT_MODE == INPUT_TYPE.VSTI:
            print("TODO")
            return
        if module.INPUT_MODE == INPUT_TYPE.LIVE_REC:
            dry_recording = recordAudio(duration,module.AUDIO_INPUT_STREAM)
        if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
            print("TODO")
            return
        
        print("TODO print stft")
        playAudio(dry_recording,module.AUDIO_OUTPUT_STREAM)
    else:
        print("AUDIO STREAMS NOT READY")
    
def previewWet(frame):
    print("TODO switch input mode case")
    if module.AUDIO_INPUT_READY and module.AUDIO_OUTPUT_READY:
        duration = 5 #sec
        
        if module.INPUT_MODE == INPUT_TYPE.VSTI:
            print("TODO")
            return
        if module.INPUT_MODE == INPUT_TYPE.LIVE_REC:
            dry_recording = recordAudio(duration,module.AUDIO_INPUT_STREAM)
        if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
            print("TODO")
            return
        
        wet_recording = postProcess(dry_recording)
        print("TODO print stft")
        playAudio(wet_recording,module.AUDIO_OUTPUT_STREAM)
    else:
        print("AUDIO STREAMS NOT READY")


# In[6]:


#SubMenu: audio config
class AudioSettingsFrame(guis.audio_settings_gui.AudioDeviceSettingsGUI):
    def __init__(self, parent):
        #initialize parent class
        guis.audio_settings_gui.AudioDeviceSettingsGUI.__init__(self,parent)
        self.parent = parent
        self.SetWindowStyle(wx.STAY_ON_TOP)
        devices = getAllAudioDevices()
        for d in devices:
            self.wxListInputDevices.Append(d)
            self.wxListOutputDevices.Append(d)
        try:
            self.wxListInputDevices.SetSelection(module.PYA_INPUT_DEVICE_INDEX)
            self.wxListOutputDevices.SetSelection(module.PYA_OUTPUT_DEVICE_INDEX)
        except:
            pass
        self.Show()
        
    def onAccept( self, event ):
        try:
            self.onKillAudioDevices("")
            module.AUDIO_INPUT_IS_ACTIVE = self.wxIsInputActive.IsChecked()
            module.AUDIO_OUTPUT_IS_ACTIVE =self.wxIsOutputActive.IsChecked()
            module.PYA_INPUT_DEVICE_INDEX = self.wxListInputDevices.GetSelection()
            module.PYA_INPUT_CHANNELS = int(self.wxNumInputChannels.GetValue())
            module.PYA_OUTPUT_DEVICE_INDEX = self.wxListOutputDevices.GetSelection()
            module.PYA_OUTPUT_CHANNELS = int(self.wxNumOutputChannels.GetValue())
            setupAudioStreams()
            self.Close()
        except Exception as e:
            logger.exception('Failed: ' + str(e))
            box = wx.MessageDialog(None,"Error while parsing. Check log", "Parse Error", wx.OK)
            box.ShowModal()
            box.Destroy()
            
    def onKillAudioDevices( self, event ):
        #if both are the same device and should be active:
        if module.PYA_INPUT_DEVICE_INDEX == module.PYA_OUTPUT_DEVICE_INDEX:
            if module.AUDIO_INPUT_IS_ACTIVE and module.AUDIO_OUTPUT_IS_ACTIVE:
                closeInputStream(module.AUDIO_INPUT_STREAM) # since it's the same stream we can just close one of them
                module.AUDIO_INPUT_READY = False
                module.AUDIO_INPUT_STREAM = None
                module.AUDIO_OUTPUT_READY = False
                module.AUDIO_OUTPUT_STREAM = None
                
        if module.AUDIO_INPUT_READY or module.AUDIO_INPUT_STREAM is not None:
            closeInputStream(module.AUDIO_INPUT_STREAM)
            module.AUDIO_INPUT_READY = False
            module.AUDIO_INPUT_STREAM = None
        if module.AUDIO_OUTPUT_READY or module.AUDIO_OUTPUT_STREAM is not None:
            closeOutputStream(module.AUDIO_OUTPUT_STREAM)
            module.AUDIO_OUTPUT_READY = False
            module.AUDIO_OUTPUT_STREAM = None
        if module.PYA is not None:
            closePYA(module.PYA)
        

#Define frame and its behavior for the VST windows
class VSTChildFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, size=(150,100), title='VST FX Frame')
        self.parent = parent
        
    def openVST(self, plugin):
        print(self.GetHandle())
        plugin.open_edit(self.GetHandle())
        rect = plugin.get_erect()
        self.SetClientSize((rect.right, rect.bottom))
        self.SetTitle(plugin.get_name().decode("utf-8"))
        self.Show()
        
    def OnClose(self, event):
        #self.Hide()
        self.Close()

#A derived class from our GUI class that we created with the wxFormBuilder
class LibRecordFrame(guis.lib_recorder_gui.LibRecorderGUI):
    def __init__(self, parent):
        #initialize parent class
        guis.lib_recorder_gui.LibRecorderGUI.__init__(self,parent)
        
        self.isInit = False
        
        self.onInputeModeChange(0) #hide some items depending on the input mode
        
        bitmap = wx.Bitmap('guis\img\splash.png', wx.BITMAP_TYPE_PNG)

        splash = wx.adv.SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                     6000, None, -1, wx.DefaultPosition, wx.DefaultSize,
                                     wx.BORDER_SIMPLE | wx.STAY_ON_TOP)
        wx.Yield()
        
        time.sleep(2) # don't open audio settings instantly..
        
        self.audioSettingsFrame = AudioSettingsFrame(self)
        self.audioSettingsFrame.Show(True)
        
        self.isInit = True
    
    def toInt(self, myString):
        try:
            myInt = int(myString);
            return myInt
        except ValueError:
            print("Int Value Error:")
            print(myString)
            box = wx.MessageDialog(None,"Attribute {} is not an Integer".format(myString), "Int Value Error", wx.OK)
            box.ShowModal()
            box.Destroy()
            return int(0)
    
    def toFloat(self, myString):
        try:
            myFloat = float(myString);
            return myFloat
        except ValueError:
            print("Float Value Error:")
            print(myString)
            box = wx.MessageDialog(None,"Attribute {} is not an Float".format(myString), "Float Value Error", wx.OK)
            box.ShowModal()
            box.Destroy()
            return float(0)
    
    def str2bool(self, myString):
        return myString.lower() in ("yes", "true", "1", "y", "Ja", "j")
    
    def assert_all_important_vars_are_set(self):
        if module.assert_all_important_vars_are_set() == False:
            box = wx.MessageDialog(None,"Some values are not set correctly. Check log", "Parameter Error", wx.OK)
            box.ShowModal()
            box.Destroy()
            return False
        return True
    
    def updateNoteValues(self, noteString=".", velocityString=".", roundRobinString=".", modWheelString="."):
        # why is it so hard to update some values while executing...
        self.wxCurNoteValue.SetLabel(noteString)
        self.wxCurNoteValue.Hide()
        self.wxCurNoteValue.Show()
        self.wxCurVelValue.SetLabel(velocityString)
        self.wxCurVelValue.Hide()
        self.wxCurVelValue.Show()
        self.wxCurRRValue.SetLabel(roundRobinString)
        self.wxCurRRValue.Hide()
        self.wxCurRRValue.Show()
        self.wxCurMWValue.SetLabel(modWheelString)
        self.wxCurMWValue.Hide()
        self.wxCurMWValue.Show()
        self.Refresh()
        self.Update()
    
    def saveChangesFromGUI(self, event):
        parsePassed = False
        try:
            #Global Variables
            module.MY_LIB_NAME = self.wxLibName.GetValue()
            module.SAVE_DIR = self.wxSavePath.GetPath()+"\\"
            module.MY_SAMPLE_PREFIX = self.wxSamplePrefix.GetValue()

            module.SAMPLERATE = self.toInt(self.wxSamplerate.GetString(self.wxSamplerate.GetSelection()))
            PYVST_SAMPLERATE = module.SAMPLERATE #to update callback in the included file
            module.BLOCKSIZE = self.toInt(self.wxBlocksize.GetString(self.wxBlocksize.GetSelection()))
            PYVST_BLOCKSIZE = module.BLOCKSIZE #to update callback in the included file
            module.SAMPLE_DURATION = self.toFloat(self.wxSampleDuration.GetValue())
            module.BEHIND_ZERO_PADDING = self.toFloat(self.wxZeroPadding.GetValue())
            module.PRE_START = self.toFloat(self.wxPreStartDuration.GetValue())

            #Input Variables
            module.INPUT_MODE = INPUT_TYPE(self.toInt(self.wxInputMode.GetSelection()))
            module.FROM_NOTE = self.wxFromNote.GetValue()
            module.TO_NOTE = self.wxToNote.GetValue()
            exec(str("module.VELOCITY_STEPS = "+self.wxVelSteps.GetValue()))
            exec(str("module.VELOCITY_RANGES = "+self.wxVelRanges.GetValue()))
            exec(str("module.MOD_WHEEL_STEPS = "+self.wxMWSteps.GetValue()))
            module.ROUND_ROBINS = self.toInt(self.wxNumRRs.GetValue())
            module.VST_INSTRUMENT_PATH = self.wxVSTiPath.GetPath()
            module.MIDI_OUT_DEVICE_ID = self.toInt(self.wxMIDIOutDevice.GetValue())
            module.MIDI_IN_DEVICE_ID = self.toInt(self.wxMIDIInDevice.GetValue())
            module.USE_VSTI_AS_TUNER = self.wxTuningTarget.IsChecked()

            #Post Processing Variables
            module.ON_THRESHOLD = self.toFloat(self.wxOnThresh.GetValue())
            module.OFF_THRESHOLD = self.toFloat(self.wxOffThresh.GetValue())

            module.FX_VST1_PATH = self.wxVst1Path.GetPath()
            module.FX_VST1_IS_ACTIVE = self.wxVst1isActive.IsChecked()

            module.FX_VST2_PATH = self.wxVst2Path.GetPath()
            module.FX_VST2_IS_ACTIVE = self.wxVst2isActive.IsChecked()

            module.FX_VST3_PATH = self.wxVst3Path.GetPath()
            module.FX_VST3_IS_ACTIVE = self.wxVst3isActive.IsChecked()

            module.FX_VST4_PATH = self.wxVst4Path.GetPath()
            module.FX_VST4_IS_ACTIVE = self.wxVst4isActive.IsChecked()

            module.FX_VST5_PATH = self.wxVst5Path.GetPath()
            module.FX_VST5_IS_ACTIVE = self.wxVst5isActive.IsChecked()
            parsePassed = True
        except Exception as e:
            logger.exception('Failed: ' + str(e))
            box = wx.MessageDialog(None,"Error while parsing. Check log", "Parse Error", wx.OK)
            box.ShowModal()
            box.Destroy()
        
        if parsePassed:
            self.assert_all_important_vars_are_set()
            save_all_vars()
            
        print_all_vars()
    def startRecording(self, event):
        if self.assert_all_important_vars_are_set():           
            self.wxRecordButton.SetBackgroundColour(module.GUI_BUTTON_RECORDING_COLOR)
            self.wxRecordButton.Hide()
            self.wxRecordButton.Show()
            self.Refresh()
            self.Update()
            
            startSampling(self)
            
            self.wxRecordButton.SetBackgroundColour(module.GUI_BUTTON_DEFAULT_COLOR)
            self.wxRecordButton.Hide()
            self.wxRecordButton.Show()
            self.Refresh()
            self.Update()

    def previewDry(self, event):
        if self.assert_all_important_vars_are_set():
            self.wxPreviewDryButton.SetBackgroundColour(module.GUI_BUTTON_RECORDING_COLOR)
            self.wxPreviewDryButton.Hide()
            self.wxPreviewDryButton.Show()
            self.Refresh()
            self.Update()
            
            previewDry(self)
            
            self.wxPreviewDryButton.SetBackgroundColour(module.GUI_BUTTON_DEFAULT_COLOR)
            self.wxPreviewDryButton.Hide()
            self.wxPreviewDryButton.Show()
            self.Refresh()
            self.Update()

    def previewWet(self, event):
        if self.assert_all_important_vars_are_set():
            self.wxPreviewWetButton.SetBackgroundColour(module.GUI_BUTTON_RECORDING_COLOR)
            self.wxPreviewWetButton.Hide()
            self.wxPreviewWetButton.Show()
            self.Refresh()
            self.Update()
            
            previewWet(self)
            
            self.wxPreviewWetButton.SetBackgroundColour(module.GUI_BUTTON_DEFAULT_COLOR)
            self.wxPreviewWetButton.Hide()
            self.wxPreviewWetButton.Show()
            self.Refresh()
            self.Update()
    
    def onSamplerateChange( self, event ):
        module.SAMPLERATE = self.toInt(self.wxSamplerate.GetString(self.wxSamplerate.GetSelection()))
        #update vsts
        if module.VST_INSTRUMENT != None:
            module.VST_INSTRUMENT.set_sample_rate(module.SAMPLERATE)
        if module.FX_VST1 != None:
            module.FX_VST1.set_sample_rate(module.SAMPLERATE)
        if module.FX_VST2 != None:
            module.FX_VST2.set_sample_rate(module.SAMPLERATE)
        if module.FX_VST3 != None:
            module.FX_VST3.set_sample_rate(module.SAMPLERATE)
        if module.FX_VST4 != None:
            module.FX_VST4.set_sample_rate(module.SAMPLERATE)
        if module.FX_VST5 != None:
            module.FX_VST5.set_sample_rate(module.SAMPLERATE)
        
        print("Please restart audio device")
        module.AUDIO_INPUT_READY = False
        module.AUDIO_OUTPUT_READY = False
            
    def onBlockSizeChange( self, event ):
        module.BLOCKSIZE = self.toInt(self.wxBlocksize.GetString(self.wxBlocksize.GetSelection()))
        #update vsts
        if module.VST_INSTRUMENT != None:
            module.VST_INSTRUMENT.set_block_size(module.BLOCKSIZE)
        if module.FX_VST1 != None:
            module.FX_VST1.set_block_size(module.BLOCKSIZE)
        if module.FX_VST2 != None:
            module.FX_VST2.set_block_size(module.BLOCKSIZE)
        if module.FX_VST3 != None:
            module.FX_VST3.set_block_size(module.BLOCKSIZE)
        if module.FX_VST4 != None:
            module.FX_VST4.set_block_size(module.BLOCKSIZE)
        if module.FX_VST5 != None:
            module.FX_VST5.set_block_size(module.BLOCKSIZE)
            
        print("Please restart audio device")
        module.AUDIO_INPUT_READY = False
        module.AUDIO_OUTPUT_READY = False
        
    def onInputeModeChange( self, event ):
        module.INPUT_MODE = INPUT_TYPE(self.toInt(self.wxInputMode.GetSelection()))
        #TODO disable certain options in the GUI
        if module.INPUT_MODE == INPUT_TYPE.VSTI:
            self.wxOnThreshText.Hide()
            self.wxOnThresh.Hide()
            self.wxPreStartText.Hide()
            self.wxPreStartDuration.Hide()
            self.wxMidiOutDeviceText.Hide()
            self.wxMIDIOutDevice.Hide()
            self.wxVSTiName.Show()
            self.wxVSTiPath.Show()
            self.wxVSTiOpenButton.Show()
            self.wxMidiInDeviceText.Show()
            self.wxMIDIInDevice.Show()
            self.wxTuningTarget.Hide()
            
        if module.INPUT_MODE == INPUT_TYPE.LIVE_REC:
            self.wxOnThreshText.Show()
            self.wxOnThresh.Show()
            self.wxPreStartText.Show()
            self.wxPreStartDuration.Show()
            self.wxMidiOutDeviceText.Hide()
            self.wxMIDIOutDevice.Hide()
            self.wxVSTiName.Hide()
            self.wxVSTiPath.Hide()
            self.wxVSTiOpenButton.Hide()
            self.wxMidiInDeviceText.Hide()
            self.wxMIDIInDevice.Hide()
            self.wxTuningTarget.Show()
            if self.wxTuningTarget.IsChecked():
                self.wxVSTiName.Show()
                self.wxVSTiPath.Show()
                self.wxVSTiOpenButton.Show()
            
        if module.INPUT_MODE == INPUT_TYPE.MIDI_REC:
            self.wxOnThreshText.Show()
            self.wxOnThresh.Show()
            self.wxPreStartText.Show()
            self.wxPreStartDuration.Show()
            self.wxMidiOutDeviceText.Show()
            self.wxMIDIOutDevice.Show()
            self.wxVSTiName.Hide()
            self.wxVSTiPath.Hide()
            self.wxVSTiOpenButton.Hide()
            self.wxMidiInDeviceText.Hide()
            self.wxMIDIInDevice.Hide()
            self.wxTuningTarget.Hide()
        
        
        if module.AUDIO_INPUT_READY == False or module.AUDIO_OUTPUT_READY == False:
            if self.isInit: #Don't complain on startup
                print("Please restart audio device")
    
    def onVSTiTuningTargetChange( self, event ):
        module.USE_VSTI_AS_TUNER = self.wxTuningTarget.IsChecked()
        if module.USE_VSTI_AS_TUNER:
            self.wxVSTiName.Show()
            self.wxVSTiPath.Show()
            self.wxVSTiOpenButton.Show()
        else:
            self.wxVSTiName.Hide()
            self.wxVSTiPath.Hide()
            self.wxVSTiOpenButton.Hide()
    
    def onVSTiBrowse(self, event):
        module.VST_INSTRUMENT_PATH = self.wxVSTiPath.GetPath()
        module.VST_INSTRUMENT = loadVST(module.VST_INSTRUMENT_PATH,module.SAMPLERATE,module.BLOCKSIZE)
        self.wxVSTiName.SetLabel(":".join(["VSTi",module.VST_INSTRUMENT.get_name().decode("utf-8")]))
        print(module.VST_INSTRUMENT.number_of_inputs,module.VST_INSTRUMENT.number_of_outputs)

    def open_VST_instrument(self, event):
        try:
            self.childVSTI.Close()
        except:
            pass
        self.childVSTI = VSTChildFrame(self)
        self.childVSTI.openVST(module.VST_INSTRUMENT)

    def onVST1Browse(self, event):
        module.FX_VST1_PATH = self.wxVst1Path.GetPath()
        module.FX_VST1 = loadVST(module.FX_VST1_PATH,module.SAMPLERATE,module.BLOCKSIZE)
        self.wxVst1isActive.SetValue(True)
        self.wxVST1Name.SetLabel(":".join(["FX1",module.FX_VST1.get_name().decode("utf-8")]))
        print(module.FX_VST1.number_of_inputs,module.FX_VST1.number_of_outputs)

    def open_VST_fx_1(self, event):
        try:
            self.childVST1.Close()
        except:
            pass
        self.childVST1 = VSTChildFrame(self)
        self.childVST1.openVST(module.FX_VST1)

    def onVST2Browse(self, event):
        module.FX_VST2_PATH = self.wxVst2Path.GetPath()
        module.FX_VST2 = loadVST(module.FX_VST2_PATH,module.SAMPLERATE,module.BLOCKSIZE)
        self.wxVst2isActive.SetValue(True)
        self.wxVST2Name.SetLabel(":".join(["FX2",module.FX_VST2.get_name().decode("utf-8")]))
        print(module.FX_VST2.number_of_inputs,module.FX_VST2.number_of_outputs)

    def open_VST_fx_2(self, event):
        try:
            self.childVST2.Close()
        except:
            pass
        self.childVST2 = VSTChildFrame(self)
        self.childVST2.openVST(module.FX_VST2)

    def onVST3Browse(self, event):
        module.FX_VST3_PATH = self.wxVst3Path.GetPath()
        module.FX_VST3 = loadVST(module.FX_VST3_PATH,module.SAMPLERATE,module.BLOCKSIZE)
        self.wxVst3isActive.SetValue(True)
        self.wxVST3Name.SetLabel(":".join(["FX3",module.FX_VST3.get_name().decode("utf-8")]))
        print(module.FX_VST3.number_of_inputs,module.FX_VST3.number_of_outputs)

    def open_VST_fx_3(self, event):
        try:
            self.childVST3.Close()
        except:
            pass
        self.childVST3 = VSTChildFrame(self)
        self.childVST3.openVST(module.FX_VST3)

    def onVST4Browse(self, event):
        module.FX_VST4_PATH = self.wxVst4Path.GetPath()
        module.FX_VST4 = loadVST(module.FX_VST4_PATH,module.SAMPLERATE,module.BLOCKSIZE)
        self.wxVst4isActive.SetValue(True)
        self.wxVST4Name.SetLabel(":".join(["FX4",module.FX_VST4.get_name().decode("utf-8")]))
        print(module.FX_VST4.number_of_inputs,module.FX_VST4.number_of_outputs)

    def open_VST_fx_4(self, event):
        try:
            self.childVST4.Close()
        except:
            pass
        self.childVST4 = VSTChildFrame(self)
        self.childVST4.openVST(module.FX_VST4)

    def onVST5Browse(self, event):
        module.FX_VST5_PATH = self.wxVst5Path.GetPath()
        module.FX_VST5 = loadVST(module.FX_VST5_PATH,module.SAMPLERATE,module.BLOCKSIZE)
        self.wxVst5isActive.SetValue(True)
        self.wxVST5Name.SetLabel(":".join(["FX5",module.FX_VST5.get_name().decode("utf-8")]))
        print(module.FX_VST5.number_of_inputs,module.FX_VST5.number_of_outputs)

    def open_VST_fx_5(self, event):
        try:
            self.childVST5.Close()
        except:
            pass
        self.childVST5 = VSTChildFrame(self)
        self.childVST5.openVST(module.FX_VST5)
    
    def onMenuAudioDeviceSettings( self, event ):
        try:
            self.audioSettingsFrame.Close()
        except:
            pass
        self.audioSettingsFrame = AudioSettingsFrame(self)
        self.audioSettingsFrame.Show(True)


# In[7]:


#create an object of our GUI class
frame = LibRecordFrame(None)
#we will want to see the frame
frame.Show(True)
#Let's run this thing :)
WX_APP.MainLoop()


# In[ ]:




