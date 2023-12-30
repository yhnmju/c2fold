#!/usr/bin/env python3

from mutagen.id3 import ID3, APIC, TCON, TCOP, TIT2, TALB, TPE1, TDRC, TRCK, TYER, TPE2
import sys
from getopt import getopt


def updatemeta(filename, m):
#    print ("opts is", opts, "args is", args)
#    print("mp3file is", mp3file, "and arguments are", args)
    print("filename is", filename, "m is", m)
    id3 = ID3(filename)
    if("Artist" in m.keys()):
         artist = m["Artist"]
         id3['TPE1'] = TPE1(encoding=3, text=artist)
    if("Group" in m.keys()):
         artist = m["Group"]
         id3['TPE2'] = TPE2(encoding=3, text=artist)
    if("Title" in m.keys()):
         title = m['Title']
         id3['TIT2'] = TIT2(encoding=3, text=title)
    if("Album" in m.keys()):
         album = m['Album']
         id3['TALB'] = TALB(encoding=3, text=album)
    if("Position" in m.keys()):
         position = m['Position']
         id3['TRCK'] = TRCK(encoding=3, text=position)
    if("Year" in m.keys()):
         year = m['Year']
         id3['TYER'] = TYER(encoding=3, text=year)
    if("Genre" in m.keys()):
         genre = m['Genre']
         id3['TCON'] = TCON(encoding=3, text=genre)
    id3.save(filename)
#



def processargs(arguments):
    opts, args = getopt(sys.argv[1:], '-e:-a:-g:-t:-c:-y:-p:', ['Genre', 'Artist', 'Group', 'Title', 'Album', 'Year', 'Position'])
#    Artist = ""
#    Title = ""
#    Album = ""
#    Year = ""
#    Position = ""
#    Genre = ""
#    Group = ""
    m = {}
    for opt, arg in opts:
        if(opt in ('-a', '--artist')):
            m['Artist'] = arg
        if(opt in ('-g', '--group')):
            m['Group'] = arg
        if(opt in ('-t', '--title')):
            m['Title'] = arg
        if(opt in ('-c', '--album')):
            m['Album'] = arg
        if(opt in ('-p', '--position')):
            m['Position'] = arg
        if(opt in ('-y', '--year')):
            m['Year'] = arg
        if(opt in ('-e', '--genre')):
            m['Genre'] = arg

 #   print("artist is", Artist, "title is", Title, "album is", Album)
  #  updatemeta(mp3file, Artist, Album, Title)


#    print("args is", opts, "m is", m)
    filename = args
    for f in filename:
        updatemeta(f, m)

if(__name__ == "__main__"):
    try:
        processargs(sys.argv[1:])
#        processargs(sys.argv[1:], sys.argv[2:])
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
