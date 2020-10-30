import xmlrpc.client

putdata1 = bytearray(b'\x12\x34\x56\x78')
putdata2 = bytearray(b'\x9a\xbb\xde\xf0')

s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)
print(s.put("key1",putdata1))  
print(s.put("key2",putdata2))  
value1 = s.get("key1")  
value2 = s.get("key2")  
print(str(putdata1.hex()))
print(str(value1.hex()))
print(str(putdata2.hex()))
print(str(value2.hex()))

