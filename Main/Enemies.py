'''
Created on Aug 3, 2014

@author: Thomas
'''
from random import randint

def getActingEnemies(player):
    return player.currentLocation.enemies

def getMovingEnemies(player):
    movingEnemies = list()
    for link in player.currentLocation.connectedAreas:
        for enemy in link.destination.enemies:
            movingEnemies.append(enemy)
            
    return movingEnemies

def enemyAction(player, actingEnemies):
    resultString = ""
    for enemy in actingEnemies:
        resultString += enemy.takeAction(player) + "\n"
    return resultString

def enemyMovement(movingEnemies, enemyDestination):
    for enemy in movingEnemies:
        enemy.travel(enemyDestination)

class Enemy(object):
    
    def __init__(self, name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, speed, dodgeChance, armor, idNum=0):
        self.name = name
        self.description = description
        idNum = idNum
        self.seenDescription = seenDesc
        self.keywords = keywords
        self.maxHealth = maxHealth
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.accuracy = accuracy
        self.speed = speed
        self.dodgeChance = dodgeChance
        self.armor = armor
        self.health = maxHealth
        self.enemyState = 0
        self.baseExorciseChance = 5
        self.distanceToPlayer = 3
        self.currentLocation = None
        self.actionTimer = 1
        self.stunnedTimer = 0
        self.isChasing = False
        self.talkCount = 0
        self.stunDesc = ""
        self.exorciseDialogue = ["\"Back to hell with you demon!\"", "\"In the name of god, DIE!\"", "\"With the lord as my weapon, I will destroy you!\""]
        self.talkDialogue = ["It doesn't respond."]
        self.critDialogue = "You charge forward and knock the creature to the ground. As it struggles to rise, you finish it off with a single strike."
        self.advanceDialogue = "The " + self.name + " moves towards you.\n" + self.getDistance()
        self.retreatDialogue = "The " + self.name + " moves away from you.\n" + self.getDistance()
        
    def travel(self, location):
        for link in self.currentLocation.connectedAreas.itervalues():
            if not link.destination == location:
                continue
            
            self.currentLocation.removeEnemy(self)
            link.travel(self)
            self.currentLocation.addEnemy(self)
        
    def takeAction(self, player):
        if self.stunnedTimer != 0:
            self.stunnedTimer -= 1
            return "The " + self.name + " is dazed."
        
        if self.actionTimer == 1:
            if self.distanceToPlayer == 1:
                result = self.attack(player)
                self.actionTimer = self.speed
            else:
                result = self.advance()
                self.actionTimer = self.speed
        else:
            self.actionTimer -= 1
            result = "The " + self.name + " does nothing."
        
        return result

    def attack(self, player):
        return self.basicAttack(player)

    def basicAttack(self, player):
        resultString = "The " + self.name + " attacks you.\n"
        hitChance = self.accuracy - player.dodgeChance
        if player.isDefending:
            hitChance = self.playerIsDefending(hitChance)
            
        attackRoll = randint(0,100)
        if attackRoll <= hitChance:
            damageAmount = randint(self.minDamage + 1, self.maxDamage)
            if player.armor:
                damageAmount -= player.armor.armorRating
            
            resultString += "The " + self.name + " hits you! "
            resultString += player.takeDamage(damageAmount)
        else:
            resultString += "The " + self.name + " misses."
            
        return resultString
        
    def playerIsDefending(self, hitChance):
        return hitChance - 20
        
    def advance(self):
        if self.distanceToPlayer > 1:
            self.distanceToPlayer -= 1
            return self.advanceDialogue
        return "The " + self.name + " does nothing."
    
    def retreat(self):
        if self.distanceToPlayer < 3:
            self.distanceToPlayer += 1
            return self.retreatDialogue
        return "The " + self.name + " does nothing."
    
    def playerAdvances(self):
        if self.distanceToPlayer <= 1:
            return "You are already right in front of it!"
        else:
            self.distanceToPlayer -= 1
            return "You advance on the " + self.name, True
        
    def playerRetreats(self):
        if self.distanceToPlayer >= 3:
            return "Your back is to the wall."
        else:
            self.distanceToPlayer -= 1
            return "You retreat from the " + self.name, True
    
    def makeStunned(self, stunTime, stunDesc):
        if self.stunnedTimer == 0:
            self.stunnedTimer = stunTime
            self.stunDesc = stunDesc
        
    def takeHit(self, weapon, attackType):
        damageAmount = (randint(weapon.minDamage, weapon.maxDamage))
        if (self.stunnedTimer > 0) and (attackType == "heavy"):
            resultString = self.takeCrit(weapon)
        elif attackType == "heavy":
            critRoll = randint(0,100)
            if critRoll <= weapon.critChance:
                resultString = self.takeCrit(weapon)
            else:
                self.makeStunned(weapon.stunLength)
        else:
            resultString = "You hit the " + self.name + "!"
            resultString += self.takeDamage(damageAmount)
        return resultString
        
    def takeDamage(self, damageAmount):
        damageAmount -= self.armor
        self.health -= damageAmount
        if self.health <= 0:
            return self.kill()
        else:
            return self.getCondition()
        
    def takeCrit(self, weapon):
        self.health = 0
        self.kill()
        return self.critDialogue[randint(0, len(self.exorciseDialogue) - 1)]
        
    def exorciseAttempt(self, player):
        resultString = "You draw upon your faith to banish the demon. You yell out:\n" + self.exorciseDialogue[randint(0, len(self.exorciseDialogue) - 1)] + "\n"
        
        hitChance = self.baseExorciseChance
        hitChance += (player.spirit - 50)
        attackRoll = randint(0, 100)
        if attackRoll <= hitChance:
            resultString += self.takeExorcise()
            return resultString
        else:
            resultString += "It doesn't seem to have any effect."
            return resultString
        
    def takeExorcise(self):
        self.stunnedTimer = 2
        return "It works! The " + self.name + " is dazed."
        
    def kill(self):
        self.currentLocation.killEnemy(self)
        return "The " + self.name + " falls to the ground dead."
    
    def talk(self):
        resultString = self.talkDialogue[self.talkCount]
        if self.talkCount < len(self.talkDialogue) - 1:
            self.talkCount += 1
        return resultString, True
            
    def setState(self, newState):
        self.enemyState = newState
    
    def setDistance(self, newDistance):
        if newDistance >= 3:
            self.distanceToPlayer = 3
        else:
            self.distanceToPlayer = newDistance
        
    def setLocation(self, location):
        self.currentLocation = location
        
    def setExorciseDialogue(self, textList):
        self.exorciseDialogue = textList
        
    def addExorciseDialogue(self, text):
        self.exorciseDialogue.append(text)
    
    def setTalkDialogue(self, textList):
        self.talkDialogue = textList
        
    def addTalkDialogue(self, text):
        self.talkDialogue.append(text)
    
    
    def removeExorciseDialogue(self, index):
        del self.exorciseDialogue[index]
        
    def setAdvanceDialogue(self, text):
        self.advanceDialogue = text
        
    def setRetreatDialogue(self, text):
        self.retreatDialogue = text
    
    def getCondition(self):
        if self.health == self.maxHealth:
            return "It looks unharmed."
        elif self.health > (self.maxHealth * 0.75):
            return "It appears to be slightly injured."
        elif self.health > (self.maxHealth * 0.50):
            return "It appears to be injured."
        elif self.health > (self.maxHealth * 0.25):
            return "It appears to be severely injured."
        elif self.health > (0):
            return "It appears to be nearly dead."
    
    def getDistance(self):
        distanceDescription = ""
        if self.distanceToPlayer == 1:
            distanceDescription = "It is right in front of you."
        if self.distanceToPlayer == 2:
            distanceDescription = "It is a few meters away."
        if self.distanceToPlayer == 3:
            distanceDescription = "It is across the room."
        return distanceDescription
    
    def lookAt(self):
        lookResult = self.description
        lookResult += "\n" + self.getCondition()
        lookResult += "\n" + self.getDistance()
        return lookResult
    
    def setIdNum(self, number):
        self.idNum = number

class TestDemon(Enemy):
    
    def __init__(self):
        name = "Test Demon"
        description = "A slavering, red skinned, bat winged demon. Pretty standard stuff actually."
        seenDesc = "You see a Winged Demon glaring at you menacingly."
        keywords = "demon,red demon,winged demon"
        maxHealth = 125
        minDamage = 15
        maxDamage = 19
        accuracy = 65
        speed = 1
        dodgeChance = 5
        armor = 0
        super(TestDemon, self).__init__(name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, speed, dodgeChance, armor)