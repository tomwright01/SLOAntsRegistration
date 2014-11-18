import subprocess
import argparse

def main(finput,dest,name,verbose,avconvPath):
    """
    Uses avconv executable to extract frames in a movie.
    """

    cmd = '{0} -i {1} -f image2 {2}{3}'.format(avconvPath,finput,dest,name)
    if verbose:
        print "Called command:{0}".format(cmd)
    subprocess.check_call(cmd,shell=True,executable='/bin/bash')
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses avconv to extract frames in a movie')
    parser.add_argument('input',help="Path to the input movie")
    parser.add_argument('-d','--dest',help="path to place the extracted frames",
                        default='frames/')
    parser.add_argument('-n','--name',help="filename to use for extracted frames",
                        default='frame-%03d.tiff')
    parser.add_argument('-v','--verbose',action="store_true")
    parser.add_argument('--avconvPath',help='path to the avconv executable',
                        default='/usr/bin/avconv')

    args=parser.parse_args()
    main(args.input,args.dest,args.name,args.verbose,args.avconvPath)
