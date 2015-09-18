# -*- coding: utf-8 -*

' Get real-links from tudou.com '

__author__ = "piratf"

import urllib2
import string
import sys
import time
import re
import webbrowser
from sgmllib import SGMLParser

Website = 'tudou'
# get wordtype of current machine with Windows OS
type = sys.getfilesystemencoding()

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
# }

# URl check


def linkServer(url):
    try:
        myPage = urllib2.urlopen(url).read()   # get first page in search
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request. (●°o°●)​ 」\n 意思就是说输入的内容没找到 囧'
            print 'Error code:', e.code
        elif hasattr(e, 'reason'):
            print 'We failed to reach the server (●°o°●)​ 」 \n 服务器挂了或者断网了'
            print 'Error code', e.reason
    else:
        pass
        # print decodeStr('Linked Success! (●°w°●)​ 」' )
    return myPage
###

### decode and encode


def decodeStr(str):
    return str.decode('utf8', 'ignore').encode(type, 'ignore')
###

# check number


def isNum(value):
    try:
        x = int(value)
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception, e:
        return False
    else:
        return True
###


class GetList(SGMLParser):

    def __init__(self, ai=False, attribute='class', value='G', subSubAtt='alt', title=''):
        self.reset(ai, attribute, value, subSubAtt, title)

    def reset(self, ai, attribute, value, subSubAtt, title):
        self.IDlist = []     # save the content
        self.ai = ai            # search a or img ? true is img, false is a
        self.getDiv = False     # if get div
        self.getdata = False    # if start to get data
        self.verbatim = 0       # floors
        self.attribute = attribute  # attribute of div
        self.value = value          # value of div
        self.subSubAtt = subSubAtt  # attribute of inside(img or a)
        self.title = title          # title for links
        SGMLParser.reset(self)

    def start_div(self, attrs):
        if self.getDiv == True:
            self.verbatim += 1   # add 1 more when get into sublayer
            return
        for k, v in attrs:  # traversal all properties
            if k == self.attribute and v == self.value:  # get in!
                self.getDiv = True
                return

    def end_div(self):  # found </div>
        if self.verbatim == 0:
            self.getDiv = False
        if self.getDiv == True:   # minus 1 when get out
            self.verbatim -= 1

    def start_a(self, attrs):
        if self.getDiv == False or self.ai == True:
            return
        if self.title == 'v':
            for k, v in attrs:
                if k == 'href':
                    self.IDlist.append(v)
                    return
        else:
            for k, v in attrs:  # traversal all properties
                # get in!
                if k == '_log_title' and v == self.title.decode(type).encode('utf-8'):
                    for k, v in attrs:
                        if k == 'site' and v == Website:
                            for i, j in attrs:
                                if i == 'href':
                                    self.IDlist.append(j)
                                return
        self.getdata = True

    def end_a(self):
        if self.getdata and self.ai == False:
            self.getdata = False

    def start_img(self, attrs):
        if self.getDiv == False or self.ai == False:
            return
        for k, v in attrs:  # traversal all properties
            if k == self.subSubAtt:  # get in!
                self.IDlist.append(decodeStr(v))
                return
        self.getdata = True

    def end_img(self):
        if self.getdata and self.ai == True:
            self.getdata = False

    def empty(self):
        return not self.IDlist

    def printID(self):
        print 'ID - '
        no = 0
        for i in self.IDlist:
            # ternary operator in python
            print no, ':', '$' if self.value == 'G' else '', i
            no += 1


class BTSpider:

    def __init__(self, condition):
        condition = urllib2.quote(
            condition.decode(type).encode('utf-8'), ":?=/")
        self.myUrl = 'http://www.soku.com/t/nisearch/' + condition
        self.condition = condition
        self.title = condition
        self.recordcount = 0    # how many records have gotten now
        self.myPage = ''
        self.type = ''
        print decodeStr('tudouSpider Searching..(●°7°●)​ 」')

    # Get information from search page:
    def spider(self):
        # print real url
        print self.myUrl.decode('utf8', 'ignore').encode(type, 'ignore')
        self.myPage = linkServer(self.myUrl)
        self.dealSearch()

    def dealSearch(self):
        # overload the 'GetList' function
        lister = GetList(True, 'class', 'G', 'alt')
        self.type = 'drama'
        lister.feed(self.myPage)
        if lister.empty():
            # if just some video not drama, the value of class will change
            lister = GetList(True, 'class', 'v', 'alt')
            self.type = 'video'
            lister.feed(self.myPage)
        lister.printID()    # print the result list out
        ###

        # choose items to analyze
        if self.type == 'video':
            choosed = raw_input(
                'enter the No. to visit online or enter \'q\' to quit: ')
            while choosed != 'q':
                while not isNum(choosed):
                    choosed = raw_input(
                        'need a number or enter \'q\' please: ')
                    if choosed == 'q':
                        return
                listerlink = GetList(False, 'class', 'v-link', 'herf', 'v')
                listerlink.feed(self.myPage)
                webbrowser.open(listerlink.IDlist[int(choosed)])
                choosed = raw_input(
                    'enter the No. to visit online or enter q to quit: ')
        elif self.type == 'drama':
            choosed = raw_input(
                'enter the No. or enter a to download, q to quit: ')
            while choosed != 'q':
                while not isNum(choosed) and choosed != 'a':
                    choosed = raw_input('need a number or enter a please: ')
                    if choosed == 'q':
                        return
                if choosed == 'a':
                    for dramaTitle in lister.IDlist:
                        listerlink = GetList(
                            False, 'class', 'panel_15', 'herf', dramaTitle)
                        listerlink.feed(self.myPage)
                        self.writeText(dramaTitle, listerlink)
                else:
                    # transfer to digit
                    dramaTitle = str(lister.IDlist[int(choosed)])
                    listerlink = GetList(
                        False, 'class', 'panel_15', 'herf', dramaTitle)
                    listerlink.feed(self.myPage)
                    self.writeText(dramaTitle, listerlink)
                choosed = raw_input(
                    '\renter the No. or enter a to download all: ')
        ###

    def writeText(self, dramaTitle,  listerlink):
        if not listerlink.empty():
            i = 0
            f = open(dramaTitle + '.txt', 'w')
            for link in listerlink.IDlist:
                f.write('\nEpisode %d\n\n' % i)
                f.write(' ' + link + '\n')  # if you need original address
                # self.getReallink(dramaTitle, link, f)
                i += 1
            f.close()
        else:
            print('can\'t find links')

    def justNeedTitle(self, dramaTitle):
        listerlink = GetList(False, 'class', 'panel_15', 'herf', dramaTitle)
        listerlink.feed(self.myPage)
        if not listerlink.empty():
            i = 0
            f = open(dramaTitle + '.txt', 'w')
            for link in listerlink.IDlist:
                f.write('\nEpisode %d\n\n' % i)
                self.getReallink(dramaTitle, link, f)
                i += 1
                # f.write(link + '\n')  # if you need original address
            f.close()
        else:
            print 'can\'t find links'

    def getReallink(self, dramaTitle, link, f):
        realPage = linkServer(
            'http://www.flvcd.com/parse.php?format=&kw=' + link + '&format=super')
        linkmatch = re.compile(
            r'http://k.youku.com/player\S{1,400}(?=")')  # 正则表达式
        reallink = linkmatch.findall(realPage)
        if reallink:
            for link in reallink:
                if link[-1] == '|':
                    link = link[0:len(link) - 1]
                f.write(link + '\n')
                sys.stdout.write('\rdealing %d records\r' % self.recordcount)
                sys.stdout.flush()
                self.recordcount += 1
        else:
            print decodeStr('nothing (●°y°●)​ 」')

# def _waiting_for_update..
    def getNextPage(self, myPage):
        next = re.compile(r'(?<=href=")/s/%s/\d+.htm(?=">Next)' %
                          self.condition.decode('gbk').encode('utf8'))
        nextmatch = next.search(myPage)
        if(nextmatch):
            return nextmatch.group()
        else:
            print 'Not Found nextPage..'

print decodeStr('''
###############   Welcome to tudouSpider ############
#
#   (●°-°●)​ 」[ 一脸正经
#
#   你输入的任何内容将被提交到土豆网上进行搜索
#
#    名字前面带'$'符号的是剧集，纯名字的是视频
#
#   独立视频可以调用浏览器中打开
#
#   剧集可以选择一集，整季，或整个系列进行地址解析
#
#   解析后的real-links会保存在当前文件夹下的txt文件中
#
####################################################
''')

condition = raw_input('tell me what you want:\n =>')
mySpider = BTSpider(condition)
mySpider.spider()
print decodeStr('\rDone! (●°u°●)​ 」')
