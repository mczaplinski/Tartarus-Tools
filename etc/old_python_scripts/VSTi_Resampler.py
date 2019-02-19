from ProcessingFunctions import *

VSTPATH = "D:/VST64/Sampler/Kontakt 6 x64/Kontakt 6.dll"
#VSTPATH = "D:/VST64/Sampler/play_VST_x64.dll"
#VSTPATH = "D:/VST64/Synth/Massive/Massive.dll"
#VSTPATH = "D:/VST64/Synth/Xfer/x64/Serum_x64.dll"
SAMPLERATE = 44100
#BLOCKSIZE = 2048
BLOCKSIZE = 2048
DURATION_PER_SAMPLE = 10*SAMPLERATE #5sec. Todo: Check if sample has died out, otherwise: process longer
CUTTING_THRESHOLD = -80 #dB Cut signal after it dropped below this level

KEY_RANGE = ['A#0','E5']
VELOCITY_STEPS = [30,90,127] #0...127
VELOCITY_RANGES = [[0,45],[46,90],[91,127]] #Zones to map the above values to (don't leave any gaps)
MODWHEEL_STEPS = [30, 127]
ROUND_ROBINS = 3

SAVEPATH = "samples/Resamples/Orchestrations/Fanfare Equestria/TTFTFfEq"  #<-- also include instrument sample prefix here

if __name__ == '__main__':
    #Load plugin
    plugin = loadVST(VSTPATH,SAMPLERATE,BLOCKSIZE)
    configVST(plugin)#We need to choose the instrument/patch right here
    print(plugin.number_of_inputs,plugin.number_of_outputs)
    
    #Get subset of notes we want to trigger
    fromIdx = 0
    toIdx = 127
    keys = list(MIDI_KEY.keys())
    for idx,curKey in enumerate(keys):
        if curKey == KEY_RANGE[0]: #Lowest note we want to sample
            fromIdx = idx
        if curKey == KEY_RANGE[1]: #Highest note we want to sample
            toIdx = idx+1 #because that's how pythons list index subscripts works bitch (see next line)
    keys = keys[fromIdx:toIdx]
    sub_midi_dict = {k:v for k,v in MIDI_KEY.items() if k in keys}
    
    
    savedirpath = os.path.dirname(SAVEPATH)
    if not os.path.exists(savedirpath):
        os.makedirs(savedirpath)
        
    errors = 0
    
    for key_name, key_value in sub_midi_dict.items():
    #e.g.: key_name,key_value = G2, 55 ...
        for velocity in VELOCITY_STEPS:
            for mw in MODWHEEL_STEPS:
                for rr in range(1,ROUND_ROBINS+1):
                    print(key_name,velocity,rr)
                    #Note On Event
                    midiEvent1 = getNoteOnEvent(key=key_value, velocity=velocity, deltaFrames=0, channel=1)
                    midiEvent2 = getMidiCCEvent(cc=1, val=mw, channel=1, deltaFrames=0)
                    
                    #Merge MidiEvents to VstEventList
                    midiEventList = []
                    midiEventList.append(midiEvent1)
                    midiEventList.append(midiEvent2)
                    mergedMidiEvents = mergeMidiEvents(midiEventList)

                    #Send events to plugin
                    sendMidiEventsToPlugin(plugin, mergedMidiEvents)

                    #Sometimes the first note doesn't work, but all other are... (f.u. spitfire DDD:)
                    try:
                        #Retrieve output for given duration
                        output = processInstrument(plugin, length=DURATION_PER_SAMPLE)

                        #TODO check if there is actually something written into the output

                        outputL,outputR = gateStereoSample(output[0],output[1],trimFront=False, trimBehind=True, offThreshold=CUTTING_THRESHOLD, mode='dBFSR')
                    except:
                        print("Was not able to get output. Trying again...")
                        try:
                            #Let's just try it again DDD:
                            #Note On Event
                            midiEvent1 = getNoteOnEvent(key=key_value, velocity=velocity, deltaFrames=0, channel=1)
                            #Merge MidiEvents to VstEventList
                            midiEventList = []
                            midiEventList.append(midiEvent1)
                            mergedMidiEvents = mergeMidiEvents(midiEventList)
                            #Send events to plugin
                            sendMidiEventsToPlugin(plugin, mergedMidiEvents)
                            output = processInstrument(plugin, length=DURATION_PER_SAMPLE)
                            outputL,outputR = gateStereoSample(output[0],output[1],trimFront=False, trimBehind=True, offThreshold=-80, mode='dBFSR')
                        except:
                            print("failed again...")
                            errors = errors + 1
                            if errors > 9:
                                print("Too many errors... Exiting...")
                                break
                            continue

                    outputL = limitSample(outputL, valdB=-0.1)
                    outputR = limitSample(outputR, valdB=-0.1)

                    #Save sample
                    velRange = VELOCITY_RANGES[VELOCITY_STEPS.index(velocity)]
                    savefilepath = '_'.join([SAVEPATH,key_name,str(velRange[0]),str(velRange[1]),'rr{}mw{}.wav'.format(rr,mw)])
                    outputdata = np.array([outputL, outputR]).T
                    scipy.io.wavfile.write(savefilepath, SAMPLERATE, outputdata)

                    #Send note-off and process (just in case to supress any form of reverb/feedback)
                    midiEvent2 = getNoteOffEvent(key=key_value, velocity=velocity, deltaFrames=0, channel=1)
                    midiEvent3 = getNoteOnEvent(key=key_value, velocity=0, deltaFrames=0, channel=1) #Do both types of note-offs
                    midiEventList = []
                    midiEventList.append(midiEvent2)
                    midiEventList.append(midiEvent3)
                    mergedMidiEvents = mergeMidiEvents(midiEventList)
                    sendMidiEventsToPlugin(plugin, mergedMidiEvents)
                    output = processInstrument(plugin, length=DURATION_PER_SAMPLE) #don't save this output :p
                    print("next")
            
    #EXIT
    closePlugin(plugin)
    print("Done!")
    sys.exit()