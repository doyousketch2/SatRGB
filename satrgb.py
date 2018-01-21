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
import struct                    ## deconstructed bytearray
import pickle                   ## save previously used dir
import platform               ## determine if color teminal
from sys import exit
import easygui as eg           ##  Graphical User Interface
from binascii import hexlify   ##  convert bytes into ASCII
""" script  ============================================"""

info  = 'Convert Sega Saturn RGB images to PNG'
title  = 'satrgb'

def generate_png( buf, width, height ): 
  import zlib, struct
  ''' RGBA buf: must be bytes or a bytearray in Python3.x,
           or a regular string in Python2.x  '''

  width_byte_4  = width *4  ##  reverse vertical line order and add null bytes at start
  raw_data  = b'' .join( b'\x00' +buf[ span:span +width_byte_4 ]
                  for span in range( ( height -1 ) *width_byte_4, -1, -width_byte_4 ) )

  def png_pack( png_tag, data ):
    chunk_head  = png_tag +data
    beui  = '!I'  ##  big endian, u_int = 8 hex digits
    return ( struct .pack( beui,  len(data) ) +chunk_head +
             struct .pack( beui,  0xFFFFFFFF & zlib .crc32( chunk_head ) ) )

  return b''.join( [
      b'\x89PNG\r\n\x1a\n',  ##  big endian, 2 u_ints, 5 u_chars, so 26 hex digits
      png_pack( b'IHDR',  struct .pack( '!2I5B',  width,  height, 8, 6, 0, 0, 0 ) ),
      png_pack( b'IDAT',  zlib .compress( raw_data, 9 ) ),
      png_pack( b'IEND',  b'' ) ] )


def convert( img, outputpath ):
  with open( img, 'rb' ) as data:
    head, tail = os.path .split( img )
    root, ext  = os.path .splitext( tail )

    Identifier   = data .read(0x10)  ##  first 16 bytes, then discard gibberish
    ID   = Identifier .split(b'\x00')[0] .split(b'\xFF')[0] .split(b'/')[0]
    ID2  = ID[:2]  ##  DGT2 only use 2 chars for it's magic word
    ID4  = ID[:4]  ##  a few types use 4 chars

    SEGA2D   = b'SEGA_32BIT2DSCR\x1A'  ##  standard scroll data format
    SCR      = b'SEGA SATURN SCR'      ##
    DGT      = b'DIGITIZER 3 Ver2'     ##  index color mode
    RGB      = b'SEGA 32BITGRAPH\x1A'  ##  RGB color mode - 8 bit
    SX2D     = b'Sega Super32X 2D'     ##  32X scroll data format
    SEGA3D   = b'SEGA 3D'  ##  unused, but there's the header anyway
    DGT2PP   = b'PP'    ##  Packed Pixel  DGT2 types handle 15-bit colors
    DGT2DC   = b'DC'    ##  Direct Color
    DGT2RLE  = b'RL'    ##  RunLength Encoding
    AIFF     = b'FORM'  ##  Audio Interchange File
    FILM     = b'FILM'  ##  Cinepack Codec - Audio and/or Video

    ##   ext  header:      best guess            example of filetype found in...
    ##  ~~~~  ~~~~~~       ~~~~~~~~~~~           ~~~~~~~
    ##  .arc  b'ARCH'      archive format        Zero Divide
    ##  .bz   b'BZ.w\x01'  nonstandard bzip      Tamagatchi Park
    ##  .cmp               compression           Lunar SSS
    ##  .mf                multi file            Cotton 2
    ##  .mfc  b'Rev.EXB'   similar to .tar       240 Body
    ##  .mid               nonstandard MIDI      Mortal Kombat 2
    ##  .mat               3D material

    ##  enable color for terminals that support it
    ten  = int( platform.release() .split('.')[0] )
    if os.name == 'posix' or 'ANSICON' in os.environ or ten >= 10:
      if ten >= 10:  ##  enable VT100 Escape Sequence for Win 10
        os.system('')  ##  dunno if this voodoo does anything, try ANSICON instead
      skip   = '\033[31mSkipping\033[0m'
      decode = '\033[32mDecoding\033[0m'
      cyan   = '\033[36m'
      purple = '\033[35m'
      outro  = '\033[0m'
    else:
      skip   = 'Skipping'
      decode = 'Decoding'
      cyan   = ''
      purple = ''
      outro  = ''


    if ID == SEGA2D:
      print( '{}  {} {}  SEGA2D scroll data format {}'.format( skip, tail, cyan, outro ) )


    elif ID == RGB:
      print( '{}  {} {}  SEGA_32BITGRAPH data in RGB color mode {}'.format( decode, tail, cyan, outro ) )
      data .seek(0x18)  ##  header, where size is stored
      w  = hexlify( data .read(0x02) )
      h  = hexlify( data .read(0x02) )  ##  0x02 = 16 bit word

      offset  = 256
      width   = int( w, 16 )
      height  = int( h, 16 )

      args = [ 'convert ',
               '-depth 8 ',
               '-endian MSB '
               '-size {}x{}+{} '.format( width, height, offset ) ]
      call  = '' .join( args )

      inner  = 'RGB:{} '.format( img )
      outer  = '{}.rgb.png'.format( root )
      output  = os.path .join( outputpath, outer )

      os .system( call + inner + output )
      print( '{}\n{}\n{}\n'.format( call, inner, output ) )

      ##  convert -depth 8 -endian MSB -size 144x192+256
      ##  RGB:inpath/input.rgb  outpath/output.rgb.png


    elif ID == SX2D:
      print( '{}  {} {}  Sega Super32X 2D scroll data {}'.format( skip, tail, cyan, outro ) )


    elif ID2 == DGT2PP:
      print( '{}  {} {}  DGT2 PP - Packed Pixel data {}'.format( decode, tail, cyan, outro ) )
      data .seek(0x02)  ##  header, where size is stored
      w  = hexlify( data .read(0x02) )
      h  = hexlify( data .read(0x02) )  ##  0x02 = 16 bit word

      width   = int( w, 16 )
      height  = int( h, 16 )

      CLUT  = bytearray()
      for x in range( 256 ):  ##  256 possible colors in table
        sixteenbit  = int( hexlify( data .read(0x02) ), 16 )

        ##  still 16 bits, we'll just ignore unused top bit  xbbbbbgggggrrrrr
        fifteenbit  = format( color, '0>16b' )

        bb  = int( fifteenbit[1:6 ], 2 )  ##  bbbbb
        gg  = int( fifteenbit[6:11], 2 )  ##  ggggg
        rr  = int( fifteenbit[11: ], 2 )  ##  rrrrr

        ##  expand 5 bits to 8
        BB  = ( bb << 3 ) | ( bb >> 2 )  ##  bbbbbbbb
        GG  = ( gg << 3 ) | ( gg >> 2 )  ##  gggggggg
        RR  = ( rr << 3 ) | ( rr >> 2 )  ##  rrrrrrrr

        CLUT .append( RR )
        CLUT .append( GG )
        CLUT .append( BB )

      barr  = bytearray()
      data2read  = True
      while data2read:
        try:  ##                                  v~~ byte
          eightbit  = int( hexlify( data .read(0x01) ), 16 )

          RR  = CLUT[ eightbit *3 ]
          GG  = CLUT[ eightbit *3 +1 ]
          BB  = CLUT[ eightbit *3 +2 ]
          AA  = 255     ##  full alpha, no transparency

          barr .append( AA )  ##  Image is mirrored and upside-down.
          barr .append( BB )  ##  data's being stored as ABGR here,
          barr .append( GG )  ##  this will actually read as RGBA in a moment,
          barr .append( RR )  ##  once we reverse the bytearray()

        except:  ##  quit trying once there's nothing left to read
          data2read  = False

      barr .reverse()  ## this fixes the upside-down part
      data  = generate_png( barr, width, height )

      outputname  = '{}.pp.png'.format( tail )
      fullname  = os.path .join( outputpath, outputname )
      with open( fullname, 'wb' ) as output:
        output .write( data )

      ##  it's right-side-up now, but backwards, need to mirror it.
                                 ##  'convert' would generate a new image
      imagemagick  = 'mogrify '  ##  'mogrify' will edit image in place.
      options  = '-flop '        ##  -flop  = horizontal flip

      os .system( imagemagick + options + fullname )


    elif ID2 == DGT2DC:
      print( '{}  {} {}  DGT2 DC - Direct Color data {}'.format( decode, tail, cyan, outro ) )
      data .seek(0x02)  ##  header, where size is stored
      w  = hexlify( data .read(0x02) )
      h  = hexlify( data .read(0x02) )  ##  0x02 = 16 bit word

      width   = int( w, 16 )
      height  = int( h, 16 )

      barr  = bytearray()
      data2read  = True
      while data2read:
        try:  ##                                    v~~ word
          sixteenbit  = int( hexlify( data .read(0x02) ), 16 )

          ##  still 16 bits, we'll just ignore unused top bit  xbbbbbgggggrrrrr
          fifteenbit  = format( sixteenbit, '0>16b' )

          bb  = int( fifteenbit[1:6 ], 2 )  ##  bbbbb
          gg  = int( fifteenbit[6:11], 2 )  ##  ggggg
          rr  = int( fifteenbit[11: ], 2 )  ##  rrrrr

          ##  expand 5 bits to 8
          BB  = ( bb << 3 ) | ( bb >> 2 )  ##  bbbbbbbb
          GG  = ( gg << 3 ) | ( gg >> 2 )  ##  gggggggg
          RR  = ( rr << 3 ) | ( rr >> 2 )  ##  rrrrrrrr
          AA  = 255     ##  full alpha, no transparency

          barr .append( AA )  ##  Image is mirrored and upside-down.
          barr .append( BB )  ##  data's being stored as ABGR here,
          barr .append( GG )  ##  this will actually read as RGBA in a moment,
          barr .append( RR )  ##  once we reverse the bytearray()

        except:  ##  quit trying once there's nothing left to read
          data2read  = False

      barr .reverse()  ## this fixes the upside-down part
      data  = generate_png( barr, width, height )

      outputname  = '{}.dc.png'.format( tail )
      fullname  = os.path .join( outputpath, outputname )
      with open( fullname, 'wb' ) as output:
        output .write( data )

      ##  it's right-side-up now, but backwards, need to mirror it.
                                 ##  'convert' would generate a new image
      imagemagick  = 'mogrify '  ##  'mogrify' will edit image in place.
      options  = '-flop '        ##  -flop  = horizontal flip

      os .system( imagemagick + options + fullname )


    elif ID2 == DGT2RLE:
      print( '{}  {} {}  DGT2 RL - Run Length Encoding {}'.format( decode, tail, cyan, outro ) )
      data .seek(0x02)  ##  header, where size is stored
      w  = hexlify( data .read(0x02) )
      h  = hexlify( data .read(0x02) )  ##  0x02 = 16 bit word

      width   = int( w, 16 )
      height  = int( h, 16 )

      CLUT  = bytearray()
      for x in range( 256 ):  ##  256 possible colors in table
        sixteenbit  = int( hexlify( data .read(0x02) ), 16 )

        ##  still 16 bits, we'll just ignore unused top bit  xbbbbbgggggrrrrr
        fifteenbit  = format( color, '0>16b' )

        bb  = int( fifteenbit[1:6 ], 2 )  ##  bbbbb
        gg  = int( fifteenbit[6:11], 2 )  ##  ggggg
        rr  = int( fifteenbit[11: ], 2 )  ##  rrrrr

        ##  expand 5 bits to 8
        BB  = ( bb << 3 ) | ( bb >> 2 )  ##  bbbbbbbb
        GG  = ( gg << 3 ) | ( gg >> 2 )  ##  gggggggg
        RR  = ( rr << 3 ) | ( rr >> 2 )  ##  rrrrrrrr

        CLUT .append( RR )
        CLUT .append( GG )
        CLUT .append( BB )

      barr  = bytearray()
      data2read  = True
      while data2read:
        try:  ##                                   v~~ byte
          runlength  = int( hexlify( data .read(0x01) ), 16 )
          eightbit  = int( hexlify( data .read(0x01) ), 16 )

          for x in range( runlength ):  ##  repeat amount specified by run length
            RR  = CLUT[ eightbit *3 ]
            GG  = CLUT[ eightbit *3 +1 ]
            BB  = CLUT[ eightbit *3 +2 ]
            AA  = 255     ##  full alpha, no transparency

            barr .append( AA )  ##  Image is mirrored and upside-down.
            barr .append( BB )  ##  data's being stored as ABGR here,
            barr .append( GG )  ##  this will actually read as RGBA in a moment,
            barr .append( RR )  ##  once we reverse the bytearray()

        except:  ##  quit trying once there's nothing left to read
          data2read  = False

      barr .reverse()  ## this fixes the upside-down part
      data  = generate_png( barr, width, height )

      outputname  = '{}.rl.png'.format( tail )
      fullname  = os.path .join( outputpath, outputname )
      with open( fullname, 'wb' ) as output:
        output .write( data )

      ##  it's right-side-up now, but backwards, need to mirror it.
                                 ##  'convert' would generate a new image
      imagemagick  = 'mogrify '  ##  'mogrify' will edit image in place.
      options  = '-flop '        ##  -flop  = horizontal flip

      os .system( imagemagick + options + fullname )


    elif ID == AIFF:
      print( '{}  {} {}  Audio Interchange File Format {}'.format( skip, tail, cyan, outro ) )


    elif ID == FILM:
      print( '{}  {} {}  Cinepak Codec - Audio and/or Video {}'.format( skip, tail, cyan, outro ) )


    elif ID4 == b'RIFF':
      print( '{}  {} {}  AudioVideo Interleave / Resource Interchange FileFormat {}'.format( skip, tail, cyan, outro ) )


    elif tail[:4] == 'cdda': 
      padding = ' ' * (len(tail) +10)
      print( '{}  {} {}  CDDA "Red Book" Audio {}'.format( skip, tail, cyan, outro ) )
      print( '{} {} RAW 16‑bit Signed PCM,  44.1 kHz\n'.format( '\033[35m', padding, outro ) )


    else:  ##  DGT
      data .seek(0x10)
      Identifier2  = data .read(0x10)
      if Identifier2 == DGT:
        print( '{}  {} {}  DGT index color mode {}'.format( decode, tail, cyan, outro ) )

        data .seek(0x02)  ##                      v~~ 16 bit Word
        headerSize  = int( hexlify( data .read(0x02) ), 16 )

        data .seek(0x07)  ##                    v~~ Byte
        dirEntry  = int( hexlify( data .read(0x01) ), 16 )

        ##  File size excluding header...  does that exclude CLUT as well?
        fileSize = int( hexlify( data .read(0x04) ), 16 )
        data .seek(0x100)  ##  Directory       }~~ 32 bit Long
        dirSize  = int( hexlify( data .read(0x04) ), 16 )
        CLUTsize = dirSize -0x20

        ##  horiz and vert display positions not really needed for our purposes,
        horizDispPos = int( hexlify( data .read(0x02) ), 16 )
        vertDispPos  = int( hexlify( data .read(0x02) ), 16 )
        ##  but who knows, might be needed for alignment with other sprites,
        ##  so we could print the info out, later on, if needed.

        width  = int( hexlify( data .read(0x02) ), 16 )
        height = int( hexlify( data .read(0x02) ), 16 )

        ##  file name excluding extension...  filename for what ??
        dirName  = hexlify( data .read(0x10) )
        if dirName .startswith(' '):  pass  ##  if it starts with a space, dir's empty?
        else:                         pass  ##  otherwise, what?

        data .seek(0x120)  ##  CLUT
        colors  = CLUTsize /4
        CLUT  = {}
        for color in range( colors ):
          key  = int( hexlify( data .read(0x02) ), 16 )
          val  = int( hexlify( data .read(0x02) ), 16 )
          CLUT[ key ]  = val

        barr  = bytearray()
        data2read  = True
        while data2read:
          try:  ##                                    v~~ word
            sixteenbit  = int( hexlify( data .read(0x02) ), 16 )

            RR  = CLUT[ sixteenbit ][1:6 ]
            GG  = CLUT[ sixteenbit ][6:11]
            BB  = CLUT[ sixteenbit ][11: ]
            AA  = 255     ##  full alpha, no transparency

            barr .append( AA )  ##  Image is mirrored and upside-down.
            barr .append( BB )  ##  data's being stored as ABGR here,
            barr .append( GG )  ##  this will actually read as RGBA in a moment,
            barr .append( RR )  ##  once we reverse the bytearray()

          except:
            data2read  = False  ##  quit trying once there's nothing left to read

        barr .reverse()  ## this fixes the upside-down part
        data  = generate_png( barr, width, height )

        outputname  = '{}.DGT.png'.format( tail )
        fullname  = os.path .join( outputpath, outputname )
        with open( fullname, 'wb' ) as output:
          output .write( data )

        ##  it's right-side-up now, but backwards, need to mirror it.
                                   ##  'convert' would generate a new image
        imagemagick  = 'mogrify '  ##  'mogrify' will edit image in place.
        options  = '-flop '        ##  -flop  = horizontal flip

        os .system( imagemagick + options + fullname )




      elif ext:
        if ext[-1] .isdigit():
          if ext[:-1] == '.en' or ext[:-1] == '.el':
            print( '{}  {} {}  RAW Signed 8 or 16 bit PCM Audio {}\n'.format( skip, tail, purple, outro ) )


        elif ext == '.seq':
          print( '{}  {} {}  SSF - Saturn Sound Format sequence {}'.format( skip, tail, cyan, outro ) )


        elif ext == '.ton':
          print( '{}  {} {}  Audio Tones for SSF - Saturn Sound Format sequence {}'.format( skip, tail, cyan, outro ) )
          print( '{}         Signed 8 or 16 bit PCM, Mono, likely 22050 Hz {}\n'.format( purple, outro ))


        elif ext == '.snd' or ext == '.pcm':
          print( '{}  {} {}  RAW Signed 8 or 16 bit PCM Audio {}\n'.format( skip, tail, purple, outro ) )


        elif ext == '.fon':
          print( '{}  {} {}  Indexed Font, likely 4BPP 8x16 {}'.format( skip, tail, cyan, outro ) )
          print( '{}          uses separate palette file for colors. {}\n'.format( purple, outro ))
          

        elif ext == '.col' or ext == '.pal':
          print( '{}  {} {}  CLUT / Color LookUp Table / Indexed Palette {}'.format( decode, tail, cyan, outro ) )

          colors  = 0
          data .seek(0x00)
          CLUT  = bytearray()

          data2read  = True
          while data2read:
            try:  ##                                    v~~ word
              sixteenbit  = int( hexlify( data .read(0x02) ), 16 )
              colors += 1

              ##  still 16 bits, we'll just ignore unused top bit  xbbbbbgggggrrrrr
              fifteenbit  = format( sixteenbit, '0>16b' )

              bb  = int( fifteenbit[1:6 ], 2 )  ##  bbbbb
              gg  = int( fifteenbit[6:11], 2 )  ##  ggggg
              rr  = int( fifteenbit[11: ], 2 )  ##  rrrrr

              ##  expand 5 bits to 8
              BB  = ( bb << 3 ) | ( bb >> 2 )  ##  bbbbbbbb
              GG  = ( gg << 3 ) | ( gg >> 2 )  ##  gggggggg
              RR  = ( rr << 3 ) | ( rr >> 2 )  ##  rrrrrrrr
              AA  = 255     ##  full alpha, no transparency

              CLUT .append( RR )
              CLUT .append( GG )
              CLUT .append( BB )
              CLUT .append( AA )
            except:  data2read  = False  ##  quit trying once there's nothing left to read

          print( colors, 'Colors', '\n' )

          if   colors > 32: width  = 16
          elif colors > 16: width  = 8
          elif colors > 8:  width  = 4
          else:             width  = 1

          height = colors //width
          data   = generate_png( CLUT, width, height )

          outputname  = '{}.png'.format( tail )
          fullname  = os.path .join( outputpath, outputname )
          with open( fullname, 'wb' ) as output:
            output .write( data )


        elif ext == '.bin' or ext == '.dat' or ext == '.raw':
          print( '{}  {} {}  Possibly RAW 15-bit BGR555 image. Width >> 320 or 352 {}'.format( decode, tail, cyan, outro ) )
          print( '{}  May contain multiple images with smaller widths, especially if you see juttered pixels. {}'.format( purple, outro ) )
          print( '{}  Sizes tend to be multiples of 8.  Though it could be indexed, audio, or other binary data... {}'.format( purple, outro ))
          print( '{}  Expanding to 24-bit colorspace, so you can attempt opening in GIMP. {}'.format( purple, outro ))

          data .seek(0x03)
          headerSize = int( hexlify( data .read(0x01) ), 16 ) *3
                                                           ##  ^~~  this would be 2,
                                                           ##  but after expanding colorspace, 2 bytes = 3 bytes
          print( '{}  expected Offset: {}  >>  noted in file extension {} \n'.format( cyan, headerSize, outro ))

          data .seek(0x00)
          barr  = bytearray()
          data2read  = True
          while data2read:
            try:  ##                                    v~~ word
              sixteenbit  = int( hexlify( data .read(0x02) ), 16 )

              ##  still 16 bits, we'll just ignore unused top bit  xbbbbbgggggrrrrr
              fifteenbit  = format( sixteenbit, '0>16b' )

              bb  = int( fifteenbit[1:6 ], 2 )  ##  bbbbb
              gg  = int( fifteenbit[6:11], 2 )  ##  ggggg
              rr  = int( fifteenbit[11: ], 2 )  ##  rrrrr

              ##  expand 5 bits to 8
              BB  = ( bb << 3 ) | ( bb >> 2 )  ##  bbbbbbbb
              GG  = ( gg << 3 ) | ( gg >> 2 )  ##  gggggggg
              RR  = ( rr << 3 ) | ( rr >> 2 )  ##  rrrrrrrr

              barr .append( RR )
              barr .append( GG )
              barr .append( BB )

            except:  ##  quit trying once there's nothing left to read
              data2read  = False

          outputname  = '{}.{}.data'.format( tail, headerSize )
          fullname  = os.path .join( outputpath, outputname )
          with open( fullname, 'wb' ) as output:
            output .write( barr )


        elif ext == '.tga':
          print( '{}  {} {}  Truevision TGA image {}'.format( decode, tail, cyan, outro ) )

          call  = 'convert '
          inner  = 'TGA:{} '.format( img )
          outer  = '{}.tga.png'.format( root )
          output  = os.path .join( outputpath, outer )

          print( '{}{}\n            {}\n'.format( call, inner, output ) )
          os .system( call + inner + output )
          ##  convert TGA:inpath/input.tga outpath/output.raw.png


        elif len(ID) > 1:  ##  unknowns, print for observation
          print( '{}  {} {}  header: {} {}'.format( skip, tail, cyan, ID, outro ) )


        else:  ##  don't bother printing a blank 0x00 or 0xFF header
          print( '{}  {}'.format( skip, tail, cyan, outro ) )


      elif tail[:3] == 'bgm':
        padding = ' ' * (len(tail) +10)
        print( '{}  {} {}  RAW Signed 8 or 16 bit PCM Audio {}'.format( skip, tail, cyan, outro ) )
        print( '{} {} Little or No Endian, 22050 or 44100\n'.format( '\033[35m', padding, outro ) )


      elif len(ID) > 1:  ##  unknowns, print for observation
        print( '{}  {} {}  header: {} {}'.format( skip, tail, cyan, ID, outro ) )


      else:  ##  don't bother printing a blank 0x00 or 0xFF header
        print( '{}  {}'.format( skip, tail, cyan, outro ) )


""" main  ============================================="""

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
