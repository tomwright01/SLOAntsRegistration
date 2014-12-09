import processRecordingSession
import tempfile
import os
import re
import shutil
import logging

logging.basicConfig(filename='log.log',level=logging.DEBUG)
logging.info('Started')

baseDir = '/mnt/AO/AO Data'
antsPath = '/home/tom/Documents/Source/antsbin/bin'

sourceDirs = [['539','141010'],
              ['496','141021'],
              ['538','141103'],
              ['545','141112'],
              ['544','141111'],
              ['547','141112'],
              ['546','141118'],
              ['549','141121'],
              ['548','141124'],
              ['552','141203'],
              ['515','141205'],
              ['550','141205'],
              ['304','141208']]

for iDir in range(len(sourceDirs)):
    logging.debug('Processing source dir:{0}/{1}'.format(sourceDirs[iDir][0],sourceDirs[iDir][1]))
                  
    localDir=tempfile.mkdtemp()
    sourceDir=os.path.join(baseDir,sourceDirs[iDir][0],sourceDirs[iDir][1])
    #copy the source files into localDir
    input_files = [f for f in os.listdir(sourceDir) if re.match(r'(SLO_refl_video).*(avi)',f)]
    input_files = [f for f in input_files if os.stat(os.path.join(sourceDir,f)).st_size < 100000000]
    
    for f in input_files:
        try:
            shutil.copyfile(os.path.join(sourceDir,f),
                            os.path.join(localDir,f))
        except:
            logging.debug('Failed copying file:{0}'.format(os.path.join(sourceDir,f)))
            
    #all files copied locally, call processRecordingSession
    processRecordingSession.main(localDir,None,None,1,1,antsPath)
    #This should have created a directory called 'Registered', this is all we need to copy back
    #this currently contains all the registered images, there are large. Going to delete them for now.
    purge(localDir,'nii.gz')
    
    shutil.copytree(os.path.join(localDir,'Registered'),
                    os.path.join(sourceDir,'Registered'))
    
    
    shutil.rmtree(localDir)
    
def purge(dir,pattern,inclusive=True):
    regexObj = re.compile(pattern)
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            if bool(regexObj.search(path)) == bool(inclusive):
                os.remove(path)
        for name in dirs:
            path = os.path.join(root, name)
            if len(os.listdir(path)) == 0:
                os.rmdir(path)