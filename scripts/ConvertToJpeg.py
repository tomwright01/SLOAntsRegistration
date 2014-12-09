import subprocess
import argparse
import os

def main(finput,output,verbose,antsPath):
    """
    Uses ANT executable ConvertToJpg to convert from *.nii.gz to jpg.
    """
    exePath = os.path.join(antsPath,'ConvertToJpg')
    cmd = '{0} "{1}" "{2}"'.format(exePath,finput,output)
    if verbose:
        print "Called command:{0}".format(cmd)
    subprocess.check_call(cmd,shell=True,executable='/bin/bash')
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses ANT executable ConvertToJpg to convert from *.nii.gz to jpg')
    parser.add_argument('input',help="Path to the input image")
    parser.add_argument('output',help="Path to the output image")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--antsPath',help='path to the antsbin binaries',
                        default='/home/tom/Documents/Projects/antsbin/bin/ConvertToJpg')

    args=parser.parse_args()
    main(args.input,args.output,args.verbose,args.exePath)
