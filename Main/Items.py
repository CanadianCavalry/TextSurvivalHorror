'''
Created on Aug 22, 2014

@author: Thomas
'''
import random
import pyglet

class Item(object):
    #required params. instance cannot be created without these
    def __init__(self, name, description, seenDescription, keywords, **kwargs):
        self.name = name
        self.description = description
        self.seenDescription = seenDescription
        self.keywords = keywords

        #set default values for case when no values are given
        self.initPickupDesc = None
        self.quantity = 1
        self.accessible = True
        self.firstSeen = True
        self.firstTaken = True
        self.initPickupDesc = None
        self.initSeenDesc = None
        self.notTakenDesc = None
        self.carried = False
        self.inAccessibleDesc = "You can't reach it."
        self.pickupDesc = "You pick up the " + self.name + "."
        
        #populate optional stats
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)

    def get(self, holder, player):
        if not self.accessible:
            return self.inaccessibleDesc,True
        
        self.carried = True
        player.addItem(self)
        holder.removeItem(self)
        
        if self.firstTaken:
            if self.initPickupDesc:
                resultString = self.initPickupDesc
            else:
                resultString = self.pickupDesc
        else:
            resultString = self.pickupDesc
    
        self.firstSeen = False
        self.firstTaken = False

        if (player.mainHand == None) and (isinstance(self, Weapon)):
            self.equip(player)
        return resultString, True
    
    def drop(self, player):
        player.removeItem(self)
        player.currentLocation.addItem(self)
        return "You drop the " + self.name,True
    
    def destroy(self, holder):
        holder.removeItem(self)
        
    def makeAccessible(self):
        self.accessible = True
        
    def makeInAccessible(self, desc):
        self.accessible = False
        self.inaccessibleDesc = desc
        
    def setPickupDesc(self, desc):
        self.pickupDesc = desc
        
    def setInitPickupDesc(self,desc):
        self.initPickupDesc = desc
    
    def setIdNum(self, number):
        self.idNum = number
    
    def lookAt(self):
        return self.description

    def exorciseAttempt(self, player):
        return "After several minutes of yelling biblical phrases and waving your hands around wildly, you determine that the object is not, in fact, possessed."

    def playerRetreats(self):
        #if player is holding
        return "No matter how you duck and weave to escape, it manages to stay right behind you the entire time. Possibly this has something to do with the fact that it is still in your pack."

class Armor(Item):
    
    def __init__(self, name, description, seenDescription, keywords, armorRating, **kwargs):
        self.armorRating = armorRating
        super(Armor, self).__init__(name, description, seenDescription, keywords, **kwargs)
        
    def equip(self, player):
        if player.armor == self:
            return "You are already wearing that."
        
        player.armor = self
        return "You put on the " + self.name + ".",True

    def wear(self, player):
        return self.equip(player)
    
class Weapon(Item):
    
    def __init__(self, name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs):
        #required
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.accuracy = accuracy
        self.size = size

        #defaults
        self.attackDesc = "You attack."
        self.critChance = 10
        self.defenseBonus = 0

        super(Weapon, self).__init__(name, description, seenDescription, keywords, **kwargs)
        
    def equip(self, player):
        if player.mainHand == self:
            return "That is already equipped."
        if self.size == 1:
            if player.mainHand == player.offHand:
                player.offHand = None
            player.mainHand = self
            return "You equip the " + self.name,True
        elif self.size == 2:
            player.mainHand = self
            player.offHand = self
            return "You equip the " + self.name,True

    def attack(self):
        pass
        
class RangedWeapon(Weapon):
    
    def __init__(self, name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, capacity, **kwargs):
        #required
        self.capacity = capacity

        #defaults
        self.ammoRemaining = capacity
        self.fireSound = None
        self.rangeMod = [0,5,10]
        self.emptySound = "Sounds/Combat/EmptyGun.mp3"
        self.attackDesc = "You open fire!"

        super(RangedWeapon, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)
                            #Me name es Wayne Purkle coz when I nommin' grapes day be PURKLE!!!
    def attack(self, enemy, player, attackType):
        try:
            if attackType == "heavy":
                return "You are not holding a melee weapon."
            
            if self.ammoRemaining <= 0:
                source = pyglet.media.load(self.emptySound, streaming=False)
                source.play()
                return "You are out of ammo!"
            
            if self.fireSound:
                source = pyglet.media.load(self.fireSound, streaming=False)
                source.play()
            
            self.ammoRemaining -= 1
            hitChance = self.accuracy
            hitChance -= enemy.dodgeChance
            
            if enemy.distanceToPlayer == 1:
                hitChance -= self.rangeMod[0]
            elif enemy.distanceToPlayer == 2:
                hitChance -= self.rangeMod[1]
            elif enemy.distanceToPlayer == 3:
                hitChance -= self.rangeMod[2]
                
            if player.intoxication > 75:
                hitChance -= 25
            elif player.intoxication > 60:
                hitChance -= 15
            elif player.intoxication > 40:
                hitChance -= 10
            elif player.intoxication > 25:
                hitChance -= 5
            elif player.intoxication > 10:
                hitChance += 8
            elif player.intoxication > 1:
                hitChance += 5
            elif player.intoxication > 60:
                hitChance -= 5
                
            if enemy.stunnedTimer > 0:
                hitChance += 10
                
            if hitChance < 5:
                hitChance = 5
                
            attackRoll = random.randint(0, 100)
            if attackRoll <= hitChance:
                resultString = enemy.takeHit(self, "ranged")
            else:
                resultString = self.attackDesc
                resultString += "\nYou miss!"
            return resultString, True
        except AttributeError:
            return "That isn't worth wasting ammo on..."

    def shoot(self, enemy, player):
        return self.attack(enemy, player)
    
    def reload(self, player):
        for item in player.inventory.itervalues():
            try:
                weaponType = item.weaponType
            except AttributeError:
                continue
            
            if self.name == weaponType:
                self.ammoRemaining = self.capacity
                item.destroy(player)
                return "You reload the " + self.name + ".",True
            
        return "You don't have any ammo."
        
    def lookAt(self):
        resultString = self.description + "\n"
        resultString += "It has " + str(self.ammoRemaining) + " shots remaining."
        return resultString
        
class MeleeWeapon(Weapon):

    def __init__(self, name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs):
        #required

        #defaults
        self.stunLength = 2
        self.missSound = "Sounds/Combat/MeleeMiss.mp3"
        self.attackDesc = "You swing your weapon!"
        
        super(MeleeWeapon, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)   

    def attack(self, enemy, player, attackType):
        try:
            if enemy.distanceToPlayer > 1:
                return "You are not within striking distance."

            hitChance = self.accuracy
            hitChance -= enemy.dodgeChance
            
            if player.intoxication > 75:
                hitChance -= 25
            elif player.intoxication > 60:
                hitChance -= 15
            elif player.intoxication > 40:
                hitChance -= 10
            elif player.intoxication > 25:
                hitChance -= 5
            elif player.intoxication > 10:
                hitChance += 8
            elif player.intoxication > 1:
                hitChance += 5
                
            if attackType == "heavy":
                hitChance -= 10
            
            if enemy.stunnedTimer > 0:
                hitChance += 50
            
            if hitChance < 5:
                hitChance = 5
            attackRoll = random.randint(0, 100)
            if attackRoll <= hitChance:
                resultString = "\n" + enemy.takeHit(self, attackType)
            else:
                resultString = self.attackDesc
                resultString += "\nYou miss!"
                source = pyglet.media.load(self.missSound, streaming=False)
                source.play()
            return resultString, True
        except AttributeError:
            return "That isn't an enemy..."

    def shoot(self, enemy, player):
        return "Try as you might, you can't find a good way to use your " + player.mainHand.name + " as a gun."

class Ammo(Item):
    
    def __init__(self, name, description, seenDescription, keywords, weaponType, **kwargs):
        self.weaponType = weaponType
        super(Ammo, self).__init__(name, description, seenDescription, keywords, **kwargs)
    
class Usable(Item):
    
    def __init__(self, name, description, seenDescription, keywords, useDescription, **kwargs):
        self.useDescription = useDescription
        super(Usable, self).__init__(name, description, seenDescription, keywords, **kwargs)
        
class Drinkable(Usable):
    
    def __init__(self, name, description, seenDescription, keywords, useDescription, **kwargs):
        super(Drinkable, self).__init__(name, description, seenDescription, keywords, useDescription, **kwargs)
        
class Alchohol(Drinkable):
    
    def __init__(self, name, description, seenDescription, keywords, useDescription, alcoholAmount, **kwargs):
        self.alcoholAmount = alcoholAmount
        super(Alchohol, self).__init__(name, description, seenDescription, keywords, useDescription, **kwargs)
        
    def drink(self, player):
        player.increaseIntox(self.alcoholAmount)
        spiritDecrease = self.alcoholAmount / 2
        if spiritDecrease > 10:
            spiritDecrease = 10
        player.decreaseSpirit(spiritDecrease)
        player.removeItem(self)
        return self.useDescription,True
    

class Readable(Item):
    
    def __init__(self, name, description, seenDescription, keywords, **kwargs):
        super(Readable, self).__init__(name, description, seenDescription, keywords, **kwargs)
            
    def read(self):
        pass

class Note(Readable):
    
    def __init__(self, name, description, seenDescription, keywords, contents, **kwargs):
        self.contents = contents
        super(Note, self).__init__(name, description, seenDescription, keywords, **kwargs)
    
    def read(self):
        return self.contents,True        

class Corpse(Item):
    def __init__(self, name, description, seenDescription, keywords, **kwargs):
        super(Corpse, self).__init__(name, description, seenDescription, keywords, **kwargs)
    
    def get(self, holder, player):
        return "I've no desire to carry around a corpse."