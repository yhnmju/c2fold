# c2f - Cloud To File

## About

c2f is a utility to download videos and convert them to mp3 or ogg files.
It identfiies the song and album, using a combination songrec (Shazam client) and Musicbrainz, and updates the audio file with metadata (id3).
It then uses the metadata to update the name of the audio file.

## TODO
Loads.
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
