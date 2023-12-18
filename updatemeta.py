#!/usr/bin/env python3

import json, subprocess, glob, musicbrainzngs
import subprocess, argparse, os, glob, sys, json, getopt, requests
import mbzMusic, shzMusic
from mutagen.id3 import ID3, APIC, TCON, TCOP, TIT2, TALB, TPE1, TDRC, TRCK, TYER
from mutagen.mp3 import MP3
from pathlib import Path
DEBUG=0

musicbrainzngs.set_useragent(
    "c2f",
    "1.1",
    "https://github.com/yhnmju/c2f/",
)

# Config dictionary is used to
config = {}
mbSong = {}
szSong = {}
szAlbum = {}
exe = {}

def readConfig(file):
    with open(file) as fd:
        for line in fd:
            line = line.strip("\n")
            line = line.strip("\r")
#            aaa = line.rstrip("\r\n")
            c = line.split(';')
            if (c[0] == 'Album'):
                config['Album'] = c[1]
            elif (c[0] == 'Artist'):
                config['Artist'] = c[1]
            elif(c[0] == 'Genre'):
                config['Genre'] = c[1]

def UtilConfig(configFile):
#    p = {}
    try:
        with open(configFile) as fd:
            for l in fd:
                l = l.rstrip("\r\n")
                s = l.split("=")
                exe[s[0]] = s[1]
    except:
        print("Failed reading file", configFile)

def EncodeMetadata():
    for s in szSong:
        file = szSong[s].GetFile()
        title = szSong[s].Title()
        album = szSong[s].Album
        AlbumIndex = s2i(album)
        artist = szSong[s].Artist
        position = szSong[s].Position()
        filebg = mbSong[s].getBgImage()
        year  = szAlbum[AlbumIndex].Year
        genre = szAlbum[AlbumIndex].Genre

        print("debug3: album="+album, "Artist="+artist, "title="+title, "genre="+genre, "year="+year, "song position="+position)

        r = requests.get(filebg)
        bgfile = open("cover.jpg", "wb")
        bgfile.write(r.content)
        bgfile.close()


        id3 = ID3(file)
        id3['TALB'] = TALB(encoding=3, text=album)
        id3['TIT2'] = TIT2(encoding=3, text=title)
        id3['TPE1'] = TPE1(encoding=3, text=artist)
        id3['TCON'] = TCON(encoding=3, text=genre)
        id3['TYER'] = TYER(encoding=3, text=year)
        id3['TRCK'] = TRCK(encoding=3, text=position)


        with open('cover.jpg', 'rb') as albumart:
       #     print(albumart.read())
            id3['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=albumart.read()
            )
        id3.save(file)


def s2i(stringname):
    # String2Index
    # One problem that I had was trying to tie metabrain and shazam database entries together.
    # It wasn't uncommon for there to be differences in album and song titles with
    # difference in capitilisation, spacing or different punctuation.
    # Easiest way around this was to use a dictionary key with lower case
    # and punctuation removed.

    stringname = stringname.lower()
    stringname = stringname.replace('’', '')
    stringname = stringname.replace("'", '')
    stringname = stringname.replace(" ", '')
    return(stringname)

def processFiles():
    mbResults = getTracklist(config['Artist'], config['Album'])
    configFile = (str(Path.home()) + '/.config/c2f/c2f.cfg')
    UtilConfig(configFile)
    if("songrec" in exe ):
        songrecexe = exe['songrec']
    else:
        songrecexe = "songrec"

    # For each song in the album as determined by musicbrainz, create a Song object
    # This is so we have a list of songs (and their attributes) that should be on an album
    for a in mbResults:
#        print("Looping over mbResults. a is", a)
        mb = mbzMusic.Song(a['recording']['title'], config['Album'], config['Artist'], a['position'], a['recording']['length'])
        s = mb.getTitle()
        s = s2i(s)
        mbSong[s] = mb

    # Loop over all mp3 files in CWD, and then use Shazam (songrec) to check the
    # attributes of the song
    position = 0
#    print("Going to start looping")
    for f in glob.iglob('*.mp3'):
#        print("Looping over all mp3 files -", f)
        exec = [ songrecexe, 'audio-file-to-recognized-song', f ]
        p = subprocess.check_output(exec, shell=False)
        shazamDS   = json.loads(p)
        genre      = shazamDS['track']['genres']['primary']
        bgimage    = shazamDS['track']['images']['coverarthq']
        artist     = shazamDS['track']['subtitle']
        songtitle  = shazamDS['track']['title']
#        print("Songtitle is", songtitle)
        if(len(shazamDS['track']['sections'][0]['metadata']) > 0):
            album      = shazamDS['track']['sections'][0]['metadata'][0]['text']
            year       = shazamDS['track']['sections'][0]['metadata'][2]['text']
            albumIndex = s2i(album)
            if (albumIndex not in szAlbum):
                szAlbum[albumIndex] = shzMusic.Album(album, artist, genre, year)

            songtitleindex = s2i(songtitle)
            if(songtitleindex in mbSong.keys()):
                position = mbSong[songtitleindex].getPosition()
                mbSong[songtitleindex].setBgImage(bgimage)
                szSong[songtitleindex] = shzMusic.Song(songtitle, album, artist, genre, f)
                szSong[songtitleindex].setPosition(position)
            else:
                print("error: I didn't find", songtitleindex, "in", mbSong.keys())



#    return(szSong)

def getTracklist(artist, album):
    result = musicbrainzngs.search_releases(artist=artist, release=album, format='CD')
    id = result["release-list"][0]["id"]
    new_result = musicbrainzngs.get_release_by_id(id, includes=["recordings"])
    if (DEBUG == 1):
        print("debug getTracklist:", result)
        print("debug getTracklist id:", id)
        print("debug get_release_by_id:", new_result)

    return(new_result["release"]["medium-list"][0]["track-list"])


if(__name__ == "__main__"):
    try:
        readConfig(sys.argv[1])
        processFiles()
#        print("s is", s)
        EncodeMetadata()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
