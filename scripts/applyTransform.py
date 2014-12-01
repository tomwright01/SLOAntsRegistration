import subprocess
import argparse

def main(input, output, transform, reference ,verbose, applyPath):
    cmd = '{0} -d 2 -i {1} -o {2} -t {3} -r {4}'.format(applyPath, input, output, transform, reference)
    if verbose:
        print "Called command:{0}".format(cmd)
    subprocess.check_call(cmd,shell=True,executable='/bin/bash')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses ANT executable antsApplyTransform to apply a previously generated transform to an image')
    parser.add_argument('input',help="Path to the input image")
    parser.add_argument('output',help="Path to the output image")
    
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--transform',help='transform file')
    parser.add_argument('--reference',help='reference file')

    parser.add_argument('--exePath',help='path to the antsApplyTransform executable',
                        default='/home/tom/Documents/Projects/antsbin/bin/antsApplyTransform')

    args=parser.parse_args()
    main(args.framelist,args.output,args.transform,args.reference,args.verbose,args.exePath)
