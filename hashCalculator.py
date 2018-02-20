#!/usr/bin/python

from binascii import unhexlify
from hashlib import sha256
import json
import urllib2
import sys

#convert into little endian format
def littleEndian(string):
	splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
	splited.reverse()
	return "".join(splited)

helpMessage = 'Please give arguments to read the block data\nTo read the block as a json file\n-f <fileName>\nTo read the block from a url as a json body\n-i <url>\n'

if (len(sys.argv) < 3):
	print helpMessage
	sys.exit()
elif sys.argv[1] == '-f':
	response = json.load(open(sys.argv[2]))
elif sys.argv[1] == '-i':
	response = json.loads(urllib2.urlopen(sys.argv[2]).read())

version = '01000000'
little_endian_previousHash = littleEndian(response['prev_block'])
little_endian_merkleRoot = littleEndian(response['mrkl_root'])
little_endian_time = littleEndian(hex(response['time'])[2:])
little_endian_difficultyBits = littleEndian(hex(response['bits'])[2:])
little_endian_nonce = littleEndian(hex(response['nonce'])[2:])

#append
header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce

header = unhexlify(header)
#sent hash by the miner
Responsehash = littleEndian(response['hash'])
#calculated hash
CalculatedHash = sha256(sha256(header).digest()).hexdigest()

#verify the hash is smaller than the target
solved = 'Hash is smaller than the target' if Responsehash <= little_endian_difficultyBits else 'Hash is larger than the target'
print solved
#Equality of the calculated and received hashes
state = 'Hash of the block is acceptable.' if Responsehash == CalculatedHash else 'Hash of the block is not acceptable.'
print state

