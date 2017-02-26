import argparse
import os
import sys
import pydub
import random

#Let's add random noise to audio files!
def main():
    # parse all the arguments to the client 
    parser = argparse.ArgumentParser(description="Audio Hasher\nMinimum audio length is 3 seconds!")
    parser.add_argument('-s','--sourceFile', help='Path to the audio file to modify', required=True)
    parser.add_argument('-n','--noiseFile', help='Path to the audio file to interpolate into the source', required=True)
    parser.add_argument('-f','--noiseFactor', help='Fraction of the source audio to replace with noise. (Number between 0 and 1 please!)', required=False)
    parser.add_argument('-o','--outputFile', help='Specify the name of the output audio file', required=False)
    # get the arguments into local variables
    args = vars(parser.parse_args())

    sourceFile = args['sourceFile']
    noiseFile = args['noiseFile']
    outputFile = args['outputFile']
    noiseFactor = int(args['noiseFactor'])
    source_audio = pydub.AudioSegment.empty()
    noise_audio = pydub.AudioSegment.empty()

    try:
        fileFormat = sourceFile[-3:]
        source_audio = pydub.AudioSegment.from_file(sourceFile, format=fileFormat)
        if(len(source_audio) < 3000):
            print("error! The source file is too short! It should be at least 3 seconds long")
            exit(-2)
    except:
        print ( "error opening the source file: %s" % (sourceFile))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        exit(-1)

    try:
        fileFormat = noiseFile[-3:]
        noise_audio = pydub.AudioSegment.from_file(noiseFile, format=fileFormat)
        if(len(noise_audio) < 3000):
            print("error! The noise file is too short! It should be at least 3 seconds long")
            exit(-2)
    except:
        print ( "error opening the noise file: %s" % (noiseFile))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        exit(-1)
    
    final_audio = pydub.AudioSegment.empty()

    # source_audio[2000:7000] + noise_audio[3000:5000] + source_audio[9000:14000]
    #save the length of the original audio for bound checking
    original_length = len(source_audio)
    # leave the first 1% of the audio unedited
    currentIndex = original_length/100
    final_audio += source_audio[0:currentIndex]

    # Define the noise factor
    if(noiseFactor):
        if(noiseFactor < 0):
            noiseFactor = random.random()
        while(noiseFactor > 1):
            noiseFactor = noiseFactor / 10
    else:
        noiseFactor = 0.6
    # A boolean flag to safeguard against playing the noise too many
    # times in a row
    noiseJustUsed = False
    
    while(currentIndex < original_length):
        percentage = 100*currentIndex/original_length
        print ("\tProgress: %d percent\r" % percentage),
        # Randomly pick how many seconds of the audio we will work on in
        # this step of the loop
        nextSegment = random.randint(600,2350)
        audioSnippet = pydub.AudioSegment.empty()
        if(random.random() < noiseFactor and noiseJustUsed == False):
            # Choose a random starting point in the noise audio
            startIndex = random.randint(0,len(noise_audio)-nextSegment)
            # Pull out a segment of the noise file
            audioSnippet = noise_audio[startIndex:startIndex+nextSegment]
            noiseJustUsed = True
        else:
            # Pull out the next segment of the source file
            audioSnippet = source_audio[currentIndex:currentIndex+nextSegment]
            noiseJustUsed = False
        final_audio += audioSnippet
        currentIndex += nextSegment
    #
    print("\nSaving the output..."),
    if (outputFile):
        try: 
            fileFormat = outputFile[-3:]
            file_handle = final_audio.export(outputFile, format=fileFormat)
        except:
            print ( "error opening the output file: %s" % (outputFile))
            exit(-1)
    else:
    	outputFile = "./output%d.mp3" % random.randint(1,9999)
    	file_handle = final_audio.export(outputFile, format="mp3")
    print "Done!"
    exit(0)
# this gives a main function in Python
if __name__ == "__main__":
    main()
#end