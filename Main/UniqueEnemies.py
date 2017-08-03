'''
Created on Jan 23, 2015

@author: CanadianCavalry
'''
import Enemies
import Items
from random import randint

class Hellhound(Enemies.Enemy):    
    def __init__(self, **kwargs):
        name = "Hellhound"
        description = (["A massive canine the size of a horse. Most of it's skin is missing, showing muscle and sinew under tufts "
        "of bloodstained fur. It's milky white eyes stare blankly ahead while it's nose sniffs endlessly. Jagged shards of bone "
        "protrude from it's form all over, and between that and the enormous jaws it would clearly be a mistake to let this thing "
        "anywhere near you."])
        seenDesc = "A massive Hellhound is in the room, growling at you."
        keywords = "enemy,dog,hound,hellhound,hell hound,huge dog,big dog,huge hound,big hound"
        maxHealth = 160
        minDamage = 24
        maxDamage = 29
        accuracy = 90
        corpse = Items.Corpse(
            "Hellhound Corpse", 
            "There's so much blood and broken bones that it's almost impossible to tell which wounds killed "
            "it and which it already had. There is a growing pool of blood underneath it, and the smell is even worse than you expected.",
            "A blood smeared hellhound corpse is lying on the floor.", 
            "body,corpse,hellhound,hellhound body,dead hellhound,hellhound corpse,dead hound,hound,dead dog,dog")
        
        kwargs.update({
            "speed":1, 
            "meleeDodge":0,
            "rangedDodge": 5,
            "baseExorciseChance":-100,
            "stunResist":10,
            "defaultStunDesc":"The hellhound is slowly staggering back to it's feet.",
            "attackDesc": ["The hellhound leaps towards you, trying to tear into you with it's jaws.", "The hellhound snarls and snaps at you."],
            "firstSeenDesc":"As you walk forward you hear a loud crunching noise from up ahead. You round a shelf to find a massive canine creature at least 2 meters tall at the shoulders, covered in open wounds and bits of protruding bone. It's standing over a mangled corpse, it's head buried in the bloody entrails, as wet crunching and tearing noises fill the room.\nThe creature pauses, sniffing the air for a moment, before turning towards you with a deep, unnatural growl.",
            "firstSeenSound":"Sounds/Monsters/HellhoundGrowl.mp3",
            "deathSound":"Sounds/Monsters/HellhoundDeath.mp3",
            "advanceDialogue":["The massive canine tears towards you, barking.", "The hellhound bolts straight at you with a deep growl."],
            "retreatDialogue":["The beast dashes away, yelping."],
            "deathText":"The hellhound crashes to the floor and lies still.",
            "travelDesc":"The hellhound tears into the room after you, right on your heels."
        })

        super(Hellhound, self).__init__(name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, corpse, **kwargs)

    def takeCrit(self, weapon):
        self.health = 0
        self.kill()
        if weapon.name == "Axe":
            return "You stand oven the thrashing, flailing hellhound, axe held high above you. You mumble a prayer under your breath before bringing the weapon down on it's neck. The beasat let's out a sharp yelp and jerks suddenly, before finally emitting a low whimper and going limp."
        elif weapon.name == "Kitchen Knife":
            return "You wait for an opening between the hounds flailing attempts to rise, then dash forward, thrusting the knife towards it's head. The blade finds it's eye, driving in deep and drawing a pained scream from the canine, before it goes limp."
        elif weapon.name == "Long Sword":
            return "Acting quickly, you come along side the thrashing hellhound. You wait for an opening between it's frantic twisting and thrashing, then quickly reverse your grip on the sword, plunging it down into the things side. The tip finds what passes for the hounds heart, and with a final yelp it lies still."
        else:
            return "You kick the stunned creature hard in the chest, knocking it to the ground. You fall upon it with your weapon, striking over and over until it lies still."

    def hitEffect(self, player, weapon, attackType):
        if isinstance(weapon, Items.MeleeWeapon):
            player.takeDamage(randint(7,10))
            return "\nAs you hit the Hellhound, you cut yourself on the jagged bone spikes.\nYou are " + player.getCondition() + "."

class BentHost(Enemies.Enemy):    
    def __init__(self, **kwargs):
        name = "Bent Host"
        description = (["A twisted, tortured human posessed by a demonic entity. Though incapable of controlling their bodies, "
            "these \'bent hosts\' are fully aware and forced to spectate while their captor does what it wishes. They tend to be "
            "clumsy and have little regard for their own safety, but should not be underestimated."])
        seenDesc = "A wounded, blood soaked man carrying a pair of scissors is here with you."
        keywords = "enemy,host,man,bent host,possessed,possessed man,lunatic,maniac,demon"
        maxHealth = 40
        minDamage = 10
        maxDamage = 14
        accuracy = 70
        corpse = Items.Corpse(
            "Human Corpse", 
            "The demon has left this host. It's unfortunate what you had to do, but at least he can rest now.",
            "The bloody remains of a demonic host is lying on the floor.", 
            "body,corpse,human,human body,dead human,human corpse,dead host,host,host corpse,dead demon,demon,demon corpse")
        
        kwargs.update({
            "speed":1,
            "meleeDodge":0,
            "rangedDodge": 0,
            "baseExorciseChance":25,
            "stunResist":-10,
            "defaultStunDesc":"The demonic host is stumbling around, dazed.",
            "defaultRecoveryDesc":"The bent host snaps back to it's senses.",
            "attackDesc": ["The host swings it's weapon at you.", "The host lunges towards you with it's blade."],
            "takeExorciseDesc":["It works! The hosts eyes roll back in it's head and it collapses to the ground. You'll need to complete the exorcism to free the host from it's demonic captor."],
            "advanceDialogue":["The demonic host stumbles towards you, giggling to itself.", "The host suddenly let's loose a scream and breaks into a wild sprint towards you.", "The possessed human walks towards you silently.", "The possessed has trouble keeping it's balance and stumbles forward."],
            "retreatDialogue":["The host stumbles backwards, trying to get away from you.", "The demonic host scrabbles away from you."],
            "deathText":"The demonic host falls to the ground dead.",
            "travelDesc":"The possessed human bursts into the room."
        })

        super(BentHost, self).__init__(name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, corpse, **kwargs)

    def takeCrit(self, weapon):
        self.health = 0
        self.kill()
        if weapon.name == "Axe":
            return "You stand oven the prone host and whisper an apology. You bring the axe down hard with a solid thunk, and they cease to move."
        elif weapon.name == "Kitchen Knife":
            return "With a whispered prayer, you seize the host by the hair and lift their head. In a single motion you draw the knife across their throat, leaving them to cough and sputter on the floor. After a few seconds, they lie still."
        else:
            return "You kick the stunned creature hard in the chest, knocking it to the ground. You fall upon it with your weapon, striking over and over until it lies still."
