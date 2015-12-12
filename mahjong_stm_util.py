import random
import itertools

'''
TILES:
Number tiles: '1'....'9'
Circle tiles: c1.....c9
Wind suit: N, S, E, W
3 special tiles: Dollar, dragon, TV
'''


tiles = []
numberTiles = []
circleTiles = []
windTiles = []
specialTiles = []

winningComboNumber = []
winningComboCircle = []

#number tiles: 'number'
numberTiles.append('number_1')
numberTiles.append('number_2')
numberTiles.append('number_3')
numberTiles.append('number_4')
numberTiles.append('number_5')
numberTiles.append('number_6')
numberTiles.append('number_7')
numberTiles.append('number_8')
numberTiles.append('number_9')

for i in range(0, len(numberTiles)-2):
	winningComboNumber.append([numberTiles[i], numberTiles[i+1], numberTiles[i+2]])


#circle tiles: 'number_circle'
circleTiles.append('circle_1')
circleTiles.append('circle_2')
circleTiles.append('circle_3')
circleTiles.append('circle_4')
circleTiles.append('circle_5')
circleTiles.append('circle_6')
circleTiles.append('circle_7')
circleTiles.append('circle_8')
circleTiles.append('circle_9')

for i in range(0, len(circleTiles)-2):
	winningComboCircle.append([circleTiles[i], circleTiles[i+1], circleTiles[i+2]])


#special tiles: dragon, dollar and tv
specialTiles.append('dragon')
specialTiles.append('dollar')
specialTiles.append('tv')

#wind tiles:
windTiles.append('north')
windTiles.append('south')
windTiles.append('east')
windTiles.append('west')

tiles.extend(circleTiles)
tiles.extend(numberTiles)
tiles.extend(windTiles)
tiles.extend(specialTiles)

currentTiles = ['north', 'north', 'north']


global winningCombinations
winningCombinations = []
for i in tiles:
	winningCombinations.append([i]*3)

winningCombinations.extend(winningComboNumber)
winningCombinations.extend(winningComboCircle)


#print winningCombinations	#to win

########################################################

'''
Gameplay:
**Assume that both players are ready**
Both player flips up 2 tiles.
turnP1: Draws 1 tile.Flips 1 down (discards it if tiles are not suitable for winning). End of turn
turnP2: Chooses to take the discarded tile or draws a new one. Discards 1 if tiles are not suitable for winning

#TODO:
1. Random tile generator function.
2. Check if a player has won
'''
#########################################################

'''
FUNCTION 1: GENERATES RANDOM TILES
Basically takes a number of tiles to generate(numTiles) and generates them.
Makes sure that tiles generated are in the tiles set.
**tile can repeat 4 times
'''
def randomTileGen(numTiles):
	tilesToGenerate = []
	tilesGenerated = []
	while len(tilesGenerated) != numTiles:
		for i in range(0, numTiles):
				tilesToGenerate.append(random.randint(0, len(tiles)-1))
				generated = tiles[tilesToGenerate[i]]
				if(currentTiles.count(generated) <= 4 and tilesToGenerate.count(generated) <= 4):
					tilesGenerated.append(generated)

	return tilesGenerated

# print randomTileGen(2)

########################################################

'''
FUNCTION 2: CHECK IF PLAYER HAS WON
Here, checks if tiles that player has form a winning combination
'''


def hasWon(tiles):
	if(tiles in winningCombinations):
		return "Win!"
	else:
		return "Continue playing"

# print hasWon(currentTiles)