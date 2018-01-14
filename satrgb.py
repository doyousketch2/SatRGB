#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""====================================================="""
##  satrgb.py                                   14 Jan 2018
##  extract RGB images from Saturn files

##  @ Doyousketch2
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
""" required  ========================================="""
##  you'll need imagemagick.  Try your package manager or
##  https://www.imagemagick.org/script/download.php

##  you'll need easygui, depending on your OS:
##        sudo pip3 install easygui
##        sudo python3 -m pip install easygui
##        py -m pip install easygui

##  you might need the tkinter module
##        sudo apt-get install python-tk python3-tk
""" libs  ============================================="""
import os                         ##  commandline utilities
from sys import exit
import easygui as eg           ##  Graphical User Interface
from binascii import hexlify   ##  convert bytes into ASCII
""" script  ============================================"""

def convert( img, outputpath ):
  with open( img, 'rb' ) as data:
    head, tail = os.path .split( img )
    root, ext  = os.path .splitext( tail )

    MagicWord  = b'SEGA 32BITGRAPH\x1a'
    Identifier  = data .read(0x10)

    if Identifier != MagicWord:
      words  = Identifier.split(b'\x00')[0]
      if len(words) < 1:  ##  don't bother printing a blank header
        print( 'skipping  {}'.format( tail ) )
      else:
        print( 'skipping  {}  header: {}'.format( tail, words ) )
    else:  ##  found a match, convert it
      data .read(0x4)  ##  discard 0xFFFF FFFF
      data .read(0x4)  ##  discard 0x0000 0000

      w  = hexlify( data .read(0x02) )
      h  = hexlify( data .read(0x02) )

      offset  = 256
      width   = int( w, 16 )
      height  = int( h, 16 )
      output  = '{}.png'.format( root )

      args = [ 'convert ',
               '-depth 8 ',
               '-endian MSB '
               '-size {}x{}+{} '.format( width, height, offset ) ]
      call  = '' .join( args )
      inner  = 'RGB:{} '.format( img )
      outer  = os.path .join( outputpath, output )
      print( '{}\n{}\n{}\n'.format( call, inner, outer ) )
      os .system( call + inner + outer )

##  convert -depth 8 -endian MSB -size 144x192+256
##  rgb:inpath/input.rgb  outpath/output.png

def main():
  info  = 'Convert Sega Saturn RGB images to PNG'
  title  = 'satrgb'

  choice  = eg.buttonbox( info, title, ['one file', 'entire directory'] )

  if choice == 'one file':
    imagefile  = eg.fileopenbox( 'choose image', title )
    if imagefile is None:  exit()
    else:
      outputdir  = eg.diropenbox( 'choose output dir', title )
      if outputdir is None:  exit()
      else:
        convert( imagefile, outputdir )

  elif choice == 'entire directory':
    directory  = eg.diropenbox( 'choose dir', title )
    if directory is None:  exit()
    else:
      outputdir  = eg.diropenbox( 'choose output dir', title )
      if outputdir is None:  exit()
      else:
        for name in os .listdir( directory ):
          obj  = os.path .join( directory, name )
          if os.path .isfile( obj ):
            convert( obj, outputdir )
  else:
    exit()

main()

""" eof  ==============================================="""
