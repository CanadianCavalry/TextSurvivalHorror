import os
import pyglet
import GUI

class Player(object):

    def __init__(self):
        self.currentLocation = None
        self.inventory = {}
        self.health = 100
        self.spirit = 100
        self.intoxication = 0
        self.isDefending = False
        self.mainHand = None
        self.offHand = None
        self.dodgeChance = 0
        self.armor = None
        self.armorRating = 0
        self.isRestricted = False
        self.restrictedDesc = ""
        self.lastAction = None
        
    def increaseSpirit(self, amount):
        self.spirit += amount
        if self.spirit > 100:
            self.spirit = 100
        
    def decreaseSpirit(self, amount):
        self.spirit -= amount
        if self.spirit < 0:
            self.spirit = 0
        
    def heal(self, healNumber):
        self.health += healNumber
        if self.health > 100:
            self.health = 100
        
    def takeDamage(self, damageNumber):
        self.health -= damageNumber
        if self.health < 0:
            self.health = 0
        return "You are " + self.getCondition() + "."
        
    def increaseIntox(self, amount):
        self.intoxication += amount
        if self.intoxication > 100:
            self.intoxication = 100
        
    def decreaseIntox(self, amount):
        self.intoxication -= amount
        if self.intoxication < 0:
            self.intoxication = 0
        
    def restrictPlayer(self, desc):
        self.isRestricted = True
        self.restrictedDesc = desc
        
    def unrestrictPlayer(self):
        self.isRestricted = False
        
    def addItem(self, itemToAdd):
        if itemToAdd.keywords in self.inventory:
        	if itemToAdd.stackable:
        		self.inventory[itemToAdd.keywords].quantity += itemToAdd.quantity
        	else:
        		self.inventory[itemToAdd.keywords].quantity += 1
        else:
        	self.inventory[itemToAdd.keywords] = itemToAdd
        
    def removeItem(self, itemToRemove):
        if self.mainHand == itemToRemove:
            self.mainHand = None
        if self.offHand == itemToRemove:
            self.offHand = None
        if self.armor == itemToRemove:
            self.armor = None
            
    	if self.inventory[itemToRemove.keywords].quantity > 1 and (not itemToRemove.stackable):
            self.inventory[itemToRemove.keywords].quantity -= 1
        else:
            del self.inventory[itemToRemove.keywords]
        
    def attack(self, enemy):
        if self.isRestricted:
            return self.restrictedDesc
        
        #try:
        return self.mainHand.attack(enemy, self, "light")
        #except AttributeError:
            #return "You are not holding a weapon."
        
    def heavyAttack(self, enemy):
        if self.isRestricted:
            return self.restrictedDesc
        
       	try:
        	return self.mainHand.attack(enemy, self, "heavy")
        except AttributeError:
            return "You are not holding a weapon."
        
    def shoot(self, enemy):
        if self.isRestricted:
            return self.restrictedDesc
        
        try:
        	return self.mainHand.shoot(enemy, self)
        except AttributeError:
    		return "You are not holding a gun."
        
    def reload(self):
        if self.isRestricted:
            return self.restrictedDesc
        
        if self.mainHand:
            try:
                return self.mainHand.reload(self)
            except AttributeError:
                return "You are not holding a gun."
        else:
            return "You are not holding anything."
        
    def defend(self):
        if self.isRestricted:
            return self.restrictedDesc
        
        self.isDefending = True
        return "You take a defensive stance.", True
        
    def exorcise(self, enemy):
        return enemy.exorciseAttempt(self), True
        
    def advance(self, enemy):
        if self.isRestricted:
            return self.restrictedDesc
        
        return enemy.playerAdvances()
    
    def retreat(self, enemy):
        if self.isRestricted:
            return self.restrictedDesc
        
        return enemy.playerRetreats()
        
    def wait(self):
        return "You wait.", True
        
    def getCondition(self):
        healthString = ""
        if self.health >= 95:
            healthString += "Unhurt"
        elif self.health >= 85:
            healthString += "Bruised and Scratched"
        elif self.health >= 60:
            healthString += "Injured"
        elif self.health >= 35:
            healthString += "Seriously Injured"
        elif self.health >= 10:
            healthString += "Grievously Wounded"
        elif self.health >= 1:
            healthString += "Dying"
        elif self.health < 1:
            healthString += "Dead"
        
        return healthString    

    def getSpirit(self):
        spiritString = ""
        if self.spirit >= 90:
            spiritString += "Saint Like"
        elif self.spirit >= 75:
            spiritString += "Pious"
        elif self.spirit >= 68:
            spiritString += "Faithful"
        elif self.spirit >= 59:
            spiritString += "Good"
        elif self.spirit >= 50:
            spiritString += "Lukewarm"
        elif self.spirit >= 40:
            spiritString += "Impure"
        elif self.spirit >= 30:
            spiritString += "Sinful"
        elif self.spirit >= 20:
            spiritString += "Evil"
        elif self.spirit >= 1:
            spiritString += "Diabolical"
        elif self.spirit == 0:
            spiritString += "Satanic"
            
        return spiritString

    def getIntoxication(self):
        intoxicationString = ""
        if self.intoxication == 0:
            intoxicationString += "Sober"
        elif self.intoxication < 10:
            intoxicationString += "Tipsy"
        elif self.intoxication < 25:
            intoxicationString += "Buzzed"
        elif self.intoxication < 40:
            intoxicationString += "Drunk"
        elif self.intoxication < 60:
            intoxicationString += "Very Drunk"
        elif self.intoxication < 80:
            intoxicationString += "Hammered"
        elif self.intoxication < 90:
            intoxicationString += "Blacked Out"
        elif self.intoxication < 100:
            intoxicationString += "Near Lethal"
            
        return intoxicationString
    
    def getMainHand(self):
        return self.mainHand
    
    def getOffHand(self):
        return self.offHand
    
    def getArmor(self):
        return self.armor

    def calcDodgeChance(self):
        return self.dodgeChance
    
    def calcArmorRating(self):
        armorRating = 0
        if self.armor:
            armorRating += self.armor.armorRating
        armorRating += self.intoxication * 0.25
        return armorRating
        
    def beginTurn(self):
        self.isDefending = False
        self.armorRating = self.calcArmorRating()
        
    def getActingEnemies(self):
        enemyList = list()
        for enemy in self.currentLocation.enemies.itervalues():
            enemyList.append(enemy)
        return enemyList
    
    def getPursuingEnemies(self):
        enemyList = list()
        for link in self.currentLocation.connectedAreas.itervalues():
            for enemy in link.destination.enemies.itervalues():
                if not enemy.isChasing:
                    continue
                else:
                    enemyList.append(enemy)
        return enemyList
        
    def setLastAction(self, actionName):
        self.lastAction = actionName
        
def launch():
    window = GUI.Window(Player())      #start the GUI
    pyglet.app.run()
    
launch()