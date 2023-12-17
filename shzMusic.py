class Song:
    def __init__(self, songtitle, album, artist, genre, file):
        self.Songtitle = songtitle
        self.Album = album
        self.Artist = artist
        self.File = file
        self.Genre = genre

    def Title(self):
        return(self.Songtitle)

    def Album(self):
    #    return(self.Album)
        album = self.Album
        return(album)

    def Artist(self):
        artist = self.Artist
        return(artist)

    def setBgImage(self, file):
        self.bgimage = file

    def setPosition(self, pos):
        self.position = pos

    def GetFile(self):
        return(self.File)

    def Genre(self):
       return(self.Genre)

    def Position(self):
       return(self.position)

    def file(self):
        return(self.File)

class Album:
    def __init__(self, title, artist, genre, year):
        self.Albumtitle = title
        self.Artist = artist
        self.Genre = genre
        self.Year = year

    def Year(self):
        return(self.Year)
