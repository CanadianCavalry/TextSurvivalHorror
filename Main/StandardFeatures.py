'''
Created on Jun 29, 2014

@author: Thomas
'''
import AreasFeatures

class StandardOpenDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords):
        super(StandardOpenDoor, self).__init__(description, keywords, True, "", "You open the door and step through.")

class StandardOpenMetalDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords):
        super(StandardOpenMetalDoor, self).__init__(description, keywords, True, "", "You open the door and step through.", "Sounds/Misc/HeavyDoor.mp3")

        
class StandardLockedDoor(AreasFeatures.Door):
    
    def __init__(self, description, keywords, itemToOpen):
        self.itemToOpen = itemToOpen
        super(StandardLockedDoor, self).__init__(description, keywords, False, "The door is locked. It won't budge.", "You open the door and step through.")
        
    def unlock(self, usedItem):
        if usedItem == self.itemToOpen:
            self.isAccessible = True
            return usedItem.useDescription,True
        else:    
            return "The key does not appear to work for this door."
        
class StandardUpwardStairs(AreasFeatures.Link):
    
    def __init__(self, description, keywords):
        super(StandardUpwardStairs, self).__init__(description, keywords, True, "", "You climb the stairs.")
    
    def open(self, player):
        return "I can't open that"
    
    def climb(self, player):
        self.travel(player)
    
class StandardDownwardStairs(AreasFeatures.Link):
    
    def __init__(self, description, keywords):
        super(StandardDownwardStairs, self).__init__(description, keywords, True, "", "You descend the stairs.")
    
    def open(self, player):
        return "I can't open that"
    
    def descend(self, player):
        self.travel(player)
    
class UnlockedContainer(AreasFeatures.Container):
    
    def __init__(self, description, keywords, openDesc, closeDesc):
        super(UnlockedContainer, self).__init__(description, keywords, False, True, None, openDesc, closeDesc)
        
    def unlock(self, usedItem):
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
        
    def unlock(self, usedItem):
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
    
    def read(self):
        return self.readDescription

    def lookAt(self):
        return self.description[self.state] + "\n\nIt reads: \n" + self.read()
