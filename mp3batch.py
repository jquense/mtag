import os.path
import os
import glob
import eyeD3
import shutil
from path import path
from output import *
import settings

musicbase = settings.musicbase

def getValidDest():
	l=[]
	for f in glob.glob1(musicbase, '*'):
		if os.path.isdir( os.path.join(musicbase, f)):
			l.append(f)
	return l

#def checkDest(dest):
#    for f in glob.glob1(musicbase, '*'):
#        if os.path.isdir(os.path.join(musicbase,f)):
#            if dest == f:
#                return True
#    return False

def hasMp3(dir):
    count = 0
    for f in glob.glob1(dir, '*.mp3'):
        count+=1

    if count ==0:
        return False
    return True


def getRenameStr(mp3):

    if os.path.splitext(mp3)[1] == ".mp3":
        tag = eyeD3.Tag()
        tag.link(mp3)
        rename =''
        if tag.getDiscNum()[0] != "None":
            rename = str(tag.getDiscNum()[0])
        if tag.getTrackNum()[0] != "None" or tag.getTrackNum()[0] is not None:
            rename = str(tag.getTrackNum()[0]).zfill(2)

        rename = rename + " " + tag.getArtist()
        rename = rename + " - " + tag.getAlbum()
        rename = rename + ": " + tag.getTitle()
        return rename

def setFileName(files):
    print ''
    print bold(purple('Renaming Files:'))
    print '------------------------------------'
    retval = 0

    for f in files:
        folder = os.path.dirname(f)
        fname = getRenameStr(f)

        title, ext = os.path.splitext(os.path.basename(f))
        try:
            if fname != title:
                os.rename(f, os.path.join(folder, fname + ext))
                print os.path.basename(f) + '   -->    ' + fname + ext
                retval += 1
        except:
            print warn("Error Renaming: ", f)

    return retval


def setTags(files, artist ='', album ='', genre ='', year = ''):
    retval = 0
    for f in files:
        tag = eyeD3.Tag()
        tag.link(f)
        f = os.path.basename(f)
        changed = []
        if artist:
            if tag.getArtist() != artist:
                tag.setArtist(artist)
                tag.update()
                changed.append("Artist")
        if album:
            if tag.getAlbum() != album:
                tag.setAlbum(album)
                tag.update()
                changed.append("Album")
        if genre:
            if genre.isdigit():
                if tag.getGenre().getId() != int(genre):
                    tag.setGenre(genre)
                    tag.update()
                    changed.append("Genre")
            else:
                if tag.getGenre().getName().lower() != genre.lower():
                    tag.setGenre(genre)
                    tag.update()
                    changed.append("Genre")
        if year:
            if tag.getDate() != year:
                tag.setDate(year)
                tag.update()
                changed.append("Year")
        if changed:
            retval =+ 1
            results(f, changed)
    return retval

def results(f, changed):
    #print f + ":"
    str = ''
    for t in changed:
        str = str + ', ' + t

    print ('...'+ f[-55:]).rjust(60),  ('   -->   ' + red(str[1:]))

    return 1
def getDest(dest, file):
    tag = eyeD3.Tag()
    tag.link(file)

    artist = str(tag.getArtist())
    album = str(tag.getAlbum())

    dest = os.path.join(musicbase, os.path.join(dest, artist))
    dest = os.path.join(musicbase, os.path.join(dest, album))

    return dest

def setDirs(dest, files):
    #print "got here"
    tag = eyeD3.Tag()
    dests = []
    for f in files:
        tag.link(f)
        artist = str(tag.getArtist())
        album = str(tag.getAlbum())

        dir = os.path.join(musicbase, os.path.join(dest, artist))

        try:
            os.mkdir(dir)
        except OSError:
            pass
        else:
            print yellow("--------------------------------------------------------------")
            print warn("Creating Dir: " + dir)
            print yellow("--------------------------------------------------------------")

        os.chmod(dir, 0775)
        os.chown(dir, 115, 1001)

        dir = os.path.join(dir, album)

        try:
            os.mkdir(dir)
        except OSError:
            pass

        os.chmod(dir, 0775)
        os.chown(dir, 115, 1001)
        if dir not in dests:
            dests.append(dir)

    return dests

def moveFiles(dest, files):
    folders = setDirs(dest, files)
    folders.sort(key = len)

    for folder in folders:
        print ""
        print bold(yellow(folder))
        print "-----------------------------"
        for f in files:
            if not os.path.exists(f):
                pass
            elif getDest(dest, f) == folder:
                try:
                    os.chmod(f, 0775)
                    os.chown(f, 115, 1001)
                except OSError as (errno, strerror):
                    print warn(strerror + ": Are you root?")
                    sys.exit()
                else:
                    try:
                        shutil.move(f, str(folder))
                    except (IOError, OSError) as (errno, strerror):
                        print warn("Error({0}): {1}".format(errno, strerror))
                    else:
                        print ' -->  ' +os.path.basename(f)

                    pics = glob.glob1(folder, "*.jpg")
                    if pics:
                        i = 0
                        for p in pics:
                            picdest = os.path.join(str(folder), "cover-" + str(i)+".jpg")
                            i=+1
                            os.chmod(p, 0775)
                            os.chown(p, 115, 1001)
                            try:
                                shutil.move(p, picdest)
                            except:
                                pass

def convertID3(files):

    for f in files:
        tag = eyeD3.Tag()
        tag.link(f)
        updateVersion = eyeD3.ID3_V2_3

        v = eyeD3.utils.versionToString(updateVersion);
        if updateVersion == tag.getVersion():
            print ("No conversion necessary, tag is "\
                       "already version %s" % v);
        else:
            print ("Converting tag to ID3 version %s" % v);

        # Update the tag.
        print ("Writing tag...");
        #tag.do_tdtg = not opts.no_tdtg
        if not tag.update(updateVersion):
            print ("Error writing tag: %s" % f);
            return R_HALT;
##############################################




