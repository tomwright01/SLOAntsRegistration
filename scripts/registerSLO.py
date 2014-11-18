import os
import argparse
import tempfile
import shutil
import operator

import extractFrames
import registerFrame
import ConvertToJpeg
import calcSimilarity
import averageFrames
import calcFrameBrightness

def main(input_avi,outdir,mask1,mask2,verbose,force,avconvPath,convtojpegPath,imPath,antsPath,avgimgPath):
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

    #make a directory to store the frames
    frame_dir = os.path.join(outdir,'frames/')
    os.mkdir(frame_dir)
    
    #extract the frames
    extractFrames.main(input_avi,frame_dir,'frame-%03d.tiff',verbose,avconvPath)
    
   
    #get the list of frames
    frames = [ f for f in os.listdir(frame_dir) if os.path.isfile(os.path.join(frame_dir,f)) ]


    #set the fixed frame
    frame_brightness=[]
    
    for frame in frames:
        frame_brightness.append(calcFrameBrightness.main(os.path.join(frame_dir,frame),None,verbose,imPath))
        
    fixedFrameIdx = frame_brightness.index(max(frame_brightness))
    fixedFrame = os.path.join(frame_dir,frames[fixedFrameIdx])

    
    workingDir = os.path.join(outdir,'tmp/')
    if not os.path.isdir(workingDir):
        os.mkdir(workingDir)
    else:
        #empty any files in the working dir
        for f in os.listdir(workingDir):
            os.remove(os.path.join(workingDir,f))

    similarityMetrics = []            
    for frame in frames:
        #first register the frame
        movingFrame=os.path.join(frame_dir,frame)
        registerFrame.main(fixedFrame,movingFrame,verbose,workingDir,mask1,antsPath)
        createdFrame = os.path.join(workingDir,'Warped.nii.gz')
        #convert the generated frame into a jpg
        ConvertToJpeg.main(createdFrame,
                           os.path.join(outdir,frame),
                           verbose,
                           convtojpegPath)
        #for each generated frame calculate the similarity to the fixed frame
        
        similarityMetrics.append(calcSimilarity.main(fixedFrame,
                                                    os.path.join(outdir,frame),
                                                    mask2,
                                                    verbose,
                                                    imPath))
    
    #similarity metrics is a list of floats, want to sort these to get the most similar
    #using the NormalizedCorrelation measure, most similar has a value of -1
    orderedList = sorted(enumerate(similarityMetrics),key=operator.itemgetter(1))
    index = [i[0] for i in orderedList]
    
    filesToAverage = [os.path.join(outdir,frames[i]) for i in index[:4]]
    
    
    averageFrames.main(filesToAverage,os.path.join(workingDir,'average.nii.gz'),verbose,avgimgPath)
    
    #convert the average frame back to a tiff file
    ConvertToJpeg.main(os.path.join(workingDir,'average.nii.gz'),
                       os.path.join(outdir,'average.tiff'),
                       verbose,
                       convtojpegPath)
    #clean up
    shutil.rmtree(frame_dir)
    shutil.rmtree(workingDir)

    
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
    parser.add_argument('--avconvPath',help='path to the avconv executable',
                        default='/usr/bin/avconv')
    parser.add_argument('--convtojpegPath',help='path to the ConvertToJpg executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/ConvertToJpg')
    parser.add_argument('--imPath',help='path to the ImageMath executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/ImageMath')
    parser.add_argument('--antsPath',
                        help="Path to the antsRegistration executable",
                        default="/home/tom/Documents/Projects/antsbin/bin/antsRegistration")
    parser.add_argument('--avgimgPath',
                        help="Path to the AverageImage executable",
                        default="/home/tom/Documents/Projects/antsbin/bin/AverageImages")


    args=parser.parse_args()
    
    main(args.input_avi,
        args.outdir,
        args.mask1,
        args.mask2,
        args.verbose,
        args.force,
        args.avconvPath,
        args.convtojpegPath,
        args.imPath,
        args.antsPath,
        args.avgimgPath)
