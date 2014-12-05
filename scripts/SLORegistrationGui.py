import numpy as np
import os
import sys
import matplotlib as mpl
import tkFileDialog
import tempfile
import shutil
import subprocess
import re

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

import extractFramesFromAvi
import cleanImageList
import writeNpArrayAsImages
import registerFrame
import ConvertToJpeg
import calcSimilarity

mpl.use('TKAgg')

class SLORegistrationGui:
    def __init__(self):
        self.root = Tk.Tk()
        self.src_file=''
        self.raw_data=[]
        self.data=[]
        self.frameids=[]
        self.frameCount = 1
        self.str_currentFrame = Tk.StringVar()
        self.int_threshold = 128
        self.b_threshold = Tk.IntVar()
        self.config={}
        self.str_currentFrame.trace("w",self.changeFrameText)
        
        self.getConfig()
        self.createGui()

        Tk.mainloop()
    
    def getConfig(self):
        self.config['basedir']=''
        self.config['timestamp']='Registered'
        self.config['frame_pattern']= 'frame-{0:02d}.tiff'
        self.config['verbose']=True
        self.config['force']=False
        self.config['paths']={}
        self.config['paths']['convToJpeg']='/home/tom/Documents/Projects/antsbin/bin/ConvertToJpg'
        self.config['paths']['imageMath']='/home/tom/Documents/Projects/antsbin/bin/ImageMath'
        self.config['paths']['antsPath']="/home/tom/Documents/Projects/antsbin/bin/antsRegistration"
        self.config['paths']['applyPath']="/home/tom/Documents/Projects/antsbin/bin/antsApplyTransform"
        self.config['mask']='../data/mask_s.bmp'
        
    def createGui(self):
        #Create the main window
        
        self.root.wm_title("SLO Image Registration")
        
        #Create two frames to display
        frame_left = Tk.Frame(self.root,width=500,height=450)
        frame_right = Tk.Frame(self.root,width=250,height=500)
        frame_bottom = Tk.Frame(self.root,width=500,height=50)
        
        #Create a figure to hold the displayed frame
        
        self.fig_frame = Figure(figsize=(3,3), dpi=200)
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
        
        btn_register = Tk.Button(master=frame_right, text = 'Register', width=25, command = self.registerMovie)
        
        self.scl_frameNumber = Tk.Scale(master=frame_bottom,from_=0, to=1,orient=Tk.HORIZONTAL,command=self.changeFrame,showvalue=0)
        self.scl_frameNumber.set(0)
        
        self.txt_frameNumber = Tk.Entry(master=frame_bottom,width=5,textvariable=self.str_currentFrame)
        

        btn_loadSource.pack()
        btn_quit.pack()
        chk_threshold.pack()
        self.scl_threshold.pack()
        btn_register.pack()
        
        self.scl_frameNumber.grid(row=0,column=0,sticky='W')
        self.txt_frameNumber.grid(row=0,column=1,sticky='E')
        
        #Place the frames on the canvas    
        frame_left.grid(row=0, column=0)
        frame_right.grid(row=0, column=1)
        frame_bottom.grid(row=1, column=0)
            
    
    def loadMovie(self):
        self.src_file = tkFileDialog.askopenfilename()
        self.config['basedir'] = os.path.dirname(self.src_file)

        match=re.search('(SLO_refl_video).*([0-9]{6})(.avi)',self.src_file)
        if not match is None:
            self.config['timestamp']=match.group(2)
            
        self.raw_data = extractFramesFromAvi.main(self.src_file,1)
        clean_data = cleanImageList.main(self.raw_data)
        self.data = clean_data['data']
        self.frameids = clean_data['fids']
        self.scl_frameNumber.config(to=self.data.shape[2])
        self.displayFrame()

    def registerMovie(self):
        #check the directory structure exists
        #basedir must exist
        working_dir = os.path.join(self.config['basedir'],self.config['timestamp'])
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        
        registered_dir = os.path.join(working_dir,'registered/')
        if not os.path.isdir(registered_dir):
            os.mkdir(registered_dir)
        
        frame_dir = os.path.join(working_dir,'frames')
        if not os.path.isdir(frame_dir):
                    os.mkdir(frame_dir)
        if self.b_threshold.get():
            #threshold is on...
            frame_thresholded_dir = os.path.join(frame_dir,'thresholded')
            if not os.path.isdir(frame_thresholded_dir):
                        os.mkdir(frame_thresholded_dir)
            src_dir = frame_thresholded_dir 
            data=np.empty_like(self.data)
            
            for iFrame in range(data.shape[2]):
                data[:,:,iFrame] = self.thresholdData(self.data[:,:,iFrame])
            writeNpArrayAsImages.main(data,
                                      self.frameids,
                                      frame_thresholded_dir,
                                      self.config['frame_pattern'])
        else:
            src_dir = frame_dir
            
        writeNpArrayAsImages.main(self.data,
                                  self.frameids,
                                  frame_dir,
                                  self.config['frame_pattern'])
        
        tmp_dir = os.path.join(working_dir,'tmp/')
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
        else:
            for f in os.listdir(tmp_dir):
                os.remove(os.path.join(tmp_dir,f))
                
        fnotes = open(os.path.join(working_dir,'notes.txt'),'w')
        fixedFrameIdx = self.getFixedFrameIdx()
        fixedFrameName = self.config['frame_pattern'].format(self.frameids[fixedFrameIdx])
        fixedFrameImg = os.path.join(src_dir,fixedFrameName)
        
        fnotes.write("FixedFrame:{0}\n".format(fixedFrameImg))
        
        
        #now do the registration
        similarityMetrics = []
        for idxFrame in self.frameids:
            movingFrameName = self.config['frame_pattern'].format(idxFrame)
            movingFrameImg = os.path.join(src_dir,movingFrameName)
            
            try:
                registerFrame.main(fixedFrameImg,
                                   movingFrameImg,
                                   self.config['verbose'],
                                   tmp_dir,
                                   None,
                                   self.config['paths']['antsPath'])
                createdFrame = os.path.join(tmp_dir,'Warped.nii.gz')
                ConvertToJpeg.main(createdFrame,
                                   os.path.join(registered_dir,movingFrameName),
                                   self.config['verbose'],
                                   self.config['paths']['convToJpeg'])
                similarityMetrics.append(calcSimilarity.main(fixedFrameImg,
                                                             os.path.join(registered_dir,movingFrameName),
                                                             self.config['mask'],
                                                             self.config['verbose'],
                                                             self.config['paths']['imageMath']))
            except subprocess.CalledProcessError:
                similarityMetrics.append(0)
        print('Similarity Metrics:{0}'.format(similarityMetrics))
        #clean up                                             
        shutil.rmtree(frame_dir)
        shutil.rmtree(tmp_dir)
        fnotes.close()
                
            
    def getFixedFrameIdx(self):
        """Going to use the brightest orginal frame as the fixed frame"""
        brightness=[self.data[:,:,f].sum() for f in range(self.data.shape[2])]
        return(np.argmax(brightness))
        
    def displayFrame(self):
        if self.src_file == '':
            #source file not set
            return
        
        if self.b_threshold.get():
            #thresholding is on
            display_data = np.empty_like (self.data[:,:,int(self.str_currentFrame.get())])
            display_data[:] = self.data[:,:,int(self.str_currentFrame.get())]
            display_data = self.thresholdData(display_data)
        else:
            display_data = self.data[:,:,int(self.str_currentFrame.get())]
        
        self.a.cla()
        self.a.imshow(display_data,cmap=mpl.cm.Greys_r)
        self.canvas.draw()
        
    def thresholdData(self,data):
        data[data<self.int_threshold]=0
        #data[data>=self.int_threshold]=255
        return(data)
    
    def changeThreshold(self,value):
        """Callback for the threshold slider"""
        self.int_threshold = int(value)
        self.displayFrame()
        
    def changeFrame(self,value):
        """Callback for the frame index slider"""
        self.str_currentFrame.set(value)
        
    def changeFrameText(*args):
        """Callback for the Tk.StringVar txt_frameNumber"""
        self=args[0]
        
        if self.str_currentFrame.get() == '':
            """updating the text box causes this to fire twice,
            Once as a delete"""
            return
        
        newVal = self.str_currentFrame.get()
        oldVal = self.scl_frameNumber.get()
        try:
            newInt = int(newVal)
        except ValueError:
            self.txt_frameNumber.setvar(str(oldVal))
            return

        if not (0 <= newInt <= self.scl_frameNumber.config('to')):
            self.txt_frameNumber.setvar(str(oldVal))
            
        self.scl_frameNumber.set(newInt)
        self.displayFrame()
        
        
if __name__ == "__main__":
    gui=SLORegistrationGui()