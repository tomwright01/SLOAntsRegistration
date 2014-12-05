import nibabel as nib
import numpy as np

def write(array,fname):
    """Write a numpy array as a nifti format image
    array - numpy array currently NxM
    fname - full path to output file"""
    
    img=nib.Nifti1Image(array,np.eye(4))
    img.to_filename(fname)
    
def read(fname):
    img=nib.load(fname)