import os.path
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
import re
import os
import sys
import eyeD3
import settings

from output import *
def getParseOpts():
    t = "\t"
    print ''
    print bold("File Parsing Options:")
    print t + 'y - accept tags'
    print t + 'n - decline tags'
    print t + "a - accept and don't ask again"
    print t + "h - this help"
    print t + "q - quit"

def getCodeStr(code):
    if code =='%n':
        return "Track"
    if code =='%a':
        return "Artist"
    if code =='%A':
        return "Album"
    if code =='%t':
        return "Title"
    if code == '%i':
        return "IGNORE"
    else:
        print warn('Invalid Format')
        sys.exit()

def parseToTags(f, codes, vals):
    tag = eyeD3.Tag()
    tag.link(f)

    print warn('writing tags...')
    for c in range(0, len(codes)):
        if codes[c] =='%n':
            tag.setTrackNum(vals[c])
        if codes[c] =='%a':
            tag.setArtist(vals[c])
        if codes[c] =='%A':
            tag.setAlbum(vals[c])
        if codes[c] =='%t':
            tag.setTitle(vals[c])
        if codes[c] == '%i':
            pass
        tag.update()

def parseFile(format, files):
    print ""
    print bold(purple('File Name Parser:'))
    print '-' * 70
    if format.lower() == 'd':
        format = settings.format
        
    noAsk = False
    code = re.compile('/*(\%[a-zA-Z])/*')   #Sorts the %[*]
    p = re.compile('\%[a-zA-Z]')            #Sorts for the middle pieces
    delims = p.split(format)
    codes = code.findall(format)
    files.sort()

    
    for c in codes:     #Check for valid Format
        getCodeStr(c)
        
    for file in files:
        f, ext = os.path.splitext(os.path.basename(file))

        vals = []
        total = len(delims)-1
        for d in range(0, total):
            if d == 0:
                start = d + len(delims[d])
                end = f.find(delims[d+1])
            elif d == total-1:
                start = f.find(delims[d])+len(delims[d])
                end = len(f)-len(delims[d+1])
            else:
                start = f.find(delims[d])+len(delims[d])
                end = f.find(delims[d+1])

            vals.append(f[start:end])

        print blue(bold(f + ext))
        print "  parsed: " + format + ' as...'
        for v in range(0, len(vals)):
            vals[v] = vals[v].replace("_", " ")
            print ((' ' * 6) + bold(getCodeStr(codes[v]))).rjust(17) +" => ", vals[v]

        if noAsk == False:
            next = False
            while next == False:
                reslt = raw_input("Accept these tags [ynah]? (Default yes) [h for help]: ")
                if reslt.lower() == "y" or reslt == '':
                    next = True
                    parseToTags(file, codes, vals)
                elif reslt.lower() == 'n':
                    next = True
                    print warn('canceled')
                elif reslt.lower() == 'a':
                    noAsk = True
                    next = True
                    parseToTags(file, codes, vals)
                elif reslt.lower() == 'q':
                    print warn('quitting...')
                    sys.exit()
                elif reslt == 'h':
                    getParseOpts()
                else:
                    print warn("didn't understand response")
        else:
            parseToTags(file, codes, vals)
        print '-' * 40