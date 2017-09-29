'''
Created on Jun 29, 2014

@author: Thomas
'''
import AreasFeatures

class StandardOpenDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords):
        kwargs = {
            "travelDesc":"You open the door and step through.",
            "breakable":True
        }

        super(StandardOpenDoor, self).__init__(description, keywords, True, **kwargs)

class StandardOpenMetalDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords):
        kwargs = {
            "travelDesc":"You open the door and step through."
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

        super(StandardLockingDoor, self).__init__(description, keywords, isAccessible, **kwargs)
        
    def tryUnlock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]

        if self.isAccessible:
            return "It isn't locked."

        if self.health <= 0:
            return "It's smashed open, the lock doesn't work anymore."

        if self.keyRequired:
            if not usedItem:
                for key, item in player.inventory.iteritems():
                    if item == self.itemToOpen:
                        self.unlock()
                        return self.unlockDesc, True
                return "You aren't carrying a key that fits this lock."
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

        if not self.isAccessible:
            return "It's already locked."

        if self.health <= 0:
            return "It's smashed open, the lock doesn't work anymore."

        if self.keyRequired:
            if not usedItem:
                for key, item in player.inventory.iteritems():
                    if item == self.itemToOpen:
                        self.lock()
                        return self.lockDesc, True
                return "You aren't carrying a key that fits this lock."
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

class StandardUnopenableDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords, blockedDesc, **kwargs):

        kwargs.update({
            "blockedDesc":blockedDesc
        })

        super(StandardUnopenableDoor, self).__init__(description, keywords, False, **kwargs)
        
    def tryUnlock(self, usedItem, player):
        return self.blockedDesc

    def tryLock(self, usedItem, player):
        return "It's already locked."

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
            "travelDesc":"You climb the stairs.",
            "travelSound":None
        }

        super(StandardUpwardStairs, self).__init__(description, keywords, True, **kwargs)
    
    def open(self, player):
        return "I can't open that"
    
    def climb(self, player):
        self.travel(player)
    
class StandardDownwardStairs(AreasFeatures.Link):
    
    def __init__(self, description, keywords):
        kwargs = {
            "travelDesc":"You descend the stairs.",
            "travelSound":None
        }
        super(StandardDownwardStairs, self).__init__(description, keywords, True, **kwargs)
    
    def open(self, player):
        return "I can't open that"
    
    def descend(self, player):
        self.travel(player)
    
        
class LockingContainer(AreasFeatures.Container):
    
    def __init__(self, description, keywords, keyRequired, itemToOpen, **kwargs):
        self.keyRequired = keyRequired
        self.itemToOpen = itemToOpen
        if not ("unlockDesc" in kwargs):
            self.unlockDesc = "You unlock it."
        if not ("lockDesc" in kwargs):
            self.lockDesc = "You lock it."

        kwargs.update({
            "isAccessible":False,
            "isOpen":False
        })
        super(LockingContainer, self).__init__(description, keywords, **kwargs)
        
    def tryUnlock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]
        
        if self.isAccessible:
            return "It isn't locked."

        if self.keyRequired:
            if not usedItem:
                for key, item in player.inventory.iteritems():
                    if item == self.itemToOpen:
                        self.unlock()
                        return self.unlockDesc, True
                return "You aren't carrying a key that fits this lock."
            if usedItem == self.itemToOpen:
                self.unlock()
            else:    
                return "The key does not appear to work for this lock."
        else:
            self.unlock()
        return self.unlockDesc, True
        
    def unlock(self):
        self.isAccessible = True

    def tryLock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]

        if not self.isAccessible:
            return "It's already locked."

        if self.keyRequired:
            if not usedItem:
                for key, item in player.inventory.iteritems():
                    if item == self.itemToOpen:
                        self.unlock()
                        return self.unlockDesc, True
                return "You aren't carrying a key that fits this lock."
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

class AlwaysOpenContainer(AreasFeatures.Container):
    
    def __init__(self, description, keywords):
        kwargs = {
            "isOpen":True,
            "isOpenDesc":" "
        }

        super(AlwaysOpenContainer, self).__init__(description, keywords, **kwargs)
        
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

    def lookAt(self, player):
        return self.description[self.state] + "\n\nIt reads: \n" + self.read(None)
