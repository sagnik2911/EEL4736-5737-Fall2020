In this design+implementation assignment, you will further extend the in-memory file system and shell, as described below. You may start from the Python files you extended in the previous assignment, or from the solutions.

 

## What to turn in on Canvas ##

- A file HW2.pdf with a brief description of your design

- Your modified memoryfs.py

- Your modified memoryfs_shell.py

 

## Design/implementation ##

1) Extend your design to support the path name layer. In particular, extend the FileName() class with these two methods:

def PathToInodeNumber(self, path, dir):

Similar to the book's description, this supports lookups for a path name, with "/" as your separator. path is a string, while dir is an integer (inode number

def GeneralPathToInodeNumber(self, path, cwd):

Similar to the book's description, allows using a leading "/" to refer to an absolute path. path is a string, while cwd is an integer (inode number of the current working directory)

 

Hint: look up Python .split() and .join methods for strings

Hint: you can "slice" a string the same way as a bytearray, e.g. sliced = string[1:len(string)]

 

2) Extend your design to support links, by extending the FileName() class with:

def Link(self, target, name, cwd):

Here, target is a string with a path to the file to link to; name is the name of the link; cwd is the current directory

This method should create an entry in the cwd with "name", and the inode number is the one looked up from target

Your code should check that the target is a file, that there is room for an additional entry in cwd, and whether the name already exists

 

3) Extend your design to support the following additional shell commands:

mkdir dirname

- create a new directory in the cwd

create filename

- create a new file in the cwd

append filename string

- appends a string to a file (you may assume the string has no spaces)

ln target linkname

- creates a link to target, with name linkname, in the cwd

ls

- [EEL5737 students only]: extend your ls implementation to have a prefix [refcnt]: for every object, and suffix "/" for directories, e.g:
[cwd=0]:ls <br>
[8]:./ <br>
[2]:data/ <br>
[3]:foo/ <br>
[3]:bar/ <br>
[1]:file1.txt <br>
[1]:file2.txt <br>
[1]:file3.txt <br>
[1]:file4.txt <br>

Hint: build upon the FileName.Create() method
