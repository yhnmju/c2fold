#!/usr/bin/env python3

import json, subprocess, glob, musicbrainzngs
import subprocess, argparse, os, glob, sys, json, getopt, requests
import mbzMusic, shzMusic, eyed3
from mutagen.id3 import ID3, TCON, TCOP, TIT2, TALB, TPE1, TDRC, TRCK, TYER
from pathlib import Path

musicbrainzngs.set_useragent(
    "c2f",
    "0.1",
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
            line.strip("\n")
            line.strip("\r")
            aaa = line.rstrip("\r\n")
            c = aaa.split(';')
            if (c[0] == 'Album'):
                config['Album'] = c[1]
            elif (c[0] == 'Artist'):
                config['Artist'] = c[1]
            elif(c[0] == 'Genre'):
                config['Genre'] = c[1]

def UtilConfig(configFile):
    p = {}
#    print("Opening", configFile)
    try:
        with open(configFile) as fd:
            for l in fd:
                l = l.rstrip("\r\n")
                s = l.split("=")
                exe[s[0]] = s[1]
    except:
        print("Failed reading file", configFile)

def EncodeMetadata(song):
  #  file = open("temp.jpg", "wb")
  #  file.write(r.content)
  #  file.close
#    print("EncodeMetadata song is", song.Title(), "and file is", song.GetFile())
    filename = song.GetFile()
    id3 = ID3(filename)
    title       = song.Title()
    album       = song.Album
    artist      = song.Artist
    position    = song.Position()
#    print("debug: position is", position)
    year        = szAlbum[album].Year
    id3['TALB'] = TALB(encoding=3, text=album)
    id3['TIT2'] = TIT2(encoding=3, text=title)
    id3['TPE1'] = TPE1(encoding=3, text=song.Artist)
    id3['TCON'] = TCON(encoding=3, text=song.Genre)
    id3['TYER'] = TYER(encoding=3, text=year)
    id3['TRCK'] = TRCK(encoding=3, text=position)
    id3.save(song.file())

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
        mb = mbzMusic.Song(a['recording']['title'], config['Album'], config['Artist'], a['position'], a['recording']['length'])
        mbSong[mb.getTitle()] = mb

    # Loop over all mp3 files in CWD, and then use Shazam (songrec) to check the
    # attributes of the song
    for f in glob.iglob('*.mp3'):
        exec = [ songrecexe, 'audio-file-to-recognized-song', f ]
        p = subprocess.check_output(exec, shell=False)
        shazamDS   = json.loads(p)
        genre      = shazamDS['track']['genres']['primary']
        bgimage    = shazamDS['track']['images']['coverarthq']
        artist     = shazamDS['track']['subtitle']
        songtitle  = shazamDS['track']['title']
#        print("debug: songtitle found is", songtitle)
#        print("debug: when looking for searches", shazamDS['track']['sections'][0])
        if(len(shazamDS['track']['sections'][0]['metadata']) > 0):
            album      = shazamDS['track']['sections'][0]['metadata'][0]['text']
            year       = shazamDS['track']['sections'][0]['metadata'][2]['text']
#            print("debug: album is", album, "and year is", year)
            if (album not in szAlbum):
                szAlbum[album] = shzMusic.Album(album, artist, genre, year)

            szSong[songtitle] = shzMusic.Song(songtitle, album, artist, genre, f)
        for song in mbSong:
            if(song in szSong.keys()):
               # szSong[song].setPosition(mbSong[song].getPosition())
                if(artist in config['Artist']):
                    if(album in config['Album']):
                        print(f, "album is", album, "and", sys.argv[1], "is", config['Album'])
                        szSong[song].setPosition(mbSong[song].getPosition())
                        EncodeMetadata(szSong[song])

def getTracklist(artist, album):
    result = musicbrainzngs.search_releases(artist=artist, release=album)
    id = result["release-list"][0]["id"]
    new_result = musicbrainzngs.get_release_by_id(id, includes=["recordings"])
    return(new_result["release"]["medium-list"][0]["track-list"])


if(__name__ == "__main__"):
    try:
        readConfig(sys.argv[1])
        processFiles()
   #     EncodeMetadata()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
