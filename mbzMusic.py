class Song:
    def __init__(self, songtitle, album, artist, position, length):
        self.Songtitle = songtitle
        self.Album = album
        self.Artist = artist
        self.Position = position
        self.Length = length

    def getPosition(self):
        return(self.Position)

    def getTitle(self):
        return(self.Songtitle)

    def setBgImage(self, file):
        self.bgimage = file

class Album:
    def __init__(self, title, artist, genre, year):
        self.Albumtitle = title
        self.Artist = artist
        self.Genre = genre
        self.Year = year
