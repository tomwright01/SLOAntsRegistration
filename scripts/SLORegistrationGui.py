import numpy as np
import os
import sys
import matplotlib as mpl
import tkFileDialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

import extractFramesFromAvi

mpl.use('TKAgg')

class SLORegistrationGui:
    def __init__(self):
        self.root = Tk.Tk()
        self.src_file=''
        self.raw_data=[]
        self.int_threshold = 128
        self.b_threshold = Tk.IntVar()

        self.createGui()

        Tk.mainloop()
        pass
    
    def createGui(self):
        #Create the main window
        
        self.root.wm_title("SLO Image Registration")
        
        #Create two frames to display
        frame_left = Tk.Frame(self.root,width=500,height=500)
        frame_right = Tk.Frame(self.root,width=250,height=500)
        
        #Create a figure to hold the displayed frame
        
        self.fig_frame = Figure(figsize=(5,5), dpi=200)
        self.a = self.fig_frame.add_subplot(1,1,1)        
        self.a.get_xaxis().set_visible(False)
        self.a.get_yaxis().set_visible(False)

        #Create a tk.DrawingArea to display the figure
        self.canvas = FigureCanvasTkAgg(self.fig_frame, master=frame_left)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=None, expand=0)
        
        self.canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.NONE, expand=0)
        
        # Add the tools
        btn_loadSource = Tk.Button(master=frame_right, text = 'Load Source', width =25, command = self.loadMovie)
        btn_quit = Tk.Button(master=frame_right, text='Quit', width=25, command=sys.exit)

        chk_threshold = Tk.Checkbutton(master=frame_right,text="Threshold",variable=self.b_threshold,command=self.displayFrame)
        
        self.scl_threshold = Tk.Scale(master=frame_right,from_=0, to=255,orient=Tk.HORIZONTAL,command=self.changeThreshold)
        self.scl_threshold.set(128)

        btn_loadSource.pack()
        btn_quit.pack()
        chk_threshold.pack()
        self.scl_threshold.pack()
        
        
        #Place the frames on the canvas    
        frame_left.pack(side=Tk.LEFT,fill=None,expand=True)
        frame_right.pack(side=Tk.RIGHT,fill=None,expand=True)
            
    
    def loadMovie(self):
        self.src_file = tkFileDialog.askopenfilename()
        self.raw_data = extractFramesFromAvi.main(self.src_file,1)
        self.displayFrame()
        
    def displayFrame(self):
        if self.src_file == '':
            #source file not set
            return
        
        if self.b_threshold.get():
            #thresholding is on
            display_data = np.empty_like (self.raw_data[:,:,0])
            display_data[:] = self.raw_data[:,:,0]
            display_data = self.thresholdData(display_data)
        else:
            display_data = self.raw_data[:,:,0]
        
        self.a.cla()
        self.a.imshow(display_data,cmap=mpl.cm.Greys_r)
        self.canvas.draw()
        
    def thresholdData(self,data):
        data[data<self.int_threshold]=0
        data[data>=self.int_threshold]=255
        return(data)
    
    def changeThreshold(self,value):
        """Callback for the threshold slider"""
        self.int_threshold = int(value)
        self.displayFrame()
    
if __name__ == "__main__":
    gui=SLORegistrationGui()