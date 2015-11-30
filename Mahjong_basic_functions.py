import random
import itertools
''' 
Tiles: (16 tiles)
Character suit tiles: (9) 1,2,3,4,5,6,7,8,9
Dragon suit tiles: (3) A,B,C
Wind suit tiles: (4) N,S,E,W
***Add more?
'''

tiles = []
characterTiles = []
dragonTiles = []
windTiles = []
currentTiles = ['N', 'S', 'N']

#character suit: characterTiles, tiles
for i in range(1,10):
	tiles.append(str(i))
	characterTiles.append(str(i))


#dragon suit: dragonTiles, tiles
dragonTiles.append('A')
dragonTiles.append('B')
dragonTiles.append('C')

tiles.append('A')
tiles.append('B')
tiles.append('C')

#wind suit: wind tiles, tiles
windTiles.append('N')
windTiles.append('S')
windTiles.append('E')
windTiles.append('W')

tiles.append('N')
tiles.append('S')
tiles.append('E')
tiles.append('W')


print tiles
print windTiles
print characterTiles
print dragonTiles

winningCombinations = []
for i in tiles:
	winningCombinations.append([i]*3)

print winningCombinations	#to win

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
Make sure that tiles are not repeated.
**necessary?
'''
def randomTileGen(numTiles):
	tilesToGenerate = []
	tilesGenerated = []
	while len(tilesGenerated) != numTiles:
		for i in range(0, numTiles):
				tilesToGenerate.append(random.randint(0, len(tiles)-1))
				generated = tiles[tilesToGenerate[i]]
				if(currentTiles.count(generated) <= 3 and tilesToGenerate.count(generated) <=3):
					tilesGenerated.append(generated)

	return tilesGenerated

print randomTileGen(2)

########################################################

'''
FUNCTION 2: CHECK IF PLAYER HAS WON 
Here, checks if tiles that player has form a winning combination
'''


def hasWon(tiles):
	if(tiles in winningCombinations):
		print "Win!"
	else:
		print "Continue playing"

print hasWon(currentTiles)
