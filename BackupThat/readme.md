##BackupThat
------

List "SourceDir" you want to backup, give me "targetDir" you want to put the zip files in, and I can jump over the folders in "ignoreDir" you don't want to keep.

the directory structure under the sourcePath will be kept.
empty folders will be skipped.

with Python3.
or .exe file in folder "exec" has the same function.

###Usage:
Open the settings.txt file. (It's saved with utf-8 encoding)

Here is en example:
``` json
{
    "source":"E:\Code\Python\Backups\complete,E:\Code\Python\Backups\新建文件夹",
    "target":"E:\Code\Python\Backups\bak",
    "ignore":"E:\Code\Python\Backups\新建文件夹\123"
}
```

list the path of folders you want to backup in the quotes after "source", split with `,`, same as other two.

Attention: "target" path must be single.

Then running the .exe file or .py file. enter the comment you want for this backup.