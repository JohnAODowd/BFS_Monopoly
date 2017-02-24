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


def roll_dice(verbose = False):
	MAX_HEX = 42949672.95  # 'FFFFFFFF' in dec

	client_range = 6  # 6-sided dice {0...5}

	# TODO make these seeds functional 
	client_seed = uuid.uuid4().hex
	server_seed = uuid.uuid4().hex
	secret_seed = uuid.uuid4().hex

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
		print
		print(str(perc))
		print(str(result))

	return result

def double_roll():
	first_roll = roll_dice()
	second_roll = roll_dice()
	result = first_roll + second_roll
	double = False
	if ((result % 2) == 0):
		double = (first_roll == second_roll)
	return result, double

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
