#!/bin/bash
# Credit to Otello M Roscioni from Bristol who kindly shared his script : https://matsci.org/u/hothello

export LC_NUMERIC="en_US.UTF-8"

set -e

format=1920x1136 # 480x284 # 960x568

# resize and add transparent backgroung
# AA
#for file in _AA-dark/_untitled.*.ppm; 
#do
#    convert $file -resize $format ${file:0:24}.png; # -transparent black 
#done
# CG
#for file in _CG-dark/_untitled.*.ppm; 
#do
#    convert $file -resize $format ${file:0:24}.png; # -transparent black
#done

for i in {0..199}; 
do
    # x1 = start of the gradient
    x1=$(printf "%.0f" $(bc -l<<<\($i+1\)*8))
    # x2 = end of the gradient
    x2=$(printf "%.0f" $(bc -l<<<\($i+1\)*10))
    j=$(printf "%05i" $(bc -l<<<$i))
    # create a linear gradient file
    convert -size $format -define gradient:vector=$x1,500,$x2,500,angle=90 gradient:white-black linear_gradient.png
	# compose the 2 images
    convert simulation/CG-dark.$j.ppm linear_gradient.png -alpha remove -compose CopyOpacity -composite simulation/AA-dark.$j.ppm -compose DstOver -composite base_out.png
    convert -alpha remove base_out.png merged/untitled.$j.png
done

#rm linear_gradient.png base_out.png
# q is compression factor, default 75, d is the duration
img2webp -o PEG.webp  -q 45 -d 33.33 merged/*.png # -q 100 -mixed
