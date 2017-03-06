import hashlib
import uuid
from math import ceil

"""
Provably Fair Dice
==================
Monopoly Usage:
def getRoll():
	return ( result, isDouble = dice.double_roll() )
"""


def roll_dice(range=6, verbose = False):
	MAX_HEX = 42949672.95  # 'FFFFFFFF' in dec

	client_range = range  # 6-sided dice {0...5}

	# TODO make these seeds functional 
	client_seed = uuid.uuid4().hex.encode("utf-8")
	server_seed = uuid.uuid4().hex.encode("utf-8")
	secret_seed = uuid.uuid4().hex.encode("utf-8")

	# Create sha256 of seeds 
	hash_object = hashlib.sha256((secret_seed + server_seed + client_seed))
	hex_digest = hash_object.hexdigest()

	# Convert first 8 chars to DEC
	dec_digest = int(hex_digest[:8], 16)

	perc = dec_digest / MAX_HEX
	result = client_range * ( perc / 100 )
	result = int(ceil( result ))

	if (verbose):
		print('Client: ' + client_seed)
		print('Server: ' + server_seed)
		print('Secret: ' + secret_seed)
		print(str(perc))
		print(str(result))

	return result

def double_roll():
	ret 				= {}
	# ret['firstRoll']	= roll_dice()
	# ret['secondRoll']	= roll_dice()
	ret['firstRoll']	= 4
	ret['secondRoll']	= 2
	ret['value'] 		= ret['firstRoll'] + ret['secondRoll']
	ret['double']		= ret['firstRoll'] == ret['secondRoll']
	return ret


def drawFromDeck(deckSize=16):
	#return roll_dice(deckSize)
	return 0
'''
def test_single(verbose = False):
	results = [0 for x in range(6)]
	for i in range(100):
		results[roll_dice() - 1] += 1

	if (verbose):
		for i in range(len(results)):
			print(str(i+1) + " : " + str(results[i]) + " " + ("=" * results[i]))
	print(results)

def test_double(verbose = False):
	results = [0 for x in range(11)]
	for i in range(420):
		results[double_roll() - 2] += 1

	if (verbose):
		for i in range(len(results)):
			print(str(i+2) + " : " + str(results[i]) + " " + ("=" * results[i]))
	print(results)
'''

if __name__ == '__main__':
	double_roll()
	#test_double()
	#double_roll()
	#roll_dice()
	#roll_dice(verbose = True)
