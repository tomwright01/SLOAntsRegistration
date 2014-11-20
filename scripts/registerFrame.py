import subprocess
import argparse

def main(fixed,moving,verbose,working,mask,antsPath):
    """
    Uses ANTs scripts and executables to register frames in a movie.
    INPUTS:
    fFixed - path to fixed image
    fMoving - path to moving image
    fFixedMask [optional]    
    fMovingMask [optional]
    
    Example:
    registerMovie('frames/image-001.tiff','image-014.tiff')
    """
   
                       
    antsArgs = {'dimensionality':'2',
                'float':'0',
                'interpolation':'Linear',
                'use-histogram-matching':'0',
                'winsorize-image-intensities':'[0.005,0.995]',
                'transform':'Rigid[0.1]',
                'convergence':'[1000x500x250x0,1e-6,10]',
                'shrink-factors':'12x8x4x2',
                'smoothing-sigmas':'4x3x2x1vox',
                'output':'[{0},{0}Warped.nii.gz,{0}InverseWarped.nii.gz]'.format(working),
                'initial-moving-transform':'["{0}","{1}",1]'.format(fixed,moving),
                'metric':'MI["{0}","{1}",1,32,Regular,0.25]'.format(fixed,moving)
                }
                
    if mask is not None:
        antsArgs['masks']='[{0},{0}]'.format(mask)
        
    #Build the argument string from the argument dictionary
    str_args = ''
    for k,v in antsArgs.items():
        str_args+='--{0} {1} '.format(k,v)

    str_args = antsPath + ' ' + str_args    

    if verbose:
        print(str_args)
        #print(args.antsPath + ' ' + str_args)

    subprocess.check_call(str_args,shell=True,executable='/bin/bash')
    #subprocess.check_call([args.antsPath,'--help'])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Use ANTs scripts to register an image')
    parser.add_argument('fixed',help="Path to the fixed image")
    parser.add_argument('moving',help="Path to the moving image")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('-w','--working',
                        help="Path and prefix for the working files",
                        default='tmp/output')
    parser.add_argument('-m','--mask',
                        help="name of the image to use as a mask")
    parser.add_argument('--antsPath',
                        help="Path to the antsRegistration executable",
                        default="/home/tom/Documents/Projects/antsbin/bin/antsRegistration")

                        
    args = parser.parse_args()

    main(args.fixed,args.moving,args.verbose,args.working,args.mask,args.antsPath)
