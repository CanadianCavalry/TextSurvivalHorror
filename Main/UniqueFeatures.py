'''
Created on Jul 5, 2014

@author: Thomas
'''
import AreasFeatures
import StandardFeatures

class TutorialExitGate(StandardFeatures.StandardLockingDoor):
    def __init__(self, itemToOpen):
        description = [("A massive gate carved from some unknown metal, or maybe stone? It's hard to be sure, as looking at it for too long makes your "
        "head hurt. It's covered with intricate carvings of demonic creatures and symbols, which you swear move around when you look "
        "away. There is no visible handle, only a single keyhole in the center. You can faintly hear it whispering your name."),
        ("The gate has opened, leaving a black curtain of liquid darkness. You can make out absolutely nothing through the veil, which "
        "seems to twist and writhe.")]
        keywords = "gate,exit,north,north gate,north door,door,demon gate,demon door,portal,south portal"
        isAccessible = False
        keyRequired = True

        kwargs = {
            "unlockDesc":"As you turn the key in the lock, the gate silents swings open of it's own accord. You are greeted by a sheet "
            "of inky blackness, darkness given physical form. It's the only way out of here...",
            "blockedDesc":"You aren't even certain how you would open it if it were unlocked. Touching it makes your skin crawl.",
            "travelDesc":"You slowly, tentatively step across the threshold, through the inky substance.\nAt first everything is black. "
            "Slowly, shapes begin to form around you, and you recognize the shabby furnishings of your apartment. Glancing around, you "
            "see you are sitting up in your bed, sheets damp from your sweat.\nNightmare. Again. They never seem to leave you in peace.\nYou "
            "slowly lower yourself back into bed, trying to calm your shaken nerves. As you roll over and start to close your eyes, you "
            "notice something."
            "\n\nA long handled axe, head covered in fresh blood, rests "
            "against your nightstand.\n\nWith a sigh, you lift yourself out of bed and reach for the weapon.\nTime to get to work."
        }

        super(TutorialExitGate, self).__init__(description, keywords, isAccessible, keyRequired, itemToOpen, **kwargs)

    def lookAt(self, player):
        desc = self.description[self.state]
        return desc

    def tryUnlock(self, usedItem, player):
        for key, enemy in player.currentLocation.enemies.iteritems():
            if self in enemy.protectedThings:
                return enemy.protectedThings[self]

        if self.isAccessible:
            return "The gate is open."

        if self.keyRequired:
            if not usedItem:
                for key, item in player.inventory.iteritems():
                    if item == self.itemToOpen:
                        self.unlock(player)
                        return self.unlockDesc, True
                return "You aren't carrying a key that fits this lock."
            if usedItem == self.itemToOpen:
                self.unlock(player)
            else:    
                return "The key does not appear to work for this door."
        else:
            self.unlock(player)
        return self.unlockDesc, True

    def unlock(self, player):
        self.isAccessible = True
        player.removeItem(self.itemToOpen)
        self.state = 1

    def tryLock(self, usedItem, player):
        return "The gate is wide open and you can't reach the keyhole. Trying to pull the gate shut proves useless."

    def travel(self, player):
        if self.isAccessible:
            player.returnToMenu = True
        return super(TutorialExitGate, self).travel(player)

    def close(self, player):
        if self.isAccessible:
            resultString = "Despite your best efforts, the huge gate refuses to budge even an inch."
        else:
            resultString = "The gate is already closed. Opening it is the hard part."
        return resultString

    def open(self, player):
        if self.isAccessible:
            resultString = "The gate is already wide open. You need only to walk through it."
        else:
            resultString = "You aren't even certain how you would open it if it were unlocked. Touching it makes your skin crawl."
        return resultString

class BathroomSink102(AreasFeatures.Feature):
    def __init__(self):
        self.featureToAdd = AreasFeatures.Feature(
                description=["Somehow you're certain you've never seen a liquid as repulsive as this. It's jet black, thick as pudding, and and smells downright atrocious. For a moment you swear you see tiny creatures writhing within it, then they are gone. You can't seem to bear looking at this filth for more than a few seconds.",
                            "It's been washed down the drain and can no longer be seen."],
                keywords="liquid,black liquid,ooze,black ooze,black stuff,gunk,black gunk,goop,black goop,goo,black goo",
                **{
                    "getDescription":"Something deep inside you panics at the mere thought of touching it. You'd rather bathe in sewege then touch that stuff."
                })

        description = ["It's very dirty and covered with grease and grime. You'd give it a good wipe but you're not sure you'd be able to muster the energy or willpower.",
                        "It's very dirty and covered with grease and grime. At the bottom is a small pool of disgusting black ooze of some kind. Looking at it makes your skin crawl.",
                        "It's very dirty and covered with grease and grime. Thankfully the black goop has been washed down the drain."]
        keywords = "sink,bathroom sink,my sink"

        kwargs = {
            "useDescription":["As you turn the sink faucet a black and sickening liquid begins slowly oozing out. Filled with revulsion, you immediately turn it off.",
                              "You gingerly turn it back on. Mercifully, it begins producing tap water and the black liquid slowly washes down the drain. Maybe something leaked into your building's water supply...",
                              "Something must be wrong with your plumbing. You don't want to turn it on again until you get it fixed and you can do that after you wake up tomorrow. Time to get to bed."]
        }

        super(BathroomSink102, self).__init__(description, keywords, **kwargs)

    def use(self, player):
        resultString = self.useDescription[self.state]
        if self.state == 0:
            self.currentLocation.addFeature(self.featureToAdd)
        elif self.state == 1:
            self.featureToAdd.state += 1
        if self.state < 2:
            self.state += 1
        return resultString

class TransitionBed101(AreasFeatures.Transition):
    def __init__(self, gameState, builderFunction):
        description = ["It's your bed. It's time to jump in and surrender to sweet, sweet sleep..."]
        keywords = "bed,bunk,sack,mattress,cot,your bed,your bunk,your cot,your sack,your mattress,your cot,my bed,my bunk,my sack,my mattress,my cot,sleep"
        isAccessible = True

        kwargs = {
            "travelDesc":"You crawl under the sheets and slip into darkness...\n\nYou awake to the sound of screams coming from your living room. you blearily stumble out of bed and rub your eyes."
        }

        super(TransitionBed101, self).__init__(description, keywords, isAccessible, gameState, builderFunction, **kwargs)