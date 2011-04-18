#!/usr/bin/env python

import os
import glob
import eyeD3
import math
from output import *

#path = os.getcwd()


#def boldText(s):
    #return "\033[1m" + s + "\033[0;0m"

def isOdd(number):
    if number%2==0:
        return False
    else:
        return True

def getW(s):
    width = len(s)
    while width < 35:
        width +=1
    return width

def isEmpty(s):
    if s == '' or s is None or s == "None":
        return True
    else:
        return False

def getFolders(files):
    folders = []
    for f in files:
        f = os.path.dirname(f)
        if f not in folders:
            folders.append(f)
    return folders

def getTagStr(s, short = False):

    s = str(s)
    if isEmpty(s) and short == False:
        return "XXXXXXXXXXXX"
    elif isEmpty(s):
        return "XXX"
    else:
        return s
def setEmptyStr(s):
    if str(s) == '' or s is None:
        return "[Empty Tag]"
    else:
        return s


##############The Work
def printGenresName():
    genres = [];
    displayed = []
    i = 0
    # Filter out 'Unknown'
    for g in eyeD3.genres:
        if g != "Unknown":
            genres.append([g, i]);
        i +=1
    genres.sort()

    cols = 3;
    offset = int(math.ceil(float(len(genres)) / cols));

    for i in range(offset):
        c1, c2, c3 = '', '', ''
        if i < len(genres):
          if i not in displayed:
              c1 = "%3s: %s" % (str(genres[i][1]).zfill(2), genres[i][0]);
              displayed.append(i)
        else:
          c1 = "";
        if (i * 2) < len(genres):
           try:
              if (i + offset) not in displayed:
                  c2 = "%3s: %s" % (str(genres[i + offset][1]).zfill(2), genres[i + offset][0]);
                  displayed.append(i + offset)
           except IndexError:
               pass
        if (i * 3) < len(genres):
           try:
              if (i + (offset*2)) not in displayed:
                  c3 = "%3s: %s" % (str(genres[i + (offset*2)][1]).zfill(2), genres[i + (offset *2)][0]);
                  displayed.append(i + (offset*2))
           except IndexError:
               pass
        else:
          c2 = "";
        print c1 + (" " * (40 - len(c1))) + c2 + (" " * (40 - len(c2))) + c3
    print ""

def printGenresNum():
    genres = [];
    displayed = []
    # Filter out 'Unknown'
    for g in eyeD3.genres:
        if g != "Unknown":
            genres.append(g);
    cols = 3;
    offset = int(math.ceil(float(len(genres)) / cols));

    for i in range(offset):
        c1, c2, c3 = '', '', ''
        if i < len(genres):
          if i not in displayed:
              c1 = "%3s: %s" % (str(i).zfill(2), genres[i]);
              displayed.append(i)
        else:
          c1 = "";
        if (i * 2) < len(genres):
           try:
              if (i + offset) not in displayed:
                  c2 = "%3s: %s" % (str(i + offset).zfill(2), genres[i + offset]);
                  displayed.append(i + offset)
           except IndexError:
               pass
        if (i * 3) < len(genres):
           try:
              if (i + (offset*2)) not in displayed:
                  c3 = "%3s: %s" % (str(i + (offset*2)).zfill(2), genres[i + (offset *2)]);
                  displayed.append(i + (offset*2))
           except IndexError:
               pass
        else:
          c2 = "";
        print c1 + (" " * (40 - len(c1))) + c2 + (" " * (40 - len(c2))) + c3
    print ""

def getOccur(folder, long=False):
    artists = []
    albums = []
    genres = []
    years = []
    tag = eyeD3.Tag()

    for f in glob.glob1(folder, '*.mp3'):
        tag.link(os.path.join(folder, f))
        genreStr = "None"

        try:
            genre = tag.getGenre();
        except eyeD3.GenreException, ex:
            printError(ex);
        if genre:
            genreStr = genre.getName()+ " (" +str(genre.getId()) + ")"

        if long is False:
            if artists.count(setEmptyStr(tag.getArtist())) == 0:
                artists.append(setEmptyStr(tag.getArtist()))
            if albums.count(setEmptyStr(tag.getAlbum())) == 0:
                albums.append(setEmptyStr(tag.getAlbum()))
            if genres.count(setEmptyStr(genreStr)) == 0:
                genres.append(genreStr)
            if years.count(setEmptyStr(tag.getYear())) == 0:
                years.append(setEmptyStr(tag.getYear()))
        else:
            artists.append(setEmptyStr(tag.getArtist()))
            albums.append(setEmptyStr(tag.getAlbum()))
            genres.append(setEmptyStr(genreStr))
            years.append(setEmptyStr(tag.getYear()))

    return[artists, albums, genres, years]

def getMissing(folder):
    missing = []
    tag = eyeD3.Tag()

    for f in glob.glob1(folder, '*.mp3'):
        tag.link(os.path.join(folder, f))
        #f = os.path.basename(f)
        str = "$##$"
        genreStr = ""

        try:
            genre = tag.getGenre();
        except eyeD3.GenreException, ex:
            printError(ex);
        if genre:
            genreStr = genre.getName()

        if isEmpty(tag.getArtist()):
            str += "Artist" + "$##$"
        if isEmpty(tag.getAlbum()):
            str += "Album" + "$##$"
        if isEmpty(tag.getTitle()) or "track" in tag.getTitle().lower():
            str += "Title" + "$##$"
        if isEmpty(tag.getTrackNum()[0]):
            str += "Track No" + "$##$"
        if isEmpty(genreStr):
            str += "Genre" + "$##$"
        if isEmpty(tag.getYear()):
            str += "Year" + "$##$"

        if str != "$##$":
            str = f + str.rstrip("$##$")
            missing.append(str)
    return missing

def getDbls(files):
    tag = eyeD3.Tag()
    tracks = []
    summary = []
    for f in files:
        tag.link(f)
        f = os.path.basename(f)
        tracks.append(tag.getTrackNum()[0])

    for t in tracks:
        if tracks.count(t) > 1:
            if summary.count("Double of Track " + str(t).zfill(2)) == 0:
                summary.append("Double of Track " + str(t).zfill(2))

    return summary

def listTags(files):
    files.sort()
    for f in files:
        tag = eyeD3.Tag()
        tag.link(f)
        f = os.path.basename(f)
        infos = []
        genreStr = "None"

        try:
            genre = tag.getGenre();
        except eyeD3.GenreException, ex:
            printError(ex);
        if genre:

            genreStr = genre.getName()

        astr = "%s: %s" % (bold("album"), getTagStr(tag.getAlbum()))
        bstr = "%s: %s" % (bold("year"), getTagStr(tag.getYear()))
        infos.append(astr)
        infos.append(bstr)

        astr = "%s: %s" % (bold("track"), getTagStr(str((tag.getTrackNum()[0])).zfill(2), True))
        bstr = "%s: %s" % (bold("genre"), getTagStr(genreStr, True))
        infos.append(astr)
        infos.append(bstr)
        width = max(len(w) for w in infos) + 15

        print " "
        print yellow(( " "+"-" * (getW(f)+ 2)))
        print yellow(("|").ljust(1)), blue(f.center(getW(f))), yellow(("|").rjust(1))
        print yellow(( " "+"-" * (getW(f)+ 2)))

        print "%s: %s %s" % ( bold("title"),
                                getTagStr(tag.getTitle()),
                                bold(""))
        print "%s: %s %s" % ( bold("artist"),
                                getTagStr(tag.getArtist()),
                                bold(""))
        cnt = 0
        for i in range(0,2):
            print infos[cnt].ljust(width), infos[cnt+1].ljust(10)
            cnt += 2
    print yellow(("-" * 79))
    print " "

def getFolderStr(folder, base):
    folder = os.path.relpath(folder, start=base)
    return "../" +folder
    #print folder

def getMaxWidths(folders):
    awidth=[]
    Awidth=[]
    gwidth=[]
    ywidth=[]

    for f in folders:
        occurs = getOccur(f,True)

        #print f
        #print occurs
        if max(len(a) for a in occurs[0]) not in awidth:
            awidth.append(max(len(a) for a in occurs[0]))
        if max(len(A) for A in occurs[1]) not in Awidth:
            Awidth.append(max(len(A) for A in occurs[1]))
        if max(len(g) for g in occurs[2]) not in gwidth:
            gwidth.append(max(len(g) for g in occurs[2]))
        if max(len(y) for y in occurs[3]) not in ywidth:
            ywidth.append(max(len(y) for y in occurs[3]))

    return max(awidth), max(Awidth), max(gwidth), max(ywidth)

def ocurranceRslts(files):
    folders = getFolders(files)

    h = "Ocurrances of Tags in Folder(s)"
    print ""
    #print ( " "+"-" * (getW(h)+ 2))
    print bold(purple(h))
    print ( "-" * (60))
    #print ""

    base, tail = os.path.split(min(folder for folder in folders))
    folders.sort(key = len)
    #print folders
   # print occurs
    #sys.exit()
    widths = getMaxWidths(folders)

    for folder in folders:
        inst = getOccur(folder)
        occurs = getOccur(folder,True)

        #print occurs

        p = (" " * 3)
        p1 = bold(yellow(""))
        p2 = yellow(" | ")

        awidth = widths[0] + 6 + len(p) + len(p1)
        Awidth = widths[1] + 6 + len(p) + len(p1)
        gwidth = widths[2] + 6 + len(p) + len(p1)
        ywidth = widths[3] + 6 + len(p) + len(p1)

        total = max(len(inst[0]),
                    len(inst[1]),
                    len(inst[2]),
                    len(inst[3]))


        astr = bold(yellow("Artists:"))
        alstr = bold(yellow("Albums:"))
        gstr = bold(yellow("Genres:"))
        ystr = bold(yellow("Years:"))

        print bold(blue(getFolderStr(folder, base)+ " $ " )+ str(len(glob.glob1(folder, '*.mp3'))) + " file(s) ")
        print p + astr.ljust(awidth) + p + p2, alstr.ljust(Awidth) + p + p2, gstr.ljust(gwidth) + p + p2, ystr.ljust(ywidth) + p

        for i in range(0, total):
            if len(inst[0]) <= i:
                arcol = "" + p1
            else:
                arcol = "(" + str(occurs[0].count(inst[0][i])) + ") x " + inst[0][i] + p1
            if len(inst[1]) <= i:
                alcol = "" + p1
            else:
                alcol = "(" + str(occurs[1].count(inst[1][i])) + ") x " + inst[1][i] + p1
            if len(inst[2]) <= i:
                gcol = "" + p1
            else:
                gcol = "(" + str(occurs[2].count(inst[2][i])) + ") x " + inst[2][i] + p1
            if len(inst[3]) <= i:
                ycol = "" + p1
            else:
                ycol = "(" + str(occurs[3].count(inst[3][i])) + ") x " + inst[3][i] + p1
            print p + p + arcol.ljust(awidth) + p2, p + alcol.ljust(Awidth) +p2, p + gcol.ljust(gwidth) + p2, p + ycol.ljust(ywidth)
            print " "

def missingRslts(files):
    folders = getFolders(files)

    base, tail = os.path.split(min(folder for folder in folders))
    folders.sort(key = len)

    print ""
    print bold(purple("Files with Missing Information"))
    print ("-" * 60)
    for folder in folders:
        missing = getMissing(folder)
        filenames = []
        for m in missing:
            filenames.append(os.path.basename(m.split("$##$")[0]))

        print bold(blue(getFolderStr(folder, base)+ " $ " ))

        if filenames:
            width = max(len(f) for f in filenames)

            for m in missing:
                str =''
                file = m.split("$##$")
                for i in range(1, len(file)):   # start at 1 to skip file name
                    str += ", " + file[i]
                str = str.lstrip(", ")

                print ("  " + os.path.basename(file[0])).rjust(width + 2) + "","..." +bold(red(str))
            print ("-" * (width +25))
        else:
            print "\tNo Missing Tags!"
            print ""

