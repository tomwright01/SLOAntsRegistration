import subprocess
import os

def main(img1,img2,antsBin):
    cmd = '{0} 2 1 {1} {2}'.format(os.path.join(antsBin,'MeasureImageSimilarity'),
                                   img1,
                                   img2)
    try:
        correlationResult = subprocess.check_output(cmd,shell=True,executable='/bin/bash').split(' ')
        correlationIndex = correlationResult.index('metricvalue') + 1
        correlation = float(correlationResult[correlationIndex])
        return(correlation)
    except subprocess.CalledProcessError:
        return(0)