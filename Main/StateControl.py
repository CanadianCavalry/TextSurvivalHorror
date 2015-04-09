'''
Created on Sep 5, 2014

@author: Thomas
'''
import sys
import Builder
import jsonpickle

global SAVEGAME_FILENAME
SAVEGAME_FILENAME = 'save.json'

class GameState(object):
    
    def __init__(self):
        self.player = None
        self.areaList = list()
        self.turnCount = 0
        
    def addArea(self, area):
        self.areaList.append(area)
        
    def removeArea(self, area):
        self.areaList.remove(area)
        
    def addPlayer(self, player):
        self.player = player
        self.player.currentLocation = self.areaList[0]

def newGameState(player):
    state = GameState()
    Builder.buildWorld(state)
    state.addPlayer(player)
    return state

def newSimulationState(player):
    state = GameState()
    Builder.buildAreaOne200(state) #Debug for encounter 1
    #Builder.buildCombatSimulator(state)
    state.addPlayer(player)
    return state

def save(state):
    with open(SAVEGAME_FILENAME, 'w') as savegame:
        savegame.write(jsonpickle.encode(state))
    return "Game saved."
    
def loadState(player=None):
    with open(SAVEGAME_FILENAME, 'r') as savegame:
        state = jsonpickle.decode(savegame.read())
        return state
    
def quit():
    sys.exit()