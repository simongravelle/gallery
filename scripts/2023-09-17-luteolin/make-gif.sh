#!/bin/bash

if [ -f luteolin.mp4 ] ;
then
    rm luteolin.mp4
fi

ffmpeg -r 60 -i movie.%05d.ppm -vcodec libx264 -crf 0  -pix_fmt yuv420p luteolin.mp4

if [ -f luteolin.webp ] ;
then
    rm luteolin.webp
fi

ffmpeg -i luteolin.mp4 -vcodec libwebp -filter:v fps=fps=20 -crf 0 -loop 0 -preset default -an -vsync 0 luteolin.webp

