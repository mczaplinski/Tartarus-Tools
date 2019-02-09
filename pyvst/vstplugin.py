#!/usr/bin/env python

import numpy
from ctypes import *

#To understand the following, have a look into the full VST2SDK header files

#class VstStringConstants(object):
#    kVstMaxProgNameLen = 24
#    kVstMaxParamStrLen = 8
#    kVstMaxVendorStrLen = 64
#    kVstMaxProductStrLen = 64
#    kVstMaxEffectNameLen = 32
CONST_kVstMaxProgNameLen = 256
CONST_kVstMaxParamStrLen = 256
CONST_kVstMaxVendorStrLen = 256
CONST_kVstMaxProductStrLen = 256
CONST_kVstMaxEffectNameLen = 256

#enum VstProcessLevels
CONST_kVstProcessLevelUnknown = 0
CONST_kVstProcessLevelUser = 1
CONST_kVstProcessLevelRealtime = 2
CONST_kVstProcessLevelPrefetch = 3
CONST_kVstProcessLevelOffline = 4

#update these values if needed from your host if you want some plugins to be able to read that
PYVST_SAMPLERATE = 44100
PYVST_BLOCKSIZE = 1024

class AEffect(Structure):
    _fields_ = [
        ('magic', c_int),
        ('dispatcher', c_void_p),
        ('process', c_void_p),
        ('setParameter', c_void_p),
        ('getParameter', c_void_p),
        ('numPrograms', c_int),
        ('numParams', c_int),
        ('numInputs', c_int),
        ('numOutputs', c_int),
        ('flags', c_int),
        ('resvd1', c_void_p),
        ('resvd2', c_void_p),
        ('initialDelay', c_int),
        ('realQualities', c_int),
        ('offQualities', c_int),
        ('ioRatio', c_float),
        ('object', c_void_p),
        ('user', c_void_p),
        ('uniqueID', c_int),
        ('version', c_int),
        ('processReplacing', c_void_p),
        ('processDoubleReplacing', c_void_p),
    ]

class ERect(Structure):
    _fields_ = [
        ('top', c_short),
        ('left', c_short),
        ('bottom', c_short),
        ('right', c_short),
    ]

#in this strtuct actually c_char instead of c_byte, but internet says this can lead to problems. c_byte allows more control but same size as c_char in terms of bytes. See: https://docs.python.org/3/library/ctypes.html#fundamental-data-types
class VstMidiEvent(Structure):
    _fields_ = [
        ('type', c_int),             #kVstMidiType = 1 for midi event
        ('byteSize', c_int),         #sizeof (VstMidiEvent)
        ('deltaFrames', c_int),      #sample frames related to the current block start sample position
        ('flags', c_int),            #@see VstMidiEventFlags (kVstMidiEventIsRealtime = 1 << 0 if realtime, i.e. 000...0010
        ('noteLength', c_int),       #(in sample frames) of entire note, if available, else 0
        ('noteOffset', c_int),       #offset (in sample frames) into note from note start if available, else 0
        ('midiData1', c_byte),       #1 to 3 MIDI bytes;
        ('midiData2', c_byte),       #seperating these bytes instead of putting it into array makes it easier to modfiy a single byte
        ('midiData3', c_byte),       
        ('midiData4', c_byte),       # midiData4 is reserved (zero)
        ('detune', c_byte),          #-64 to +63 cents; for scales other than 'well-tempered' ('microtuning')
        ('noteOffVelocity', c_byte), #Note Off Velocity [0, 127]
        ('reserved1', c_byte),       #zero (Reserved for future use)
        ('reserved2', c_byte),       #zero (Reserved for future use)
    ]
    
class VstEvents(Structure):
    _fields_ = [
        ('numEvents', c_int),
        ('reserved', c_void_p),
        ('events', POINTER(VstMidiEvent)*256), #actually VstEvent but we take VstMidiEvents directly since it shares the same but more specific file structure. (In reality it would be casted to a VstmidiEvent anyways)
    ]

audiomaster_callback = CFUNCTYPE(c_void_p, POINTER(AEffect), c_int, c_int, c_long, c_void_p, c_float)

def create_dispatcher_proc(pointer):
    prototype = CFUNCTYPE(c_void_p, POINTER(AEffect), c_int, c_int, c_long, c_void_p, c_float)
    return prototype(pointer)

def create_process_proc(pointer):
    prototype = CFUNCTYPE(None, POINTER(AEffect), POINTER(POINTER(c_float)), POINTER(POINTER(c_float)), c_int)
    return prototype(pointer)

def create_process_double_proc(pointer):
    prototype = CFUNCTYPE(None, POINTER(AEffect), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), c_int)
    return prototype(pointer)

def create_set_param_proc(pointer):
    prototype = CFUNCTYPE(None, POINTER(AEffect), c_int, c_float)
    return prototype(pointer)

def create_get_param_proc(pointer):
    prototype = CFUNCTYPE(c_float, POINTER(AEffect), c_int)
    return prototype(pointer)

class VstAEffectFlags(object):
    effFlagsHasEditor     = 1 << 0
    effFlagsCanReplacing  = 1 << 4
    effFlagsProgramChunks = 1 << 5
    effFlagsIsSynth       = 1 << 8
    effFlagsNoSoundInStop = 1 << 9
    effFlagsCanDoubleReplacing = 1 << 12

class AEffectOpcodes(object):
    effOpen = 0
    effClose = 1
    effSetProgram = 2
    effGetProgram = 3
    effSetProgramName = 4
    effGetProgramName = 5
    effGetParamLabel = 6
    effGetParamDisplay = 7
    effGetParamName = 8
    effSetSampleRate = 10
    effSetBlockSize = 11
    effMainsChanged = 12
    effEditGetRect = 13
    effEditOpen = 14
    effEditClose = 15
    effEditIdle = 19
    effGetChunk = 23
    effSetChunk = 24
    effNumOpcodes = 25

class AEffectXOpcodes(object):
    effProcessEvents = 25
    effCanBeAutomated = 26
    effString2Parameter = 27
    effGetProgramNameIndexed = 29
    effGetInputProperties = 33
    effGetOutputProperties = 34
    effGetPlugCategory = 35
    effOfflineNotify = 38
    effOfflinePrepare = 39
    effOfflineRun = 40
    effProcessVarIo = 41
    effSetSpeakerArrangement = 42
    effSetBypass = 44
    effGetEffectName = 45
    effGetVendorString = 47
    effGetProductString = 48
    effGetVendorVersion = 49
    effVendorSpecific = 50
    effCanDo = 51
    effGetTailSize = 52
    effGetParameterProperties = 56
    effGetVstVersion = 58
    effEditKeyDown = 59
    effEditKeyUp = 60
    effSetEditKnobMode = 61
    effGetMidiProgramName = 62
    effGetCurrentMidiProgram = 63
    effGetMidiProgramCategory = 64
    effHasMidiProgramsChanged = 65
    effGetMidiKeyName = 66
    effBeginSetProgram = 67
    effEndSetProgram = 68
    effGetSpeakerArrangement = 69
    effShellGetNextPlugin = 70
    effStartProcess = 71
    effStopProcess = 72
    effSetTotalSampleToProcess = 73
    effSetPanLaw = 74
    effBeginLoadBank = 75
    effBeginLoadProgram = 76
    effSetProcessPrecision = 77
    effGetNumMidiInputChannels = 78
    effGetNumMidiOutputChannels = 79

class AudioMasterOpcodes(object):
    audioMasterAutomate = 0
    audioMasterVersion = 1
    audioMasterCurrentId = 2
    audioMasterIdle = 3
    
class AudioMasterOpcodesX(object):
    audioMasterGetTime = 7
    audioMasterProcessEvents = 8
    audioMasterIOChanged = 13
    audioMasterSizeWindow = 15
    audioMasterGetSampleRate = 16
    audioMasterGetBlockSize = 17
    audioMasterGetInputLatency = 18
    audioMasterGetOutputLatency = 19
    audioMasterGetCurrentProcessLevel = 23
    audioMasterGetAutomationState = 24
    audioMasterOfflineStart = 25
    audioMasterOfflineRead = 26
    audioMasterOfflineWrite = 27
    audioMasterOfflineGetCurrentPass = 28
    audioMasterOfflineGetCurrentMetaPass = 29
    audioMasterGetVendorString = 32
    audioMasterGetProductString = 33
    audioMasterGetVendorVersion = 34
    audioMasterVendorSpecific = 35
    audioMasterCanDo = 37
    audioMasterGetLanguage = 38
    audioMasterGetDirectory = 41
    audioMasterUpdateDisplay = 42
    audioMasterBeginEdit = 43
    audioMasterEndEdit = 44
    audioMasterOpenFileSelector = 45
    audioMasterCloseFileSelector = 46

kHostVersion = 2400
#kHostVendorString = c_char_p("Shurrikane".encode('utf-8'))
#kHostProductString = c_char_p("PySampling".encode('utf-8'))
kHostVendorVersion = 2400
    
def basic_callback(effect, opcode, index, value, ptr, opt):
    #print("Received Opcode from Plugin {}: Opcode =".format(plugin.get_name().decode("utf-8")))
    #print(opcode)
    #print(index)
    #print(value)
    #print(ptr)
    #print(opt)
    #print("\n")
    
    if opcode == AudioMasterOpcodes.audioMasterVersion:
        return kHostVersion
    if opcode == AudioMasterOpcodesX.audioMasterGetTime:
        return None #null?
    if opcode == AudioMasterOpcodesX.audioMasterGetCurrentProcessLevel:
        return CONST_kVstProcessLevelOffline #Change Realtime of Offline Processing here
    #if opcode == AudioMasterOpcodesX.audioMasterGetVendorString:
    #    return kHostVendorString
    #if opcode == AudioMasterOpcodesX.audioMasterGetProductString:
    #    return kHostProductString
    if opcode == AudioMasterOpcodesX.audioMasterGetVendorVersion:
        return kHostVendorVersion
    if opcode == AudioMasterOpcodesX.audioMasterUpdateDisplay:
        print("I should have updated the VST display. Rip..")
    if opcode == AudioMasterOpcodesX.audioMasterGetSampleRate:
        return c_double(PYVST_SAMPLERATE)
    if opcode == AudioMasterOpcodesX.audioMasterGetBlockSize:   
        return c_double(PYVST_BLOCKSIZE)
    if opcode == AudioMasterOpcodesX.audioMasterCanDo:   
        #0 : don't know (default)
        #1 : yes
        #-1: no
        return 0  #TODO decode and handle those CanDos
    return 0

class VSTPlugin(object):
    """
    An actual VST plugin wrapper
    """
    def __init__(self, filename, audio_callback = basic_callback):
        """
        Constructor
        Parameters:
          filename is the name of the plugin to load
          audio_callback is the Python function to call (optional)
        """
        self.__lib = CDLL(filename)
        self.__callback = audiomaster_callback(audio_callback)

        try:
            self.__lib.VSTPluginMain.argtypes = [audiomaster_callback, ]
            self.__lib.VSTPluginMain.restype = POINTER(AEffect)
            self.__effect = self.__lib.VSTPluginMain(self.__callback).contents
        except AttributeError:
            self.__lib.main.argtypes = [audiomaster_callback, ]
            self.__lib.main.restype = POINTER(AEffect)
            self.__effect = self.__lib.main(self.__callback).contents

        self.__populate_methods()

    def __populate_methods(self):
        self.dispatcher = create_dispatcher_proc(self.__effect.dispatcher)
        self.__process_replacing = create_process_proc(self.__effect.processReplacing)
        if(self.__effect.processDoubleReplacing):
            self.__process_double_replacing = create_process_double_proc(self.__effect.processDoubleReplacing)
        self.__set_param = create_set_param_proc(self.__effect.setParameter)
        self.__get_param = create_get_param_proc(self.__effect.getParameter)

    def open(self):
        return self.dispatcher(byref(self.__effect), AEffectOpcodes.effOpen, 0, 0, None, 0)

    def close(self):
        return self.dispatcher(byref(self.__effect), AEffectOpcodes.effClose, 0, 0, None, 0)

    def open_edit(self, window = None):
        return self.dispatcher(byref(self.__effect), AEffectOpcodes.effEditOpen, 0, 0, window, 0)

    def close_edit(self):
        return self.dispatcher(byref(self.__effect), AEffectOpcodes.effEditClose, 0, 0, None, 0)
  
    def get_erect(self):
        rect = POINTER(ERect)()
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effEditGetRect, 0, 0, byref(rect), 0)
        return rect.contents
    
    def set_sample_rate(self, sample_rate):
        self.__sample_rate = sample_rate
        return self.dispatcher(byref(self.__effect), AEffectOpcodes.effSetSampleRate, 0, 0, None, sample_rate)

    def set_block_size(self, block_size):
        self.__block_size = block_size
        return self.dispatcher(byref(self.__effect), AEffectOpcodes.effSetBlockSize, 0, block_size, None, 0)

    def process_replacing(self, inputs, outputs):
        f4ptr = POINTER(c_float)
        float_input_pointers = (f4ptr*len(inputs))(*[row.ctypes.data_as(f4ptr) for row in inputs])
        float_output_pointers = (f4ptr*len(outputs))(*[row.ctypes.data_as(f4ptr) for row in outputs])
        self.__process_replacing(byref(self.__effect), float_input_pointers, float_output_pointers, len(inputs[0]))

    def process_double_replacing(self, inputs, outputs):
        d4ptr = POINTER(c_double)
        double_input_pointers = (d4ptr*len(inputs))(*[row.ctypes.data_as(d4ptr) for row in inputs])
        double_output_pointers = (d4ptr*len(outputs))(*[row.ctypes.data_as(d4ptr) for row in outputs])
        self.__process_double_replacing(byref(self.__effect), double_input_pointers, double_output_pointers, len(inputs[0]))

    def process(self, inputs, outputs):
        if inputs[0].dtype == numpy.float32:
            self.process_replacing(inputs, outputs)
        else:
            self.process_double_replacing(inputs, outputs)
    
    def processEvents(self, vstEvents):
        #Send midi events to plugin
        ePtr = POINTER(VstEvents)(vstEvents)
        return self.dispatcher(byref(self.__effect), AEffectXOpcodes.effProcessEvents, 0, 0, ePtr, 0.0)        

    def process_replacing_output(self, outputs):
        #No inputs. This is for VSTis
        f4ptr = POINTER(c_float)
        float_output_pointers = (f4ptr*len(outputs))(*[row.ctypes.data_as(f4ptr) for row in outputs])
        self.__process_replacing(byref(self.__effect), POINTER(c_float)(), float_output_pointers, outputs.shape[1])
        
    def process_double_replacing_output(self, outputs):
        #No inputs. This is for VSTis
        d4ptr = POINTER(c_double)
        double_output_pointers = (d4ptr*len(outputs))(*[row.ctypes.data_as(d4ptr) for row in outputs])
        self.__process_double_replacing(byref(self.__effect), POINTER(d4ptr)(), double_output_pointers, outputs.shape[1])

    def process_output(self, outputs):
        if outputs.dtype == numpy.float32:
            self.process_replacing_output(outputs)
        else:
            self.process_double_replacing_output(outputs)
        
    def set_parameter(self, index, value):
        return self.__set_param(byref(self.__effect), index, value)
  
    def get_parameter(self, index):
        return self.__get_param(byref(self.__effect), index)

    def get_name(self):
        name = c_char_p(b'\0' * CONST_kVstMaxEffectNameLen)
        self.dispatcher(byref(self.__effect), AEffectXOpcodes.effGetEffectName, 0, 0, name, 0.)
        return name.value

    def get_vendor(self):
        name = c_char_p(b'\0' * CONST_kVstMaxVendorStrLen)
        self.dispatcher(byref(self.__effect), AEffectXOpcodes.effGetVendorString, 0, 0, name, 0.)
        return name.value

    def get_product(self):
        name = c_char_p(b'\0' * CONST_kVstMaxProductStrLen)
        self.dispatcher(byref(self.__effect), AEffectXOpcodes.effGetProductString, 0, 0, name, 0.)
        return name.value

    def get_number_of_programs(self):
        return self.__effect.numPrograms

    number_of_programs = property(get_number_of_programs)
  
    def get_number_of_parameters(self):
        return self.__effect.numParams

    number_of_parameters = property(get_number_of_parameters)

    def get_number_of_inputs(self):
        return self.__effect.numInputs

    number_of_inputs = property(get_number_of_inputs)

    def get_number_of_outputs(self):
        return self.__effect.numOutputs

    number_of_outputs = property(get_number_of_outputs)

    def get_sample_rate(self):
        return self.__sample_rate

    sample_rate = property(get_sample_rate)
    
    def get_block_size(self):
        return self.__block_size

    block_size = property(get_block_size)

    def get_program_name_indexed(self, index):
        name = c_char_p(b'\0' * CONST_kVstMaxProgNameLen)
        if self.dispatcher(byref(self.__effect), AEffectXOpcodes.effGetProgramNameIndexed, index, 0, name, 0.):
            raise IndexError("No program with this index (%d)" % index)
        return name.value

    def set_program(self, index):
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effSetProgram, index, 0, None, 0.)

    def get_program_name(self):
        name = c_char_p(b'\0' * CONST_kVstMaxProgNameLen)
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effGetProgramName, 0, 0, name, 0.)
        return name.value

    def get_parameter_name(self, index):
        name = c_char_p(b'\0' * CONST_kVstMaxParamStrLen)
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effGetParamName, index, 0, name, 0.)
        return name.value

    def get_parameter_label(self, index):
        name = c_char_p(b'\0' * CONST_kVstMaxParamStrLen)
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effGetParamLabel, index, 0, name, 0.)
        return name.value

    def get_parameter_display(self, index):
        name = c_char_p(b'\0' * CONST_kVstMaxParamStrLen)
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effGetParamDisplay, index, 0, name, 0.)
        return name.value

    def suspend(self):
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effMainsChanged, 0, 0, None, 0.)

    def resume(self):
        self.dispatcher(byref(self.__effect), AEffectOpcodes.effMainsChanged, 0, 1, None, 0.)

    def can_process_double(self):
        return (self.__effect.flags & VstAEffectFlags.effFlagsCanDoubleReplacing) == VstAEffectFlags.effFlagsCanDoubleReplacing

    def has_editor(self):
        return (self.__effect.flags & VstAEffectFlags.effFlagsHasEditor) == VstAEffectFlags.effFlagsHasEditor
    
def get_effect_properties(effect):
    """
    Return a dictionary of the effect properties
    """
    properties_dict = {}
    properties_dict["Plugin name"] = effect.get_name()
    properties_dict["Vendor name"] = effect.get_vendor()
    properties_dict["Product name"] = effect.get_product()

    properties_dict["numPrograms"] =  effect.number_of_programs
    properties_dict["numParams"] = effect.number_of_parameters
    properties_dict["numInputs"] = effect.number_of_inputs
    properties_dict["numOutputs"] = effect.number_of_outputs

    programs_list = []
    for program_index in range(effect.number_of_programs):
        try:
          program_name = effect.get_program_name_indexed(program_index)
          effect.set_program(program_index)
          program_name = effect.get_program_name()
          programs_list.append(program_name)
        except:
            pass
    properties_dict["Program names"] = programs_list

    params_list = []
    for param_index in range(effect.number_of_parameters):
        param_name = effect.get_parameter_name(param_index)
        param_display = effect.get_parameter_display(param_index)
        param_label = effect.get_parameter_label(param_index)
        value = effect.get_parameter(param_index)
        params_list.append({'param_name': param_name, 'param_display': param_display, 'param_label': param_label, 'curr_value': value})
    properties_dict["Parameters"] = params_list
    return properties_dict

def dump_effect_properties(effect):
    """
    Dump on the screen every thing about the effect properties
    """
    properties_dict = get_effect_properties(effect)
    for k in ["Plugin name", "Vendor name", "Product name", 
            "numPrograms", "numParams", "numInputs", "numOutputs"]:
        print('%s: %s'.format(k, properties_dict[k]))

    for each_idx, each_program in enumerate(properties_dict["Program names"]):
        print('Program %03d: %s'.format(each_idx, each_program))

    for param_index, each_param  in enumerate(properties_dict["Parameters"]):
        param_name = effect.get_parameter_name(param_index)
        param_display = effect.get_parameter_display(param_index)
        param_label = effect.get_parameter_label(param_index)
        value = effect.get_parameter(param_index)
        print("Param %03d: %s [%s %s] (normalized = %f)".format(param_index, each_param['param_name'], each_param['param_display'], each_param['param_label'], each_param['curr_value']))
