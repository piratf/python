##BackupThat
------

中文参考内容：http://piratf.github.io/2015/09/19/BackupThat/

Tell me "SourceDir" which you want to backup, give me "targetDir" which you want to put the bak files in, and I can skip the folders in "ignoreDir" which you don't want to keep.

the directory structure under the sourcePath will be kept.
empty folders will be skipped.

with Python3.
or use the .exe file in folder "exec" if you don't have a python runtime.

'/' or '\' will all ok.

---

####Usage:
Open the settings.txt file. (It's saved with utf-8 encoding, notepad on windows might have "BOM head" but it's still ok)

Here is en example:
``` json
{
    "source":"E:/Git/python/BackupThat/exec,
        E:/Git/python/BackupThat/新建文件夹",
    "target":"E:/Git/python/BackupThat/bak",
    "ignore":"E:/Git/python/BackupThat/新建文件夹/2"
}
```

list the path of folders you want to backup in the quotes after "source", split with `,`, than the other two as well.

Attention: I could work with **only one** "target" path.

Then running the .exe file or .py file. enter the comment you want for this backup.

---