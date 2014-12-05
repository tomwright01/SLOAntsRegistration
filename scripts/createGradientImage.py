import subprocess
import logging

def main(dims,outputName,inputName,Sigma,imPath):
    """Use the ANTs ImageMath to create a gradient image"""
    cmd = '{0} {1} {2} Grad {3} {4}'.format(imPath,dims,outputName,inputName,Sigma)
    logging.info('Creating Gradient Image with command:')
    logging.info('=======================')
    logging.info(cmd)
    logging.info('=======================')
    try:
        subprocess.check_call(cmd,shell=True,executable='/bin/bash')
        return True
    except subprocess.CalledProcessError:
        return False
    