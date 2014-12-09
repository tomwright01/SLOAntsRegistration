import numpy as np

def main(imgs):
    """Cleans an list of npArray created from extractFramesFromAvi.py"""
    #first convert the list into an HxWxN array for convenience
    #only going to take the first slice from each image as they are all grayscale
    if isinstance(imgs,list):
        frameSize = imgs[0].shape
        working = np.zeros((frameSize[0],frameSize[1],len(imgs)))
        
        for iFrame in range(len(imgs)):
            working[:,:,iFrame] = imgs[iFrame][:,:]
    else:
        working = np.float32(imgs)
        frameSize=working.shape

    #convert to use the whole range
    working = (working / working.max()) * 255
        
    """Blink rejections"""
    frameids=np.array(range(frameSize[2])) #holds the identities of the frames we keep
    brightness = [working[:,:,i].sum() for i in frameids]
    working = working[:,:,brightness>np.average(brightness)-(2*np.std(brightness))]
    frameSize=working.shape
    frameids = list(frameids[brightness>np.average(brightness)-(2*np.std(brightness))])
    
    
    """going to find how wide the interlace is in this movie,
    to do this we need to find which rows are black"""
    #split a frame into odd and even rows
    odd=working[0:frameSize[0]:2,:,:]
    even=working[1:frameSize[0]:2,:,:]
    odd[odd<=10]=0
    even[even<=10]=0
    
    odd=odd.sum(axis=2).sum(axis=0)
    even=even.sum(axis=2).sum(axis=0)
    #looks like we get a bit of noise here
    #odd[odd<1000]=0
    #even[even<1000]=0

    if odd[0]==0:
        left=odd
        right=even
    elif even[0]==0:
        left=even
        right=odd
    else:
        raise Exception("Interlace rows not found")
    working=working[:,(left>0),:]
    right=right[(left>0)]
    working=working[:,(right>0),:]
    

    
    working = np.uint8(working)
    return({'data':working,'fids':frameids})