# -*- coding: utf-8 -*
# author : piratf

import urllib2
import string
import sys
import time
import re
from sgmllib import SGMLParser

Website = 'tudou'
type = sys.getfilesystemencoding()

# build headers if tudou needs that
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
# }

### URl check
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
        myPage = ""
    else:
        pass
        # print dStr('Linked Success! (●°w°●)​ 」' )
    return myPage
###

### decode and encode
def dStr(str):
    return str.decode('utf-8').encode(type)
###

### check number
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
    def __init__(self, ai = False, attribute = 'class', value = 'G', subSubAtt = 'alt', title = ''):
        self.reset(ai, attribute, value, subSubAtt, title)

    def reset(self, ai, attribute, value, subSubAtt, title):
        self.IDlist = []     # save the content
        self.ai = ai            # search a or img ? true is a, false is img
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
            self.verbatim +=1   # add 1 more when get into sublayer
            return
        for k,v in attrs:   #traversal all properties
            # print k, v
            if k == self.attribute and v == self.value:  # get in!
                # print 'hello'
                self.getDiv = True
                return

    def end_div(self):  # found </div>
        if self.verbatim == 0:
            self.getDiv = False
        if self.getDiv == True:   # minus 1 when get out
            self.verbatim -=1

    def start_a(self, attrs):
        if self.getDiv == False or self.ai == True:
            return
        for k,v in attrs:   #traversal all properties
            if k == '_log_title' and v == self.title.decode(type).encode('utf-8'):  # get in!
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
        for k,v in attrs:   #traversal all properties
            if k == self.subSubAtt:  # get in!
                # print 'hello'
                self.IDlist.append(v.decode('utf8','ignore').encode(type, 'ignore'))
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
            print no, ':', i
            no += 1;

class BTSpider:
    def __init__(self, condition):
        condition = urllib2.quote(condition.decode(type).encode('utf-8'))
        self.myUrl = 'http://www.soku.com/t/nisearch/'+ condition
        self.condition = condition
        self.title = condition
        #self.want = 0  # how many records you want
        self.recordcount = 0    # how many records have gotten now
        #self.lastcount = 0
        #self.prograssbar = '#'
        #self.datas = []
        self.myPage = ''
        print dStr('tudouSpider Searching..(●°7°●)​ 」')

    # Get information from search page:
    def spider(self):
        print self.myUrl.decode('utf8', 'ignore').encode(type, 'ignore')    # print real url
        self.myPage = linkServer(self.myUrl)
        self.dealSearch()

    def dealSearch(self):
        ### 
        lister = GetList(True, 'class', 'G', 'alt')
        lister.feed(self.myPage)
        if lister.empty():
            lister = GetList(True, 'class', 'v', 'alt')   # if just some video not drama, the value of class will change
            lister.feed(self.myPage)
        lister.printID()
        ###

        choosed = raw_input('enter the No. or enter "a" to download all: ')

        while not isNum(choosed) and choosed != 'a':
            choosed = raw_input('need a number or enter "a" please: ')
        if choosed == 'a':
            for dramaTitle in lister.IDlist:
                listerlink = GetList(False, 'class', 'panel_15', 'herf', dramaTitle)
                listerlink.feed(self.myPage)
                if not listerlink.empty():
                    i = 0
                    f = open(dramaTitle + '.txt', 'w')
                    for link in listerlink.IDlist:
                        f.write('\nEpisode %d\n\n' % i)
                        # self.getReallink(dramaTitle, link, f)
                        i += 1
                        # f.write(link + '\n')  # if you need original address
                    f.close()
                else:
                    print 'can\'t find links'
        else:
            dramaTitle = str(lister.IDlist[int(choosed)])
            listerlink = GetList(False, 'class', 'panel_15', 'herf', dramaTitle)
            listerlink.feed(self.myPage)
            if not listerlink.empty():
                i = 0
                f = open(dramaTitle + '.txt', 'w')
                for link in listerlink.IDlist:
                    f.write('\nEpisode %d\n\n' % i)
                    f.write(link + '\n')
                    # self.getReallink(dramaTitle, link, f)
                    i += 1
                    # f.write(link + '\n')  # if you need original address
                f.close()
            else:
                print 'can\'t find links'

    def justNeedTitle(dramaTitle):
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
        realPage = linkServer('http://www.flvcd.com/parse.php?format=&kw=' + link + '&format=super')

        linkmatch = re.compile(r'http://k.youku.com/player\S{1,400}(?=")')
        reallink = linkmatch.findall(realPage)
        if reallink:
            for link in reallink:
                if link[len(link)-1] == '|':
                    link = link[0:len(link)-1]
                f.write(link+'\n')
                sys.stdout.write('\rdealing %d records\r' % self.recordcount)
                sys.stdout.flush()
                self.recordcount += 1
        else:
            sys.stdout.write('\rdealing %d records\r' % self.recordcount)
            sys.stdout.flush()
            self.recordcount += 1
            pass
            # print dStr('nothing (●°y°●)​ 」')

# waiting for update..
#    def getNextPage(self, myPage):
#        next = re.compile(r'(?<=href=")/s/%s/\d+.htm(?=">Next)' % self.condition.decode('gbk').encode('utf8'))
#        nextmatch = next.search(myPage)
#        if(nextmatch):
#            return nextmatch.group()
#        else:
#            print 'Not Found nextPage..'


print dStr('''
##########   Welcome to tudouSpider ###########
#
#   (●°-°●)​ 」[ 一脸正经
#
#   你输入的任何内容将被提交到土豆网上进行搜索
#
#   选择一集进行下载
#
#   在当前文件夹里出现真实下载地址的txt文件
#
#   复制所有地址到下载工具即可[ 勾
#
#   8月更新：由于版权原因，解析过程关闭。
#   目前依然可以搜索和抓取土豆链接。欢迎使用~
#
###############################################
''')

condition = raw_input('tell me what you want:\n =>')
mySpider = BTSpider(condition)
mySpider.spider()
print dStr('Done! (●°u°●)​ 」')