import argparse
import os
import sys
import pydub
import random

#Let's add random noise to audio files!
def main():
    # parse all the arguments to the client 
    parser = argparse.ArgumentParser(description="Audio Hasher")
    parser.add_argument('-s','--sourceFile', help='Path to the audio file to modify', required=True)
    parser.add_argument('-n','--noiseFile', help='Path to the audio file to interpolate into the source', required=True)
    parser.add_argument('-o','--outputFile', help='Specify the name of the output audio file', required=False)
    # get the arguments into local variables
    args = vars(parser.parse_args())

    sourceFile = args['sourceFile']
    noiseFile = args['noiseFile']
    outputFile = args['outputFile']
    source_audio = []
    noise_audio = []

    try:
        fileFormat = sourceFile[-3:]
        source_audio = pydub.AudioSegment.from_file(sourceFile, format=fileFormat)
    except:
        print ( "error opening the source file: %s" % (sourceFile))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        exit(-1)

    try:
        fileFormat = noiseFile[-3:]
        noise_audio = pydub.AudioSegment.from_file(noiseFile, format=fileFormat)
    except:
        print ( "error opening the noise file: %s" % (noiseFile))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        exit(-1)
    
    #
    final_audio = source_audio[2000:7000] + noise_audio[3000:5000] + source_audio[9000:14000]
    #
    #
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
    exit(0)
# this gives a main function in Python
if __name__ == "__main__":
    main()
#end