[![OpenSource](https://img.shields.io/badge/Open-Source-orange.svg)](https://github.com/doyousketch2)  [![PythonVersions](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPL--v3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)  [![Git.io](https://img.shields.io/badge/Git.io-vNcV1-233139.svg)](https://git.io/vNcV1) 

**satrgb.py** -- *extract RGB images from Sega Saturn files*  

---
So far, this script extracts:  
>SEGA_32BITGRAPH data in RGB color mode  
>DGT2 DC - Direct Color data  

Can possibly read, need to find a disk with these image types to test on.
>DGT2 RL - Run Length Encoding
>DGT2 PP - Packed Pixel data

There's a few more formats, I'll add them, once deciphered.  

Open one file, or an entire directory.  
Select where you want your file(s) to be saved.  

It reads header information to determine image size,  
then uses ImageMagick to do the conversion.  

---
You'll need **Python**.  You may already have it installed.  If not:  
https://www.python.org/downloads

You'll need **ImageMagick**.  Try your package manager or  
https://www.imagemagick.org/script/download.php  
    `sudo apt-get install imagemagick`  

You'll need the **EasyGui** module for Python.  Depending on your OS:  
    `sudo pip3 install easygui`  
    `sudo python3 -m pip install easygui`  
    `py -m pip install easygui`  

You might need the *tkinter* module (Debian, Ubuntu)  
    `sudo apt-get install python-tk python3-tk`  

---
Usage depends on how you call Python scripts within your OS:  
    `./satrgb.py`  
    `py -m satrgb.py`  
    `python3 -m satrgb.py`  

Console output prefers to *print in color*,  
so if you're on an old version of windows  
that doesn't, then *enable VT100 emulation*  
or try ANSICON  http://adoxa.altervista.org/ansicon
