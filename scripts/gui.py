import matplotlib
matplotlib.use('TKAgg')

import numpy
import os
import sys

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import cm as cm

import extractFramesFromAvi

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def destroy(e): sys.exit()

def updateImage(h_axes,data):
    a.imshow(data,cmap=cm.Greys_r)
def changeThreshold(val):
    
    print(scl_threshold.get())
    


root = Tk.Tk()
root.wm_title("SLO Image Registration")

frame_left = Tk.Frame(root,width=500,height=500)
frame_right = Tk.Frame(root,width=250,height=500)

frame_left.pack(side=Tk.LEFT,fill=None,expand=True)
frame_right.pack(side=Tk.RIGHT,fill=None,expand=True)

f = Figure(figsize=(5,5), dpi=200)
a = f.add_subplot(1,1,1)

fname = '../data/SLO_refl_video.avi'

imgs = extractFramesFromAvi.main(fname,1)


#updateImage(a,imgs[:,:,0])

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=frame_left)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=None, expand=0)

canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.NONE, expand=0)
# add a button
button = Tk.Button(master=frame_right, text='Quit', width=25, command=sys.exit)
button.pack(side=Tk.TOP)
b_threshold=Tk.IntVar()
chk_threshold = Tk.Checkbutton(master=frame_right,text="Threshold",variable=b_threshold)
chk_threshold.pack()
scl_threshold = Tk.Scale(master=frame_right,from_=0, to=255,orient=Tk.HORIZONTAL,command=changeThreshold)
scl_threshold.set(128)
scl_threshold.pack()
Tk.mainloop()
