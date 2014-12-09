import subprocess
import logging
import os

def main(fixedImage,movingImage,blobFixed,blobMoving,candidateCount,finalCount,dilate,antsPath):
    """find blobs"""
    logging.info('Finding Blobs with command')
    imPath=os.path.join(antsPath,'ImageMath')
    cmd_findBlobs = '{0} {1} {2} BlobDetector {3} {4} {5} {6} {7}'.format(imPath,
                                                                          2,
                                                                          blobFixed,
                                                                          fixedImage,
                                                                          candidateCount,
                                                                          movingImage,
                                                                          blobMoving,
                                                                          finalCount)
    cmd_dilate = '{0} {1} {2} GD {2} {3}'
    try:
        logging.info('==========================')
        logging.info(cmd_findBlobs)
        logging.info('==========================')
        subprocess.check_call(cmd_findBlobs,shell=True,executable='/bin/bash')
        logging.info('Dilating blobs with command')
        cmd=cmd_dilate.format(imPath,
                              2,
                              blobFixed,
                              dilate)
        subprocess.check_call(cmd,shell=True,executable='/bin/bash')
        logging.info('==========================')
        logging.info(cmd)
        logging.info('==========================')        
        cmd=cmd_dilate.format(imPath,
                              2,
                              blobMoving,
                              dilate)
        logging.info('==========================')
        logging.info(cmd)
        logging.info('==========================')                
        subprocess.check_call(cmd,shell=True,executable='/bin/bash')        
        return True
    except subprocess.CalledProcessError:
        return False    