from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from memoryfs_client import BLOCK_SIZE,TOTAL_NUM_BLOCKS

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


if __name__ == "__main__":
  block = []
  for i in range(0,TOTAL_NUM_BLOCKS):
    block.insert(i,bytearray(BLOCK_SIZE))

  # Create server
  server = SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler)

  def Put(block_number,value):
    block[block_number] = value
    return 0

  server.register_function(Put, 'Put')

  def Get(block_number):
    return block[block_number]

  server.register_function(Get, 'Get')

  def ReadSetBlock(block_number, data):
    r = block[block_number]
    block[block_number] = data
    return r

  server.register_function(ReadSetBlock, 'RSB')

  # Run the server's main loop
  server.serve_forever()

