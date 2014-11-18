import subprocess
import argparse

def main(framelist,output,verbose,avgimgPath):
    """
    Create an average frame from frames in framelist
    """
    frameStr = ' '.join(framelist)
    cmd = '{0} 2 {1} 1 {2}'.format(avgimgPath,output,frameStr)
    if verbose:
        print "Called command:{0}".format(cmd)
    subprocess.check_call(cmd,shell=True,executable='/bin/bash')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses ANT executable AverageImage to average frames together')
    parser.add_argument('framlist',help="list of frames to include in average")
    parser.add_argument('output',help="Path to the output image")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--exePath',help='path to the AverageImage executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/AverageImages')

    args=parser.parse_args()
    main(args.framelist,args.output,args.verbose,args.exePath)
