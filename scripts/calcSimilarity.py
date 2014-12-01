import subprocess
import argparse
import tempfile
import os
def main(img1,img2,mask,verbose,IMPath):
    """
    Uses ANT executable ImageMath to calculate similarity between two images.
    """
    temploc = os.path.join(tempfile.gettempdir(),'place.nii')
    if mask is not None:
        cmd = '{0} 2 {4} NormalizedCorrelation {1} {2} {3}'.format(IMPath,img1,img2,mask,temploc)
    else:
        cmd = '{0} 2 {4} NormalizedCorrelation {1} {2}'.format(IMPath,img1,img2,mask,temploc)
    #cmd = '{0} 2 place.jpg Mattes {1} {2} {3}'.format(IMPath,img1,img2,mask)
    
    if verbose:
        print("Called command:{0}".format(cmd))
    
    correlation = subprocess.check_output(cmd,shell=True,executable='/bin/bash')
    
    if __name__ == "__main__":
        print("Correlation={0}".format(correlation))
    
    return(float(correlation.strip()))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses ANT executable ConvertToJpg to convert from *.nii.gz to jpg')
    parser.add_argument('img1',help="Path to the first image")
    parser.add_argument('img2',help="Path to the second image")
    parser.add_argument('-m','--mask',
                        help="name of the image to use as a mask")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--IMPath',help='path to the ImageMath executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/ImageMath')

    args=parser.parse_args()
    main(args.img1,args.img2,args.mask,args.verbose,args.IMPath)    
