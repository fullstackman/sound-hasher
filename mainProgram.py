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
    mp3_audio = []

    try:
        #with open(sourceFile, "rb") as source_file:
    		#mp3_audio = pydub.AudioSegment.from_file(source_file, format="mp3")
        mp3_audio = pydub.AudioSegment.from_file(sourceFile, format="mp3")
    except:
        print ( "error opening the source file: %s" % (sourceFile))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        exit(-1)

    try: 
        #filesize = os.path.getsize(noiseFile)
        fd = open(noiseFile, "rb")
        usefile = True
    except:
        print ( "error opening the noise file: %s" % (noiseFile))
        exit(-1)
    
    #
    mp3_audio = mp3_audio[2000:7000]
    #
    #
    if (outputFile):
        try: 
            file_handle = mp3_audio.export(outputFile, format="mp3")
        except:
            print ( "error opening the output file: %s" % (outputFile))
            exit(-1)
    else:
    	outputFile = "./output%d.mp3" % random.randint(1,9999)
    	file_handle = mp3_audio.export(outputFile, format="mp3")
# this gives a main function in Python
if __name__ == "__main__":
    main()
#end