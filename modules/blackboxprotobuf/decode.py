#! /usr/bin/python
import sys
sys.path.insert(1, './blackboxprotobuf')
sys.path.insert(1, '../../modules/protobuf-3.11.4/python')
import blackboxprotobuf
import pickle

if len(sys.argv) != 2:
  print "Usage:", sys.argv[0], "PROTOBUF FILE TO DECODE"
  sys.exit(-1)

f = open(sys.argv[1], "rb")
data=f.read()
message,typedef = blackboxprotobuf.decode_message(data)
with open('decoded.pickle', 'wb') as handle:
    pickle.dump(message, handle, protocol=pickle.HIGHEST_PROTOCOL)

json,typedef = blackboxprotobuf.protobuf_to_json(data)
print(json)
print(type(json))
f2 = open(sys.argv[1]+'.json', 'w')
f2.write(json)
