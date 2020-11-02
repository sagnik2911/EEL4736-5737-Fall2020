import pickle, logging

from memoryfs_client import *

## This class implements an interactive shell to navigate the file system

class FSShell():
  def __init__(self, file):
    # cwd stored the inode of the current working directory
    # we start in the root directory
    self.cwd = 0
    self.FileObject = file

  # implements cd (change directory)
  def cd(self, dir):
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    i = self.FileObject.GeneralPathToInodeNumber(dir,self.cwd)
    if i == -1:
      print ("Error: not found\n")
      return -1
    inobj = InodeNumber(self.FileObject.RawBlocks,i)
    inobj.InodeNumberToInode()
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    if inobj.inode.type != INODE_TYPE_DIR:
      print ("Error: not a directory\n")
      return -1
    self.cwd = i

  # implements ls (lists files in directory)
  def ls(self):
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    inobj = InodeNumber(self.FileObject.RawBlocks, self.cwd)
    inobj.InodeNumberToInode()
    block_index = 0
    while block_index <= (inobj.inode.size // BLOCK_SIZE):
      block = self.FileObject.RawBlocks.Get(inobj.inode.block_numbers[block_index])
      if block_index == (inobj.inode.size // BLOCK_SIZE):
        end_position = inobj.inode.size % BLOCK_SIZE
      else:
        end_position = BLOCK_SIZE
      current_position = 0
      while current_position < end_position:
        entryname = block[current_position:current_position+MAX_FILENAME]
        entryinode = block[current_position+MAX_FILENAME:current_position+FILE_NAME_DIRENTRY_SIZE]
        entryinodenumber = int.from_bytes(entryinode, byteorder='big')
        inobj2 = InodeNumber(self.FileObject.RawBlocks, entryinodenumber)
        inobj2.InodeNumberToInode()
        if inobj2.inode.type == INODE_TYPE_DIR:
          print ("["+ str(inobj2.inode.refcnt) +"]:"+entryname.decode() + "/")
        else:
          print ("["+ str(inobj2.inode.refcnt) +"]:"+entryname.decode())
        current_position += FILE_NAME_DIRENTRY_SIZE
      block_index += 1
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    return 0

  # implements cat (print file contents)
  def cat(self, filename):
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    i = self.FileObject.Lookup(filename, self.cwd)
    if i == -1:
      print ("Error: not found\n")
      return -1
    inobj = InodeNumber(self.FileObject.RawBlocks,i)
    inobj.InodeNumberToInode()
    if inobj.inode.type != INODE_TYPE_FILE:
      print ("Error: not a file\n")
      return -1
    data = self.FileObject.Read(i, 0, MAX_FILE_SIZE)
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    print (data.decode())
    return 0

  # implements ln (link target to name)
  def ln(self, target, linkname):
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    res = self.FileObject.Link(target,linkname,self.cwd)
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    if res == -1 :
      print("Error: Specified name to link to is a directory type\n")
      return -1
    elif res == -2:
      print("Error: Specified name already exist in current directory\n")
      return -1
    elif res == -3:
      print("Error: Specified target is not a file\n")
      return -1
    return 0

  # implements ln (link target to name)
  def append(self, filename, string):
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    i = self.FileObject.Lookup(filename,self.cwd)
    if i == -1:
      print("Error: File not found\n")
      return -1
    inobj = InodeNumber(self.FileObject.RawBlocks, i)
    inobj.InodeNumberToInode()
    count = self.FileObject.Write(i, inobj.inode.size, bytearray(string, 'utf-8'))
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    if count == -1:
      print("Error: String could not be appended\n")
      return -1
    print("Bytes Written: " + str(count) + "\n")
    return 0

  # implement mkdir (create directory under current working directory)
  def mkdir(self, dirname):
    if "/" in dirname:
      print("Error: Specified name contains Slash\n")
      return -1
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    i = self.FileObject.Create(self.cwd,dirname,INODE_TYPE_DIR)
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    if ( i == -1):
      print("Error: Couldn't create a directory. Check log for reason.\n")
    return 0

    # implement create (create file under current working directory)
  def create(self, filename):
    if "/" in filename:
      print("Error: Not a valid filename\n")
      return -1
    logging.debug("Acquiring Lock")
    self.FileObject.RawBlocks.Acquire(RSM_BLOCK_NUM)
    i = self.FileObject.Create(self.cwd, filename, INODE_TYPE_FILE)
    logging.debug("Releasing Lock")
    self.FileObject.RawBlocks.Release(RSM_BLOCK_NUM)
    if (i == -1):
      print("Error: Couldn't create a file. Check log for reason.\n")
    return 0

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
      elif splitcmd[0] == "ln":
        if len(splitcmd) != 3:
          print("Error: ln requires two arguments")
        else:
          self.ln(splitcmd[1],splitcmd[2])
      elif splitcmd[0] == "append":
        if len(splitcmd) != 3:
          print("Error: append requires two arguments")
        else:
          self.append(splitcmd[1],splitcmd[2])
      elif splitcmd[0] == "mkdir":
        if len(splitcmd) != 2:
          print("Error: mkdir requires two arguments")
        else:
          self.mkdir(splitcmd[1])
      elif splitcmd[0] == "create":
        if len(splitcmd) != 2:
          print("Error: create requires two arguments")
        else:
          self.create(splitcmd[1])
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
  myshell.Interpreter()
