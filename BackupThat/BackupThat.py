# -*- coding: utf-8 -*
# Filename: BackupHexo.py

__author__ = 'Piratf'

import os
import re
import sys
import time
import json
import codecs
import zipfile

class BackupThat:
    sourceDir = []
    targetDir = []
    ignoreDir = []

    def __init__(self):
        sourceDir = []
        targetDir = []
        ignoreDir = []

    # read sourceDir from settings.txt
    def getSourceDir(self):
        ''' Get SourceDir, TargetDIr, ignoreFiles from source.txt

        '''

        try:
            # relocate to where the program running
            fileHandle = codecs.open(
                os.getcwd() + "\settings.txt", 'r+', encoding='utf-8-sig')
            # fileHandle = open(r"source.txt", 'r')
            sourceText = fileHandle.read()
            fileHandle.close()
            sourceText = sourceText.replace("\\", "/")
            sourceText = re.sub("\s+", "", sourceText)
            data = json.loads(sourceText)
            self.sourceDir = [s.strip() for s in data["source"].split(',')]
            self.targetDir = [s.strip() for s in data["target"].split(',')]
            self.ignoreDir = [s.strip() for s in data["ignore"].split(',')]
        except IOError as err:
            print("Attention: ->reading setting files error")
            print(err)

    # check end and create inexistent folders
    def checkDirs(self, dirs):
        newdir = []
        for d in dirs:
            if d == "":
                continue
            if d[-1] != '/':
                d = d + '/'
            if not os.path.isdir(d):
                print('Attention: ' + d +
                      r" is not a dir, but in the dir array. it's will be created.")
                os.makedirs(d)
            newdir.append(d)
        return newdir

    # check len of folders, change targetDir list to one targetDir string
    def checkLens(self):
        # judge lengths
        if len(self.targetDir) > 1:
            print("target more than one, please modify that")
            return
        elif len(self.targetDir) < 1:
            print("can't find any target path")
            return
        else:
            self.targetDir = self.targetDir[0]
        if len(self.sourceDir) < 1:
            print("can't find any source path")
            return

    # print folders path to check again
    def printDirInfo(self):
        print("the sources dir:")
        for d in self.sourceDir:
            print('  ', d)
        print("the target dir:\n  ", self.targetDir)
        print("the ignore dir:")
        if len(self.ignoreDir) == 0:
            print("   None")
        else:
            for d in self.ignoreDir:
                print('  ', d)

    # now make target folder structure before write things
    def makeStructure(self):
        ### date and times
        # the process use date to name and pigeonhole the folders
        today = self.targetDir + '/' + time.strftime('%Y%m%d')
        if not os.path.exists(today):
            os.makedirs(today)
            print("Successfully created today's directory")
        # use time to name the backup dirs
        now = time.strftime('%H%M%S')
        ##################################################################

        # comments
        # you can input the comment at each time
        comment = 'test'
        # comment = input('Enter a comment if you need --> ')
        # the space will be replace to '_'
        if len(comment) == 0:
            self.targetDir = today + '/' + now
        else:
            self.targetDir = today + '/' + now + '_' + \
                comment.replace(' ', '_')
        ##################################################################
        # start zip
        # count time
        # check if need to build the new folder
        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)
            print("Successfully created target directory")
        print("Welcome today")

    # backup main process
    def backup(self):
        # sourceDir is the folder you want to build a backup from
        # you can modify it as you wish, use same format anyway please
        # targetDir is the target, same as above
        # ignoreDir list folders under sourceDir but you don't want to keep
        self.getSourceDir()
        # now check the dirs
        self.sourceDir = self.checkDirs(self.sourceDir)
        self.targetDir = self.checkDirs(self.targetDir)
        self.ignoreDir = self.checkDirs(self.ignoreDir)
        # modify targetDir from list to string
        self.checkLens()
        self.printDirInfo()
        self.makeStructure()

        startTime = time.clock()
        # backup each folder you want
        for it in self.sourceDir:
            targetPath = self.targetDir + "/" + it.split('/')[-2] + ".zip"
            zipFiles2TargetPath(it, targetPath, exclude=self.ignoreDir)

        endTime = time.clock()

        print('backup completed')
        print('use time: %fs' % (endTime - startTime))
        input(
            "-----------------------------------------------\nCompression has been  completed! \nPress Enter key to continue.")


def zipFiles2TargetPath(sourcePath, targetPath, exclude=[]):
    ''' zip files in sourcePath, recursively

    the targetPath means the path of the target zip file, including the name of the zip file.
    if you want to exclude some folders in the sourcePath, list them in the third parameter.
    the directory structure under the sourcePath will be kept.
    empty folders will be skipped.
    using "zipfile" in the standard library'''

    print (sourcePath)
    print (targetPath)
    print (exclude)

    print("start zip")
    filesCount = 0
    # ignore unnecessary path in zip file
    os.chdir(sourcePath)
    f = zipfile.ZipFile(targetPath, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(sourcePath):
        # print ('before exclude')
        # print ('++++++++++++++++++++++++++++')
        # print (dirpath)
        # print ('============================')
        # print (dirnames)
        # print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print (filenames)

        # Rule out the folders in ignoreDir
        for excludePath in exclude:
            for dn in dirnames:
                print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print (dirpath + dn + '/')
                if excludePath == dirpath + dn + '/':
                    dirnames.remove(excludePath.split('/')[-2])

        # print ('============================')
        # print ('after exclude')
        # for dirs in dirnames:
        #     print (dirs)
        # print ('============================')

        # Write files
        for filename in filenames:
            filesCount += 1
            # at here we will report the process
            print('dealing %s\r' % filesCount, end='')
            sys.stdout.flush()
            filePath = dirpath + '/' + filename
            # print (dirpath.split('/'))
            print (filePath)
            f.write(filePath)
    f.close()
    print("zip completed")
    return filesCount

try:
    demo = BackupThat()
    demo.backup()
except:
    print("Unexpected error:", sys.exc_info())  # 返回出错信息
    input('Press Enter key to exit')
