#!/bin/bash

if [ -f fullrene.mp4 ] ;
then
    rm fullrene.mp4
fi

ffmpeg -r 60 -i video/untitled.%05d.ppm -vcodec libx264 -crf 0  -pix_fmt yuv420p fullrene.mp4

if [ -f fullrene.webp ] ;
then
    rm fullrene.webp
fi

ffmpeg -i fullrene.mp4 -vcodec libwebp -filter:v fps=fps=20 -crf 0 -loop 0 -preset default -an -vsync 0 fullrene.webp

