import pickle, logging

from memoryfs import *

if __name__ == "__main__":

  # Initialize file for logging
  # Changer logging level to INFO to remove debugging messages
  logging.basicConfig(filename='memoryfs.log', filemode='w', level=logging.DEBUG)

  # Replace with your UUID, encoded as a byte array
  UUID = b'\x12\x34\x56\x79'

  # Initialize file system data
  logging.info('Initializing data structures...')
  RawBlocks = DiskBlocks()
  RawBlocks.InitializeBlocks(True,UUID)

  # Show file system information and contents of first few blocks
  RawBlocks.PrintFSInfo()
  RawBlocks.PrintBlocks("Initialized",0,16)

  # Initialize root inode
  file = FileName(RawBlocks)
  file.InitRootInode()

  i1 = file.Create(0, "epl", INODE_TYPE_DIR)
  i2 = file.Create(0, "laliga", INODE_TYPE_DIR)
  i3 = file.Create(0, "seriea", INODE_TYPE_DIR)
  i4 = file.Create(0, "rules.txt", INODE_TYPE_FILE)
  i5 = file.Create(0, "referee.txt", INODE_TYPE_FILE)
  i6 = file.Create(0, "alloc.txt", INODE_TYPE_FILE)
  i7 = file.Create(i1, "pool.txt", INODE_TYPE_FILE)
  i8 = file.Create(i1, "mancity.txt", INODE_TYPE_FILE)
  i9 = file.Create(i2, "rmadrid.txt", INODE_TYPE_FILE)
  i10 = file.Create(i3, "juventus.txt", INODE_TYPE_FILE)
  i11 = file.Create(i3, "inter.txt", INODE_TYPE_FILE)
  i12 = file.Create(i2, "segunda", INODE_TYPE_DIR)
  i13 = file.Create(i12, "castilla.txt", INODE_TYPE_FILE)

  print ('Lookup (epl,0) = ' + str(file.Lookup('epl',0)))
  print ('Lookup (laliga,0) = ' + str(file.Lookup('laliga',0)))
  print ('Lookup (seriea,0) = ' + str(file.Lookup('seriea',0)))
  print ('Lookup (ligue1,0) = ' + str(file.Lookup('ligue1',0)))
  print ('Lookup (rules.txt,0) = ' + str(file.Lookup('rules.txt',0)))
  print ('Lookup (referee.txt,0) = ' + str(file.Lookup('referee.txt',0)))
  print ('Lookup (allocation.txt,0) = ' + str(file.Lookup('alloc.txt',0)))
  print ('Lookup (liverpool.txt,0) = ' + str(file.Lookup('pool.txt',i1)))
  print ('Lookup (mancity.txt,i1) = ' + str(file.Lookup('mancity.txt',i1)))
  print ('Lookup (realmadrid.txt,i2) = ' + str(file.Lookup('rmadrid.txt',i2)))
  print ('Lookup (juventus.txt,i3) = ' + str(file.Lookup('juventus.txt',i3)))
  print ('Lookup (inter.txt,i3) = ' + str(file.Lookup('inter.txt',i3)))
  print ('Lookup (second devision,i2) = ' + str(file.Lookup('segunda',i2)))
  print ('Lookup (castilla.txt,i12) = ' + str(file.Lookup('castilla.txt',i12)))

  f = file.Lookup('inter.txt',i3)
  data = bytearray("Contents of inter.txt.","utf-8")
  offset = file.Write(f, 0, data)
  data2 = bytearray("Conte has improved the side.","utf-8")
  file.Write(f, offset, data2)

  f2 = file.Lookup('rmadrid.txt',i2)
  data3 = bytearray("Contents of rmadrid.txt","utf-8")
  offset = file.Write(f2, 0, data3)
  data3 = bytearray("The greatest football club in history.","utf-8")
  file.Write(f2,offset,data3)

  f4 = file.Lookup('rules.txt',0)
  data5 = bytearray("5 substitues allowed in 3 phases","utf-8")
  file.Write(f4, 0, data5)

  read1 = file.Read(f4,0,256)
  print ('read1: ' + str(read1))

  RawBlocks.PrintBlocks("End",0,32)
  RawBlocks.DumpToDisk(UUID)


