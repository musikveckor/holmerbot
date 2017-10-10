from HTMLParser import HTMLParser
import urllib
import re
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#opener =  urllib.FancyURLopener({})
#url = "http://musikveckor.blogspot.se/"
#f = opener.open(url)
#content = f.read()

class State():
    level = 0
    name = ""

    def __init__(self, name):
        self.name = name
        self.level = 0

class StateStack():
    stack = list()

    def __init__(self):
        self.push('root')

    def push(self, stateToken):
        self.stack.append(State(stateToken))

    def pop(self):
        self.stack.pop()

    def incLevel(self):
        self.get().level += 1

    def decLevel(self):
        assert(self.get().level > 0)
        self.get().level -= 1

    def get(self):
        return self.stack[len(self.stack)-1]

    def currentStateLevel(self):
        return self.get().level

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

    def hasName(self, name):
        return self.name == name

    def isLink(self):
        return self.hasName('a') and self.getAttr('href') is not None

    def isDiv(self):
        return self.hasName('div')

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

class BlogPostData():
    title = None
    url = None
    dateTime = None
    id = None
    body = None
    poster = None
    playlistLinks = None

    def __init__(self):
        self.title = None
        self.url = None
        self.dateTime = None
        self.id = None
        self.body = None
        self.poster = None
        self.playlistLinks = list()  # PlayListLink[]

    def verifyAndGenerateWarnings(self):
        return

    def debugPrint(self):
        print self.title
        print self.url
        print self.dateTime
        print self.id
        print self.body
        print self.poster
        print self.playlistLinks

#
class BlogPostParser(HTMLParserBase):
    blogPostData = None
    readerState = None
    stateLevel = 0

    def __init__(self):
        HTMLParserBase.__init__(self)
        self.blogPostData = BlogPostData()
        self.readerState = StateStack()
        self.stateLevel = 0

    def stateIs(self, state):
        return self.readerState.get().name == state

    def pushState(self, state):
        self.readerState.push(state)

    def popState(self):
        self.readerState.pop()

    def handle_starttag(self, tagName, attrs):
        tag = Tag(tagName, attrs)
        self.readerState.incLevel()

        # Post title
        if tag.hasName('h3') and tag.hasClass('post-title entry-title'):
            self.pushState("in-title")
        # Post body
        elif tag.isDiv() and tag.hasClass('post-body entry-content'):
            self.pushState('in-body')

        return

    def handle_endtag(self, tagName):
        if self.readerState.currentStateLevel() == 0 and self.readerState.get() != 'root':
            self.popState()
        self.readerState.decLevel()

    def handle_data(self, data):
        if self.stateIs('root'):
            pass
        elif self.stateIs('in-title'):
            if self.blogPostData.title is None:
                self.blogPostData.title = ""
            self.blogPostData.title += data
        elif self.stateIs('in-body'):
            if self.blogPostData.body is None:
                self.blogPostData.body = ""
            self.blogPostData.body += data

    def process(self, blogPostURL):
        #fancy = urllib.FancyURLopener({})
        #pageFile = fancy.open(blogPostURL)
        #blogPostContent = pageFile.read()
        #HTMLParserBase.feed(self, blogPostContent)
        print "Parsing blog post " + blogPostURL
        with open('blog_post2.html') as f:
            content = f.read()
        HTMLParserBase.feed(self, content)
        self.blogPostData.verifyAndGenerateWarnings()
        self.blogPostData.debugPrint()
        return self.blogPostData

#
class MonthPageParser(HTMLParserBase):
    blogPostURLList = list()

    # This parser looks for the post href link in all month posts
    # <a class='timestamp-link' href='http://musikveckor.blogspot.se/2011/02/blandband.html' rel='bookmark' title='permanent link'>
    #   <abbr class='published' itemprop='datePublished' title='2011-02-11T09:39:00+01:00'>09:39</abbr>
    # </a>

    def handle_starttag(self, tag, attrs):
        tag = Tag(tag, attrs)
        if tag.isLink() and tag.hasClass('timestamp-link'):
            self.blogPostURLList.append(tag.getAttr('href'))

    def process(self, pageLink):
        print "Parsing month page " + pageLink + "..."
        with open('month_page_2011_02.html') as f:
            content = f.read()
        HTMLParserBase.feed(self, content)
        #fancy = urllib.FancyURLopener({})
        #pageFile = fancy.open(pageLink)
        #monthPageContent = pageFile.read()
        #HTMLParserBase.feed(self, monthPageContent)


#
class PageArchiveParser(HTMLParserBase):
    monthPageURLList = list()

    def handle_starttag(self, tag, attrs):
        tag = Tag(tag, attrs)
        if tag.isLink() and tag.hasClass('post-count-link'):
            m = re.match('http://musikveckor.blogspot.se/[0-9]*/[0-9]*/', tag.getAttr('href'))
            if m is not None:
                self.monthPageURLList.append(m.group(0))
                print m.group(0)
            else:
                print "Skipping " + attrs[1][1]

    def feed(self, data):
        print "Parsing blog post archive..."
        HTMLParser.feed(self, data)


with open('mvroot.html') as f:
    content = f.read()

# instantiate the parser and fed it some HTML
pageArchiveParser = PageArchiveParser()
pageArchiveParser.feed(content)
print str(len(pageArchiveParser.monthPageURLList)) + " pages to process"

monthPageParser = MonthPageParser()
for monthPageURL in pageArchiveParser.monthPageURLList:
    monthPageParser.process(monthPageURL)
    break
print str(len(monthPageParser.blogPostURLList)) + " blog posts to process"

blogPostDataList = list()
for blogPostURL in monthPageParser.blogPostURLList:
    blogPostParser = BlogPostParser()
    data = blogPostParser.process(blogPostURL)
    blogPostDataList.append(data)