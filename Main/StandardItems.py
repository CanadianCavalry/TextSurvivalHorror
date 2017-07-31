'''
Created on Jul 5, 2014

@author: Thomas
'''
import Items
import AreasFeatures

#Melee Weapons
class Axe(Items.MeleeWeapon):
    
    def __init__(self, **kwargs):
        name="Axe"
        description="A long handled fire axe, intended for emergency use. The current situation probably qualifies. It's heavy and unwieldy, and will seriously ruin the day of anyone on the recieving end."
        seenDescription="A fire axe is lying on the floor."
        keywords="axe,fire axe,weapon"
        minDamage=18
        maxDamage=23
        accuracy=75
        size=2

        kwargs.update({
            "stunChance":25, 
            "notTakenDesc":"A long-handled fire axe is lying across the table.",
            "initPickupDesc":"You lift the axe from the table. It has a weight and heft that is comfortable in your hands.",
            "stunlength": 2,
            "defenseBonus":5
        })

        super(Axe, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)

class LongSword(Items.MeleeWeapon):
    
    def __init__(self, **kwargs):
        name="Long Sword" 
        description="A long bladed medieval weapon, excellent for slaying men, demons and ferocious rabbits. It's suprisingly light for it's size."
        seenDescription="A long sword is lying on the floor."
        keywords="sword,long sword,blade"
        minDamage=16
        maxDamage=21
        accuracy=85
        size=2

        kwargs.update({
            "stunChance":20,
            "initSeenDesc":"A large sword has been thrust into wooden floor here. It seems to glow faintly at first, then fades.",
            "notTakenDesc":"A large sword has been thrust into wooden floor here.",
            "initPickupDesc":"With considerable effort, you pull the blade free from the ground. It's lighter than you expected.",
            "stunlength": 2,
            "defenseBonus":10,
            "attackDesc":"You swing your blade."
        })

        super(LongSword, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)
        
#class Scalpel(Items.MeleeWeapon):
#    
#    def __init__(self):
#        super(Scalpel, self).__init__("Scalpel201", "A common surgical tool. Sharp and lightweight, but its small size and tiny reach make it a poor weapon.", 
#                                      "A scalpal is lying on the ground.", 1, "scalpal", 5, 11, 1, 60, 15, 0)
        
class KitchenKnife(Items.MeleeWeapon):
    
    def __init__(self, **kwargs):
        name="Kitchen Knife" 
        description="A 12 inch chefs knife. You know what they say: 'Guns are for show, knives are for pro.'"
        seenDescription="A knife is lying on the floor."
        keywords="knife,kitchen knife,weapon,blade"
        minDamage=13
        maxDamage=18
        accuracy=95
        size=1

        kwargs.update({
            "stunChance":5,
            "notTakenDesc":"A kitchen knife is lying on the table.",
        })

        super(KitchenKnife, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, **kwargs)
        
#Ranged Weapons
class Revolver(Items.RangedWeapon):

    def __init__(self, **kwargs):
        name="Revolver"
        description="A heavy .457 magnum revolver. It holds 6 rounds."
        seenDescription="A revolver is lying on the floor."
        keywords="gun,handgun,pistol,revolver,magnum"
        minDamage=30
        maxDamage=38
        size=1
        accuracy=75
        capacity=6

        kwargs.update({
            "ammoRemaining":4,
            "fireSound":"Sounds/Combat/RevolverShot.mp3",
            "reloadSound":"Sounds/Combat/RevolverReload.mp3", 
            "notTakenDesc":"A revolver rests in the corner of the table.",
            "initPickupDesc":"It's heavier than it looks. You look it over to ensure the safety is off. Let's hope it still fires.",
            "attackDesc":"You open fire with your revolver."
        })
        
        super(Revolver, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, capacity, **kwargs)

class Crossbow(Items.RangedWeapon):

    def __init__(self, **kwargs):
        name="Crossbow"
        description="A wood and steel crossbow, straight out of the middle ages. Despite the obvious wear from excessive use, it appears to be very well maintained. It is considerably smaller than most, and as such is much easier to reload."
        seenDescription="A crossbow is lying on the floor."
        keywords="crossbow,worn crossbow"
        minDamage=70
        maxDamage=85
        size=2
        accuracy=90
        capacity=1

        kwargs.update({
            "ammoRemaining":1,
            "fireSound":"Sounds/Combat/CrossbowShot.mp3", 
            "notTakenDesc":"A crossbow rests on a display next to the door.",
            "initPickupDesc":"It's nowhere near as bulky as most weapons of this type. The string is oiled and the mechanism appears to have been recently cleaned.  You sling it over your shoulder.",
            "attackDesc":"You carefully line up your crossbow, and fire."
        })
        
        super(Crossbow, self).__init__(name, description, seenDescription, keywords, minDamage, maxDamage, accuracy, size, capacity, **kwargs)

#Ammo
class RevolverAmmo(Items.Ammo):
    def __init__(self, **kwargs):
        name="Revolver Ammo"
        description="A speed-loader for a six shot revolver. It is filled with .457 ammunition."
        seenDescription="A speed-loader is on the ground."
        keywords="ammo,revolver ammo,magnum ammo,ammunition,revolver ammunition,speed-loader,speed loader,bullets,speedloader"
        weaponType="Revolver"

        kwargs.update({
            "stackable":True
        })

        super(RevolverAmmo, self).__init__(name, description, seenDescription, keywords, weaponType, **kwargs)

class CrossbowBolt(Items.Ammo):
    def __init__(self, **kwargs):
        name="Crossbow Bolt"
        description="A steel crossbow bolt. The head appears to be made from silver."
        seenDescription="A crossbow bolt is on the ground."
        keywords="ammo,crossbow ammo,crossbow bolt,bolt,ammunition,crossbow ammunition"
        weaponType="Crossbow"

        kwargs.update({
            "stackable":True
        })

        super(CrossbowBolt, self).__init__(name, description, seenDescription, keywords, weaponType, **kwargs)


#Armor
class LeatherJacket(Items.Armor):
    def __init__(self, **kwargs):
        name="Leather Jacket"
        description="An old, faded brown leather jacket. I've had this for longer than I can remember."
        seenDescription="A faded leather jacket is on the floor."
        keywords="armor,jacket,leather jacket"
        armorRating=10

        kwargs.update({
            "initPickupDesc":"It's old and weatherbeaten, and looks like it's been patched extensively, but it should provide a bit of protection at least.",
            "notTakenDesc":"A faded leather jacket is hanging off one of the cages."
        })

        super(LeatherJacket, self).__init__(name, description, seenDescription, keywords, armorRating, **kwargs)

#Consumables
class Flask(Items.Alchohol):
    def __init__(self, **kwargs):
        name="Flask of Scotch"
        description="A small silver flask which holds about 4 oz. I received this as a gift from a friend form church before they realized I had a problem. I'm sure they regretted giving it to me once they found out."
        seenDescription="There is a small silver flask on the floor."
        keywords="flask,whiskey,scotch,silver flask,flask of scotch,alcohol,booze"
        useDescription="You unscrew the cap and drain the remaining liquid from the flask. Delicious."
        alcoholAmount=10

        kwargs.update({
            "initPickupDesc":"By some miracle it's still about half full. You can almost feel the contents calling you."
        })

        super(Flask, self).__init__(name, description, seenDescription, keywords, useDescription, alcoholAmount, **kwargs)

class FirstAidKit(Items.Usable):
    def __init__(self, **kwargs):
        name="First Aid Kit"
        description="A small, self contained medical kit with bandages, painkillers, antiseptic, closures and gauze. You could treat most minor wounds with this, but it's small size means there is not a lot to it. It will only be good for a single treatment."
        seenDescription="A small first aid kit is on the floor."
        keywords="first aid kit,first aid,kit,medical kit,medkit,healing"
        useDescription="You lay out the kit and get to work. You manage to do a decent job with the paltry supplies, and clean up your wounds as best you can. By the time you're finished, there's nothing useful left in the kit."

        kwargs.update({
            "stackable":True,
            "initPickupDesc":"It's small, but it's got the most important items for trauma care. It's been a while since you had to stich anyone up, so hopefully you remember what you're doing."
        })

        super(FirstAidKit, self).__init__(name, description, seenDescription, keywords, useDescription, **kwargs)

    def use(self, player):
        if player.currentLocation.enemies:
            return "You can't perform first aid when an enemy is nearby."
        if player.health == 100:
            return "You don't have any wounds that need attention."
        
        player.heal(40)
        del player.inventory[self.keywords]
        return self.useDescription, True

#Misc
class Key(Items.Usable):
    
    def use(self, player):
        return "Use the key on what?"
    
    def useOn(self, player, recipient):
        if (isinstance(recipient, AreasFeatures.Door)) or (isinstance(recipient, AreasFeatures.Container)):
            return recipient.unlock(self)
        else:
            return "It doesn't have a lock to put the key in..."