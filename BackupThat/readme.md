##BackupThat
------

中文参考内容：http://piratf.github.io/2015/09/19/BackupThat/

List "SourceDir" you want to backup, give me "targetDir" you want to put the zip files in, and I can jump over the folders in "ignoreDir" you don't want to keep.

the directory structure under the sourcePath will be kept.
empty folders will be skipped.

with Python3.
or .exe file in folder "exec" has the same function.

'/' or '\' will all ok.

---

the `bak` folder was for test, there are some generated output file built when testing. it's unnecessary.

####Usage:
Open the settings.txt file. (It's saved with utf-8 encoding, notepad.exe on windows might have BOM head but it's ok)

Here is en example:
``` json
{
    "source":"E:/Git/python/BackupThat/exec,
        E:/Git/python/BackupThat/新建文件夹",
    "target":"E:/Git/python/BackupThat/bak",
    "ignore":"E:/Git/python/BackupThat/新建文件夹/2"
}
```

list the path of folders you want to backup in the quotes after "source", split with `,`, same as other two.

Attention: "target" path must be single.

Then running the .exe file or .py file. enter the comment you want for this backup.

---