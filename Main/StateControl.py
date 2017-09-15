'''
Created on Sep 5, 2014

@author: Thomas
'''
import sys
import Builder
import Player
import jsonpickle

global SAVEGAME_FILENAME
SAVEGAME_FILENAME = 'save.json'

class GameState(object):
    
    def __init__(self):
        self.player = None
        self.areaList = list()
        self.turnCount = 0
        self.introText = ""
        self.returnOnEnter = False
        
    def addArea(self, area):
        self.areaList.append(area)
        
    def removeArea(self, area):
        self.areaList.remove(area)
        
    def addPlayer(self, player):
        self.player = player
    
    def spawnPlayer(self, player):
        self.player.currentLocation = self.areaList[0]

def newGameState():
    state = GameState()
    player = Player.Player()
    state.addPlayer(player)
    Builder.buildWorld(state)
    state.spawnPlayer(player)
    state.returnOnEnter = False
    return state

def newSimulationState():
    state = GameState()
    player = Player.Player()
    state.addPlayer(player)
    Builder.buildCombatSimulator(state)
    state.spawnPlayer(player)
    state.returnOnEnter = False
    return state

def save(state):
    with open(SAVEGAME_FILENAME, 'w') as savegame:
        savegame.write(jsonpickle.encode(state))
    return "Game saved."
    
def loadState():
    with open(SAVEGAME_FILENAME, 'r') as savegame:
        state = jsonpickle.decode(savegame.read())
        state.introText = "Game Loaded"
        return state
    
def quit():
    sys.exit()