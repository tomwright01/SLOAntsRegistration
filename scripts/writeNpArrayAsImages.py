import numpy
import os
from PIL import Image

def main(lstImages,fids,path,fname):
    """Writes a list of npArrays as files of type extension
    fname should be in the format 'frame-{0:02d}.tiff'"""
    if isinstance(lstImages,list):
        #convert to an nparray
        frameSize = imgs[0].shape
        working = np.zeros((frameSize[0],frameSize[1],len(imgs)))
        
        for iFrame in range(len(imgs)):
            working[:,:,iFrame] = imgs[iFrame][:,:,0]
    else:
        working = lstImages
        
    for iFrame in range(working.shape[2]):
        frame=working[:,:,iFrame]

        Image.fromarray(frame).save(os.path.join(path,fname).format(fids[iFrame]))
        