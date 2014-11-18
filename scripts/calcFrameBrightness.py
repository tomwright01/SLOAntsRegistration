import argparse
import subprocess

def main(img1,mask,verbose,exePath):
    """Uses the ANTs ImageMath executable to calulate the total brightness of an image.
    The brightest frame is often the one in best focus.
    """
    if mask is None:
        cmd = '{0} 2 place.nii total {1}'.format(exePath,img1)
    else:
        cmd = '{0} 2 place.nii total {1} {2}'.format(exePath,img1,mask)
        
    if verbose:
        print("Called command:{0}".format(cmd))
    
    brightness = subprocess.check_output(cmd,shell=True,executable='/bin/bash')
    brightness = float(brightness.split(' ')[3])
    if __name__ == "__main__":
        print("Correlation={0}".format(brightness))
    
    return(brightness)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses the ANTs ImageMath executable to calulate the total brightness of an image')
    parser.add_argument('img1',help="Path to the first image")
    parser.add_argument('-m','--mask',
                        help="name of the image to use as a mask")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--IMPath',help='path to the ImageMath executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/ImageMath')

    args=parser.parse_args()
    main(args.img1,args.mask,args.verbose,args.IMPath)    
