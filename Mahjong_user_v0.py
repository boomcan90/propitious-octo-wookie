'''
TODO: 
1. Create a class called user.
Attributes: username
			status- online/offline
			game status- inGame, notPlaying(default), startGame
			turn status- true, false
			tiles - true, false
			winning- true, false

2. Find out how to get and send commands to android.
3. Integrate with algo file
'''

class User:
	onlineStatus = false
	tiles = false
	gameStatus = null
	winning = null 
	turnStatus = null 

	def __init__(self, username, status):
		self.username = username
		self.status = status

	def isOnline(self, status):
		return self.status
