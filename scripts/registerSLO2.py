import os
import argparse
import tempfile
import shutil
import operator
import subprocess
import numpy as np
import logging

import extractFramesFromAvi
import cleanImageList
import writeNpArrayAsNifti
import createGradientImage
import findBlobs
import registerFrame2
import calcSimilarity2
import averageFrames
import ConvertToJpeg

def main(input_avi,outdir,mask1,mask2,verbose,force,antsPath):
    """
    Register frames in an SLO file using scripts and executables from ANTs
    https://stnava.github.io/ANTs/
    """
    #check the output directory exists
    if not os.path.isdir(outdir):
        if force:
            os.mkdir(outdir)
        else:
            raise Exception("Invalid outdir, try setting force")
    else:
        #outdir exists, check it's empty
        contents = os.listdir(outdir)
        if len(contents) > 0:
            #directory is not empty
            if force:
                #force is set, deleting contents
                for f in contents:
                    f = os.path.join(outdir,f)
                    if os.path.isfile(f):
                        os.remove(f)
                    else:
                        shutil.rmtree(f)
            else:
                raise Exception("Outdir is not empty, quitting, override with --force")
    logging.info('Output directory cleaned')
    #make a directory to store the frames
    frame_dir = os.path.join(outdir,'frames/')
    os.mkdir(frame_dir)

    workingDir = os.path.join(outdir,'tmp/')
    if not os.path.isdir(workingDir):
        os.mkdir(workingDir)
    else:
        #empty any files in the working dir
        for f in os.listdir(workingDir):
            os.remove(os.path.join(workingDir,f))
    logging.info('output directories created')
    #Open a file to keep store information about the registration process
    fnotes = open(os.path.join(outdir,'notes.txt'),'w')
    
    #extract the frames
    #extractFrames.main(input_avi,frame_dir,'frame-%03d.tiff',verbose,avconvPath)
    imgs=extractFramesFromAvi.main(input_avi,True)
    #imgs=imgs[:,:,0:10]
    logging.info('frames extracted')
    cleanimgs=cleanImageList.main(imgs)
    logging.info('frames cleaned')
    imgs=cleanimgs['data']
    frameNos=cleanimgs['fids']
   
    #set the fixed frame
    frame_brightness=[]
    
    for frameIdx in range(imgs.shape[2]):
        frame_brightness.append(imgs[:,:,frameIdx].sum())
        
    fixedFrameIdx = frame_brightness.index(max(frame_brightness))
    fixedFramePath = os.path.join(frame_dir,'fixed.nii.gz')
    fixedGradientPath = os.path.join(frame_dir,'fixed_grad.nii.gz')
    writeNpArrayAsNifti.write(imgs[:,:,fixedFrameIdx],fixedFramePath)
    logging.info('Fixed frame:{0}'.format(fixedFramePath))
    createGradientImage.main(2,fixedGradientPath,fixedFramePath,10,antsPath)
    logging.info('Fixed gradient:{0}'.format(fixedGradientPath))
    fnotes.write("FixedFrame:{0}\n".format(frameNos[fixedFrameIdx]))
    
    #create a mask frame
    mask=np.zeros((imgs.shape[0],imgs.shape[1]))
    mask[100:(imgs.shape[0]-100),100:(imgs.shape[1]-100)] = 1
    maskPath = os.path.join(frame_dir,'mask.nii.gz')
    writeNpArrayAsNifti.write(mask,maskPath)
    
    similarityMetrics = []   
    
    for frameIdx in range(imgs.shape[2]):
        #create the moving frame gradients
        movingFramePath = os.path.join(workingDir,'moving.nii.gz')
        movingGradientPath = os.path.join(workingDir,'moving_grad.nii.gz')
        writeNpArrayAsNifti.write(imgs[:,:,frameIdx],movingFramePath)
        createGradientImage.main(2,movingGradientPath,movingFramePath,10,antsPath)
        logging.info('Moving frame:{0}'.format(movingFramePath))
        logging.info('Moving gradient:{0}'.format(movingGradientPath))
        
        #find the blobs
        fixedBlobPath = os.path.join(workingDir,'fixedBlob.nii.gz')
        movingBlobPath = os.path.join(workingDir,'movingBlob.nii.gz')
        findBlobs.main(fixedGradientPath,
                       movingGradientPath,
                       fixedBlobPath,
                       movingBlobPath,
                       400,
                       50,
                       5,
                       antsPath)
        #Begin the registration
        outputFramePath = os.path.join(outdir,'frame-{0:02d}.nii.gz'.format(frameNos[frameIdx]))
        logging.info('Starting registration')
        logging.info('Output path:{0}'.format(outputFramePath))
        registerFrame2.main(fixedFramePath,
                            movingFramePath,
                            fixedBlobPath,
                            movingBlobPath,
                            outputFramePath,
                            maskPath,
                            workingDir,
                            antsPath)
                       
        logging.info('Registration done for frame:frame-{0:02d}.nii.gz'.format(frameNos[frameIdx]))
        similarityMetrics.append(calcSimilarity2.main(fixedFramePath,outputFramePath,antsPath))
            
    #similarity metrics is a list of floats, want to sort these to get the most similar
    #using the NormalizedCorrelation measure, most similar has a value of 1
    orderedList = sorted(enumerate(similarityMetrics),key=operator.itemgetter(1),reverse=True)
    index = [i[0] for i in orderedList]
    
    
    filesToAverage = [os.path.join(outdir,'frame-{0:02d}.nii.gz'.format(frameNos[i])) for i in index[:4]]
    
    #store this info
    fnotes.write('Frames in average:\n')
    for i in index[:4]:
        fnotes.write('frame-{0:02d}.nii.gz'.format(frameNos[i]) + "\n")
    
    averageFrames.main(filesToAverage,os.path.join(workingDir,'average.nii.gz'),verbose,antsPath)
    
    #convert the average frame back to a tiff file
    ConvertToJpeg.main(os.path.join(workingDir,'average.nii.gz'),
                       os.path.join(outdir,'average.tiff'),
                       verbose,
                       antsPath)
    #clean up
    shutil.rmtree(frame_dir)
    shutil.rmtree(workingDir)
    fnotes.close()
    
    print(filesToAverage)
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Register frames in an SLO file using scripts and executables from ANTs')
    parser.add_argument('input_avi',help="Path to the input movie")
    parser.add_argument('--outdir',help="Path to the output directory",
                        default='output/')
    parser.add_argument('--mask1',
                        help="name of the image to use as a mask for the registration process")
    parser.add_argument('--mask2',
                        help="name of the image to use as a mask for the correlation process")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('-f','--force',action="store_true")
    parser.add_argument('--antsPath',
                        help="Path to the antsRegistration executable",
                        default="/home/tom/Source/ANTsStuff/antsbin/bin")

    args=parser.parse_args()
    
    main(args.input_avi,
        args.outdir,
        args.mask1,
        args.mask2,
        args.verbose,
        args.force,
        args.antsPath)
