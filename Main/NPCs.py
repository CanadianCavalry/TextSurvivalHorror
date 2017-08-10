'''
Created on Aug 16, 2014

@author: Thomas
'''
class Dialogue(object):

    def __init__(self, keywords, response):
        self.keywords = keywords
        self.response = response

class NPC(object):
    
    def __init__(self, name, description, seenDesc, talkResponse, keywords):
        self.name = name
        self.description = description
        self.seenDescription = seenDesc
        self.inventory = {}
        self.talkResponse = talkResponse
        self.keywords = keywords
        self.dialogueTree = {}
        self.talkedTo = False
        self.location = None
        self.state = 0
        
    def setTalkResponse(self, response):
        self.talkResponse = response
        
    def addDialogue(self, dialogueToAdd):
        self.dialogueTree[dialogueToAdd.keywords] = dialogueToAdd
        
    def removeDialogue(self, dialogueToRemove):
        if dialogueToRemove.keywords in self.dialogueTree:
            del self.dialogueTree[dialogueToRemove.keywords]
            
    def clearDialogue(self):
        self.dialogueTree = {}
            
    def addToLocation(self, location):
        self.location = location
        
    def removeFromLocation(self):
        self.location = None

    def addItem(self, itemToAdd):
        if itemToAdd.keywords in self.inventory:
            if itemToAdd.stackable:
                self.inventory[itemToAdd.keywords].quantity += itemToAdd.quantity
            else:
                self.inventory[itemToAdd.keywords].quantity += 1
        else:
            self.inventory[itemToAdd.keywords] = itemToAdd
            itemToAdd.currentLocation = self

    def removeItem(self, itemToRemove):
        if (self.inventory[itemToRemove.keywords].quantity > 1) and (not itemToRemove.stackable):
            self.inventory[itemToRemove.keywords].quantity -= 1
        else:
            del self.inventory[itemToRemove.keywords]
            itemToRemove.currentLocation = None

    def dropAllItems(self):
        for key, item in self.inventory.iteritems():
            item.firstTaken = False
            self.location.addItem(item)
        
        self.inventory = {}
            
    def talk(self, player):
        return self.talkResponse
    
    def ask(self, keyword):
        matching = list()
        for key,item in self.dialogueTree.iteritems():
            keyList = key.split(",")
            if keyword in keyList:
                matching.append(item)
                
        if len(matching) == 0:
            return "\"I'm not sure what you're talking about.\"", True
        elif len(matching) > 1:
            return "You'll need to be more specific.", True
        else:
            return matching[0].response, True
                    
    def setIdNum(self, number):
        self.idNum = number
                    
    def lookAt(self):
        return self.description[self.state]