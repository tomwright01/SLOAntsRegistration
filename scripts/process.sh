#!/bin/bash

NUMBEROFTHREADS=2

ORIGINALNUMBEROFTHREADS=${ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS}
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=$NUMBEROFTHREADS
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

ants="/home/tom/Documents/Projects/antsbin/Scripts/antsRegistrationSyNQuick.sh"
IM="/home/tom/Documents/Projects/antsbin/bin/ImageMath"

fixed="frames/image-014.tiff"
METRICS=''
FILES="frames/*"
#FILES="frames/image-001.tiff"
for f in $FILES
do
    fname=${f%.*}
    fname=${fname##*/}
    moving="frames/$fname.tiff"
    #moving="-m working/new.tiff"
    #$ants -d 2 $fixed $moving -o tmp/output -t a
    #antsRegistration \
    #    --dimensionality 2 \
    #    --float 0 \
    #    --output [tmp/output,tmp/outputWarped.nii.gz,tmp/outputInverseWarped.nii.gz] \
    #    --interpolation Linear \
    #    --use-histogram-matching 0 \
    #    --winsorize-image-intensities [0.005,0.995] \
    #    --initial-moving-transform [$fixed,$moving,1] \
    #    --transform Rigid[0.1] \
    #    --metric MI[$fixed,$moving,1,32,Regular,0.25] \
    #    --convergence [1000x500x250x0,1e-6,10] \
    #    --shrink-factors 12x8x4x2 \
    #    --smoothing-sigmas 4x3x2x1vox \
    #    --masks [mask_s.bmp, mask_s.bmp]
        #--transform Affine[0.1] \
        #--metric MI[$fixed,$moving,1,32,Regular,0.25] \
        #--convergence [1000x500x250x0,1e-6,10] \
        #--shrink-factors 12x8x4x2 \
        #--smoothing-sigmas 4x3x2x1vox \

    #ConvertToJpg tmp/outputWarped.nii.gz final/$fname.jpg

    METRIC+=(`$IM 2 place.jpg NormalizedCorrelation $fixed final/$fname.jpg mask_s.bmp`)
    #rm working/new.tiff
done;
function mysort { for i in ${METRIC[@]}; do echo "$i"; done | sort -n; }

sorted_array=( $(mysort) )

echo "Sorted array: ${sorted_array[@]}"

avconv -f image2 -i final/image-%3d.jpg output.avi
