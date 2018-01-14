**satrgb.py** -- *extract RGB images from Sega Saturn files*  

---

Open one file, or an entire directory.  
Select where you want your file(s) to be saved.  

It reads header information to determine image size,  
then uses ImageMagick to do the conversion.  

---

You'll need **imagemagick**.  Try your package manager or  
https://www.imagemagick.org/script/download.php  

You'll need **easygui**.  Depending on your OS:  
    `sudo pip3 install easygui`  
    `sudo python3 -m pip install easygui`  
    `py -m pip install easygui`  

You might need the *tkinter* module  
    `sudo apt-get install python-tk python3-tk`  
