'''
Created on Jul 5, 2014

@author: Thomas
'''
import AreasFeatures
import StandardFeatures

class TutorialExitGate(StandardFeatures.StandardLockingDoor):
    def __init__(self, itemToOpen):
        description = ("A massive gate carved from some unknown metal, or maybe stone? It's hard to be sure, as looking at it for too long makes your "
        "head hurt. It's covered with intricate carvings of demonic creatures and symbols, which you swear move around when you look "
        "away. There is no visible handle, only a single keyhole in the center. You can faintly hear it whispering your name.")
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

    def lookAt(self):
        desc = self.description
        return desc

    def travel(self, player):
        player.returnToMenu = True
        return super(TutorialExitGate, self).travel(player)

#Jacobs Room

class JacobRoomWindow101(AreasFeatures.Feature):
    
    def __init__(self):
        self.description = "A large sliding window. The people who designed these rooms know what they were doing. It lets in a lot of light when it's sunny out, and helps my mood."
        self.keywords = "window,sliding window"
        
    def open(self, player):
        return "Although it's easy to open, it has a fixed screen over it. "
    
class ResidentsWingDoorsFirstFloor102(AreasFeatures.Feature):
    
    def __init__(self):
        description = "All of the doors look pretty much identical. Thick wooden slabs painted a dull blue, with brass room numbers on their front. This door is closed."
        keywords = "door 101,door 102,door 103,door 105,door 107,door 108,door 109,door 110" + \
        "room 101,room 102,room 103,room 105,room 107,room 108,room 109,room 110"
        AreasFeatures.Feature.__init__(self, description, keywords)
    
    def open(self, player):
        return "The door to this room is closed. The House's is really strict about the privacy of its residents and has a 'closed door, do not disturb policy'."

class ResidentsWingDoorsSecondFloor104(AreasFeatures.Feature):
    
    def __init__(self):
        description = "All of the doors look pretty much identical. Thick wooden slabs painted a dull blue, with brass room numbers on their front. This door is closed."
        keywords = "door 202,door 203,door 204,door 206,door 207,door 208,door 209,door 210" + \
        "room 202,room 203,room 204,room 206,room 207,room 208,room 209,room 210"
        AreasFeatures.Feature.__init__(self, description, keywords)
    
    def open(self, player):
        return "The door to this room is closed. The House's is really strict about the privacy of its residents and has a 'closed door, do not disturb policy'."

class ResidentsWingDoorsThirdFloor107(AreasFeatures.Feature):
    
    def __init__(self):
        description = "All of the doors look pretty much identical. Thick wooden slabs painted a dull blue, with brass room numbers on their front. This door is closed."
        keywords = "door 301,door 302,door 303,door 304,door 305,door 306,door 307,door 309,door 310" + \
        "room 301,room 302,room 303,room 304,room 305,room 306,room 307,room 309,room 310"
        AreasFeatures.Feature.__init__(self, description, keywords)
    
    def open(self, player):
        return "The door to this room is closed. The House's is really strict about the privacy of its residents and has a 'closed door, do not disturb policy'."
    
class MainLobbyExteriorDoor109(AreasFeatures.Feature):
    
    def __init__(self):
        description = "A heavy pair of steel and glass security doors. The panes which cover most of each door are glazed, preventing your from seeing outside."
        keywords = "door,doors,steel door,steel door,metal door,front door,south,south door"
        super(MainLobbyExteriorDoor109, self).__init__(self, description, keywords)
        
    def open(self, player):
        return "One of the guards approaches you as you move towards the door.\"Heading out, Jacob? I'm pretty sure you've got a couple hours of visiting time left \
for this week - just let me check your ID card and I'll make sure.\" You inform her that you might go out later, but you don't have time right now as you need to get to Father Malachi's talk."

class JacobsRoomCloset201(AreasFeatures.Container):
    def __init__(self):
        description = ["It's closed. The door to the closet is so dilapidated it's almost falling off the hinges. \
Why is everything in your room in such awful shape?"]
        keywords = "closet"
        isOpen = False
        isAccessible = False
        blockedDesc = "I can't get to it while I'm tied to this damn table."
        openDesc = "The door is jammed on its track, but after a strong shove it grudgingly slides open."
        closeDesc = "With a little effort, you force the door closed."
        super(JacobsRoomCloset201, self).__init__(description, keywords, isOpen, isAccessible, blockedDesc, openDesc, closeDesc)
        
class Bindings201(AreasFeatures.Feature):
    
    def __init__(self):
        description = ["They're made of rope and restrain both your wrists and both your ankles to the bedposts. You're tied quite securely, but the rope isn't very thick and you might be able to manoveure your hands and feet about a foot in each direction.",
                       "You've managed to free one hand, the rest of the bonds should be easy to cut.",
                       "With both hands free you can easily finish freeing yourself.",
                       "The tattered remains of the bindings still hang from the bedposts."]
        keywords = "bindings,rope,restraints,bonds"
        super(Bindings201, self).__init__(description, keywords)
        self.cutActions = ["Sweat drips from your forehead as you twist your right hand in an extremely awkward position to cut the bindings on your right wrist. It works - your right arm is free!",
                           "You scramble to sever the bindings on your left arm. Done, now on to your legs!",
                           "Filled with adrenaline, you sever the binding on your right ankle. Just one more!",
                           "You sever the binding on your left ankle. At last you're free!"]
    
    def cutBindings(self, player):
        if self.state < 3:
            currentState = self.state
            if currentState == 3:
                player.unrestrictPlayer()
            self.nextState()
            return self.cutActions[currentState], True
        else:
            return "You are already free."