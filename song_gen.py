from bs4 import BeautifulSoup
import requests
import random
import re

# GENERATES RANDOM SONG OBJECT with print methods
# PS: DO NOT SEND TOO MANY REQUESTS
# MEANT TO GENERATE 1 RANDOM SONG AT A TIME
# PPS: generator is not 100%, sometimes errors in generating song
# still working on fixing bugs


class Song:
    def __init__(self, title, artist, album, lyrics):
        self.title = title
        self.artist = artist
        self.album = album
        self.lyrics = lyrics

    def ptitle(self):
        print(self.title)

    def partist(self):
        print(self.artist)

    def palbum(self):
        print(self.album)

    def plyrics(self):
        print(self.lyrics)


def letterlinks():
    # Creates list of links to alphabet pages of azlyrics
    source = requests.get('https://www.azlyrics.com/')
    soup = BeautifulSoup(source.text, 'lxml')

    article = soup.find(class_="btn-group text-center")  # find div
    a = article.find_all('a')  # find all links in div
    for link in a:  # for each link, add it to list
        links.append('http:' + link['href'])
    del links[-1]  # removes the unwanted last link


def artistlinks(links, x):
    # choses a random links from alphabet pages then creates a list of artist links
    for i in range(int(x)):
        source = requests.get(random.choice(links))
        soup = BeautifulSoup(source.text, 'lxml')
        article = soup.find(class_="col-sm-6 text-center artist-col")
        a = article.find_all('a')
    for link in a:
        nextlinks.append('https://www.azlyrics.com/' + link['href'])


def songlinks(nextlinks, x):
    # choses random links from artists then creates a list of song links
    for i in range(int(x)):
        source = requests.get(random.choice(nextlinks))
        soup = BeautifulSoup(source.text, 'lxml')
        # lyrics/yelawolf/allaboard.html -- format to match
        pattern = re.compile(r'lyrics/.+\.html')
        matches = pattern.finditer(soup.text)
        for i in matches:
            nextnext.append('https://www.azlyrics.com/' + i.group(0))


def songg(nextnext, x):
    # choses random links from songs, defines song title, artist and lyrics(song)
    for i in range(int(x)):
        try:
            source = requests.get(random.choice(nextnext))
            soup = BeautifulSoup(source.text, 'lxml')
        except IndexError:
            print('IndexError Occured.  Couldn\'t create song links')

        pattern = re.compile(r'\n+".+"\slyrics')  # start of song
        matches = pattern.finditer(soup.text)
        m3 = soup.text.find('if  ( /Android|w')  # end of song

        title = ''
        for i in matches:
            for a in i.group(0):
                if a != '\n':
                    title += a  # start of song is title, eliminating new lines and saving it into title
            thesong = soup.text[i.end()+2:m3-7]  # slice the html at start and end of song
        title = title[1:-8]  # full title

        m4 = thesong.find('Lyrics')
        artist = thesong[:m4-1]  # full artist
        m5 = thesong.find(title)
        eoti = m5 + len(title) + 1  # end of title index to find start of true start of song
        thesong = thesong[eoti:]
        # matches patern before song starts, works with or without an extra featuring line under title
        p3 = re.compile(r'\n{3}')
        w1 = p3.finditer(thesong)
        for i in w1:
            songstart = i.end()
        thesong = thesong[songstart+2:]  # full lyrics

        aname = soup.text.find('ArtistName')
        sname = soup.text.find('SongName')
        fend = soup.text.find('function')

        pat = re.compile(r'album:.+\n')  # match for album
        mat = pat.finditer(soup.text)
        ooo = ''
        for i in mat:
            ooo = i.group(0)

        album = ooo[:-1]
        try:
            album_start_index = album.index(':')
            album = album[album_start_index+2:]
        except ValueError:
            pass
        a = ''  # empty album string
        for i in album:
            if i != '\"':
                a += i
        album = a

        artistname = soup.text[aname:sname-3]
        songname = soup.text[sname:fend-3]

        result = Song(title, artist, album, thesong)
        return result


links = []
nextlinks = []
nextnext = []


def song_generator():
    """
        generates random song object from azlyrics.com
    """
    letterlinks()
    artistlinks(links, 1)
    songlinks(nextlinks, 1)
    result = songg(nextnext, 1)
    return result
