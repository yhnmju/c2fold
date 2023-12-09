#!/usr/bin/env python3
import shutil
import os
from mutagen.id3 import ID3

#store='/home/shall/store/'
import mutagen, sys
audio = mutagen.File(sys.argv[1]) #path: path to file
print("audio is", audio)

#file = (str(audio['TRCK']) + '. ' + str(audio['TIT2']) + '.mp3')
#file = str(audio['TRCK']) + '. ' + str(audio['TIT2']) + '.mp3'
print("TRCK is", audio['TRCK'])
file = "Track_" + str(audio['TRCK']) + '.mp3'
dir=(str(audio['TPE1']) + '/' + str(audio['TALB']))
print("dir is", dir)

isExist = os.path.exists(dir)
if(not isExist):
    os.makedirs(dir)

path=(dir + '/' +  file)
print(sys.argv[1], "new file is", path)
os.rename(sys.argv[1], path)

