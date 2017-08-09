'''
Created on Aug 22, 2014

@author: Thomas
'''
from random import randint
import pyglet
import copy
import Enemies

class Item(object):
    #required params. instance cannot be created without these
    def __init__(self, name, description, seenDescription, keywords, **kwargs):
        self.name = name
        self.description = description
        self.seenDescription = seenDescription
        self.keywords = keywords
        self.currentLocation = None

        #set default values for case when no values are given
        self.initPickupDesc = None
        self.quantity = 1
        self.stackable = False
        self.accessible = True
        self.firstSeen = True
        self.firstTaken = True
        self.initPickupDesc = None
        self.initSeenDesc = None
        self.notTakenDesc = None
        self.pickupSound = ["Sounds/Misc/ItemGet.mp3"]
        self.inAccessibleDesc = "You can't reach it."
        self.pickupDesc = "You pick up the " + self.name + "."
        
        #populate optional stats
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)

    def get(self, holder, player):
        #print "Getting " + self.name + " - " + str(self.quantity)
        if not self.accessible:
            return self.inaccessibleDesc,True

        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]

        sources = list()
        
        #If there is more than 1, dup it and pass the dup. Quantity will be decremented later
        if (self.quantity > 1) and (not self.stackable):
            itemToGet = copy.deepcopy(self)
            itemToGet.quantity = 1
            itemToGet.firsSeen = False
            itemToGet.firstTaken = False
        else:
            itemToGet = self
        
        if self.quantity > 1 or (not self.firstTaken) or (not self.initPickupDesc):
            resultString = self.pickupDesc
            if self.stackable and (self.quantity > 1):
                resultString += "(" + str(self.quantity) + ")"
        else :
            resultString = self.initPickupDesc
            self.firstSeen = False
            self.firstTaken = False

        sources.append(pyglet.media.load(self.pickupSound[randint(0, len(self.pickupSound) - 1)], streaming=False))
        #source.play()

        player.addItem(itemToGet)
        holder.removeItem(self)

        if (player.mainHand == None) and (isinstance(itemToGet, Weapon)):
            itemToGet.equip(player)
        return resultString, True, sources
    
    def drop(self, player):
        if (self.quantity > 1) and (not self.stackable):
            itemToDrop = copy.deepcopy(self)
            itemToDrop.quantity = 1
        else:
            itemToDrop = self

        player.removeItem(self)
        player.currentLocation.addItem(itemToDrop)
        resultString = "You drop the " + self.name
        if self.quantity > 1 and self.stackable:
            resultString += "(" + str(self.quantity) + ")"
        return resultString,True
    
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
        if not(self.keywords in player.inventory):
            return "I need to pick it up first."

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

        super(Weapon, self).__init__(name, description, seenDescription, keywords, **kwargs)
        
    def equip(self, player):
        if not(self.keywords in player.inventory):
            return "I need to pick it up first."

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
        self.reloadSound = None
        self.emptySound = "Sounds/Combat/EmptyGun.mp3"
        self.rangeMod = [0,5,10,15]
        self.attackDesc = "You open fire!"

        super(RangedWeapon, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)
                            #Me name es Wayne Purkle coz when I nommin' grapes day be PURKLE!!!
    def attack(self, enemy, player, attackType):
        if isinstance(enemy, Enemies.Enemy):
            sources = list()
            if attackType == "heavy":
                return "You are not holding a melee weapon."
            
            if self.ammoRemaining <= 0:
                sources.append(pyglet.media.load(self.emptySound, streaming=False))
                #source.play()
                return "You pull the trigger but nothing happens. Shit, it's empty...", True, sources
            
            if self.fireSound:
                sources.append(pyglet.media.load(self.fireSound, streaming=False))
                #source.play()
            
            self.ammoRemaining -= 1
            hitChance = self.accuracy
            
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
            else:
                hitChance -= enemy.rangedDodge
                
            if hitChance < 5:
                hitChance = 5
                
            attackRoll = randint(0, 100)
            if attackRoll <= hitChance:
                attackResult = enemy.takeHit(player, self, "ranged")
                try:
                    resultString, enemySources = attackResult
                    sources += enemySources
                except ValueError:
                    resultString = attackResult
            else:
                resultString = self.attackDesc
                resultString += "\nYou miss!"
            return resultString, True, sources
        else:
            return "That isn't worth wasting ammo on..."

    def shoot(self, enemy, player):
        return self.attack(enemy, player)
    
    def reload(self, player):
        sources = list()
        for item in player.inventory.itervalues():
            try:
                weaponType = item.weaponType
            except AttributeError:
                continue
            
            if self.name == weaponType:
                self.ammoRemaining = self.capacity
                item.destroy(player)
                if self.reloadSound:
                    sources.append(pyglet.media.load(self.reloadSound, streaming=False))
                    #source.play()

                return "You reload the " + self.name + ".",True, sources
            
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
        self.defenseBonus = 0
        self.stunChance = 20
        self.hitSound = None
        self.missSound = "Sounds/Combat/MeleeMiss.mp3"
        self.attackDesc = "You swing your weapon!"
        
        super(MeleeWeapon, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)   

    def attack(self, enemy, player, attackType):
        if isinstance(enemy, Enemies.Enemy):
            sources = list()
            if enemy.distanceToPlayer > 1:
                return "You are not within striking distance."

            hitChance = self.accuracy
            #print "Initial hit chance: " + str(hitChance)
            
            if player.intoxication > 75:
                hitChance -= 20
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
                hitChance -= 25
                #print "Heavy attack penalty. New hit chance: " + str(hitChance)
            
            if enemy.helpless:
                hitChance = 100
            elif enemy.stunnedTimer > 0:
                hitChance += 15
                #print "Enemy stunned bonus. New hit chance: " + str(hitChance)
            else:
                hitChance -= enemy.meleeDodge
                #print "enemy dodge penalty. New hit chance: " + str(hitChance)
            
            if hitChance < 10:
                hitChance = 10
            attackRoll = randint(0, 100)
            #print "Final hit chance: " + str(hitChance)
            #print "Attack roll: " + str(attackRoll)
            if attackRoll <= hitChance:
                if self.hitSound:
                    sources.append(pyglet.media.load(self.hitSound, streaming=False))
                    #source.play()
                attackResult = enemy.takeHit(player, self, "ranged")
                try:
                    resultString, enemySources = attackResult
                    sources += enemySources
                except ValueError:
                    resultString = attackResult
            else:
                resultString = self.attackDesc
                resultString += "\nYou miss!"
                if self.missSound:
                    sources.append(pyglet.media.load(self.missSound, streaming=False))
                    #source.play()
            return resultString, True, sources
        else:
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

        kwargs.update({
            "useSound":"Sounds/Misc/LiquorDrink.mp3"
        })

        super(Alchohol, self).__init__(name, description, seenDescription, keywords, useDescription, **kwargs)
        
    def drink(self, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]

        sources = list()

        sources.append(pyglet.media.load(self.useSound, streaming=False))
        #source.play()
        player.increaseIntox(self.alcoholAmount)
        spiritDecrease = self.alcoholAmount / 2
        if spiritDecrease > 10:
            spiritDecrease = 10
        player.decreaseSpirit(spiritDecrease)
        self.currentLocation.removeItem(self)

        return self.useDescription,True, sources
    

class Readable(Item):
    
    def __init__(self, name, description, seenDescription, keywords, **kwargs):
        super(Readable, self).__init__(name, description, seenDescription, keywords, **kwargs)
            
    def read(self):
        pass

class Note(Readable):
    
    def __init__(self, name, description, seenDescription, keywords, contents, **kwargs):
        self.contents = contents

        kwargs.update({
            "pickupSound":["Sounds/Misc/PaperGet1.mp3","Sounds/Misc/PaperGet2.mp3","Sounds/Misc/PaperGet3.mp3"]
        })
        super(Note, self).__init__(name, description, seenDescription, keywords, **kwargs)
    
    def read(self, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]
        
        sources.append(pyglet.media.load(self.pickupSound[randint(0, len(self.pickupSound) - 1)], streaming=False))
        #source.play()

        return self.contents,True, sources

class Key(Item):
    def __init__(self, name, description, seenDescription, keywords, **kwargs):

        kwargs.update({
            "pickupSound":["Sounds/Misc/KeyGet.mp3"]
        })

        super(Key, self).__init__(name, description, seenDescription, keywords, **kwargs)
    
    def use(self, player):
        return "Use the key on what?"
    
    def useOn(self, player, recipient):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]
                
        try:
            if recipient.isAccessible:
                return recipient.tryLock(self, player)
            else:
                return recipient.tryUnlock(self, player)
        except AttributeError:
            return "It doesn't have a lock to put the key in..."

class Corpse(Item):
    def __init__(self, name, description, seenDescription, keywords, **kwargs):
        self.itemsContained = {}
        super(Corpse, self).__init__(name, description, seenDescription, keywords, **kwargs)
    
    def get(self, holder, player):
        return "I've no desire to carry around a corpse."

    def wear(self, player):
        return "Assuming you could even lift that, you doubt wearing a corpse will improve your fighting ability much."

    def equip(self, player):
        return "Though the idea of beating a demon to death with a dead body is incredibly metal, it doesn't seem very practical."

    def addItem(self, itemToAdd):
        if itemToAdd.keywords in self.itemsContained:
            if itemToAdd.stackable:
                self.itemsContained[itemToAdd.keywords].quantity += itemToAdd.quantity
            else:
                self.itemsContained[itemToAdd.keywords].quantity += 1
        else:
            self.itemsContained[itemToAdd.keywords] = itemToAdd
            itemToAdd.currentLocation = self

    def removeItem(self, itemToRemove):
        if (self.itemsContained[itemToRemove.keywords].quantity > 1) and (not itemToRemove.stackable):
            self.itemsContained[itemToRemove.keywords].quantity -= 1
        else:
            del self.itemsContained[itemToRemove.keywords]
            itemToRemove.currentLocation = None

    def search(self, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]
            elif self.currentLocation in enemy.protectedThings:
                return enemy.protectedThings[self.currentLocation]

        itemsToRemove = []
        resultString = "You look the body over."
        if self.itemsContained:
            for item in self.itemsContained.itervalues():    #Display all the visible items
                if item.firstSeen and item.initSeenDesc:
                    resultString += "\n" + item.initSeenDesc
                elif item.firstTaken and item.notTakenDesc:
                    resultString += "\n" + item.notTakenDesc
                else:
                    resultString += "\n" + item.seenDescription

                if item.quantity > 1:
                    resultString += " (" + str(item.quantity) + ")"
                item.firstSeen = False

                self.currentLocation.addItem(item)
                itemsToRemove.append(item.keywords)

            for keywords in itemsToRemove:
                del self.itemsContained[keywords]
        else:
            resultString += "\nYou don't find anything of interest."

        return resultString, True