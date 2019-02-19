#system libraries
import sys
import os

#some cool libraries
import scipy
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from VSTProcessor import isMono, convert_to_float, convert_float_to_other_type

if __name__ == '__main__':
    PATH = 'samples/Processed/'
    TRIM_FRONT = True
    TRIM_BEHIND = True
    ON_THRESHOLD = -25 #dB below max value
    OFF_THRESHOLD = -40 #dB below max value
    PRESTART_DURATION = 0.005 #5ms
    
    for root, dirs, files in os.walk(PATH, topdown=False):
        for name in files:
            inputfilepath = os.path.join(root, name)
            print(inputfilepath)

            #Loading sample
            rate, data = scipy.io.wavfile.read(inputfilepath)
            
            prestart = PRESTART_DURATION * rate
            
            try:
                if isMono(data):
                    isStereo = False
                    data,olddatatype = convert_to_float(data)

                    #take log/calculate level in dB referenced to maximal value
                    log =20*np.log10(np.abs(data))
                    maxValue = max(log)
                    log = log - maxValue

                    #Thresholding
                    threshLogIdx = np.where(log>ON_THRESHOLD)
                    OffthreshLogIdx = np.where(log>OFF_THRESHOLD)
                    firstThresh = threshLogLIdx[0][0]
                    lastThresh  = OffthreshLogIdx[0][-1]

                    #Slicing sample
                    if TRIM_FRONT:
                        idx = int(firstThresh-prestart)
                        if idx < 0:
                            idx = 0
                        data = data[idx:]
                    if TROM_BEHIND:
                        data = data[:lastThresh]

                    data = convert_float_to_other_type(data, olddatatype)
                    outputdata = data.T
                else:
                    isStereo = True
                    dataL,olddatatype = convert_to_float(data[:,0])
                    dataR,olddatatype = convert_to_float(data[:,1])

                    #take log/calculate level in dB referenced to maximal value
                    logL=20*np.log10(np.abs(dataL))
                    logR=20*np.log10(np.abs(dataR))
                    maxValueL = max(logL)
                    maxValueR = max(logR)
                    logL = logL - maxValueL
                    logR = logR - maxValueR

                    #Thresholding
                    threshLogLIdx = np.where(logL>ON_THRESHOLD)
                    threshLogRIdx = np.where(logR>ON_THRESHOLD)
                    OffthreshLogLIdx = np.where(logL>OFF_THRESHOLD)
                    OffthreshLogRIdx = np.where(logR>OFF_THRESHOLD)
                    firstThreshL = threshLogLIdx[0][0]
                    firstThreshR = threshLogRIdx[0][0]
                    lastThreshL  = OffthreshLogLIdx[0][-1]
                    lastThreshR  = OffthreshLogRIdx[0][-1]
                    firstThresh = min(firstThreshL,firstThreshR)
                    lastThresh = max(lastThreshL,lastThreshR)
                    #Slicing sample
                    if TRIM_FRONT == True:
                        idx = int(firstThresh-prestart)
                        if idx < 0:
                            idx = 0
                        dataL = dataL[idx:]
                        dataR = dataR[idx:]
                    if TRIM_BEHIND == True:
                        dataL = dataL[:lastThresh]
                        dataR = dataR[:lastThresh]

                    dataL = convert_float_to_other_type(dataL, olddatatype)
                    dataR = convert_float_to_other_type(dataR, olddatatype)
                    outputdata = np.array([dataL, dataR]).T

                #save to same file
                scipy.io.wavfile.write(inputfilepath, rate, outputdata)
            except:
                print("ERROR")
                pass