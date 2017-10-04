from HTMLParser import HTMLParser
import urllib
import re
from datetime import datetime

#opener =  urllib.FancyURLopener({})
#url = "http://musikveckor.blogspot.se/"
#f = opener.open(url)
#content = f.read()


# Enum for playlist link types
class PlaylistLinkType:
    UNKNOWN     = -1
    SPOTIFY_URI = 0
    SPOTIFY_WEB = 1
    YOUTUBE     = 2
    SOUNDCLOUD  = 3


class PlayListLink:
    link = ""
    linkType = None

    def __init__(self, link, type):
        self.link = link
        self.linkType = type


class Tag:
    name = ""
    attrs = []

    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs

    def isLink(self):
        return self.name == 'a' and self.getAttr('href') is not None

    def hasClass(self, classSpec):
        for a in self.attrs:
            if a[0] == 'class':
                if a[1].strip() == classSpec:
                    return True
        return False

    def getAttr(self, attrName):
        for a in self.attrs:
            if a[0] == attrName:
                return a[1]
        return None


class HTMLParserBase(HTMLParser):
    def findAttrFromTag(self, detectTag, tag, attr, attrs):
        return


#
class BlogPostParser(HTMLParserBase):
    title = ""
    dateTime = None
    post_html_content = ""
    poster = ""
    playlistLinks = list()

    def handle_starttag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        return


#
class PageArchiveParser(HTMLParserBase):
    monthPageList = list()

    def handle_starttag(self, tag, attrs):
        tag = Tag(tag, attrs)
        if tag.isLink() and tag.hasClass('post-count-link'):
            m = re.match('http://musikveckor.blogspot.se/[0-9]*/[0-9]*/', tag.getAttr('href'))
            if m is not None:
                self.monthPageList.append(m.group(0))
                print m.group(0)
            else:
                print "Skipping " + attrs[1][1]

    def feed(self, data):
        print "Parsing blog post archive..."
        HTMLParser.feed(self, data)


#
class MonthPageParser(HTMLParserBase):
    def handle_starttag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        return

    def process(self, pageLink):
        print "Parsing month page " + pageLink + "..."
        #fancy = urllib.FancyURLopener({})
        #pageFile = fancy.open(pageLink)
        #monthPageContent = pageFile.read()
        #HTMLParserBase.feed(self, monthPageContent)


with open('mvroot.html') as f:
    content = f.read()

# instantiate the parser and fed it some HTML
pageArchiveParser = PageArchiveParser()
pageArchiveParser.feed(content)
print str(len(pageArchiveParser.monthPageList)) + " pages to process"


for monthPage in pageArchiveParser.monthPageList:
    monthPageParser = MonthPageParser()
    monthPageParser.process(monthPage)

