'''
Created on Jan 23, 2015

@author: CanadianCavalry
'''
import Items
import UniqueFeatures

class Scalpel201(Items.MeleeWeapon):
    
    def __init__(self):
        super(Scalpel201, self).__init__("Scalpel", "I could almost reach it if I stretched...", 
                                      "A scalpal is lying on the ground.", "There is a scalpel almost within reach...", 1, "scalpal,scalpel", 5, 11, 1, 60, 15, 0)

        self.setInitPickupDesc("You strain against the rope as hard as you can, your fingers barely brushing the handle of the scalpel. The cords begin to cut into your wrist and sweat beads \
down your face as you force your hand the last couple of inches, and are rewarded with the feel of cold metal in your palm.")
        self.makeInAccessible("You suddenly jerk forward and try to grab the scalpel, but the man grabs your hand and stops you. \"No, no exorcist!\" he says. That's my toy, not yours!\"")
        
    def useOn(self, player, recipient):
        if isinstance(recipient, UniqueFeatures.Bindings201):
            return recipient.cutBindings(player)
        else:
            return "I don't need to use the scalpel on that."
    
class TortureTools201(Items.Item):
    
    def __init__(self):
        name = "Tools"
        description = "The tools are rusty and smeared with dark stains."
<<<<<<< HEAD
        seenDescription = "The collection of implements includes pliers, fish hooks, a long serrated wire, a trephine, and a scalpel, which is almost within reach."
        initSeenDesc = "The collection of implements includes pliers, fish hooks, a long serrated wire, a trephine, and a scalpel, which is almost within reach."
        quantity = 1
        keywords = "tools,tool,tray,pliers,hooks,fish hook,wire,serreted wire,trephine"
        Items.Item.__init__(self, name, description, seenDescription, initSeenDesc, quantity, keywords)
        self.makeInAccessible("They are just out of reach. I can probably reach the scalpel if I stretch...")
=======
        seenDesc = "The collection of implements includes pliers, fish hooks, a long serrated wire, and a trephine.."
        initDesc = "The collection of implements includes pliers, fish hooks, a long serrated wire, and a trephine."
        quantity = 1
        keywords = "tools,tool,tray,pliers,hooks,fish hook,wire,serreted wire,trephine"
        Items.Item.__init__(self, name, description, seenDesc, initDesc, quantity, keywords)
        self.makeInAccessible("They are just out of reach. I can probably reach the scalpel if I stretch...")
        
>>>>>>> origin/master
