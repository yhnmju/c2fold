class Song:
    def __init__(self, songtitle, album, artist, position, length):
        self.Songtitle = songtitle
        self.Album = album
        self.Artist = artist
        self.Position = position
        self.Length = length
        self.bgimage = ""
#        print("Artist is", self.Artist, "Album is", self.Album, "Position", self.Position)

    def dump(self):
#        print("DUMP mbzMusic object")
        print("Songtitle is", self.Songtitle)
        print("Album is", self.Album)
        print("Artist is", self.Artist)
        print("Position is", self.Position)
        print("Length is", self.Length)

    def getPosition(self):
        return(self.Position)

    def getTitle(self):
        s = self.Songtitle
        return(s)

    def setBgImage(self, file):
        self.bgimage = file

    def getBgImage(self):
        return (self.bgimage)

    def Album(self):
        a = self.Album
        return(a)

class Album:
    def __init__(self, title, artist, genre, year):
        self.Albumtitle = title
        self.Artist = artist
        self.Genre = genre
        self.Year = year
