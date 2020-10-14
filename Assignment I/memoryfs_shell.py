import pickle, logging

from memoryfs import *
import queue

## This class implements an interactive shell to navigate the file system

class FSShell():
  def __init__(self, file):
    # cwd stored the inode of the current working directory
    # we start in the root directory
    self.cwd = 0
    self.FileObject = file

  # implements cd (change directory)
  def cd(self, dir):
    i = self.FileObject.Lookup(dir,self.cwd)
    if i == -1:
      print ("Error: not found\n")
      return -1
    inobj = InodeNumber(self.FileObject.RawBlocks,i)
    inobj.InodeNumberToInode()
    if inobj.inode.type != INODE_TYPE_DIR:
      print ("Error: not a directory\n")
      return -1
    self.cwd = i

  # implements ls (lists files in directory)
  def ls(self):
    InodeRootNumber = InodeNumber(RawBlocks, self.cwd)
    InodeRootNumber.InodeNumberToInode()
    InodeRoot = InodeRootNumber.inode
    InodeRootBlocks = InodeRoot.block_numbers
    for blocknumber in InodeRootBlocks:
      if (blocknumber == 0):
        continue
      block = RawBlocks.Get(blocknumber)
      for i in range(0, FILE_ENTRIES_PER_DATA_BLOCK):
        start = i * FILE_NAME_DIRENTRY_SIZE
        filename = block[start:start + MAX_FILENAME].decode()
        print("\n" + filename)

  # implements cat (print file contents)
  def cat(self, filename):
    # your code here
    i = self.FileObject.Lookup(filename,self.cwd)
    if i == -1:
      print("Error: not found\n")
      return -1
    print(self.FileObject.Read(i,0,MAX_FILE_SIZE))

  # functions added to answer question 1
  def printInode(self,i):
    logging.debug('\n Inode Number: ' + str(i))
    InodeNumbervar = InodeNumber(RawBlocks, i)
    InodeNumbervar.InodeNumberToInode()
    InodeNumbervar.inode.Print()

  def getinode(self, num):
    fileinodenum = InodeNumber(RawBlocks, num)
    fileinodenum.InodeNumberToInode()
    return fileinodenum

  def printDirectory(self, num):
    InodeRootNumber = InodeNumber(RawBlocks,num)
    InodeRootNumber.InodeNumberToInode()
    InodeRoot = InodeRootNumber.inode
    InodeRootBlocks = InodeRoot.block_numbers
    for blocknumber in InodeRootBlocks:
      if (blocknumber == 0) :
        continue
      print("Printing Inode: " + str(num))
      block = RawBlocks.Get(blocknumber)
      for i in range(0,FILE_ENTRIES_PER_DATA_BLOCK):
        start = i*FILE_NAME_DIRENTRY_SIZE
        filename = block[start:start + MAX_FILENAME].decode()
        fileinode = self.getinode(int(block[start + MAX_FILENAME:start + FILE_NAME_DIRENTRY_SIZE].hex(), 16))
        print("\n Name: " + filename + " Type: " + str(fileinode.inode.type) + " Inode Number: " + str(fileinode.inode_number))

  def printContent(self, num):
    print(self.FileObject.Read(num, 0, MAX_FILE_SIZE))

  def Interpreter(self):
    while (True):
      command = input("[cwd=" + str(self.cwd) + "]:")
      splitcmd = command.split()
      if splitcmd[0] == "cd":
        if len(splitcmd) != 2:
          print ("Error: cd requires one argument")
        else:
          self.cd(splitcmd[1])
      elif splitcmd[0] == "cat":
        if len(splitcmd) != 2:
          print ("Error: cat requires one argument")
        else:
          self.cat(splitcmd[1])
      elif splitcmd[0] == "ls":
        self.ls()
      elif splitcmd[0] == "exit":
        return
      else:
        print ("command " + splitcmd[0] + "not valid.\n")


if __name__ == "__main__":

  # Initialize file for logging
  # Changer logging level to INFO to remove debugging messages
  logging.basicConfig(filename='memoryfs.log', filemode='w', level=logging.DEBUG)

  # Replace with your UUID, encoded as a byte array
  UUID = b'\x12\x34\x56\x78'

  # Initialize file system data
  logging.info('Initializing data structures...')
  RawBlocks = DiskBlocks()
  # Load blocks from dump file
  RawBlocks.InitializeBlocks(False,UUID)

  # Show file system information and contents of first few blocks
  RawBlocks.PrintFSInfo()
  RawBlocks.PrintBlocks("Initialized",0,16)

  # Initialize FileObject inode
  FileObject = FileName(RawBlocks)

  myshell = FSShell(FileObject)
  myshell.printContent(13)
  myshell.Interpreter()

