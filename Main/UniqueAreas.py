'''
Created on Sep 12, 2014

@author: Thomas
'''
import AreasFeatures
import StandardItems
import StandardFeatures
import UniqueNPCs
import UniqueItems
import UniqueEnemies
from __builtin__ import True
import UniqueFeatures

class TutorialExit011(AreasFeatures.Area):
     def __init__(self):
        name = " "
        description = ["Congratulations, you have completed the tutorial!\nPlease send feedback, questions and bug reports to CanadianCavalry@gmail.com\n\nPress enter to return to the menu."]

        super(TutorialExit011, self).__init__(name, description)

class interrogationRoom201(AreasFeatures.Area):
    
    def __init__(self):
        self.visited = False
        self.roomState = 0
        self.connectedAreas = {}
        self.features = {}
        self.itemsContained = {}
        self.enemies = {}
        self.NPCs = {}
        self.name = "Where am I..."
        self.description = ["What in God's name has happened to your room? It smells like a dog and the paint on the \
walls is peeling off everywhere! The only source of light comes from a very dim red bulb hanging from the ceiling. It barely \
illuminates your bed and your restraints, the small table next to your bed, your closet, and the door. The door appears to be chained shut, with a heavy padlock securing the chains. An array of grisly tools are spread out on the table.",
"The room is even more of a mess now. Bits of wood are scattered around, and several fresh bloodstains are splattered on the \
walls and floor. Joe's body is lying in a heap near the door, his neck bent at an unnatural angle."]
        self.roomState = 0

        
    #Features
        self.addFeature(AreasFeatures.Feature("You suspect the bastard discarded your blankets, pillows and sheets somewhere. \
The mattress is covered in a filthy black mould and reeks of something foul...", "bed,my bed,jacobs bed"))
        self.addFeature(AreasFeatures.Feature("You definitely don't remember having this kind of light in your room. Almost burnt out, \
it flashes on and off periodically.","light,bulb,lightbulb,lamp"))
        closet201 = UniqueFeatures.JacobsRoomCloset201()
        closet201.setIdNum(001)
        self.addFeature(closet201)
        bindings201 = UniqueFeatures.Bindings201()
        bindings201.setIdNum(002)
        self.addFeature(bindings201)
        padlock201 = AreasFeatures.Feature("A heavy steel padlock.", "padlock,lock")
        padlock201.setIdNum(003)
        self.addFeature(padlock201)
    
    #Links
        door201A = StandardFeatures.StandardOpenDoor("You don't remember your door looking so dilapidated and worn, and you certainly don't recall a padlock on it.", "door,east door, east")
        door201A.setIdNum(004)
     
    #Container
        table201 = StandardFeatures.AlwaysOpenContainer("You don't remember having this flimsy metal table in your room. It's been dragged \
so close to your bed it's actually touching the frame.", "table,metal table")
        table201.setIdNum(005)
        self.addFeature(table201)
    
    #Items
        scalpel201 = UniqueItems.Scalpel201()
        scalpel201.setIdNum(006)
        table201.addItem(scalpel201)
        tools201 = UniqueItems.TortureTools201()
        tools201.setIdNum(007)
        table201.addItem(tools201)
    
    #NPCs
    
    #Enemies
        self.addEnemy(UniqueEnemies.BentHost201())
        
    def changeState(self):
        if self.roomState == 1:
            return
        
        self.roomState = 1
        for feature in self.features.itervalues():
            if feature.idNum == 001:
                feature.isAccessible = True
            elif feature.idNum == 005:
                for item in feature.itemsContained.itervalues():
                    if item.idNum == 006:
                        item.makeAccessible()
                        item.description = "A common surgical tool. Sharp and lightweight, but its small size and tiny reach make it a poor weapon."
                    elif item.idNum == 007:
                        item.makeInAccessible("None of the other tools look very useful.")
            elif feature.idNum == 003:
                feature.description = "The padlock was completely destroyed by the shots. What remains of it is lying in a pile on the floor."
                
        for link in self.connectedAreas.itervalues():
            link.isAccessible = True
