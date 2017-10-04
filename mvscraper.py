from HTMLParser import HTMLParser
import urllib
import re

#opener =  urllib.FancyURLopener({})
#url = "http://musikveckor.blogspot.se/"
#f = opener.open(url)
#content = f.read()


#
class PageArchiveParser(HTMLParser):
    postPageList = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and  attrs[0][0] == 'class' and attrs[0][1] == 'post-count-link':
            m = re.match('http://musikveckor.blogspot.se/[0-9]*/[0-9]*/', attrs[1][1])
            if m != None:
                self.postPageList.append(m.group(0))
                print m.group(0)

#
class MonthPageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        return

with open('mvroot.html') as f:
    content = f.read()

# instantiate the parser and fed it some HTML
pageArchiveParser = PageArchiveParser()
pageArchiveParser.feed(content)
print str(len(pageArchiveParser.postPageList)) + " pages to process"


def processMonthPage(page):
    fancy = urllib.FancyURLopener({})
    pageFile = fancy.open(page)
    pageContent = pageFile.read()

for monthPage in pageArchiveParser.postPageList:
    processMonthPage(monthPage)

