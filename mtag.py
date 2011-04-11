#!/usr/bin/env python
import argparse
import shutil
import path

import settings
from mp3batch import *
from mp3check import *

argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
listing = argparser.add_argument_group("Tag Analysis")
tagging = argparser.add_argument_group('Batch Tagging')
util = argparser.add_argument_group('Utilities')

listing.add_argument('-t', '--tag-list', action="store_true", dest="tags",
						help='lists important tags' )
listing.add_argument('-o', '--occurances', action="store_true", dest="occur",
						help='analysis of batchable tags and their consistency across the folder(s)' )
listing.add_argument('-m', '--missing', action="store_true", dest="missing",
						help='list of the file names and missing tags' )

tagging.add_argument('-a', '--artist', action="store", type=str, dest="artist",
						help='define the artist' )
tagging.add_argument('-A', '--album', action="store", dest="album", type=str,
						help='define the album' )
tagging.add_argument('-g', '--genre', action="store", dest="genre",
						help='define the genre (accepts Name, or ID)\n  see -L {n, i} for ID3 recognized Genre Name & ID')
tagging.add_argument('-y', '--year', action="store", dest="year",
						help='define the year')

util.add_argument('-d', action="store", dest="dest", choices=getValidDest(),
						help=" \nmoves files to a base Subsonic music folder (valid choices above) \n--- musicbase dir can be set in 'settings.py'")
util.add_argument('-R', dest="recur", action="store_true", default=False,
						help='move Recursively through folders')
util.add_argument('-r', '--rename', action="store_true", default=False,
						help='rename files according to Tags')
util.add_argument('-c','--convert', action="store_true", default=False,
						help='convert Existing Tags to ID3v2.3 ')
util.add_argument('-L', action="store", dest="genre_list", choices=["n","i"],
						help="list of ID3 Recognized Genres: \n   n:  by Genre Name \n   i:  by Genre ID")

argparser.add_argument('Directory', action="store", nargs = '?', default = os.getcwd(),
                        help="directory to work with (default: current dir [pwd])")

results = argparser.parse_args()
args = sys.argv


if len(args) == 1:
    argparser.print_help()
    sys.exit()
########################################################

if os.path.isdir(results.Directory):
    basedir = results.Directory
else:
    basedir = os.path.dirname(results.Directory)

mufiles = []

if results.recur:
    base = path(basedir)
    for f in base.walkfiles('*.mp3'):
        mufiles.append(str(f))
else:
    for f in glob.glob1(basedir, '*.mp3' ):
        mufiles.append(os.path.join(basedir, f))

if not mufiles and not results.genre_list:
    print warn("No .mp3 Files in Dir(s): .mp3 and .MP3 are different")
    sys.exit()
else:
    print ""
    print bold(purple("MP3 Batch:"))
    print bold(purple("------------------"))

artist = ""
album = ""
genre = ""
year = ""
comment = ''
tagModified = False

if results.artist:
    artist = results.artist
    tagModified = True
if results.album:
    album = results.album
    tagModified = True
if results.genre:
    genre = results.genre
    tagModified = True
if results.year:
    year = results.year
    tagModified = True

if tagModified:
    print warn("Writing tags...")
    print "----------------------------------"
    if not setTags(mufiles, artist, album, genre, year):
        print "\tAll Tags Already Set to Specified Values"

if results.convert:
    convertID3(mufiles)
if results.tags:
    listTags(mufiles)
if results.occur:
    ocurranceRslts(mufiles)
if results.missing:
    missingRslts(mufiles)

if results.genre_list == 'n':
    printGenresName()
elif results.genre_list == 'i':
    printGenresNum()

if results.rename == True:
    if setFileName(mufiles) == 0:
        print "\tNo files needed to be renamed!"

if results.dest:
    for f in mufiles:
        try:
            dest = setDirs(results.dest, f)
            os.chmod(f, 0775)
            os.chown(f, 115, 1001)
        except OSError as (errno, strerror):
            print warn(strerror + ": Are you root?")
            sys.exit()
        else:
            try:
                shutil.move(f, str(dest))
            except (IOError, OSError) as (errno, strerror):
                print warn("Error({0}): {1}".format(errno, strerror))
            else:
                print '  -->  ' +os.path.basename(f)

            pics = glob.glob1(os.path.dirname(f), "*.jpg")
            if pics:
                i = 0
                for p in pics:
                    picdest = os.path.join(str(dest), "cover-" + str(i)+".jpg")
                    i=+1
                    os.chmod(p, 0775)
                    os.chown(p, 115, 1001)
                    try:
                        shutil.move(p, picdest)
                    except:
                        pass

