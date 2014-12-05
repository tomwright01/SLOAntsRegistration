import subprocess
import os
import logging

def main(fixedImage,movingImage,fixedBlob,movingBlob,outputImage,maskImage,workingPath,antsBinPath):
    logging.info('Registering frames')
    blobMatch = os.path.join(workingPath,'blobMatch.mat')
    logging.info('Blob match path:{0}'.format(blobMatch))
    cmd1 = '{0} {1} {2} affine {3}'.format(os.path.join(antsBinPath,'ANTSUseLandmarkImagesToGetAffineTransform'),
                                          fixedBlob,
                                          movingBlob,
                                          blobMatch)
    cmd2 = '{0} -d {1} -t {2} -i {3} -r {4} -o {5}'.format(os.path.join(antsBinPath,'antsApplyTransforms'),
                                                           2,
                                                           blobMatch,
                                                           movingImage,
                                                           fixedImage,
                                                           outputImage)
    cmd3 = """{0} -r {1} -d 2 -f --float 1 \
    --output [{2},{3},{4}] \
    --interpolation Linear \
    --use-histogram-matching 1 \
    --winsorize-image-intensities [0.005,0.995] \
    --transform affine[0.1] \
    --convergence [100x70x50x10,1e-6,10] \
    --shrink-factors 4x4x2x1 \
    --smoothing-sigmas 3x2x1x0vox \
    --metric mattes[{5},{6},1,32,Random,0.5] \
    --transform SyN[0.1,6,0.0] \
    --convergence [100x70x50x10,1e-6,10] \
    --shrink-factors 4x4x2x1 \
    --smoothing-sigmas 3x2x1x0vox \
    --metric cc[{5},{6},1,4] \
    -x {7}"""
    
    cmd3 = cmd3.format(os.path.join(antsBinPath,'antsRegistration'),
                       blobMatch,
                       os.path.join(workingPath,'output'),
                       os.path.join(workingPath,'outputWarped.nii.gz'),
                       os.path.join(workingPath,'outputInverseWarped.nii.gz'),
                       fixedImage,
                       movingImage,
                       maskImage)
    cmd4 = '{0} -d 2 -t {1} -t {2} -i {3} -r {4} -o {5}'.format(os.path.join(antsBinPath,'antsApplyTransforms'),
                                                               os.path.join(workingPath,'output1Warp.nii.gz'),
                                                               os.path.join(workingPath,'output0GenericAffine.mat'),
                                                               movingImage,
                                                               fixedImage,
                                                               outputImage)
    try:
        logging.info('Registering blobs with command:')
        logging.info('===============================')
        logging.info(cmd1)
        logging.info('===============================')
        subprocess.check_call(cmd1,shell=True,executable='/bin/bash')
        
        logging.info('Applying blob transform with command:')
        logging.info('===============================')
        logging.info(cmd2)
        logging.info('===============================')        
        subprocess.check_call(cmd2,shell=True,executable='/bin/bash')

        logging.info('Performing image registration with command:')
        logging.info('===============================')
        logging.info(cmd3)
        logging.info('===============================')        
        subprocess.check_call(cmd3,shell=True,executable='/bin/bash')

        logging.info('Applying image registration with command:')
        logging.info('===============================')
        logging.info(cmd4)
        logging.info('===============================')        
        subprocess.check_call(cmd4,shell=True,executable='/bin/bash')
        return True
    except subprocess.CalledProcessError:
        return False
    