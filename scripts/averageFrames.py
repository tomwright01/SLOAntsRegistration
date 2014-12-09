import subprocess
import argparse
import logging
import os

def main(framelist,output,verbose,antsPath):
    """
    Create an average frame from frames in framelist
    """
    logging.info('Averaging frames with command:')
    logging.info('==============================')
    avgimgPath=os.path.join(antsPath,'AverageImages')
    frameStr = ' '.join(framelist)
    cmd = '{0} 2 {1} 1 {2}'.format(avgimgPath,output,frameStr)
    logging.info(cmd)
    logging.info('==============================')
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
