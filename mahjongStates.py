from pythonMahjong import *
from MahjongFunctions import *
from statemachine import StateMachine

##########################################################################
'''INITIALISATION'''
# importing winning combinations
localWinningCombinations = winningCombinations

# Creating user objects
User1 = User('User1')
User2 = User('User2')

# Creating 3 tiles for user 1
Tile1_1 = Tile('down')
Tile1_2 = Tile('up')
Tile1_3 = Tile('up')
User1.tiles = [Tile1_1, Tile1_2, Tile1_3]

# Creating 3 tiles for user 2
Tile2_1 = Tile('down')
Tile2_2 = Tile('down')
Tile2_3 = Tile('down')
User2.tiles = [Tile2_1, Tile2_2, Tile2_3]

# Generating list of tiles.
listOfTiles = randomTileGen(100)

# Assigning tiles to the three tile objects in each user object.
for i in User1.tiles:
    i.whoami = listOfTiles[0]
    listOfTiles.remove(listOfTiles[0])
    print i.whoami

for j in User2.tiles:
    j.whoami = listOfTiles[0]
    listOfTiles.remove(listOfTiles[0])
    print j.whoami

##########################################################################
# ASSUMING THAT P1 IS USER 1.
'''
HOW THE SM WORKS:
INPUT: LIST WITH 7 ELEMENTS
pass in list with format: 6 tiles, 1 state
First 3 are p1's
Last 3 are p2's
Next states:
-game_started
-p1_turn_start
-p2_turn_start
-p1_turn_end
-p2_turn_end
-p1_win
-p2_win
-end_game
'''


def game_started(inpList):
    # Separating orientation of tiles of P1 and P2
    orientationP1 = []
    orientationP2 = []
    for i in range(0, 3):
        orientationP1.append(inpList[i].orientation)
    for j in range(3, 6):
        orientationP2.append(inpList[j].orientation)

# Now if all tiles orientation is down, start game.
# Else, error

    if (orientationP1.count('up') == 2 and orientationP1.count('down') == 1 and
            orientationP2.count('down') == 3):
        newState = 'p1TurnStart'

    else:
        newState = 'Out of range'
        print 'Error!'

    return(newState, inpList)


def p1_turn_start(inpList):

    # UPDATE TILE VALUES HERE. RUN WHILE LOOP UNTIL YOU GET ALL 3 UP. UPDATE
    # INPLIST

    # Creating 3 tiles for user 1
    Tile1_1 = Tile('up')
    Tile1_2 = Tile('up')
    Tile1_3 = Tile('up')
    User1.tiles = [Tile1_1, Tile1_2, Tile1_3]

    # Creating 3 tiles for user 2
    Tile2_1 = Tile('down')
    Tile2_2 = Tile('down')
    Tile2_3 = Tile('down')
    User2.tiles = [Tile2_1, Tile2_2, Tile2_3]

    inpList = []
    inpList.extend(User1.tiles)
    inpList.extend(User2.tiles)

    orientationP1 = []
    orientationP2 = []
    listTilesP1 = []

    for i in range(0, 3):
        orientationP1.append(inpList[i].orientation)
    for j in range(3, 6):
        orientationP2.append(inpList[j].orientation)

    for i in range(0, 3):
        listTilesP1.append(inpList[i].whoami)

    # Now, if all tiles of p1 are up, it means that it must go to p1_turn_end
    if(orientationP1.count('up') == 3):
        print 'going to p1END'
        newState = 'p1TurnEnd'

    # Check if p1 has won:
    if(listTilesP1 in localWinningCombinations):
        print 'p1 win state'
        newState = 'p1Win'

    # Else, stay in same state
    else:
        newState = 'p1TurnStart'

    return(newState, inpList)


def p1_turn_end(inpList):
    orientationP1 = []
    orientationP2 = []
    listTilesP1 = []

    # Creating 3 tiles for user 1
    Tile1_1 = Tile('up')
    Tile1_2 = Tile('down')
    Tile1_3 = Tile('up')
    User1.tiles = [Tile1_1, Tile1_2, Tile1_3]

    # Creating 3 tiles for user 2
    Tile2_1 = Tile('down')
    Tile2_2 = Tile('down')
    Tile2_3 = Tile('down')
    User2.tiles = [Tile2_1, Tile2_2, Tile2_3]

    inpList = []
    inpList.extend(User1.tiles)
    inpList.extend(User2.tiles)

    for i in range(0, 3):
        orientationP1.append(inpList[i].orientation)
    for j in range(3, 6):
        orientationP2.append(inpList[j].orientation)

    for i in range(0, 3):
        listTilesP1.append(inpList[i].whoami)

    if (orientationP1.count('up') == 2):
        print 'p2 turn'
        newState = 'p2TurnStart'

    else:
        newState = 'p1TurnEnd'

    return (newState, inpList)


def p2_turn_start(inpList):
    # UPDATE TILE VALUES HERE. RUN WHILE LOOP UNTIL YOU GET ALL 3 UP. UPDATE
    # INPLIST

    # Creating 3 tiles for user 1
    Tile1_1 = Tile('up')
    Tile1_2 = Tile('down')
    Tile1_3 = Tile('up')
    User1.tiles = [Tile1_1, Tile1_2, Tile1_3]

    # Creating 3 tiles for user 2
    Tile2_1 = Tile('up', 'circle_1')
    Tile2_2 = Tile('up', 'circle_2')
    Tile2_3 = Tile('up', 'circle_3')
    User2.tiles = [Tile2_1, Tile2_2, Tile2_3]

    inpList = []
    inpList.extend(User1.tiles)
    inpList.extend(User2.tiles)

    orientationP1 = []
    orientationP2 = []
    listTilesP2 = []

    for i in range(0, 3):
        orientationP1.append(inpList[i].orientation)
    for j in range(3, 6):
        orientationP2.append(inpList[j].orientation)

    for i in range(3, 6):
        listTilesP2.append(inpList[i].whoami)

    # Now, if all tiles of p1 are up, it means that it must go to p1_turn_end
    if(orientationP2.count('up') == 3):
        print 'p2 turn end'
        newState = 'p2TurnEnd'

    # Check if p1 has won:
    if(listTilesP2 in localWinningCombinations):
        print 'p2 win'
        newState = 'p2Win'

    # Else, stay in same state
    else:
        newState = 'p2TurnStart'

    return(newState, inpList)


def p2_turn_end(inpList):
    orientationP1 = []
    orientationP2 = []

    for i in range(0, 3):
        orientationP1.append(inpList[i].orientation)
    for j in range(3, 6):
        orientationP2.append(inpList[j].orientation)

    if (orientationP2.count('up') == 2):
        newState = 'p1_turn_start'

    else:
        newState = 'p2_turn_end'

    return(newState, inpList)


def p1_win(inpList):
    print 'player 1 wins!'
    newState = 'game_end'

    return(newState, inpList)


def p2_win(inpList):
    print 'player 2 wins!'
    newState = 'game_end'

    return(newState, inpList)


def game_end(inpList):
    print 'End of game!'
    return None


##########################################################################
# Setting up game:
allTiles = []
allTiles.extend(User1.tiles)
allTiles.extend(User2.tiles)

if __name__ == "__main__":
    m = StateMachine()
    m.add_state("GameStarts", game_started)
    m.add_state("p1TurnStart", p1_turn_start)
    m.add_state("p2TurnStart", p2_turn_start)
    m.add_state("p1TurnEnd", p1_turn_end)
    m.add_state("p2TurnEnd", p2_turn_end)
    m.add_state("p1Win", p1_win)
    m.add_state("p2Win", p2_win)
    m.add_state("GameOver", game_end)
    m.add_state("Out of range", None, end_state=1)
    m.set_start("GameStarts")
    m.run(allTiles)
