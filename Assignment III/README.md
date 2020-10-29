In this design+implementation assignment, you will further extend the in-memory file system, as described below. You may start from the Python files you extended in the previous assignment, or from the solutions.

 

## What to turn in on Canvas ##

- A file HW3.pdf with a brief description of your design

- A file memoryfs_client.py

- A file memoryfs_server.py

- A file memoryfs_shell_rpc.py

 

## Design/implementation ##

In this assignment, you will modify the file system to implement a client/server model, using XMLRPC (an RPC library available for Python). The key idea is to separate your system into a block server (which implements the raw block layer, and exposes Get() and Put() interfaces), and a file system client (which implements the layers above). You will also modify the shell code to support single-writer operations and ensure that it works with this implementation.

 

1) Block server (memoryfs_server.py)

The block server holds the file system data - think of it as implementing the raw disk (which in previous assignments was in the DiskBlocks() object) that exposes Put/Get interfaces over RPC. Your implementation must initialize with zero-filled blocks at startup

The main RPC function you must implement and expose is ReadSetBlock(), as described in 3). Get() and Put() are provided to you. Their behavior is as follows:

Get(block_number) returns a block, given its number

Put(block_number, data) writes a block, given its number and data contents

ReadSetBlock(block_number, data) reads a block, sets the block contents to a LOCKED value, and returns the block read. Equivalent of an RSM, using a disk block to hold a lock

 

Hints about XMLRPC - refer to the provided skeleton code as a starting point:

- these imports and class are needed to run an xmlrpc server:

from xmlrpc.server import SimpleXMLRPCServer

from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):

  rpc_paths = ('/RPC2',)

 

- to create a server object, listening on port 8000:

server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)

 

- once you define a function, you can register and expose an RPC function as follows:

  server.register_function(Add)

 

- the server's main loop, which waits for requests and dispatches functions, is invoked as follows. It's easier to run the server and client shell in different terminal windows. You can terminate the server loop in its terminal window with CTRL+C

  # Run the server's main loop

  server.serve_forever()

 

2) File system client (memoryfs_client.py)

Here, the key insight is that you should replace the Get() and Put() primitives that previously stored to memory in your monolithic program, to Get() and Put() RPC calls to the server. Once you properly implement Get() and Put(), all the functionality that we have implemented thus far (inodes, files, etc) should work, unmodified - except now Puts and Gets go across the network

 

Hint: Before changing your memoryfs_client.py, try to write a simple client to test Get()/Put() calls. To access the RPC client functionality, you can use:

self.block_server = xmlrpc.client.ServerProxy(server_url, use_builtin_types=True)

Where server_url should be 'http://localhost:8000' to connect to the local host server above

 

Hint: xmlrpc will return a data block as type "Bytes" for a Get() RPC call - ensure you convert it to bytearray in your client-side implementation of Get() before returning, e.g. return bytearray(rpc_return_value)

 

3) File system shell

Consider the possibility that there might be multiple clients connected to the same block server.

 

- In your design document, explain what kind of race conditions can occur with the operations supported by the shell

- Design and implement an approach that prevents race conditions by implementing a lock. For simplicity, your lock implementation may be coarse-grained, such that the lock obtained by a client guarantees it is a single-writer while it holds the lock

- Describe how you tested your design: how you observed one race condition, and how it was prevented using the lock. You only need to describe how you forced one race condition that leads to incorrect behavior as an example, but your design should prevent all race conditions

- [EEL5737 students only] Describe (there's not need to implement) how in your design you could keep track of access/modification times of files, and how that information could be used to support a client-side cache

Hint: You will need to bootstrap an equivalent of RSM for a disk block on the server code - the ReadSetBlock() method as described above. You may allocate a well-known block to serve as a lock - since the boot block is unused, it is ok to use it for this purpose. The server is single-threaded

 

Hint: race conditions are tricky to test; you can artificially delay a multi-step operation in a client by strategically placing a time.sleep() method call in memoryfs_client.py

 

Hint: You will also need to adjust the file system shell so it imports and initializes your new client implementation properly - you should only need minor changes for that:

 

from memoryfs_client import *

RawBlocks = DiskBlocks('http://localhost:8000')