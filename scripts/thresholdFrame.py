import subprocess
import argparse

def main(input, output, lowThresh, highThresh,verbose,threshPath):
    cmd = '{0} 2 {1} {2} {3} {4}'.format(threshPath, input, output, lowThresh, highThresh)
    if verbose:
        print "Called command:{0}".format(cmd)
    subprocess.check_call(cmd,shell=True,executable='/bin/bash')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses ANT executable ThresholdImage to create a BinaryImage')
    parser.add_argument('input',help="Path to the input image")
    parser.add_argument('output',help="Path to the output image")
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--lowThresh',help='low Threshold',
                        default=95)
    parser.add_argument('--highThresh',help='low Threshold',
                        default=150)
    parser.add_argument('--exePath',help='path to the ThresholdImage executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/ThresholdImage')

    args=parser.parse_args()
    main(args.input,args.output,args.lowThresh,args.highThresh,args.verbose,args.exePath)
