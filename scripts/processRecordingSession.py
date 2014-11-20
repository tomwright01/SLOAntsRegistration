import os
import re
import argparse
import registerSLO

def main(folder,mask1,mask2,verbose,force,avconvPath,convtojpegPath,imPath,antsPath,avgimgPath):
    """Uses the registerSLO.py script to process all SLO recordings in a session.
    Creates a sub folder for each SLO recording, 
    tries to register the frames and create an average image.
    """
    
    input_files = [f for f in os.listdir(folder) if re.match(r'(SLO_refl_video).*(avi)',f)]
    input_files = [f for f in input_files if os.stat(os.path.join(folder,f)).st_size < 100000000]

    output_dir = os.path.join(folder,'Registered')    
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for f in input_files:
        match=re.search('(SLO_refl_video).*([0-9]{6})(.avi)',input_files[0])
        time_stamp = match.group(2)
        working_dir = os.path.join(output_dir,time_stamp)
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        
        src_file = os.path.join(folder,f)
        
        registerSLO.main(src_file,working_dir,mask1,mask2,verbose,force,avconvPath,convtojpegPath,imPath,antsPath,avgimgPath)
        
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Register frames in an SLO file using scripts and executables from ANTs')
    parser.add_argument('input_avi',help="Path to the input directory")
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
        args.mask1,
        args.mask2,
        args.verbose,
        args.force,
        args.avconvPath,
        args.convtojpegPath,
        args.imPath,
        args.antsPath,
        args.avgimgPath)
