#!/bin/python

import os, sys, mutagen, re, acoustid, musicbrainzngs, json
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK
import acoustid, getopt, re, subprocess

def download(config):
     for t in config['tracks']:
         print("downloading", t)
         x = ['/usr/bin/youtube-dl', '-x', '--audio-format=mp3', config['tracks'][t], '-o' "./%(title)s.%(ext)s"]
         aa=subprocess.run(x, capture_output=True)


def readConfig(file):
    configfile = sys.argv[1]
    data = dict()
    data['tracks'] = dict()
    with open(configfile) as fd:
        for line in fd:
            line.rstrip("\r")
            c = line.split(';')
            if (c[0].isnumeric()):
                data['tracks'][c[0]] = c[1].rstrip("\n")
    return data


if __name__ == '__main__':
    # Firstly read through the config file that contains the files
    # we want to download
    config = readConfig(sys.argv[1])

    # Download the files
    download(config)

