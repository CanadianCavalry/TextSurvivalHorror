'''
Created on Aug 3, 2014

@author: Thomas
'''
from Items import Corpse
from random import randint

def getActingEnemies(player):
    return player.currentLocation.enemies

def enemyAction(player, actingEnemies):
    resultString = ""
    for enemy in actingEnemies:
        resultString += enemy.takeAction(player) + "\n"
    return resultString

def enemyMovement(movingEnemies, enemyDestination, player):
    print "Enemy movement phase"
    resultString = ""
    for enemy in movingEnemies:
        print enemy.name + " is moving to " + enemyDestination.name
        resultString += enemy.travel(enemyDestination, player) + "\n"
    return resultString

class Enemy(object):
    def __init__(self, name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, corpse, **kwargs):
        
        #required params. instance cannot be created without these
        self.name = name
        self.description = description
        self.seenDescription = seenDesc
        self.keywords = keywords
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.accuracy = accuracy
        self.corpse = corpse

        #set default values for case when no values are given
        self.currentLocation = None
        self.speed = 1
        self.meleeDodge = 0
        self.rangedDodge = 0
        self.armor = 0
        self.baseExorciseChance = 10
        self.firstSeenSound = None
        self.enemyState = 0
        self.distanceToPlayer = 3
        self.currentLocation = None
        self.actionTimer = 1
        self.stunnedTimer = 0
        self.isChasing = False
        self.isBlockingExit = False
        self.talkCount = 0
        self.firstSeen = True
        self.willChase = True
        self.blockingDesc = "The " + self.name + " is between you and the exit. There's no way out.\n"
        self.stunDesc = "The " + self.name + " staggers away from you, dazed.\n"
        self.attackDesc = ["The " + self.name + " attacks you.\n"]
        self.firstSeenDesc = seenDesc
        self.exorciseDialogue = ["\"Back to hell with you demon!\"", "\"In the name of god, DIE!\"", "\"With the lord as my weapon, I will destroy you!\""]
        self.talkDialogue = ["It doesn't respond."]
        self.critDialogue = ["You charge forward and knock the creature to the ground. As it struggles to rise, you finish it off with a single strike."]
        self.advanceDialogue = "The " + self.name + " moves towards you.\n"
        self.retreatDialogue = "The " + self.name + " moves away from you.\n"
        self.travelDesc = "The " + self.name + " has caught up with you. It moves to attack."

        #populate optional stats
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)
        
    def travel(self, location, player):
        for link in self.currentLocation.connectedAreas.itervalues():
            if not link.destination == location:
                continue

            link.enemyTravel(self)
            if self.currentLocation == player.currentLocation:
                return self.travelDesc
        
    def takeAction(self, player):
        #DEBUG
        print "Enemy taking turn"
        if self.willChase and not self.isChasing:
            print "Enemy now chasing"
            self.isChasing = True
        if self.health < 1:
            return ""
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
            result = ""
        
        return result

    def attack(self, player):
        return self.basicAttack(player)

    def basicAttack(self, player):
        print "Enemy attacking"
        resultString = self.attackDesc[randint(0, len(self.attackDesc) - 1)]
        hitChance = self.calcAttackAccuracy(player)
            
        attackRoll = randint(0,100)
        if attackRoll <= hitChance:
            damageAmount = randint(self.minDamage + 1, self.maxDamage)
            modDamageAmount = damageAmount - player.armorRating
            if modDamageAmount < 0:
                modDamageAmount = 0
            print "Player hit. DamageRoll: " + str(damageAmount) + ", ArmorRating: " + str(player.armorRating) + ", DamageTaken: " + str(modDamageAmount)
            resultString += " The " + self.name + " hits you! "
            resultString += player.takeDamage(modDamageAmount)
        else:
            resultString += " The " + self.name + "'s attack misses."
            
        return resultString

    def calcAttackAccuracy(self, player):
        hitChance = self.accuracy - player.dodgeChance
        if player.isDefending:
            hitChance = self.playerIsDefending(hitChance)
        if hasattr(player.mainHand, 'defenseBonus'):
            hitChance -= player.mainHand.defenseBonus

        return hitChance

    def playerIsDefending(self, hitChance):
        return hitChance - 20
        
    def advance(self):
        if self.distanceToPlayer > 1:
            self.distanceToPlayer -= 1
            return self.advanceDialogue + self.getDistance()
        return "The " + self.name + " does nothing."
    
    def retreat(self):
        if self.distanceToPlayer < 3:
            self.distanceToPlayer += 1
            return self.retreatDialogue + self.getDistance()
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
    
    def makeStunned(self, stunTime):
        if self.stunnedTimer == 0:
            self.stunnedTimer = stunTime
        
    def takeHit(self, weapon, attackType):
        resultString = weapon.attackDesc + "\n"
        damageAmount = (randint(weapon.minDamage, weapon.maxDamage))
        if (self.stunnedTimer > 0) and (attackType == "heavy"):
            resultString = self.takeCrit(weapon)
        elif attackType == "heavy":
            critRoll = randint(0,100)
            if critRoll <= weapon.critChance:
                resultString = self.takeCrit(weapon)
            else:
                self.makeStunned(weapon.stunLength)
                resultString += "You hit the " + self.name + "! "
                resultString += self.stunDesc
        else:
            resultString += "You hit the " + self.name + "! "
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
        return self.critDialogue[randint(0, len(self.critDialogue) - 1)]
        
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
        self.currentLocation.addItem(self.corpse)
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

    def removeExorciseDialogue(self, index):
        del self.exorciseDialogue[index]
    
    def setTalkDialogue(self, textList):
        self.talkDialogue = textList
        
    def addTalkDialogue(self, text):
        self.talkDialogue.append(text)
        
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

    def get(self, holder, player):
        return "It seems unlikely to hold still long enough for you to get it into your pack."

    def equip(self, player):
        return "After briefly considering the logistics required to use the " + self.name + " as a weapon, you think better of it."

class TestDemon(Enemy):
    
    def __init__(self):
        name = "Winged Demon"
        description = "A slavering, red skinned, bat winged demon. Pretty standard stuff actually. Utilizing your expertise in demonology, you know that this type of creature is highly vulnerable to exorcism."
        seenDesc = "You see a Winged Demon glaring at you menacingly."
        keywords = "demon,red demon,winged demon,enemy"
        maxHealth = 125
        minDamage = 15
        maxDamage = 19
        accuracy = 65
        corpse = Corpse("Demon Corpse", "The body is covered in wounds and blood is slowly pooling on the floor under it. The air around it stinks of sulphur.", "The freshly butchered body of a large, red-skinned demon is lying on the floor.", "body,demon body,dead demon,demon corpse,corpse,demon")
        
        kwargs = {
            "speed":1, 
            "meleeDodge":5,
            "rangedDodge" 
            "baseExorciseChance":50,
            #"isBlockingExit":True,
            "stunDesc": "The demon staggers back, dazed.",
            "attackDesc": ["The demon claws at you with it's talons.", "The demon lunges forwards and snaps at you."],
            "firstSeenDesc":"As you enter the room you hear a rush of wind followed by leathery flapping. Moments later a dark shape drops from above, landing with a heavy thud on the other side of the arena, it's bat-like wings folding behind it's back as it straightens up. The creature stands at least 8 feet tall, with red scaly skin and a long canine muzzle. It glares at you through yellow eyes with a low growl.",
            "firstSeenSound":"Sounds/Monsters/DemonCantWait.mp3",
        }

        super(TestDemon, self).__init__(name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, corpse, **kwargs)

    def takeCrit(self, weapon):
        self.health = 0
        self.kill()
        if weapon.name == "Axe":
            return "You throw yourself into the demon hard, sending you both sprawling to the ground despite it's size. Scrambling to your feet, you raise your axe above the stunned behemoth and bring it down on it's head with a loud *CRACK*. The creature jerks sharply, then lies still.\nHaving seen enough horror movies in your life, you give it one last hit for good measure."
        elif weapon.name == "Kitchen Knife":
            return "Striking quickly, you land a lucky slash across the demon's eyes, and it let's out an earsplitting screech. As it staggers away you leap onto it's back from behind, drawing the knife quickly across the beasts throat in one fluid motion. It throws you aside and stumbles away, gurgling and grasping it's wound, before slumping over to the floor."
        else:
            return "You kick the stunned creature hard in the chest, knocking it to the ground. You fall upon it with your weapon, striking over and over until it lies still."