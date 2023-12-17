# c2f - Cloud To File

## About
I wrote this utility because I had lost my collection of music on my computer when I had two disk drive loses in short succession.

Unfortunately, my collection of cd's were out of the house in storage (moving house). I didn't want to collect and unbox these as I would soon have to send them offsite again.
So instead I wrote c2f so that I could download these as a replacement from cloud, convert from mp4 to mp3, and add id3 tags.

c2f is a utility to download videos and convert them to mp3 or ogg files.
It identfiies the song, album and position on the album, using a combination of songrec (Shazam client) and Musicbrainz (additional information) and updates the audio file with metadata (id3).
It then uses the metadata within the mp3 file to update the name of the audio file.

# What's new?
* I fixed code where it wasn't correctly identifying some track numbers
* Code now identifies and downloads album art and embeds in id3 metadata

## TODO
Loads.
* Documentation on how to configure and run this
* There is no error handling
* Support for ogg files
* More to come


## How do I use this?
1. Download and install songrec (open source Shazam client), which in turn depends on having the Rust programming language installed.

2. Install c2f with pip. 
   $ python -m pip install c2f

3. Create HOME/.config/c2f.cfg and place "songrec=pathto_songrec_here"
   example;

       $ cat /home/example/.config/c2f/c2f.cfg
       songrec=/home/example/.cargo/bin/songrec

4. Create a file for an album you would like to download music for;

       $ cat example
       Artist;Smashing Pumpkins
       Album;Siamese Dream
       Genre;grunge
       3;https://www.youtube.com/watch?v=dxaK0xH9QUE


5. Download music into mp3 file;

       $ download.py example
       downloading 1
       downloading 2
       downloading 3

6. Update id3 metadata in mp3 file;

       $ updatemeta.py example

7. Lastily, rename file based on metadata contained in mp3 file and move location;

       $ renamefile.py MySong.mp3
       
       $ ls -R The\ Smashing\ Pumpkins/
       'The Smashing Pumpkins/':
       'Siamese Dream'

       'The Smashing Pumpkins/Siamese Dream':
       Track_10.mp3  Track_13.mp3  Track_2.mp3  Track_4.mp3  Track_6.mp3  Track_8.mp3
       Track_12.mp3  Track_1.mp3   Track_3.mp3  Track_5.mp3  Track_7.mp3  Track_9.mp3
   
