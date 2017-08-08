'''
Created on Aug 3, 2014

@author: Thomas
'''
from Items import Corpse
from random import randint
import pyglet

#Generator for creating unqiue enemy ID's
def createGenerator():
    idList = range(10000)
    for i in idList:
        yield i

def generateId():
    return generateId.generator.next()
generateId.generator = createGenerator()

def getActingEnemies(player):
    return player.currentLocation.enemies

def enemyAction(player, actingEnemies):
    resultString = ""
    for enemy in actingEnemies:
        resultString += enemy.takeAction(player) + "\n"
    return resultString

def enemyMovement(movingEnemies, enemyDestination, player):
    enemyActions = {}
    groupEnemyActions = {}
    for enemy in movingEnemies:
        resultString, actionType, stackable = enemy.calcMovement(enemyDestination, player)

        dictKey = str(type(enemy)) + actionType + str(stackable)
        if dictKey in groupEnemyActions:
            continue
        elif dictKey in enemyActions:
            if actionType == "travel":
                groupEnemyActions[dictKey] = enemy.groupTravelDesc
                del enemyActions[dictKey]
            elif actionType == "blocked":
                groupEnemyActions[dictKey] = enemy.groupTravelBlockedDesc
                del enemyActions[dictKey]
            else:
                oldResult, quantity = enemyActions[dictKey]
                enemyActions[dictKey] = (oldResult, quantity + 1)
        else:
            enemyActions[dictKey] = (resultString, 1)

    resultString = ""
    for key,item in groupEnemyActions.iteritems():
        resultString += item + "\n"
    for key, item in enemyActions.iteritems():
        resultString += item[0]
        if item[1] > 1:
            resultString += "(" + str(item[1]) + ")"
        resultString += "\n"

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
        self.idNum = generateId()
        #Since enemies can't stack, each needs a unique keyword string
        self.keywords = str(self.idNum) + "," + keywords

        #set default values for case when no values are given
        self.protectedThings = {}
        self.currentLocation = None
        self.actionSpeed = 1
        self.moveSpeed = 1
        self.meleeDodge = 0
        self.rangedDodge = 0
        self.armor = 0
        self.baseExorciseChance = 10
        self.stunResist = 0
        self.enemyState = 0
        self.distanceToPlayer = 1
        self.currentLocation = None
        self.actionTimer = 1
        self.stunnedTimer = 0
        self.isChasing = False
        self.isBlockingExit = False
        self.talkCount = 0
        self.willChase = True
        self.helpless = False
        self.recovering = False
        self.firstSeen = True
        self.firstSeenSound = None
        self.deathSound = None
        self.basicAttackSound = None
        self.exorciseSound = None
        self.exorciseHitSound = None
        self.exorciseFailSound = None
        self.defaultBlockDesc = "The " + self.name + " is blocking the way, you can't reach it.\n"
        self.defaultStunDesc = "The " + self.name + " is dazed.\n"
        self.defaultRecoveryDesc = "The " + self.name + " is no longer dazed."
        self.stunDesc = self.defaultStunDesc
        self.recoveryDesc = self.defaultRecoveryDesc
        self.attackDesc = ["The " + self.name + " attacks you.\n"]
        self.firstSeenDesc = seenDesc
        self.exorciseDesc = ["You stand tall and draw upon your faith, screaming out \"Back to hell with you demon!\"", "You stare the fiend in the eyes and calmly state \"With the lord as my weapon, I will destroy you.\""]
        self.takeExorciseDesc = ["It works! The creature recoils from you grasping it's head, and emits an agonizing scream."]
        self.exorciseFailDesc = ["It doesn't seem to have any effect."]
        self.exorciseStunDesc = ["The demon is cowering on the floor, clutching it's head and shrieking."]
        self.exorciseRecoveryDesc = ["The demon shakes off the effects of your exorcism attempt."]
        self.deathText = "The " + self.name + " falls to the ground dead."
        self.talkDialogue = ["It doesn't respond."]
        self.critDialogue = ["You charge forward and knock the creature to the ground. As it struggles to rise, you finish it off with a single strike."]
        self.advanceDialogue = ["The " + self.name + " moves towards you.\n"]
        self.retreatDialogue = ["The " + self.name + " moves away from you.\n"]
        self.travelDesc = "The " + self.name + " has caught up with you. It moves to attack."
        self.groupTravelDesc = "The " + self.name + "\'s have caught up with you. They move to attack."
        self.chaseDesc = "You can hear something chasing after you."
        self.travelBlockedDesc = "You hear something pounding on the door."
        self.groupTravelBlockedDesc = "You hear several somethings pounding on the door."

        #populate optional stats
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)
        
    def calcMovement(self, destination, player):
        resultString = ""
        if self.currentLocation == player.currentLocation:
            if self.stunnedTimer == 0:
                resultString += "You run straight into the " + self.name + " chasing you!\n"
            resultString += self.takeAction(player)
            return resultString, "action", False
        
        if self.stunnedTimer != 0:
            self.stunnedTimer -= 1
            if self.stunnedTimer == 0:
                self.recovering = True
            return "", "stun", False

        resultString = self.travel(destination, player)

        #If the enemy fails to get any closer to the player, OR cannot find the player nearby, then
        #they have lost the players scent and will stop chasing
        if not self.trackPlayer(player):
            self.isChasing = False
            self.stunnedTimer = 0
            self.recovering = False

        return resultString

    def trackPlayer(self, player):
        for link in self.currentLocation.connectedAreas.itervalues():
            if player.currentLocation == link.destination:
                return link
        return False

    def travel(self, destination, player):
        self.protectedThings = {}
        for link in self.currentLocation.connectedAreas.itervalues():
            if not link.destination == destination:
                continue

            if link.enemyTravel(self):
                if self.currentLocation == player.currentLocation:
                    if self.distanceToPlayer > self.currentLocation.size:
                        self.distanceToPlayer = self.currentLocation.size
                    return self.travelDesc, "travel", True
                else:
                    return self.chaseDesc, "chase", True
            else:
                if self.trackPlayer(player):
                    return self.travelBlockedDesc, "blocked", True

        return "", "none", False
        
    def takeAction(self, player):
        resultString = ""
        if self.willChase and not self.isChasing:
            self.isChasing = True
        if self.health < 1:
            return ""
        if self.stunnedTimer != 0:
            self.stunnedTimer -= 1
            if self.stunnedTimer == 0:
                self.recovering = True
            return self.stunDesc
        
        if self.recovering:
            resultString += self.recoveryDesc + "\n"
            self.recovering = False
            self.helpless = False

        if self.actionTimer == 1:
            if self.distanceToPlayer == 1:
                resultString += self.attack(player)
                self.actionTimer = self.actionSpeed
            else:
                resultString += self.advance()
                self.actionTimer = self.actionSpeed
        else:
            self.actionTimer -= 1
            resultString += ""
        
        return resultString

    def attack(self, player):
        return self.basicAttack(player)

    def basicAttack(self, player):
        #print "Enemy attacking"
        attackType = "melee"
        resultString = self.attackDesc[randint(0, len(self.attackDesc) - 1)]
        hitChance = self.calcAttackAccuracy(player, attackType)
        #print "Enemy hit chance: " + str(hitChance)
            
        if self.basicAttackSound:
            source = pyglet.media.load(self.basicAttackSound, streaming=False)
            source.play()

        attackRoll = randint(0,100)
        if attackRoll <= hitChance:
            damageAmount = randint(self.minDamage + 1, self.maxDamage)
            modDamageAmount = int(damageAmount - (damageAmount * (float(player.armorRating) / 100)))
            if modDamageAmount < 0:
                modDamageAmount = 0
            #print "Player hit. DamageRoll: " + str(damageAmount) + ", ArmorRating: " + str(player.armorRating) + ", DamageTaken: " + str(modDamageAmount)
            resultString += " It hits you! "
            resultString += player.takeDamage(modDamageAmount)
        else:
            resultString += " It misses!"
            
        return resultString

    def calcAttackAccuracy(self, player, attackType):
        hitChance = self.accuracy - player.dodgeChance
        if player.isDefending:
            hitChance = self.playerIsDefending(hitChance)
        if attackType == "melee" and hasattr(player.mainHand, 'defenseBonus'):
            hitChance -= player.mainHand.defenseBonus

        return hitChance

    def playerIsDefending(self, hitChance):
        return hitChance - 20

    def protectThing(self, thing, blockDesc=""):
        if not blockDesc:
            blockDesc = self.defaultBlockDesc
        self.protectedThings[thing] = blockDesc
        
    def advance(self):
        if self.distanceToPlayer > 1:
            self.distanceToPlayer -= self.moveSpeed
            if self.distanceToPlayer < 1:
                self.distanceToPlayer = 1
            return self.advanceDialogue[randint(0, len(self.advanceDialogue) - 1)] + "\n" + self.getDistance()
        return "The " + self.name + " does nothing."
    
    def retreat(self):
        if self.distanceToPlayer < self.currentLocation.size:
            self.distanceToPlayer += self.moveSpeed
            if self.distanceToPlayer > currentLocation.size:
                self.distanceToPlayer = currentLocation.size
            return self.retreatDialogue[randint(0, len(self.retreatDialogue) - 1)] + "\n" + self.getDistance()
        return "The " + self.name + " tries to flee, but is backed into a corner."
    
    def playerAdvances(self):
        if self.distanceToPlayer <= 1:
            return "You are already right in front of it!"
        else:
            self.distanceToPlayer -= 1
            return "You advance on the " + self.name, True
        
    def playerRetreats(self):
        if self.distanceToPlayer >= self.currentLocation.size:
            return "Your back is to the wall."
        else:
            self.distanceToPlayer += 1
            return "You retreat from the " + self.name, True
    
    def makeStunned(self, stunTime, stunDesc, recoveryDesc):
        self.stunnedTimer = stunTime
        self.stunDesc = stunDesc
        self.recoveryDesc = recoveryDesc
        
    def takeHit(self, player, weapon, attackType):
        resultString = weapon.attackDesc + "\n"
        resultString += "You hit the " + self.name + "! "
        damageAmount = (randint(weapon.minDamage, weapon.maxDamage))
        hitEffectDesc = ""
        if self.helpless and attackType == "heavy":
            resultString = self.takeCrit(weapon)
        elif attackType == "heavy":
            hitEffectDesc = self.hitEffect(player, weapon, attackType)
            damageAmount = int(damageAmount * 1.25)
            stunRoll = randint(0,100)
            stunChance = weapon.stunChance - self.stunResist
            if stunRoll <= stunChance:
                self.makeStunned(weapon.stunLength, self.defaultStunDesc, self.defaultRecoveryDesc)
                resultString += " It is dazed by the strength of your blow."
            resultString += self.takeDamage(damageAmount)
        else:
            hitEffectDesc = self.hitEffect(player, weapon, attackType)
            resultString += self.takeDamage(damageAmount)
        if hitEffectDesc:
            resultString += hitEffectDesc
        return resultString

    def hitEffect(self, player, weapon, attackType):
        pass

    def missEffect(self, player, weapon, attackType):
        pass
        
    def takeDamage(self, damageAmount):
        modDamageAmount = int(damageAmount - (damageAmount * (float(self.armor) / 100)))
        self.health -= modDamageAmount
        if self.health <= 0:
            return self.kill()
        else:
            return self.getCondition()
        
    def takeCrit(self, weapon):
        self.health = 0
        self.kill()
        return self.critDialogue[randint(0, len(self.critDialogue) - 1)]
        
    def exorciseAttempt(self, player):
        if self.exorciseSound:
            sourse = pyglet.media.load(self.exorciseSound, streaming=False)
            source.play()
        resultString = self.exorciseDesc[randint(0, len(self.exorciseDesc) - 1)] + "\n"
        
        hitChance = self.baseExorciseChance
        hitChance += (player.spirit - 50)
        attackRoll = randint(0, 100)
        if attackRoll <= hitChance:
            if self.exorciseHitSound:
                sourse = pyglet.media.load(self.exorciseHitSound, streaming=False)
                source.play()
            resultString += self.takeExorcise()
            return resultString
        else:
            if self.exorciseFailSound:
                sourse = pyglet.media.load(self.exorciseFailSound, streaming=False)
                source.play()
            resultString += self.exorciseFailDesc[randint(0, len(self.exorciseFailDesc) - 1)]
            return resultString
        
    def takeExorcise(self):
        stunDesc = self.exorciseStunDesc[randint(0, len(self.exorciseStunDesc) - 1)]
        recoveryDesc = self.exorciseRecoveryDesc[randint(0, len(self.exorciseRecoveryDesc) - 1)]
        self.makeStunned(2, stunDesc, recoveryDesc)
        self.helpless = True

        resultString = self.takeExorciseDesc[randint(0, len(self.takeExorciseDesc) - 1)]
        return resultString

    def kill(self):
        if self.deathSound:
            source = pyglet.media.load(self.deathSound, streaming=False)
            source.play()
        self.currentLocation.killEnemy(self)
        self.currentLocation.addItem(self.corpse)
        return self.deathText
    
    def talk(self):
        resultString = self.talkDialogue[self.talkCount]
        if self.talkCount < len(self.talkDialogue) - 1:
            self.talkCount += 1
        return resultString, True
            
    def setState(self, newState):
        self.enemyState = newState
    
    def setDistance(self, newDistance):
        if newDistance >= self.currentLocation.size:
            self.distanceToPlayer = self.currentLocation.size
        elif newDistance < 1:
            self.distanceToPlayer = 1
        else:
            self.distanceToPlayer = newDistance
        
    def setLocation(self, location):
        self.currentLocation = location
    
    def setTalkDialogue(self, textList):
        self.talkDialogue = textList
        
    def addTalkDialogue(self, text):
        self.talkDialogue.append(text)
    
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
            distanceDescription = "It is right next to you."
        if self.distanceToPlayer == 2:
            distanceDescription = "It is a few meters away."
        if self.distanceToPlayer == 3:
            distanceDescription = "It is a dozen meters away."
        if self.distanceToPlayer == 4:
            distanceDescription = "It is quite a ways away."
        return distanceDescription
    
    def lookAt(self):
        lookResult = self.description[self.enemyState]
        lookResult += "\n" + self.getCondition()
        lookResult += "\n" + self.getDistance()
        return lookResult
    
    def setIdNum(self, number):
        self.idNum = number

    def get(self, holder, player):
        return "It seems unlikely to hold still long enough for you to get it into your pack."

    def equip(self, player):
        return "After briefly considering the logistics required to use the " + self.name + " as a weapon, you think better of it."

    def wear(self, player):
        return "It is generally considered rude to attempt to wear something that is still alive."

class TestDemon(Enemy):
    
    def __init__(self):
        name = "Winged Demon"
        description = ["A slavering, red skinned, bat winged demon. Pretty standard stuff actually. Utilizing your expertise in demonology, you know that this type of creature is highly vulnerable to exorcism."]
        seenDesc = "You see a Winged Demon glaring at you menacingly."
        keywords = "demon,red demon,winged demon,enemy"
        maxHealth = 125
        minDamage = 15
        maxDamage = 21
        accuracy = 85
        corpse = Corpse("Demon Corpse", "The body is covered in wounds and blood is slowly pooling on the floor under it. The air around it stinks of sulphur.", "The freshly butchered body of a large, red-skinned demon is lying on the floor.", "body,demon body,dead demon,demon corpse,corpse,demon")
        
        kwargs = {
            "actionSpeed":1, 
            "meleeDodge":5,
            "rangedDodge": 5,
            "baseExorciseChance":50,
            "defaultStunDesc": "The demon staggers back, dazed.",
            "attackDesc": ["The demon claws at you with it's talons.", "The demon lunges forwards and snaps at you."],
            "firstSeenDesc":"As you enter the room you hear a rush of wind followed by leathery flapping. Moments later a dark shape drops from above, landing with a heavy thud on the other side of the arena, it's bat-like wings folding behind it's back as it straightens up. The creature stands at least 8 feet tall, with red scaly skin and a long canine muzzle. It glares at you through yellow eyes with a low growl.",
            "firstSeenSound":"Sounds/Monsters/DemonCantWait.mp3",
            "deathSound":"Sounds/Monsters/DemonDeath.mp3",
            "advanceDialogue":["The hulking red demon lumbers steadily towards you.", "With a low growl the demon closes the distance between you.", "The demon calmly walks towards you, snarling under it's breath."],
            "retreatDialogue":["Reeling and terrified, the demon stumbles away from you."],
            "exorciseRecoveryDesc":["The demon recovers, straightening up and staring at you with loathing.\n'You'll die slowly for that human.'"]
       
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


            