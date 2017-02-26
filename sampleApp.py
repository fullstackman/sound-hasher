from tkinter import *
from tkinter import filedialog
from tkinter import ttk

phase = 0
root = Tk()
#root.geometry('700x500+0+0')
root.title("Sample App!")
sourceFile = StringVar()
noiseFile = StringVar()
outputFile = StringVar()
#TODO: add noise factor
#TODO: add more formats that are supported:
# https://ffmpeg.org/general.html#File-Formats
acceptableFileTypes = [
    ('Audio Files','*.mp3;*.m4a;*.aac;*.wav;*.ogg'),
    ('Video Files','*.mp4;*.avi')
    ]

def getSourceFile(*args):
    global sourceFile, phase
    if(phase < 1):
        sourceFile.set("Empty")
        return
    sourceFile.set( filedialog.askopenfilename(filetypes=acceptableFileTypes) )

def getNoiseFile(*args):
    global noiseFile, phase
    if(phase < 1):
        noiseFile.set("Empty")
        return
    noiseFile.set( filedialog.askopenfilename(filetypes=acceptableFileTypes) )

def sliceAudio(*args):
    global sourceFile, noiseFile, phase
    if(phase < 1):
        outputFile.set("Empty!")
        return
    #
    if(len(sourceFile.get()) < 6):
        # TODO Use dialog
        print "Missing a source file!"
        return
    if(len(noiseFile.get()) < 6):
        # TODO Use dialog
        print "Missing a noise file!"
        return
    print("Doing the magic!")
    

def main():
    global root, phase, sourceFile, noiseFile
    
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    p = ttk.Panedwindow(mainframe, orient=HORIZONTAL)
    p.grid(column=1,row=1,sticky=(N,W,E,S))

    # first pane, which would get widgets gridded into it:
    f1 = ttk.Labelframe(p, text='Source Audio', width=400, height=300)
    ttk.Label(f1, text="Press \"A\" to choose the noise file", command=getSourceFile()).grid(sticky=W)
    ttk.Label(f1, textvariable=sourceFile).grid( sticky=(W, E))

    p.add(f1)
    f2 = ttk.Labelframe(p, text='Noise Audio', width=400, height=300)   # second pane
    ttk.Label(f2, text="Press \"K\" to choose the noise file", command=getNoiseFile()).grid(sticky=W)
    ttk.Label(f2, textvariable=noiseFile).grid(sticky=W)
    #f2.pack()
    p.add(f2)
    
    secondaryPane = ttk.Panedwindow(mainframe, orient=VERTICAL)
    secondaryPane.grid(column=1,row=2,sticky=(N,W,E,S))
    ttk.Label(secondaryPane, text="Press the space bar to slice the audio files", command=sliceAudio()).grid(sticky="W")
    ttk.Label(secondaryPane, text="Output:").grid(sticky=W)
    ttk.Label(secondaryPane, textvariable=outputFile).grid(sticky=W)
    
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.bind('a', getSourceFile)
    root.bind('k', getNoiseFile)
    root.bind('<space>',sliceAudio)
    phase += 1

    # Let the window wrap all of the content we just loaded and then
    # prevent it from resizing
    root.resizable(FALSE,FALSE)
    print(root.grid_size())
    root.mainloop()

# this gives a main function in Python
if __name__ == "__main__":
    main()