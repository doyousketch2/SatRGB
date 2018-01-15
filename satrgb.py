#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""====================================================="""
##  satrgb.py                                   14 Jan 2018
##  extract RGB images from Saturn files

##  @ Doyousketch2
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
""" required  ========================================="""
##  You'll need imagemagick.  Try your package manager or
##  https://www.imagemagick.org/script/download.php
##        sudo apt-get install imagemagick

##  You'll need easygui, depending on your OS:
##        sudo pip3 install easygui
##        sudo python3 -m pip install easygui
##        py -m pip install easygui

##  You might need the tkinter module (Debian, Ubuntu)
##        sudo apt-get install python-tk python3-tk
""" libs  ============================================="""
import os                         ##  commandline utilities
import pickle                   ## save previously used dir
from sys import exit
import easygui as eg           ##  Graphical User Interface
from binascii import hexlify   ##  convert bytes into ASCII
""" script  ============================================"""

def convert( img, outputpath ):
  with open( img, 'rb' ) as data:
    head, tail = os.path .split( img )
    root, ext  = os.path .splitext( tail )

    Identifier   = data .read(0x10)
    ID  = Identifier .split(b'\x00')[0] .split(b'\xFF')[0] .split(b'/')[0]

    SEGA2D   = b'SEGA_32BIT2DSCR\x1A'  ##  standard scroll data format
    DGT      = b'DIGITIZER 3 Ver2'     ##  index color mode
    RGB      = b'SEGA 32BITGRAPH\x1A'  ##  RGB color mode - 8 bit
    SX2D     = b'Sega Super32X 2D'     ##  32X scroll data format
    SEGA3D   = b'SEGA 3D'  ##  unused, but there's the header anyway
    DGT2PP   = b'PP'    ##  Packed Pixel  handles 32,768 colors
    DGT2DC   = b'DC'    ##  Direct Color
    DGT2RLE  = b'RL'    ##  RunLength Encoding
    AIFF     = b'FORM'  ##  Audio Interchange File
    FILM     = b'FILM'  ##  Cinepack Codec - Audio and/or Video

    skip  = '\033[31mSkipping\033[0m'
    intro  = '\033[36m'
    outro  = '\033[0m'

    ini  = ID[:2]
    if ini == DGT2PP or ini == DGT2DC or ini == DGT2RLE:
      ID  = ini

    elif ID[:4] == b'RIFF':
      print( '{}  {} {} AudioVideo Interleave / Resource Interchange FileFormat {}'.format( skip, tail, intro, outro ) )

    elif root[:4] == b'cdda': 
      print( '{}  {} {} CDDA "Red Book" Audio {}'.format( skip, tail, intro, outro ) )

    elif ID == SEGA2D:
      print( '{}  {} {} SEGA2D scroll data format {}'.format( skip, tail, intro, outro ) )

    elif ID == RGB:
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

    elif ID == SX2D:
      print( '{}  {} {} Sega Super32X 2D scroll data {}'.format( skip, tail, intro, outro ) )

    elif ID == DGT2PP:
      print( '{}  {} {} DGT2 PP - Packed Pixel data {}'.format( skip, tail, intro, outro ) )

    elif ID == DGT2DC:
      print( '{}  {} {} DGT2 DC - Direct Color data {}'.format( skip, tail, intro, outro ) )

    elif ID == DGT2RLE:
      print( '{}  {} {} DGT2 RL - Run Length Encoding {}'.format( skip, tail, intro, outro ) )

    elif ID == AIFF:
      print( '{}  {} {} Audio Interchange File Format {}'.format( skip, tail, intro, outro ) )

    elif ID == FILM:
      print( '{}  {} {} Cinepak Codec - Audio and/or Video {}'.format( skip, tail, intro, outro ) )

    else:
      Identifier2  = data .read(0x10)
      if Identifier2 == DGT:
        print( '{}  {} {} DGT index color mode {}'.format( skip, tail, intro, outro ) )

      elif ext == '.col':
        print( '{}  {} {} Indexed Color Palette {}'.format( skip, tail, intro, outro ) )

      elif len(ID) < 1:  ##  don't bother printing a blank 0x00 or 0xFF header
        print( '{}  {}'.format( skip, tail, intro, outro ) )
      else:
        print( '{}  {} {} header: {} {}'.format( skip, tail, intro, ID, outro ) )


def main():
  info  = 'Convert Sega Saturn RGB images to PNG'
  title  = 'satrgb'

  choice  = eg.buttonbox( info, title, ['one file', 'entire directory'] )

  cwd  = os.getcwd()
  previndir  = os.path .join( cwd, 'indir.pkl' )
  if os.path .isfile( previndir ):
    with open( previndir, 'rb' ) as picklejar:
      default_in  = pickle .load( picklejar )
  else:  default_in  = cwd


  prevoutdir  = os.path .join( cwd, 'outdir.pkl' )
  if os.path .isfile( prevoutdir ):
    with open( prevoutdir, 'rb' ) as picklejar:
      default_out  = pickle .load( picklejar )
  else:  default_out  = cwd


  if choice == 'one file':
    imagefile  = eg.fileopenbox( 'choose image', title, default_in )
    if imagefile is None:  exit()
    else:
      head, tail = os.path .split( imagefile )
      with open( previndir, 'wb' ) as picklejar:
        pickle .dump( head, picklejar )
      outputdir  = eg.diropenbox( 'choose output dir', title, default_out )
      if outputdir is None:  exit()
      else:
        with open( prevoutdir, 'wb' ) as picklejar:
          pickle .dump( outputdir, picklejar )
        convert( imagefile, outputdir )

  elif choice == 'entire directory':
    directory  = eg.diropenbox( 'choose dir', title, default_in )
    if directory is None:  exit()
    else:
      with open( previndir, 'wb' ) as picklejar:
        pickle .dump( directory, picklejar )
      outputdir  = eg.diropenbox( 'choose output dir', title, default_out )
      if outputdir is None:  exit()
      else:
        with open( prevoutdir, 'wb' ) as picklejar:
          pickle .dump( outputdir, picklejar )
        print( 'Scanning files in {}\n'.format( directory ) )

        files  = os.listdir( directory )
        def extension(x):
           return os.path .splitext(x)[::-1]
        files .sort( key = extension )

        for name in files:
          obj  = os.path .join( directory, name )
          if os.path .isfile( obj ):
            convert( obj, outputdir )
        print( '\nFinished scanning files in {}'.format( directory ) )
  else:
    exit()

main()

""" eof  ==============================================="""
