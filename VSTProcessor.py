#system libraries
import sys
import os
import glob

#some cool libraries
import scipy
import scipy.io.wavfile
import numpy as np
#import matplotlib.pyplot as plt

#Import Processing Functions
from ProcessingFunctions import *

SAMPLERATE = 44100
BLOCKSIZE = 2048
PADDING = 5.0 #seconds to run plugin after main sample already cut off (reverb..)
VSTPATH = "D:/VST64/Amplifier/Guitar Rig 5.dll"
INPUTDIR = 'samples/ToProcess/'
SAVEDIR = 'samples/PLZ_DELET/'

if __name__ == '__main__':
    # LOAD PLUGIN
    plugin = loadVST(VSTPATH,SAMPLERATE,BLOCKSIZE)
    configVST(plugin)
    datatype = getDatatype(plugin)
    
    #Add plugin and program name to savepath :)
    SAVEDIR = ''.join([SAVEDIR,plugin.get_name().decode("utf-8"),'/',plugin.get_program_name().decode("utf-8"),'/'])
    
    if not os.path.exists(INPUTDIR):
        raise Exception('Excuse me what the fuck, Code: 1337')
    
    # LOAD FILES
    for root, dirs, files in os.walk(INPUTDIR, topdown=False):
        for name in files:
            inputfilepath = os.path.join(root, name)
            print(inputfilepath)
            savefilepath = inputfilepath.replace(INPUTDIR,SAVEDIR)
            savedirpath = os.path.dirname(savefilepath)
            if not os.path.exists(savedirpath):
                os.makedirs(savedirpath)

            rate, data = scipy.io.wavfile.read(inputfilepath)
            isStereo = not isMono(data)
            if isStereo:
                #print('Stereo signal')
                dataL = data[:,0]
                dataR = data[:,1]
            else:
                dataL = data
                dataR = np.copy(data)
                #print('Mono signal')

            dataL, olddatatype = convert_to_float(dataL, datatype)
            dataR, olddatatype = convert_to_float(dataR, datatype)

            #Normalization
            if(rate != SAMPLERATE):
                print("resampling")
                dataL = resample(dataL, rate, SAMPLERATE)
                dataR = resample(dataR, rate, SAMPLERATE)
            
            #PROCESS AUDIO
            padLength = round(PADDING*SAMPLERATE)
            output1, output2 = processEffect(plugin, dataL, dataR, padLength=padLength)
            
            #Outputs should be nonzero..
            assertIsNonZero(output1)
            assertIsNonZero(output2)

            #Assume we have two outputs. If not... rip..
            #Trim Zeros from behind
            output1, output2 = zeroTrimStereoSample(output1, output2, trimBack=True)
            
            #Convert to old datatype
            output1 = convert_float_to_other_type(output1, olddatatype)
            output2 = convert_float_to_other_type(output2, olddatatype)
    
            #SAVE FILE
            outputdata = np.array([output1, output2]).T
            scipy.io.wavfile.write(savefilepath, SAMPLERATE, outputdata)

    #EXIT
    closePlugin(plugin)
    print("Done!")
    sys.exit()