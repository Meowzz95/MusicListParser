class Song:
    name=""
    singer=""
    length=""
    album=""

    def __init__(self,name=None,singer=None,length=None,album=None):
        self.name=name
        self.singer=singer
        self.length=length
        self.album=album

    def __str__(self):
        return "Title:"+self.name+"\n"+"Singer:"+self.singer+"\nLength:"+self.length+"\nAlbum:"+self.album

    def __repr__(self):
        return self.__str__()
