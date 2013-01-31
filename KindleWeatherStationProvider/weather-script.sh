#!/bin/sh

cd "$(dirname "$0")"

python2 KindleWeatherStationProvider.py
rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg
pngcrush -c 0 -ow weather-script-output.png weather-script-output-crushed.png
cp -f weather-script-output-crushed.png /home/rudzn/development_public/weather/weather-script-output.png
