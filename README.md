# CUE-Sheet-Tracks

### A script to extract tracks from a music CD with CUE sheet.
## Requirements
Python

FFmpeg
## How to use?
Install the script and run in command line.

Pass the location where the CUE sheet is located

Pass the extract location where the tracks will be extracted to. In case you dont, the tracks will be extracted to where the script is located.

Let the script run and Voilà.

## Options
`-i` : Path to the Cue sheet

`-o` : (Optional) Path where the tracks will be extracted to

`-c` : (Optional) Path to add custom album art to the tracks

## Usage:

`CUE.py -i 'Cue Path'`

`CUE.py -i 'Cue Path' -o 'ExtractLocation'`



## How to add a custom album art to the tracks?
When you run the script in command line, simply pass the image path in the following way:

`CUE.py -i "Cue Path" -c "C:\Users\Desktop\cover.jpg"`

## Issues
If there are any issues, please raise it [here](https://github.com/fischpo/CUE-Sheet-Tracks/issues).




---


#### If you want the script with the old way you can get it [here](https://github.com/fischpo/CUE-Sheet-Tracks/blob/6ab3981671d760c4313ee3c4ebf402fe41d68b95/CUE.py)
