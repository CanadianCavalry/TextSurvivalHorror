'''
Created on Jan 23, 2015

@author: CanadianCavalry
'''
import Enemies
import Items
from random import randint

class Hellhound(Enemies.Enemy):    
    def __init__(self):
        name = "Hellhound"
        description = "A massive canine the size of a horse. Most of it's skin is missing, showing muscle and sinew under tufts "
        "of bloodstained fur. It's milky white eyes stare blankly ahead while it's nose sniffs endlessly. Jagged shards of bone "
        "protrude from it's form all over, and between that and the enormous jaws it would clearly be a mistake to let this thing "
        "anywhere near you."
        seenDesc = "A massive Hellhound is in the room, growling at you."
        keywords = "dog,hound,hellhound,hell hound,huge dog,big dog,huge hound,big hound"
        maxHealth = 160
        minDamage = 38
        maxDamage = 46
        accuracy = 90
        corpse = Items.Corpse(
            "Hellhound Corpse", "There's so much blood and broken bones that it's almost impossible to tell which wounds killed "
            "it and which it already had. There is a growing pool of blood underneath it, and the smell is even worse than you expected.",
            "A blood smeared hellhound corpse is lying on the floor.", 
            "body,corpse,hellhound,hellhound body,dead hellhound,hellhound corpse")
        
        kwargs = {
            "speed":1, 
            "meleeDodge":0,
            "rangedDodge": 5,
            "baseExorciseChance":-100,
            "stunChance":10,
            #"isBlockingExit":True,
            "defaultStunDesc":"The hellhound is slowly staggering back to it's feet.",
            "attackDesc": ["The hellhound leaps towards you, trying to tear into you with it's jaws.", "The hellhound snarls and snaps at you."],
            "firstSeenDesc":"As you walk forward you hear a loud crunching noise from up ahead. You round a shelf to find a massive canine creature at least 2 meters tall at the shoulders, covered in open wounds and bits of protruding bone. It's standing over a mangled corpse, it's head buried in the bloody entrails, as wet crunching and tearing noises fill the room.\nThe creature pauses, sniffing the air for a moment, before turning towards you with a deep, unnatural growl.",
            "firstSeenSound":"Sounds/Monsters/HellhoundGrowl.mp3",
            "deathSound":"Sounds/Monsters/HellhoundDeath.mp3",
            "advanceDialogue":["The massive canine tears towards you, barking.", "The hellhound bolts straight at you with a deep growl."],
            "retreatDialogue":["The beast dashes away, yelping."],
            "deathText":"The hellhound crashes to the floor and lies still.",
            "travelDesc":"The hellhound tears into the room after you, right on your heels."
        }

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

class BentHost201(Enemies.Enemy):
    
    def __init__(self):
        self.busyStateDesc = ["BANG! BANG! Wood splinters everywhere and the padlock flies off as a huge hole is blasted through your door! The security guard Joe appears with a magnum in his hand.",
                              "The possessed man drops his knife and rushes towards Joe. Without hesitating, Joe fires two shots clean through his torso, and the lunatic howls in agony.",
                               "Somehow, the possessed man manages to stay on his feet. He wrestles Joe to the ground, quickly grabbing Joe's magnum and throwing it through your glass window. You hear the window shatter but oddly don't hear the heavy gun hit the ground...",
                               "Seizing Joe in a submission hold, the possessed man grabs Joe's head and snaps it to the side, killing him instantly. JOE WAS MY FRIEND, YOU SON OF A BITCH!!!",
                               "The lunatic clutches the two huge holes in his torso, and collapses to the ground with a loud thud. You think he must be in shock..."
                               "The possessed man slowly staggers to his feet. He turns towards you, and approaches you with a growl."
                               ]
        self.busyTimer = 0
        name = "Bent Host"
        description = "This huge, fat man wears a large, bloodstained apron and is looking at you with a deeply unsettling expression. You're quite certain he's possessed.."
        seenDesc = "A grinning maniac stands next to your bed, smiling at you."
        keywords = "maniac,man,bent host,host,enemy"
        maxHealth = 30
        minDamage = 5
        maxDamage = 7
        accuracy = 40
        speed = 1
        dodgeChance = 5
        armor = 0
        self.talkCount = 0
        self.minorTortures = []
        self.majorTortures = []
        super(BentHost201, self).__init__(name, description, seenDesc, keywords, maxHealth, minDamage, maxDamage, accuracy, speed, dodgeChance, armor)
        
        self.addMinorTorture(self.minorTortureOne)
        self.addMinorTorture(self.minorTortureTwo)
        self.addMinorTorture(self.minorTortureThree)
        self.addMajorTorture(self.minorTortureOne)
        self.setDistance(1)
        self.setExorciseDialogue(["You roar out. \"GO BACK TO THE FILTH AND MISERY OF HELL!\")","\"IN THE NAME OF CHRIST JESUS, DEPART THIS MAN AT ONCE!\", you scream with righteous fury.", "\"COME OUT, WORTHLESS PARASITE!\", you roar."])
        self.setTalkDialogue(["He peers down at you with a maniacal grin you know all too well. \"Hello, exorcist! Do you remember me? I remember you!\"",
                              "I've been waiting so long to see you again! What a wonderful day.",
                              "\"Enough talk, we have work to do!\" The demon exclaims. He back hands you across the face"])
                                     
    def attack(self, player):
        if self.enemyState == 2:
            self.seenDesc = "A bent host is staggering towards you, clutching his chest."
            if player.isRestricted:
                return self.execute(player)
            else:
                return self.basicAttack(player)
        
        elif self.enemyState == 1:
            if self.busyTimer == 0:
                self.seenDesc = "The possessed man is struggling with Joe."
            elif self.busyTimer == 4:
                self.seenDesc = "The host is sitting on the floor in a daze, though likely not for long."
            result = self.busyStateDesc[self.busyTimer]
            if self.busyTimer == 6:
                if player.isRestricted():
                    return self.execute(player)
                self.setState(2)
                return self.attack(player)
            self.busyTimer += 1
            return result
        
        elif self.enemyState == 0:
            if player.health <= 50:
                self.enemyState += 1
                self.currentLocation.changeState()
                return self.attack(player)
            if player.lastAction in ["get","attack"]:
                return self.performMajorTorture(player)
            else:
                return self.performMinorTorture(player)
        
    def playerAdvances(self):
        if self.enemyState == 0:
            return "I'm still tied to this damn table."
        if self.distanceToPlayer <= 1:
            return "You are already right in front of it!"
        else:
            self.distanceToPlayer -= 1
            return "You advance on the " + self.name, True
        
    def playerRetreats(self):
        if self.enemyState == 0:
            return "I'm still tied to this damn table."
        if self.distanceToPlayer >= 3:
            return "Your back is to the wall."
        else:
            self.distanceToPlayer -= 1
            return "You retreat from the " + self.name, True
            
    def performMinorTorture(self, player):
        return self.minorTortures[randint(0,len(self.minorTortures) - 1)](player)
    
    def performMajorTorture(self, player):
        return self.majorTortures[randint(0,len(self.majorTortures) - 1)](player)
    
    def addMinorTorture(self, method):
        self.minorTortures.append(method)
        
    def addMajorTorture(self, method):
        self.majorTortures.append(method)
        
    def removeMinorTorture(self, index):
        del self.minorTortures[index]
    
    def removeMajorTorture(self, index):
        del self.majorTortures[index]
    
    def execute(self, player):
        player.takeDamage(100)
        return "\"FUCK YOUR FUCKING GOD!\", he roars at you. \
He falls upon you like a hurricane, completely enraged. \"YOU DIE HERE, FALSE PRIEST!\" he roars. As he wraps his meaty hands around your throat and begins to choke you, you can feel him kneeing you in the groin again and again and biting you so hard he actually takes chunks out of your body. Mercifully, you die quickly."
        
    def minorTortureOne(self, player):
        player.takeDamage(10)
        return "Using the pliers, the maniac pulls off one of your fingernails, smiling at you the entire time."
    
    def minorTortureTwo(self, player):
        player.takeDamage(10)
        return "You scream as the man carves a deep slice on your torso with the knife. The sound makes him giggle."
    
    def minorTortureThree(self, player):
        player.takeDamage(10)
        return "The lunatic slams you across the skull with the trephine."
    
    def majorTortureOne(self, player):
        player.takeDamage(20)
        return "He sticks one of the fish hooks into you, then rips it out, taking out a large chunk of flesh."
    
    def majorTortureTwo(self, player):
        player.takeDamage(20)
        return "You howl in agony as he wraps the serrated metal wire around your torso and pulls with all his might!"
    
    def exorciseAttempt(self, player):
        if self.enemyState == 0:
            resultString = "You take a ragged breath and muster what faith you can.\n" + self.exorciseDialogue[randint(0, len(self.exorciseDialogue) - 1)] + "\n"
            resultString += "The demon writhes in pain and screams out, \"STOP TORTURING US, SON OF MAN!\", however it quickly recovers. "
            resultString += self.execute(player)
            return resultString
        
        resultString = "You draw upon your faith to banish the demon. You yell out:\n" + self.exorciseDialogue[randint(0, len(self.exorciseDialogue) - 1)] + "\n"
        
        hitChance = self.baseExorciseChance
        hitChance += (player.spirit - 50)
        attackRoll = randint(0, 100)
        if attackRoll <= hitChance:
            resultString += "The demon writhes in pain and screams out, \"STOP TORTURING US, SON OF MAN!\", however it quickly recovers. "
            resultString += self.takeExorcise()
            return resultString
        else:
            resultString += "It doesn't seem to have any effect."
            return resultString
        
    def takeHit(self, weapon, attackType):
        if self.busyTimer <= 6:
            self.busyTimer = 6
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
    
    def talk(self, player): #Need to remove and put in seklf.talkDialogue
        if self.talkCount == len(self.talkDialogue) - 1:
            player.takeDamage(5)
        return super(BentHost201, self).talk()