'''
Created on Jul 5, 2014

@author: Thomas
'''
import Items
import AreasFeatures

#Melee Weapons
class Axe(Items.MeleeWeapon):
    
    def __init__(self):
        super(Axe, self).__init__("Axe", "A long handled fire axe, intended for emergency use. The current situation probably qualifies. It's heavy and unwieldy, and will seriously ruin the day of anyone on the recieving end.",
                                   "A fire axe is lying on the floor.", 1, "axe,fire axe,weapon", 17, 22, 2, 75, 10, 3)

class LongSword(Items.MeleeWeapon):
    
    def __init__(self):
        super(LongSword, self).__init__(
            "Long Sword", 
            "A long bladed medieval weapon, excellent for slaying men, demons and ferocious rabbits. It's suprisingly light for it's size.",
            "A long sword is lying on the floor.",
            1, 
            "sword,long sword,blade", 
            15, 
            20, 
            2, 
            90, 
            15, 
            2, 
            "A large sword has been thrust into wooden floor here. It seems to glow faintly at first, then fades.", 
            "A large sword has been thrust into wooden floor here.", 
            "With considerable effort, you pull the blade free from the ground.")
        
class Scalpel(Items.MeleeWeapon):
    
    def __init__(self):
        super(Scalpel, self).__init__("Scalpel201", "A common surgical tool. Sharp and lightweight, but its small size and tiny reach make it a poor weapon.", 
                                      "A scalpal is lying on the ground.", 1, "scalpal", 5, 11, 1, 60, 15, 0)
        
class KitchenKnife(Items.MeleeWeapon):
    
    def __init__(self):
        super(KitchenKnife, self).__init__("Kitchen Knife", "A 12 inch chefs knife. You know what they say: 'Guns are for show, knives are for pro.'",
                                   "A knife is lying on the floor.", 1, "knife,chef knife,weapon", 9, 14, 1, 75)
        
#Ranged Weapons
class Revolver(Items.RangedWeapon):
    
    def __init__(self):
        super(Revolver, self).__init__("Revolver", "A heavy .457 revolver. It holds 6 rounds.", "A revolver is lying on the floor.",
                                        1, "gun,handgun,pistol,revolver", 30, 38, 1, 70, 6, 4, "Sounds/RevolverShot.mp3", 10, "","","","You open fire with your revolver.")

#Ammo
class RevolverAmmo(Items.Ammo):
    
    def __init__(self):
        super(RevolverAmmo, self).__init__("Revolver Ammo", "A speed-loader for a six shot revolver. It is filled with .457 ammunition.", "A speed-loader is on the ground.",
                                           1, "ammo,revolver ammo,magnum ammo,ammunition,revolver ammunition,speed-loader,speed loader", "Revolver")

#Armor
class LeatherJacket(Items.Armor):
    
    def __init__(self):
        super(LeatherJacket, self).__init__("Leather Jacket", "An old, faded brown leather jacket. I've had this for longer than I can remember.",
                                            "A faded leather jacket is on the floor.", 1, "armor,jacket,leather jacket", 5)

#Consumables
class Alchohol(Items.Drinkable):
    
    def __init__(self, name, description, seenDescription, quantity, keywords, useDescription, alcoholAmount, pickupDesc="", initPickupDesc="", initSeenDesc=""):
        self.alcoholAmount = alcoholAmount
        super(Alchohol, self).__init__(name, description, seenDescription, quantity, keywords, useDescription, pickupDesc, initPickupDesc, initSeenDesc)
        
    def drink(self, player):
        player.increaseIntox(self.alcoholAmount)
        spiritDecrease = self.alcoholAmount / 2
        if spiritDecrease > 10:
            spiritDecrease = 10
        player.decreaseSpirit(spiritDecrease)
        player.removeItem(self)
        return self.useDescription,True
    
#Misc
class Key(Items.Usable):
    
    def use(self):
        return "Use the key on what?"
    
    def useOn(self, player, recipient):
        if (isinstance(recipient, AreasFeatures.Door)) or (isinstance(recipient, AreasFeatures.Container)):
            return recipient.unlock(self)
        else:
            return "It doesn't have a lock to put the key in..."
        
class Note(Items.Readable):
    
    def __init__(self, name, description, seenDescription, quantity, keywords, contents, pickupDesc="", initPickupDesc="", initSeenDesc=""):
        self.contents = contents
        super(Note, self).__init__(name, description, seenDescription, quantity, keywords, pickupDesc, initPickupDesc, initSeenDesc)
    
    def read(self):
        return self.contents,True
    
class Book(Items.Readable):
    
    def __init__(self, name, description, seenDescription, quantity, keywords, pickupDesc="", initPickupDesc="", initSeenDesc=""):
        self.pages = []
        super(Book, self).__init__(name, description, seenDescription, quantity, keywords, pickupDesc, initPickupDesc, initSeenDesc)
        
    def read(self):
        for page in self.pages:
            print page.contents
            raw_input("Press Enter to continue...")
        return "That's the last page.",True
            
    def addPage(self, page):
        self.pages.append(page)
        
class Page(object):
    
    def __init__(self,contents):
        self.contents = contents
        