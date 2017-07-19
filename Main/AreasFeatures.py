'''
Created on Jun 29, 2014

@author: Thomas
'''
class Area(object):
    
    def __init__(self, name, description, idNum=0):
        self.name = name
        self.description = description
        self.idNum = idNum
        self.visited = False
        self.roomState = 0
        self.connectedAreas = {}
        self.features = {}
        self.itemsContained = {}
        self.enemies = {}
        self.NPCs = {}
        
    def lookAt(self):
        desc = self.name
        desc += "\n" + self.description[self.roomState]
        if self.itemsContained:
            for item in self.itemsContained.itervalues():    #Display all the visible items
                if item.accessible:
                    if item.firstSeen and item.initSeenDesc:
                        desc += "\n" + item.initSeenDesc
                    elif item.firstTaken and item.notTakenDesc:
                        desc += "\n" + item.notTakenDesc
                    else:
                        desc += "\n" + item.seenDescription
                    item.firstSeen = False
        if self.NPCs or self.enemies:
            desc += "\n"
        if self.NPCs:
            for NPC in self.NPCs.itervalues():                  #Display all the NPCs
                desc += NPC.seenDescription
        if self.enemies:
            for enemy in self.enemies.itervalues():         #Display all the enemies
                desc += enemy.seenDescription
        return desc
        
    def connect(self, area, link):
        link.setDestination(area)
        self.connectedAreas[link.keywords] = link
            
    def disconnect(self, link):
        del self.connectedAreas[link.keywords]
        link.destination = None
    
    def addItem(self, itemToAdd):
        self.itemsContained[itemToAdd.keywords] = itemToAdd
        
    def removeItem(self, itemToRemove):
        del self.itemsContained[itemToRemove.keywords]
        
    def addFeature(self, featureToAdd):
        self.features[featureToAdd.keywords] = featureToAdd
        
    def removeFeature(self, featureToRemove):
        del self.features[featureToRemove.keywords]
        
    def spawnEnemy(self, enemyToSpawn):
        self.enemies[enemyToSpawn.keywords] = enemyToSpawn
        enemyToSpawn.setLocation(self)
        
    def killEnemy(self, enemyToKill):
        del self.enemies[enemyToKill.keywords]
        
    def addEnemy(self, enemyToAdd):
        self.enemies[enemyToAdd.keywords] = enemyToAdd
        enemyToAdd.setLocation(self)
        
    def removeEnemy(self, enemyToRemove):
        del self.enemies[enemyToRemove.keywords]
        
    def addNPC(self, NPCToAdd):
        self.NPCs[NPCToAdd.keywords] = NPCToAdd
        NPCToAdd.addToLocation(self)
        
    def removeNPC(self, NPCToRemove):
        del self.NPCs[NPCToRemove.keywords]
        NPCToRemove.removeFromLocation()
         
    def setIdNum(self, number):
        self.idNum = number

class Feature(object):
    
    def __init__(self, description, keywords, idNum=0):
        self.description = description
        self.idNum = idNum
        self.keywords = keywords
        self.state = 0
        
    def lookAt(self):
        return self.description[self.state]
    
    def get(self, holder, player):
        return "That isn't something I can pick up."
    
    def setIdNum(self, number):
        self.idNum = number
        
    def setState(self, number):
        self.state = number
        
    def nextState(self):
        self.state += 1
    
class Container(Feature):
    
    def __init__(self, description, keywords, isOpen, isAccessible, blockedDesc, openDesc, closeDesc):
        self.itemsContained = {}
        self.isOpen = isOpen
        self.isAccessible = isAccessible
        self.blockedDesc = blockedDesc
        self.openDesc = openDesc
        self.closeDesc = closeDesc
        super(Container, self).__init__(description, keywords)
        
    def addItem(self, item):
        self.itemsContained[item.keywords] = item
        
    def removeItem(self, item):
        del self.itemsContained[item.keywords]
        
    def lookAt(self):
        desc = self.description
        if self.isOpen:
            desc += " It is open."
            if self.itemsContained:
                desc += " Inside you see:\n"
                for item in self.itemsContained.itervalues():
                    if item.firstSeen and item.initSeenDesc:
                        desc += "\n" + item.initSeenDesc
                    elif item.firstTaken and item.notTakenDesc:
                        desc += "\n" + item.notTakenDesc
                    else:
                        desc += "\n" + item.seenDescription
                    item.firstSeen = False
        else:
            desc += " It is closed."

        return desc
    
    def unlock(self, usedItem):
        return "It does not have a lock."
    
    def open(self, player):
        if not self.isAccessible:
            return self.blockedDesc
        elif self.isOpen:
            return "It is already open."
        else:
            self.isOpen = True
            desc = self.openDesc + " "
            if self.itemsContained:
                desc += "Inside you see:\n"
                for item in self.itemsContained.itervalues():
                    desc += item.seenDescription + "\n"
            else:
                desc += "It appears to be empty."
        return desc,True

    def close(self, player):
        if not self.isOpen:
            return "It is already closed."
        else:
            self.isOpen = False
            return self.closeDesc,True
            
class Link(object):
    
    def __init__(self, description, keywords, isAccessible, blockedDesc, travelDesc):
        self.description = description
        self.keywords = keywords
        self.isAccessible = isAccessible
        self.blockedDesc = blockedDesc
        self.travelDesc = travelDesc
        self.destination = None
        self.siblingLink = None
        
    def lookAt(self):
        return self.description
        
    def travel(self, player):
        if self.isAccessible == False:
            return self.blockedDesc
        
        if player.isRestricted:
            return player.restrictedDesc
        
        desc = self.travelDesc + "\n\n"
        player.currentLocation = self.destination
        if player.currentLocation.visited == False:
            player.currentLocation.visited = True
            desc += player.currentLocation.lookAt()
        return desc,True
            
    def makeSibling(self, sibling):
        self.siblingLink = sibling
        sibling.siblingLink = self
        
    def setDestination(self, area):
        self.destination = area
        
    def setIdNum(self, number):
        self.idNum = number
    
class Door(Link):
    
    def __init__(self, description, keywords, isAccessible, blockedDesc, travelDesc):
        super(Door, self).__init__(description, keywords, isAccessible, blockedDesc, travelDesc)
        
    def lookAt(self):
        desc = self.description
        desc += " It seems to be "
        if self.isAccessible:
            desc += "unlocked."
        else:
            desc += "locked."
        return desc,True
        
    def unlock(self, usedItem):
        return "That door does not have a lock."
    
    def open(self, player):
        return self.travel(player)
    
    def close(self, player):
        return "The door is already closed."