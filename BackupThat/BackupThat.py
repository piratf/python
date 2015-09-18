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


def zipFiles2TargetPath(sourcePath, targetPath, exclude=[]):
    ''' zip files in sourcePath, recursively

    the targetPath means the path of the target zip file, including the name of the zip file.
    if you want to exclude some folders in the sourcePath, list them in the third parameter.
    the directory structure under the sourcePath will be kept.
    empty folders will be skipped.
    using "zipfile" in the standard library'''
    print("start zip")
    filesCount = 0
    # ignore unnecessary path in zip file
    os.chdir(sourcePath)
    f = zipfile.ZipFile(targetPath, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(sourcePath):
        sourcePathList = sourcePath.split('/')
        for excludePath in exclude:
            for dn in dirnames:
                if excludePath == dirpath + '/' + dn + '/':
                    dirnames.remove(excludePath.split('/')[-2])
        for filename in filenames:
            filesCount += 1
            # at here we will report the process
            print('dealing %s\r' % filesCount, end='')
            sys.stdout.flush()
            dirname = dirpath.split('/')[-1]
            f.write(
                filename if dirname == "" else './' + dirname + '/' + filename)
    f.close()
    print("zip completed")
    return filesCount

# read sourceDir


def getSourceDir():
    ''' Get SourceDir, TargetDIr, ignoreFiles from source.txt

    '''

    try:
        fileHandle = codecs.open(
            os.getcwd() + "\settings.txt", 'r+', encoding='utf-8-sig')
        # fileHandle = open(r"source.txt", 'r')
        sourceText = fileHandle.read()
        fileHandle.close()
        sourceText = sourceText.replace("\\", "/")
        sourceText = re.sub("\s+", "", sourceText)
        print (sourceText)
        data = json.loads(sourceText)
        sourceDir = [s.strip() for s in data["source"].split(',')]
        targetDir = [s.strip() for s in data["target"].split(',')]
        ignoreDir = [s.strip() for s in data["ignore"].split(',')]
    except IOError as err:
        print("Attention: ->reading files error")
        print(err)
        return [], [], []
    return sourceDir, targetDir, ignoreDir


# check end and create inexistent folders
def checkDirs(dirs):
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


def checkLens(sourceDir, targetDir):
    # judge lengths
    if len(targetDir) > 1:
        print("target more than one, please modify that")
        return
    elif len(targetDir) < 1:
        print("can't find any target path")
        return
    else:
        targetDir = targetDir[0]
    if len(sourceDir) < 1:
        print("can't find any source path")
        return
    return targetDir


def printDirInfo(sourceDir, targetDir, ignoreDir):
    print("the sources dir:")
    for d in sourceDir:
        print('  ', d)
    print("the target dir:\n  ", targetDir)
    print("the ignore dir:")
    if len(ignoreDir) == 0:
        print("   None")
    else:
        for d in ignoreDir:
            print('  ', d)


def makeStructure(sourceDir, targetDir, ignoreDir):
    ### date and times
    # the process use date to name and pigeonhole the folders
    today = targetDir + '/' + time.strftime('%Y%m%d')
    if not os.path.exists(today):
        os.makedirs(today)
        print("Successfully created directory")
    # use time to name the backup dirs
    now = time.strftime('%H%M%S')
    ##################################################################

    # comments
    # you can input the comment at each time
    comment = input('Enter a comment if you need --> ')
    # the space will be replace to '_'
    if len(comment) == 0:
        target = today + '/' + now
    else:
        target = today + '/' + now + '_' + \
            comment.replace(' ', '_')
    ##################################################################
    # start zip
    # count time
    # check if need to build the new folder
    if not os.path.exists(target):
        os.makedirs(target)
        print("Successfully created directory")
    print("Welcome today")
    return target


def backup():
    # sourceDir is the folder you want to build a backup from
    # you can modify it as you wish, use same format anyway please
    # targetDir is the target, same as above
    # ignoreDir list folders under sourceDir but you don't want to keep
    sourceDir, targetDir, ignoreDir = getSourceDir()
    # now check the dirs
    sourceDir = checkDirs(sourceDir)
    targetDir = checkDirs(targetDir)
    ignoreDir = checkDirs(ignoreDir)

    # modify targetDir from list to string
    targetDir = checkLens(sourceDir, targetDir)

    printDirInfo(sourceDir, targetDir, ignoreDir)

    target = makeStructure(sourceDir, targetDir, ignoreDir)
    
    startTime = time.clock()
    # backup each folder you want
    for it in sourceDir:
        targetPath = target + "/" + it.split('/')[-2] + ".zip"
        zipFiles2TargetPath(it, targetPath, exclude=ignoreDir)

    endTime = time.clock()

    print('backup completed')
    print('use time: %fs' % (endTime - startTime))
    input(
        "-----------------------------------------------\nCompression has been completed! \nPress Enter key to continue.")
    ##################################################################

try:
    backup()
except:
    print("Unexpected error:", sys.exc_info())  # 返回出错信息
    input('Press Enter key to exit')
