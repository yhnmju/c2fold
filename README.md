# c2f - Cloud To File

## About

I wrote this utility because I had lost my collection of music on my computer when I had two hard disk drive loses in short succession.
Unfortunately my collection of cd's were out of the house in storage (moving house). I didn't want to collect and unbox these
as I would soon have to send them offsite again.
So instead I wrote c2f so that I could download these as a replacement from cloud, convert from mp4 to mp3 and add id3 tags.

c2f is a utility to download videos and convert them to mp3 or ogg files.
It identfiies the song and album, using a combination songrec (Shazam client) and Musicbrainz (additional information), and updates the audio file with metadata (id3).
It then uses the metadata to update the name of the audio file.

## TODO
Loads.
* Documentation on how to configure and run this
* There is no error handling
* A song can belong to multiple different albums.
    - Should be able to add additional criteria for the search
      so that it is selecting the right album, rather than just
      the first item from the list.
* If a song belongs to multiple albums, it would be nice to be
  able to do that search from this tool before updating any files
  and finding out afterwards.
* Support for ogg files
* More to come


## How do I use this?
1. Download and installl songrec (open source Shazam client)

2. Create HOME/.config/c2f.cfg and place "songrec=pathto_songrec_here"
   example;
       $ cat /home/example/.config/c2f/c2f.cfg
       songrec=/home/example/.cargo/bin/songrec

3. Create a file an album you would like to download music for;
       $ cat example
       Artist;Smashing Pumpkins
       Album;Siamese Dream
       Genre;grunge
       3;https://www.youtube.com/watch?v=dxaK0xH9QUE

4. Download music into mp3 file;
       $ download.py

5. Update id3 metadata in mp3 file
      $ updatemeta_rewrite.py example

6. Lastily, rename file based on metadata contained in mp3 file and move location
     $ renamefile.py
   
