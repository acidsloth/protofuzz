#! /usr/bin/python
import sys
sys.path.insert(1, './blackboxprotobuf')
sys.path.insert(1, '../../modules/protobuf-3.11.4/python')
import blackboxprotobuf
import pickle
import os



def convert(input):
    if isinstance(input, dict):
        return dict((convert(key), convert(value)) for key, value in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    elif isinstance(input, int):
    	return long(input)
    else:
        return input


with open('payload.pickle', 'rb') as handle:
	deserialized = pickle.load(handle)

with open('filename.pickle', 'rb') as handle:
	path = pickle.load(handle)
#	print(path)

#Dirty hack to have a typedef
f = open('../../%s' %(path))
message,typedef = blackboxprotobuf.decode_message(f.read())

#ready=blackboxprotobuf.encode_message(deserialized,typedef)


#toencode,typedef = convert(deserialized)
data = blackboxprotobuf.encode_message(convert(deserialized),typedef)
#print(data)
with open('final.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
