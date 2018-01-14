[![OpenSource](https://img.shields.io/badge/Open-Source-orange.svg)](https://github.com/doyousketch2)  [![PythonVersions](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPL--v3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)  [![Git.io](https://img.shields.io/badge/Git.io-vNcV1-233139.svg)](https://git.io/vNcV1) 

**satrgb.py** -- *extract RGB images from Sega Saturn files*  

---

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
