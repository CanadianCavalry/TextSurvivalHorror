'''
Created on Jun 29, 2014

@author: Thomas
'''
import AreasFeatures

class StandardOpenDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords):
        kwargs = {
            "travelDesc":"You open the door and step through.", 
            "travelSound":"Sounds/Misc/GenericDoor1.mp3"
        }

        super(StandardOpenDoor, self).__init__(description, keywords, True, **kwargs)

class StandardOpenMetalDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords):
        kwargs = {
            "travelDesc":"You open the door and step through.", 
            "travelSound":"Sounds/Misc/HeavyDoor.mp3"
        }

        super(StandardOpenMetalDoor, self).__init__(description, keywords, True, **kwargs)

        
class StandardLockingDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords, isAccessible, keyRequired, itemToOpen, **kwargs):
        self.itemToOpen = itemToOpen
        self.keyRequired = keyRequired

        if not ("unlockDesc" in kwargs):
            self.unlockDesc = "You unlock the door."
        if not ("lockDesc" in kwargs):
            self.lockDesc = "You lock the door."
        if not ("blockedDesc" in kwargs):
            kwargs.update({
                "blockedDesc":"It's locked. It won't budge."
            })
        if not ("travelDesc" in kwargs):
            kwargs.update({
                "travelDesc":"You open the door and step through."
            })

        super(StandardLockingDoor, self).__init__(description, keywords, isAccessible, **kwargs)
        
    def tryUnlock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
        if self.keyRequired:
            if not usedItem:
                return "This door requires a key of some kind."
            if usedItem == self.itemToOpen:
                self.unlock()
            else:    
                return "The key does not appear to work for this door."
        else:
            self.unlock()
        return self.unlockDesc, True

    def unlock(self):
        self.isAccessible = True
        self.siblingLink.isAccessible = True

    def tryLock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
        if self.keyRequired:
            if not usedItem:
                return "This door requires a key of some kind."
            if usedItem == self.itemToOpen:
                self.lock()
            else:    
                return "The key does not appear to work for this door."
        else:
            self.lock()
        return self.lockDesc,True

    def lock(self):
        self.isAccessible = False
        self.siblingLink.isAccessible = False

class StandardKeylessDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords, isAccessible, **kwargs):

        kwargs.update({
            "blockedDesc":"It's locked. It won't budge."
        })

        super(StandardKeylessDoor, self).__init__(description, keywords, isAccessible, **kwargs)
        
    def tryUnlock(self, usedItem, player):
        return "The door has no visible means of unlocking it from this side."

    def tryLock(self, usedItem, player):
        return "The door has no visible means of locking it from this side."

        
class StandardUpwardStairs(AreasFeatures.Link):
    
    def __init__(self, description, keywords, **kwargs):
        kwargs = {
            "travelDesc":"You climb the stairs."
        }

        super(StandardUpwardStairs, self).__init__(description, keywords, True, **kwargs)
    
    def open(self, player):
        return "I can't open that"
    
    def climb(self, player):
        self.travel(player)
    
class StandardDownwardStairs(AreasFeatures.Link):
    
    def __init__(self, description, keywords):
        kwargs = {
            "travelDesc":"You descend the stairs."
        }
        super(StandardDownwardStairs, self).__init__(description, keywords, True, **kwargs)
    
    def open(self, player):
        return "I can't open that"
    
    def descend(self, player):
        self.travel(player)
    
class UnlockedContainer(AreasFeatures.Container):
    
    def __init__(self, description, keywords, openDesc, closeDesc):
        super(UnlockedContainer, self).__init__(description, keywords, False, True, None, openDesc, closeDesc)
        
    def tryUnlock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]

        if self.isAccessible:
            if usedItem == self.itemToOpen:
                self.isAccessible = True
                return usedItem.useDescription,True
            else:
                return "That key does not seem to fit the lock."
        else:
            return "It isn't locked."
        
class LockedContainer(AreasFeatures.Container):
    
    def __init__(self, description, keywords, blockedDesc, openDesc, closeDesc, itemToOpen):
        self.itemToOpen = itemToOpen
        super(LockedContainer, self).__init__(description, keywords, False, False, blockedDesc, openDesc, closeDesc)
        
    def tryUnlock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]
                
        if self.isAccessible:
            if usedItem == self.itemToOpen:
                self.isAccessible = True
                return usedItem.useDescription,True
            else:
                return "That key does not seem to fit the lock."
        else:
            return "It isn't locked."
        
class AlwaysOpenContainer(AreasFeatures.Container):
    
    def __init__(self, description, keywords):
        super(AlwaysOpenContainer, self).__init__(description, keywords, True, True, "", "", "")
        
    def open(self, player):
        return "You can't open that."
    
    def close(self, player):
        return "You can't close that."
    
class Sign(AreasFeatures.Feature):
    
    def __init__(self, description, keywords, readDescription):
        self.readDescription = readDescription
        
        super(Sign, self).__init__(description, keywords)
    
    def read(self, player):
        return self.readDescription

    def lookAt(self):
        return self.description[self.state] + "\n\nIt reads: \n" + self.read()
