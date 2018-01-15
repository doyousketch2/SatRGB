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
import platform               ## determine if color teminal
from sys import exit
import easygui as eg           ##  Graphical User Interface
from binascii import hexlify   ##  convert bytes into ASCII
""" script  ============================================"""

def convert( img, outputpath ):
  with open( img, 'rb' ) as data:
    head, tail = os.path .split( img )
    root, ext  = os.path .splitext( tail )

    Identifier   = data .read(0x10)
    ID   = Identifier .split(b'\x00')[0] .split(b'\xFF')[0] .split(b'/')[0]
    ID2  = ID[:2]
    ID4  = ID[:4]

    SEGA2D   = b'SEGA_32BIT2DSCR\x1A'  ##  standard scroll data format
    DGT      = b'DIGITIZER 3 Ver2'     ##  index color mode
    RGB      = b'SEGA 32BITGRAPH\x1A'  ##  RGB color mode - 8 bit
    SX2D     = b'Sega Super32X 2D'     ##  32X scroll data format
    SEGA3D   = b'SEGA 3D'  ##  unused, but there's the header anyway
    DGT2PP   = b'PP'    ##  Packed Pixel  DGT2 types handle 15-bit colors
    DGT2DC   = b'DC'    ##  Direct Color
    DGT2RLE  = b'RL'    ##  RunLength Encoding
    AIFF     = b'FORM'  ##  Audio Interchange File
    FILM     = b'FILM'  ##  Cinepack Codec - Audio and/or Video
    ##  .arc  header: b'ARCH'   ??  archive format
    ##  .mfc  header: b'Rev.EXB'  ??

    ##  enable color for terminals that support it
    ten  = int( platform.release() .split('.')[0] )
    if os.name == 'posix' or 'ANSICON' in os.environ or ten >= 10:
      if ten >= 10:  ##  enable VT100 Escape Sequence for Win 10
        os.system('')  ##  dunno if this voodoo does anything, try ANSICON instead
      skip   = '\033[31mSkipping\033[0m'
      cyan   = '\033[36m'
      purple = '\033[35m'
      outro  = '\033[0m'
    else:
      skip   = 'Skipping'
      cyan   = ''
      purple = ''
      outro  = ''

    if ID == SEGA2D:
      print( '{}  {} {} SEGA2D scroll data format {}'.format( skip, tail, cyan, outro ) )

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
      print( '{}  {} {} Sega Super32X 2D scroll data {}'.format( skip, tail, cyan, outro ) )

    elif ID2 == DGT2PP:
      print( '{}  {} {} DGT2 PP - Packed Pixel data {}'.format( skip, tail, cyan, outro ) )

    elif ID2 == DGT2DC:
      print( '{}  {} {} DGT2 DC - Direct Color data {}'.format( skip, tail, cyan, outro ) )

    elif ID2 == DGT2RLE:
      print( '{}  {} {} DGT2 RL - Run Length Encoding {}'.format( skip, tail, cyan, outro ) )

    elif ID == AIFF:
      print( '{}  {} {} Audio Interchange File Format {}'.format( skip, tail, cyan, outro ) )

    elif ID == FILM:
      print( '{}  {} {} Cinepak Codec - Audio and/or Video {}'.format( skip, tail, cyan, outro ) )

    elif ID4 == b'RIFF':
      print( '{}  {} {} AudioVideo Interleave / Resource Interchange FileFormat {}'.format( skip, tail, cyan, outro ) )

    elif tail[:4] == 'cdda': 
      padding = ' ' * (len(tail) +10)
      print( '{}  {} {} CDDA "Red Book" Audio {}'.format( skip, tail, cyan, outro ) )
      print( '{} {} RAW 16‑bit Signed PCM,  44.1 kHz'.format( '\033[35m', padding, outro ) )

    else:
      HeaderPart2  = data .read(0x10)
      ## print('{}  {} {} Possible DGT index color mode {}'.format( skip, tail, cyan, outro ))
      if HeaderPart2 == DGT:
        print( '{}  {} {} DGT index color mode {}'.format( skip, tail, cyan, outro ) )

      elif ext == '.snd' or ext == '.pcm':
        print( '{}  {} {} RAW Signed 8 or 16 bit PCM Audio {}'.format( skip, tail, cyan, outro ) )

      elif ext:
        if ext[-1] .isdigit():
          if ext[:-1] == '.en' or ext[:-1] == '.el':
            print( '{}  {} {} RAW Signed 8 or 16 bit PCM Audio {}'.format( skip, tail, cyan, outro ) )

      elif ext == '.col':
        print( '{}  {} {} Indexed Color Palette {}'.format( skip, tail, cyan, outro ) )

      elif len(ID) < 1:  ##  don't bother printing a blank 0x00 or 0xFF header
        print( '{}  {}'.format( skip, tail, cyan, outro ) )
      else:
        print( '{}  {} {} header: {} {}'.format( skip, tail, cyan, ID, outro ) )


def main():
  ##  enable color for terminals that support it
  ten  = int( platform.release() .split('.')[0] )
  if os.name == 'posix' or 'ANSICON' in os.environ or ten >= 10:
    if ten >= 10:  ##  enable VT100 Escape Sequence for Win 10
      os.system('')  ##  dunno if this voodoo does anything, try ANSICON instead
    skip   = '\033[31mSkipping\033[0m'
    purple = '\033[35m'
    outro  = '\033[0m'
  else:
    skip   = 'Skipping'
    purple = ''
    outro  = ''

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

        listing  = os.listdir( directory )
        def extension(x):
          ##  split filename from extension, then reverse order
          ##  so we can use extension as key, and filename as value
          return os.path .splitext(x)[::-1]
        listing .sort( key = extension )

        for name in listing:
          obj  = os.path .join( directory, name )
          if os.path .isfile( obj ):
            convert( obj, outputdir )
          else:  ##  dirs
            print( skip, '        ', purple, obj, outro )
        print( '\nFinished scanning files in {}'.format( directory ) )
  else:
    exit()

main()

""" eof  ==============================================="""
