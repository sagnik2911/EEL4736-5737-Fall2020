In this design+implementation assignment, you will extend an in-memory file system that is inspired by the design described in Chapter 2 of the textbook. Please refer to the slides posted to Canvas (under Files->Design assignments) for an overview of the implementation.

Two Python code files are provided to you: memoryfs.pyPreview the document and memoryfs_shell.pyPreview the document . The memoryfs.py file implements the file system objects described in the overview presentation. The memoryfs_shell.py imports memoryfs, and implements a rudimentary "shell" for interactive access to the file system. You can invoke the shell with:

python memoryfs_shell.py

The version of the shell provided to you only implements the "cd" command, which allows you to change the working directory. You will extend it to support two additional commands: cat, and ls.

 

## What to turn in on Canvas ##

- A file HW1.pdf with:

  - your answer to question 1)

  - a brief description of how you approached solving questions 2) and 3)

- Your modified memoryfs.py

- Your modified memoryfs_shell.py

 

## Questions ##

1) You are given a "dump" file 12345678_BS_128_NB_256_IS_16_MI_16.dump with pre-loaded contents for blocks. To help you better understand the code, use this "dump" file as an input, and add code as needed to help answer the following questions:

- Which directories are present in the root directory?

- How many data blocks are in use for inode 4?

- In which directory is file9.txt located, and what are its contents?

Hint: you can use the main function in memory_shell.py to create objects and call methods appropriately to answer these questions. Make sure your code goes after blocks are initialized from the dump call (i.e., after RawBlocks.InitializeBlocks(False,UUID))

 

2) Extend the code in memoryfs.py to implement the following method of the FileName() class:

def Read(self, file_inode_number, offset, count):

This method reads and returns a bytearray from a file. file_inode_number is the inode of the file to be read; offset is the starting point to read from (note: all bytearrays in the code start from index 0); count is the number of bytes to read.

The method must handle the following error conditions, and return -1:

- inode is invalid/not a file

- offset is larger than the file's size

 

Hint: to convert the returning bytearray to a string for printing, you can use the decode() function, e.g. print (myarray.decode())

Hint: focus on understanding the Write() function provided to you, as a starting point for the implementation of Read()

Hint: make use of the logging.debug() function to help you debug as you go along. Logging information is written to memoryfs.log

 

3) Extend the code in memoryfs_shell.py to implement two additional commands:

- cat filename : this command takes one argument (filename). It looks up filename in the context of the current working directory (cwd); if the lookup is successful, and it is a file, print out the contents of the file.

- [EEL5737 students only] ls : this command takes no argument. It traverses the data blocks of the current working directory and prints out the name of each object (file or directory) present in the cwd.

Hint: memoryfs_shell.py has a skeleton for the shell interpreter - you need to add methods for ls() and cat(), and call them appropriately from the shell's loop

Hint: the shell can be exited with the "exit" command

Hint: make sure you understand the layout of directory entry data blocks and the role of the MAX_FILENAME, FILE_NAME_DIRENTRY_SIZE and FILE_NAME_DIRENTRY_SIZE constants by studying the overview presentation slides carefully

Hint: Note that your work will be tested with additional files, not just the dump file provided to you - so make sure you test your design well. In the the dump file given to you, file1.txt has the following contents:

BEGIN. Contents of file1.txt - this exceeds a BLOCK_SIZE of 128. Contents of file1.txt - this exceeds a BLOCK_SIZE of 128. Contents of file1.txt - this exceeds a BLOCK_SIZE of 128. Contents of file1.txt - this exceeds a BLOCK_SIZE of 128. END.
