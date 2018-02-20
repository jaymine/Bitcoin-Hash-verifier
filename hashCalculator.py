from binascii import unhexlify
from hashlib import sha256
import json
import urllib2

def littleEndian(string):
	splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
	splited.reverse()
	return "".join(splited)

#change the response value to json or change the url to import json
response = json.loads(urllib2.urlopen("http://webbtc.com/block/0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449.json").read())

version = '01000000'
little_endian_previousHash = littleEndian(response['prev_block'])
little_endian_merkleRoot = littleEndian(response['mrkl_root'])
little_endian_time = littleEndian(hex(response['time'])[2:])
little_endian_difficultyBits = littleEndian(hex(response['bits'])[2:])
little_endian_nonce = littleEndian(hex(response['nonce'])[2:])

header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce
header = unhexlify(header)

Responsehash = littleEndian(response['hash'])
CalculatedHash = sha256(sha256(header).digest()).hexdigest()

state = 'Hash of the block is acceptable.' if Responsehash == CalculatedHash else 'Hash of the block is not acceptable.'
print state
