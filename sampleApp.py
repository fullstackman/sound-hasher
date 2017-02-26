from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pydub
import random

phase = 0
root = Tk()
#root.geometry('700x500+0+0')
root.title("Sample App!")
sourceFileString = StringVar()
noiseFileString = StringVar()
outputFileString = StringVar()
#TODO: add noise factor
#TODO: add more formats that are supported:
# https://ffmpeg.org/general.html#File-Formats
acceptableFileTypes = [
    ('Audio Files','*.mp3;*.m4a;*.aac;*.wav;*.ogg'),
    ('Video Files','*.mp4;*.avi')
    ]

def getSourceFileString(*args):
    global sourceFileString, phase
    if(phase < 1):
        sourceFileString.set("Empty")
        return
    sourceFileString.set( filedialog.askopenfilename(filetypes=acceptableFileTypes) )

def getNoiseFileString(*args):
    global noiseFileString, phase
    if(phase < 1):
        noiseFileString.set("Empty")
        return
    noiseFileString.set( filedialog.askopenfilename(filetypes=acceptableFileTypes) )

def sliceAudio(*args):
    global sourceFileString, noiseFileString, phase, outputFileString
    if(phase < 1):
        outputFileString.set("Empty!")
        return
    #
    if(len(sourceFileString.get()) < 6):
        # TODO Use dialog
        print "Missing a source file!"
        return
    if(len(noiseFileString.get()) < 6):
        # TODO Use dialog
        print "Missing a noise file!"
        return
    print("Doing the magic!")
    sourceFile = sourceFileString.get()
    noiseFile = noiseFileString.get()
    noiseFactor = '' #int(args['noiseFactor'])
    source_audio = pydub.AudioSegment.empty()
    noise_audio = pydub.AudioSegment.empty()

    try:
        fileFormat = sourceFile[-3:]
        #print("You want to open a file of type: (%s)" % fileFormat)
        source_audio = pydub.AudioSegment.from_file(sourceFile, format=fileFormat)
        if(len(source_audio) < 3000):
            print("error! The source file is too short! It should be at least 3 seconds long")
            return
    except:
        print ( "error opening the source file: %s" % (sourceFile.get() ))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        return

    try:
        fileFormat = noiseFile[-3:]
        noise_audio = pydub.AudioSegment.from_file(noiseFile, format=fileFormat)
        if(len(noise_audio) < 3000):
            print("error! The noise file is too short! It should be at least 3 seconds long")
            return
    except:
        print ( "error opening the noise file: %s" % (noiseFile.get() ))
        e = sys.exc_info()[0]
        print( "\tError: %s" % e )
        return
    
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
    #TODO: Add support for various export file formats
    #outputFile = "./output%d.mp3" % random.randint(1,9999)
    outputFile = filedialog.asksaveasfilename(filetypes=[
    ('Basic MP3 Audio','*.mp3')]) + ".mp3"
    final_audio.export(outputFile, format="mp3")
    outputFileString.set(outputFile)

def main():
    global root, phase, sourceFileString, noiseFileString
    
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    p = ttk.Panedwindow(mainframe, orient=HORIZONTAL)
    p.grid(column=1,row=1,sticky=(N,W,E,S))

    # first pane, which would get widgets gridded into it:
    f1 = ttk.Labelframe(p, text='Source Audio', width=400, height=300)
    ttk.Label(f1, text="Press \"A\" to choose the noise file", command=getSourceFileString()).grid(sticky=W)
    ttk.Label(f1, textvariable=sourceFileString).grid( sticky=(W, E))

    p.add(f1)
    f2 = ttk.Labelframe(p, text='Noise Audio', width=400, height=300)   # second pane
    ttk.Label(f2, text="Press \"K\" to choose the noise file", command=getNoiseFileString()).grid(sticky=W)
    ttk.Label(f2, textvariable=noiseFileString).grid(sticky=W)
    #f2.pack()
    p.add(f2)
    
    secondaryPane = ttk.Panedwindow(mainframe, orient=VERTICAL)
    secondaryPane.grid(column=1,row=2,sticky=(N,W,E,S))
    ttk.Label(secondaryPane, text="Press the space bar to slice the audio files", command=sliceAudio()).grid(sticky="W")
    ttk.Label(secondaryPane, text="Output:").grid(sticky=W)
    ttk.Label(secondaryPane, textvariable=outputFileString).grid(sticky=W)
    
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.bind('a', getSourceFileString)
    root.bind('k', getNoiseFileString)
    root.bind('<space>',sliceAudio)
    phase += 1

    # Let the window wrap all of the content we just loaded and then
    # prevent it from resizing
    root.resizable(FALSE,FALSE)
    root.mainloop()

# this gives a main function in Python
if __name__ == "__main__":
    main()