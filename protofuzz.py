#!/usr/bin/env python
import argparse
import asyncio
import sys
sys.path.insert(1, './modules')
import websockets
import ssl
import re
import pickle
import os
import json

##Take wordlist from cmd
parser = argparse.ArgumentParser(description='Websocket fuzzer with protobuff support. Requires Python ≥ 3.7 and python 2.7. See readme for details')
parser.add_argument('wordlist', type=argparse.FileType('r'), help='Wordlist to parse')
parser.add_argument('URI', type=str, help='websocket URI')
parser.add_argument('inputfile', type=argparse.FileType('r'), help='Payload to send, will fuzz everything between "`" characters')
parser.add_argument('-x', action='store_true', help='Payload is protobuf')
parser.add_argument('-p', nargs=1, type=argparse.FileType('r'), help='Request to send before fuzzing')
args = parser.parse_args()

#print(args.wordlist.readlines())
#print(args.x)
#print(args.inputfile.name)
#import pdb; pdb.set_trace() 
#
#if args.p is not None:
#	prereq = ''.join(map(str, args.p[0].readlines()))
#	print("set")
#else:
#	print("not set")

if args.p is not None:
	prereq = ''.join(map(str, args.p[0].readlines()))
else:
	prereq = None

def request(payload):
	encryption = "wss://" in args.URI

	if encryption == False:
		async def hello():
			uri = args.URI
			async with websockets.connect(uri) as websocket:
				name = payload
				if prereq is not None:
					await websocket.send(prereq)
					await websocket.recv()
				await websocket.send(name)
				print(f"> {name}")

				response = await websocket.recv()
				print(f"< {response}")

		asyncio.get_event_loop().run_until_complete(hello())
	else:
		ssl_context = ssl.create_default_context()
		ssl_context.check_hostname = False
		ssl_context.verify_mode = ssl.CERT_NONE

		async def hello():
			uri = args.URI
			async with websockets.connect(
				uri, ssl=ssl_context
			) as websocket:
				name = payload
				if prereq is not None:
					await websocket.send(prereq)
					await websocket.recv()
				await websocket.send(name)
				print(f"> {name}")

				#response = await websocket.recv()
				#print(f"< {response}")	

		asyncio.get_event_loop().run_until_complete(hello())



if args.x == False:

	payload = ''.join(map(str, args.inputfile.readlines()))
	with open('%s' %(args.wordlist.name)) as f:
		wordlist = [word.strip() for word in f]
	print(wordlist)
	p = re.compile('`.*`')
	for i in wordlist:
		try:
			request(p.sub(i, payload))
		except:
			pass
else:
	#lot of weird shit due to mixing pyenv, python2 and python3, solution would be to rewrite lib for py3 
	path = os.popen('pwd').read().rstrip()
	os.chdir('%s/modules/blackboxprotobuf' %(path))
	os.system('./decode.py ../../%s' %(args.inputfile.name))
	os.chdir('%s' %(path))
	


#	with open('modules/blackboxprotobuf/decoded.pickle', 'rb') as handle:
#		decoded = pickle.load(handle)

#	os.system('./decodebin.sh %s' %(args.inputfile.name))





	def encode(payload):
		os.chdir('%s/modules/blackboxprotobuf' %(path))
		with open('payload.pickle', 'wb') as handle:
			pickle.dump(payload, handle, protocol=1)
		with open('filename.pickle', 'wb') as handle:
			pickle.dump(args.inputfile.name, handle, protocol=1)
		os.system('./encode.py')
		#f = open('final.pickle', 'r')
		#final=f.read()
		with open('final.pickle', 'rb') as handle:
			final = pickle.load(handle)
		os.chdir('%s' %(path))
		return final

	os.system('./decodebin.sh %s' %(args.inputfile.name))
	f = open(args.inputfile.name + '.json', 'r')
	jstring=f.read()
	with open('%s' %(args.wordlist.name)) as f:
		wordlist = [word.strip() for word in f]
	p = re.compile('`.*`')
	for i in wordlist:
		print(p.sub(i, jstring))
		fuzzed = p.sub(i, jstring)
		for row in fuzzed:
			try:
				global jdic 
				jdic=json.loads(fuzzed)
			except: 
				pass
		final=bytes(encode(jdic))
		request(final)

	#jdic=json.loads(jstring)
#	print(jdic)
#	print(type(jdic))
	#payload=jdic
	#final=bytes(encode(payload))
	#request(final)

