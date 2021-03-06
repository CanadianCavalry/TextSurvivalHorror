'''
Created on Jun 30, 2014

@author: Thomas
'''
import AreasFeatures
import StandardFeatures
import UniqueAreas
import UniqueFeatures
import UniqueHazards
import Items
import StandardItems
import UniqueItems
import Enemies
import UniqueEnemies
import NPCs
import UniqueNPCs

class Builder(object):

    def __init__(self):
        self.gameState = None

    def loadState(self, gameState):
        self.gameState = gameState

    #Tutorial section
    def buildCombatSimulator(self):
        #INTRO
        introText = ("Welcome to the tutorial! This area is intended to allow you to learn the basic game commands and practice "
        "fighting with various weapons. That said, it is still quite easy to die, so don't get complacent. To get started head "
        "through the north door, but before you head out, take a look around and make sure you are suitibly equipped. "
        "There's no coming back here once you leave.\n\nTo get your bearings, type \"look\". To get a closer look at anything, "
        "type \"look\" followed by the object.")
        self.gameState.introText = introText

        introMusic = None
        self.gameState.backgroundMusic = introMusic

        #Combat Test Environment
        #AREA KEYS
        key004A = Items.Key(
            name="Bent Key",
            description="An old, bent key. It looks like it's been around a while.",
            seenDescription="A bent key is lying on the floor.",
            keywords="key,bent key,archives key,old key",
            **{
                "notTakenDesc":"You notice an old, beat up key under the desk."
            }
        )
        key005A = Items.Key(
            name="Ornate Key",
            description="It's covered in strange markings and is topped with an ornate engraving of a demonic face. It looks like it's made from copper or brass.",
            seenDescription="An ornate metal key is on the ground.",
            keywords="key,ornate key,copper key,bronze key,demon key",
            **{
            "notTakenDesc":"There is a large, ornate metal key clutched in what's left of the mans hand."
            }
        )
        key009A = Items.Key(
            name="Library Key",
            description="A ordinary looking key. It has a small tag attached which says \"library - maint use only!\"",
            seenDescription="The key to the library is on the floor.",
            keywords="key,library key,metal key,small key",
            **{
                "notTakenDesc":"A lone key is hanging from a keyrack on the wall."
            }
        )

        #001 - ARMORY
        armory001 = AreasFeatures.Area(
            "Armory", 
            ["This tiny, cramped room is lined on all sides by large steel cages packed with weapons of every kind. Sadly, they are "
            "all locked. On the metal table in the center of the room is a small collection of items, and a large sign is bolted to "
            "the east wall titled \"Tips for newbies\". There is a door to the north."],
             **{"size":2})
        arenaDoorA = StandardFeatures.StandardOpenMetalDoor(
            ["A heavy steel door. It appears to have some sort of mechanism built into it that locks it once you pass through."],
            "north,north door,door,metal door,steel door")

        armory001.addFeature(AreasFeatures.Feature(
            ["The table is littered with all manner of useless junk, as well as a number of empty bottles and items of clothing."],
             "table,small table, metal table"))
        armory001.addFeature(StandardFeatures.Sign(
            ["The large metal sign looks very worn and rusted, and has been riveted straight into the metal wall. It appears that "
            "it has been here for a long time, and is not coming down any time soon."],
            "sign,metal sign, plaque, brass sign, brass plaque",
            "Tips for Newbies\n\n-Make sure you have a melee weapon and some armor before moving on.\n-Every "
            "weapon has different damage and accuracy. Bigger is not always better.\n-As a functioning alchoholic, you perform "
            "better with a bit of liquor in your system. It numbs your body, reducing incoming damage, and calms shaking hands, "
            "increasing accurracy. Don't go overboard though or you'll go downhill fast.\n\nTyping HELP will list all "
            "common commands, but a few you should get familiar with to start are:\nGET - Pick up things\nI - View your "
            "inventory\nEQUIP - Equip weapons or armor\nGO - Travel through doors or down halls\nOPEN - Open doors or containers"))
        gunCages = StandardFeatures.LockingContainer(
            ["Behind the thick bars you can see a huge array of weaponry, from handguns to rifles and even grenades. The cages are "
            "of a heavy duty steel constuction, and don't look like they'll be opening any time soon. With a sigh, you turn your "
            "attention back to the room."],
            "cages,cage,guns,weapons,weaponry,grenade,rifle,pistol,handgun,steel cage,steel cages,metal cage,metal cages",
            True,
            None,
            **{"blockedDesc":"The doors are locked and won't budge. There's no way to get in without a key."})
        armory001.addFeature(gunCages)

        armory001.addItem(StandardItems.Axe(**{
            "notTakenDesc":"A long-handled fire axe is lying across the table.",
            "initPickupDesc":"You lift the axe from the table. It has a weight and heft that is comfortable in your hands.",
            "drunkDesc":"Heeeeeeere's Johhny!",
            "drunkSearchDesc":"You clumsily examine the axe for several minutes before determining that it is indeed an axe.",
            "drunkDescThreshold":5
        }))
        armory001.addItem(StandardItems.LeatherJacket(**{
                "notTakenDesc":"A faded leather jacket is hanging off one of the cages."
            }))
        armory001.addItem(key009A)
        armory001.addItem(StandardItems.Flask())
        #armory001.addItem(Items.Note(
        #    name="Strange Note",
        #    description="A hastily written note scrawled on a napkin.",
        #    seenDescription="There is a scrunched up note pinned to the table.",
        #    keywords="note,paper,napkin,page",
        #    contents="FOR TESTER USE ONLY\nDev commands are executed with \"/dev\":\n\ndylanwantsagun: Get some firepower."
        #))
        
        #002 - ARENA
        arena002 = AreasFeatures.Area(
            "Arena", 
            ["You are standing in a large, empty colosseum. Against the east wall is a massive sign carved from stone titled "
            "\"Combat Tips\". There is a large steel door to the south, with some sort of complex locking mechanism on it. On the "
            "far end of the west wall is another, smaller metal door. To the east is a set of concrete stairs leading downwards. To "
            "the north, there is a enormous, arched gate covered in demonic symbols and glowing runes."],
            **{"size":4})
        arenaDoorB = StandardFeatures.StandardKeylessDoor(
            ["A heavy steel door. It has no handle or lock that you can see."],
            "south,south door,door,metal door,steel door",
            False)
        arenaDoorB.makeSibling(arenaDoorA)
        arena002.connect(armory001, arenaDoorB)
        armory001.connect(arena002, arenaDoorA)

        door002B = StandardFeatures.StandardLockingDoor(
            ["A steel door. It's battered and dented, and has a large, rust colored stain near the handle."],
            "west,west door,door,metal door,steel door,library,library door",
            False,
            True,
            key009A)

        door002C = StandardFeatures.StandardDownwardStairs(
            ["The concrete steps lead downward into the darkness, though you can see light further down. It must be a basement of some sort."],
            "east,east stairs,stairs,stone stairs,concrete stairs,dirty stairs,east steps,steps,staircase,stone steps")
        
        door002D = UniqueFeatures.TutorialExitGate(key005A)

        arena002.addFeature(StandardFeatures.Sign(
            "The large metal sign takes up a large portion of the east wall. It reads \"Please ensure you are prepared before continuing "
            "to the test arena. Good luck\"",
            "sign, stone sign, large sign",
            "Combat Tips\n\n-Every enemy has different strengths and weaknesses. Examining an enemy takes no time, and may yield "
            "life-saving information.\n-Heavy attacks are less accurate, but deal more damage and can even stun some foes.\n-Exorcising "
            "a demonic enemy can have numerous effects, but will often stun or incapacitate them. Some enemies are more resilient to "
            "exorcism than others.\n-Performing a heavy attack against a helpless enemy will often result in an execution.\n\nImportant "
            "combat commands:\nATTACK - Attack with an equipped weapon\nHEAVY ATTACK - Slower, stronger attack\nEXORCISE - Invoke your "
            "faith to weaken an enemy\nRELOAD - Reload your equipped gun(requires ammo)\nDEFEND - Give up your chance to strike to "
            "increase your chances of dodging the next attack."))


        #011 - Tutorial Exit
        tutorialExit011 = UniqueAreas.TutorialExit011()
            
        door011A =  StandardFeatures.StandardKeylessDoor(
            ["A door that no longer exists. Oops."],
            "non-existant",
            False)

        door002D.makeSibling(door011A)
        arena002.connect(tutorialExit011, door002D)
        tutorialExit011.connect(arena002, door011A)

        #003 - LIBRARY FOYER
        libraryFoyer003 = AreasFeatures.Area(
            "Library Foyer",
            ["This appears to be a small reception area, with a wooden desk in the corner next to some rusty filing cabinets and a "
            "couple of chairs the have been scattered haphazardly. There is a metal door to the east, and and to the west past the "
            "desk is a pair of heavy wooden doors that have been smashed partially inwards. The sign above them reads \"Library\"."],
            **{"size":2})
        
        #Links
        door003A = StandardFeatures.StandardLockingDoor(
            ["A steel door. It leads back out into the arena."],
            "east,east door,door,metal door,steel door",
            False,
            True,
            key009A)
        door003A.makeSibling(door002B)
        libraryFoyer003.connect(arena002, door003A)
        arena002.connect(libraryFoyer003, door002B)

        door003B = StandardFeatures.StandardOpenDoor(
            ["A heavy wooden door, oak or some kind of hardwood. It been smashed, as though something too large to fit forced it's way "
            "through into the library. It's hanging crooked on it's hinges and the frame has deep gouges in it."],
            "west,west door,door,wood door,wooden door,oak door,hardwood door")

        #Features
        libraryFoyer003.addFeature(AreasFeatures.Feature(
            ["These filing cabinets are in a serious state of disrepair. They are covered in dents and scratches, and the drawers have actually rusted completely shut."],
            "cabinets,cabinet,file cabinet,file cabinets,file drawers,filing cabinets,filing cabinet"
        ))
        libraryFoyer003.addFeature(AreasFeatures.Feature(
            ["A couple of cheap metal folding chairs. They look incredibly uncomfortable."],
            "chair,chairs,metal chair,metal chairs"
        ))
        libraryFoyer003.addFeature(AreasFeatures.Feature(
            ["It looks ancient, worn to the point of falling apart. From the patches of faded paint still clinging to the wood, you'd guess "
            "it used to be green. It has single drawer in it."],
            "desk,wood desk,wooden desk"
        ))
        libraryDeskDrawer = AreasFeatures.Container(
            ["Flimsy and creaky, just like the desk it's attached to."],
            "drawer,desk drawer",
            **{"openDesc":"You half expect it to break, but it slides open with a loud squeak.", "closeDesc":"You slide the drawer closed."}
        )

        #Items
        libraryDeskDrawer.addItem(StandardItems.FirstAidKit(**{
            "notTakenDesc":"A first aid kit is lying in the drawer amongst the pens and loose paper."
            }))
        libraryFoyer003.addFeature(libraryDeskDrawer)

        #004 - LIBRARY EAST WING
        libraryEast004 = AreasFeatures.Area(
            "Library - East Wing", 
            ["This part of the library is a mess, books scattered across the floor, shelves knocked over or slanted precariously over "
            "the aisle. One massive shelf in particular is leaning so far over you're amazed it's still upright. There is what looks like "
            "a reception desk by the east wall near the door. Most of the aisles are blocked or "
            "otherwise inaccessible, but it looks like you could work your way further to the west. You also see a heavy duty looking security "
            "door leading to the south, with a sign above it which reads \"Archives\", and an oak door leading east.",
            "This part of the library is a mess, books scattered across the floor, shelves knocked over or slanted precariously over "
            "the aisle. In the center of the main aisle is the shattered remains of a huge bookshelf. Most of the aisles are blocked or"
            "otherwise inaccessible, but it looks like you could work your way further to the west. You see a heavy duty looking security "
            "door leading to the south, with a sign above it which reads \"Archives\".There is also an oak door leading east."],
            **{"size":3})

        #Links
        door004A = StandardFeatures.StandardOpenDoor(
            ["A heavy wooden door, oak or some kind of hardwood. It been smashed, as though something too large to fit forced it's way "
            "through into the library. It's hanging crooked on it's hinges and the frame has deep gouges in it."],
            "east,east door,door,wood door,wooden door,oak door,hardwood door")
        door004A.makeSibling(door003B)
        libraryEast004.connect(libraryFoyer003, door004A)
        libraryFoyer003.connect(libraryEast004, door003B)

        door004B = AreasFeatures.Path(
            ["Though numerous tipped over shelves and piles of debris are in the way, you can see a clear path through to the west end "
            "of the library"], 
            "west,west wing,path",
            True,
            **{"travelDesc":"You pick your way carefully between the shelves and emerge in the west wing."}
        )

        door004C = StandardFeatures.StandardLockingDoor(
            ["This is a steel fire-door with a heavy lock built in to it. It's an unusual amount of security for a library, they must "
            "keep more valuable or rare texts in the archives."],
            "south,south door,door,steel door,security door,metal door.archives door,archives",
            False,
            True,
            key004A)

        #Features
        libraryEast004.addFeature(UniqueHazards.LeaningBookshelf())
        libraryEast004.addFeature(AreasFeatures.Feature(
            ["The entire room is lined with creaky, tipping and crumbling bookshelves."],
            "shelf,shelves,bookshelf,bookshelves,bookcase,bookcases"
        ))
        libraryEast004.addFeature(AreasFeatures.Feature(
            ["There must be thousands of books in this room, mostly religious and academic works. None jump out as being particularly "
            "interesting, and you doubt you have the time to go searching through the stacks for a certain volume."],
            "book,books"
        ))
        libraryEast004.addFeature(AreasFeatures.Feature(
            ["The desk has a series of long slashes across the top, similar to the eastern door. The drawers have all been ripped out and "
            "tossed aside, the contents spilling onto the floor and under the desk. You don't see anything interesting from where you are "
            "standing."],
            "desk,reception desk,library desk"
        ))
        libraryUnderDesk004 = StandardFeatures.AlwaysOpenContainer(
            ["Getting down on your hands and knees, you peer under the desk. Pens, loose paper and random office supplies greets you."],
            "under desk,beneath desk"
        )
        libraryUnderDesk004.addItem(key004A)
        libraryEast004.addFeature(libraryUnderDesk004)

        #Items

        #Enemies


        #010 - LIBRARY ARCHIVES
        libraryArchives010 = AreasFeatures.Area(
            "Archives", 
            ["This is a massive room filled with aisle upon aisle of bookshelves. The huge shelves run the entire length of the room, and stretch "
            "upwards toward the high, vaulted ceiling. Stacks of books and loose papers fill much of the room and make the otherwise large "
            "area feel cramped. There is a single heavy duty security door to the north."],
            **{"size":3})
        
        #Links
        door010A = StandardFeatures.StandardKeylessDoor(
            ["A steel fire-door which locks from the other side."],
            "north,north door,door,steel door,security door,metal door",
            False)
        door010A.makeSibling(door004C)
        libraryArchives010.connect(libraryEast004, door010A)
        libraryEast004.connect(libraryArchives010, door004C)

        #Features
        libraryArchives010.addFeature(AreasFeatures.Feature(
            ["The volumes in this area are much older from what you can see. Though they seem to be predominantly religious tets, you don't "
            "recognize most of the titles. Many seem to be written in different languages."],
            "book,books"
        ))
        libraryArchives010.addFeature(AreasFeatures.Feature(
            ["The room is divided up into long aisles of bookshelves, with very little space between them."],
            "shelf,shelves,bookshelf,bookshelves,bookcase,bookcases"
        ))

        #Items

        #Enemies


        #005 - LIBRARY WEST WING
        libraryWest005 = AreasFeatures.Area(
            "Library - West Wing", 
            ["The west wing looks to be in considerably better shape than the eastern section. While a number of books have been torn apart "
            "and scattered around, the rest of the room is intact for the most part. On the far wall is a large, ornate stained glass "
            "window depicting a biblical looking scene. It has been covered with metal bars."],
            **{"size":3}
        )

        #Links
        door005A = AreasFeatures.Path(
            ["Though numerous tipped over shelves and piles of debris are in the way, you can see a clear path through to the east end "
            "of the library"], 
            "east,east wing,path",
            True,
            **{"travelDesc":"Following your previous path through the debris, you return to the east wing."}
        )
        door005A.makeSibling(door004B)
        libraryWest005.connect(libraryEast004, door005A)
        libraryEast004.connect(libraryWest005, door004B)

        #Features
        libraryWest005.addFeature(AreasFeatures.Feature(
            ["The entire room is filled with huge, hardwood bookshelves."],
            "shelf,shelves,bookshelf,bookshelves,bookcase,bookcases"
        ))
        libraryWest005.addFeature(AreasFeatures.Feature(
            ["There must be thousands of books in this room, mostly religious and academic works. None jump out as being particularly "
            "interesting, and you doubt you have the time to go searching through the stacks for a certain volume."],
            "book,books"
        ))
        libraryWest005.addFeature(AreasFeatures.Feature(
            ["This circular stained glass window takes up a good portion of the west wall. It depicts an ancient scholar being attacked "
            "by a large dog. The robed figure is holding out a book, which seems to be warding off the animal. Though the style looks "
            "biblical, it's nothing I remember learning about.\nThe entire thing is covered with steel bars with only about 6 inches "
            "between them. Doesn't look like you'll be getting out through here."],
            "window,stained glass,glass,mural,"
        ))
        libraryCorpse005 = Items.Corpse(
            name="Dead Human",
            description="It looks like it was a man at some point, though he's mostly beyond recognition. He's been badly mauled, "
            "and from the tooth marks it looks like his head and limbs have been chewed on. His clothing indicates he was an employee, "
            "possibly an orderly.",
            seenDescription="A badly mauled corpse is splayed out on the floor.",
            keywords="corpse,dead body,body,dead man,dead human,dead person,victim",
            **{
                "initSeenDesc":" "
            }
        )
        libraryCorpse005.addItem(key005A)
        libraryWest005.addItem(libraryCorpse005)

        #Items

        #Enemies
        libraryHellhound = UniqueEnemies.Hellhound()
        libraryWest005.spawnEnemy(libraryHellhound, 3)
        libraryHellhound.protectThing(libraryCorpse005, "The hellhound is directly between you and the corpse.")

        #006 - BASEMENT ENTRANCE
        basementEntrance006 = AreasFeatures.Area(
            "Basement Entrance", 
            ["You find yourself in a small room with cement floors and walls. Mold and mildew have spread across much of the walls, "
            "and the steady sound of dripping water fills the space. The room is bare, with nothing of note besides a set of concrete "
            "stairs to the west, and two metal doors, one to the east and one to the south.\nIt looks like someone has scratched words "
            "into the east door."],
            **{"size":2}
        )

        #Links
        door006A = StandardFeatures.StandardUpwardStairs(
            ["Like everything else in this room, they're wet, dirty and covered in mildew. At least the concrete steps seem to be in "
            "relatively good condition, so there's that."],
            "west,west stairs,stairs,stone stairs,concrete stairs,dirty stairs,west steps,steps,staircase,stone steps")
        door006A.makeSibling(door002C)
        basementEntrance006.connect(arena002, door006A)
        arena002.connect(basementEntrance006, door002C)

        door006B = StandardFeatures.StandardLockingDoor(
            ["It's covered in rust, mold, and several other unidentifiable stains. There is a heavy duty steel bolt handle on this side of the door.\nSomeone has scratched a message into the metal: \"DON'T LET THEM OUT\"\n"],
            "east,east door,door,metal door,steel door,rusty door,dirty door",
            False,
            False,
            None,
            **{"unlockDesc":"With some effort, you pull the bolt back. For a moment, you think you can hear something rustling on the other side of the door.",
            "lockDesc":"You quickly slide the bolt into place, locking it again."}
        )

        door006C = StandardFeatures.StandardOpenDoor(
            ["It's cleaner than the other door, but that isn't saying much considering the condition of the room. You can hear a faint humming "
            "noise from beyond the door."],
            "south,south door,door,metal door,steel door")

        #Features

        #Items

        #Enemies


        #007 - GENERATOR ROOM
        generatorRoom007 = AreasFeatures.Area(
            "Generator Room", 
            ["The door leads to a small cramped room. A large generator takes up most of the south wall, humming loudly. Someone has built a "
            "makeshift bed here out of dirty blankets, and the floor is littered with garbage. It looks like someone has been living here. A "
            "door leads back to the north."],
            **{"size":1}
        )

        #Links
        door007A = StandardFeatures.StandardOpenDoor(
            ["A sturdy metal door that leads back to the basement entrance."],
            "north,north door,door,metal door,steel door")
        door007A.makeSibling(door006C)
        generatorRoom007.connect(basementEntrance006, door007A)
        basementEntrance006.connect(generatorRoom007, door006C)

        #Features
        generatorRoom007.addFeature(AreasFeatures.Feature(
            ["The blankets are disgusting, covered in layers of dirt and dried blood, among other things. It looks like he was living here for some time."],
            "bed,blanket,blankets"
        ))
        generatorRoom007.addFeature(AreasFeatures.Feature(
            ["Food wrappers, rags, and various used toiletries make up the bulk of the mess. Nothing worth taking, and it's doubtful you'd "
            "want to touch it if there was."],
            "floor,trash,garbage,mess,wrappers,rags,toiletries"
        ))

        #Items
        crossbow007 = StandardItems.Crossbow(**{
            "notTakenDesc":"Lying on the floor next to the makeshift bed is a loaded crossbow."
        })
        generatorRoom007.addItem(crossbow007)

        #Enemies
        bentHost007A = UniqueEnemies.BentHost(**{
            "firstSeenDesc":"A man suddenly rises from the bed, previously hidden by blankets. He locks eyes with you, and a wide, terrifying grin spreads "
                "across his face. He raises his arm and you see a pair of bloody scissors clutched in his hand. He lets out a small giggle and charges towards you."
        })
        bentHost007A.description = ["Though human, the twisted facial features and sadistic grin mark him as the puppet of a demonic creature. "
                "Long, deep slashes cover his exposed forearms and wrists, and his clothes are smeared in blood both dried and fresh. "
                "He carries a pair of scissors in one hand."]
        bentHost007A.seenDescription = "A wounded, blood soaked man carrying a pair of scissors is here with you."
        bentHost007A.addItem(StandardItems.CrossbowBolt(**{
            "notTakenDesc":"There is a crossbow bolt tucked into his waistband."
        }))
        bentHost007A.protectThing(crossbow007)
        generatorRoom007.spawnEnemy(bentHost007A, 1)


        #008 - UTILITIES ROOM
        utilitiesRoom008 = AreasFeatures.Area(
            "Utilities Room", 
            ["This room is quite large, and filled with all kinds of pipes, electrical conduits, and ventilation ducts. It seems "
            "to be a central utility room. Most of the equipment is in a state of disrepair, and several inches of water cover the floor. "
            "There is a sign bolted to the wall titled \"Possession\"There is a narrow door on the wall to the south, and another one leading back the basement entrance to the west."],
            **{"size":3}
        )

        #Links
        door008A = StandardFeatures.StandardKeylessDoor(
            ["A sturdy metal door that leads back to the basement entrance."],
            "west,west door,door,metal door,steel door",
            False
        )
        door008A.makeSibling(door006B)
        utilitiesRoom008.connect(basementEntrance006, door008A)
        basementEntrance006.connect(utilitiesRoom008, door006B)

        door008B = StandardFeatures.StandardOpenDoor(
            ["A narrow metal door. It looks like a storage room or closet."],
            "south,south door,door,metal door,steel door,storage door,closet door")
        #Features
        utilitiesRoom008.addFeature(AreasFeatures.Feature(
            ["The machinery is all ancient, rusted and on the verge of falling apart. You doubt very much if any of it still functions."],
            "pipes,vents,machinery,machines,ventilation,plumbing,pipe,conduit,electrical conduit,wires"
        ))
        utilitiesRoom008.addFeature(AreasFeatures.Feature(
            ["It's murky and stagnant. If must have come from a burst pipe or leaking pump, but that had to have been some time ago."],
            "water,floor,flooding"
        ))
        utilitiesRoom008.addFeature(StandardFeatures.Sign(
            ["The large metal sign looks very worn and rusted, and has been riveted straight into the metal wall. It appears that "
            "it has been here for a long time, and is not coming down any time soon."],
            "sign,metal sign,possession sign",
            "Possession\n\nHumans who are possessed by demons can be freed by continuing the exorcism once they have been rendered "
            "helpless. This can take some time and is quite difficult when facing multiple foes. Killing a host on the other hand "
            "is quick, but has it's own cost."))


        #Items

        #Enemies
        bentHost008A = UniqueEnemies.BentHost(**{
            "firstSeenDesc":"As you step through the door, maniacal laughter fills the room. A figure emerges from the darkness, a young "
            "woman carrying a large kitchen knife. A moment later she is joined by another, then another. In unison, all three begin walking "
            "towards you.",
            "firstSeenSound": "Sounds/Monsters/BentHostLaugh.mp3"
        })
        bentHost008A.protectThing(door008B, "There's no way you can reach the door with the hosts in the way.")
        utilitiesRoom008.spawnEnemy(bentHost008A, 3)

        bentHost008B = UniqueEnemies.BentHost(**{
            "firstSeenDesc":" "
        })
        bentHost008B.protectThing(door008B, "There's no way you can reach the door with the hosts in the way.")
        utilitiesRoom008.spawnEnemy(bentHost008B, 3)

        bentHost008C = UniqueEnemies.BentHost(**{
            "firstSeenDesc":" "
        })
        bentHost008C.protectThing(door008B, "There's no way you can reach the door with the hosts in the way.")
        utilitiesRoom008.spawnEnemy(bentHost008C, 3)


        #009 - MAINTENANCE CLOSET
        maintenanceCloset009 = AreasFeatures.Area(
            "Maintenance Closet", 
            ["You find yourself in a tiny maintenance closet used to store tools, cleaning supplies and the like. The door is to the north."],
            **{"size":1}
        )

        #Links
        door009A = StandardFeatures.StandardOpenDoor(
            ["A sturdy metal door that leads back to the basement entrance."],
            "north,north door,door,metal door,steel door"
        )
        door009A.makeSibling(door008B)
        maintenanceCloset009.connect(utilitiesRoom008, door009A)
        utilitiesRoom008.connect(maintenanceCloset009, door008B)

        #Features
        maintenanceCloset009.addFeature(AreasFeatures.Feature(
            ["There are a variety of small hand tools, tape, screws, gloves and more stored in a large red toolbox. Nothing "
            "that looks particularly useful at the moment unfortunately."],
            "tools,tape,screws,toolbox"
        ))
        maintenanceCloset009.addFeature(AreasFeatures.Feature(
            ["A decent collection of cleaning supplies, all with numerous warnings about toxicity, corrosivness, and flamability. "
            "You have the sudden urge to leave this closet as soon as possible."],
            "cleaning,cleaning supplies,supplies,chemicals,bleach,ammonia"
        ))
        maintenanceCloset009.addFeature(AreasFeatures.Feature(
            ["A small wooden key rack that looks more like it belongs in a suburban home than a maintenance room."],
            "keyrack,keyring,key holder,key rack"
        ))

        #Items
        maintenanceCloset009.addItem(key009A)

        #Enemies


        #Debug Config:
        spawnLocation = armory001

        return spawnLocation
        
    def buildPrologue100(self):
        #INTRO
        introText = ("Your life is in shambles. Once a respected priest, alcoholism put an end to your career years ago. Every "
        "aspect of your life hurts. As you stare at your flask of cheap whiskey, you wonder what it would take to redeem one "
        "such as yourself. They say God is all powerful and loving, yet can even God save those who refuse to help themselves? "
        "You take another shot of whiskey. Oblivion - it seems - tastes very sweet indeed.\n\nLike too many nights in the past, "
        "you find yourself sitting down in your bedroom armchair with a bottle of whiskey in hand. Drowsy from too much alcohol, "
        "you long to bury yourself under your bedsheets and blissfully fall asleep. Escape reality even further.")
        self.gameState.introText = introText

        introMusic = "Music/Sadness6.mp3"
        self.gameState.backgroundMusic = introMusic

        bufferRoom = AreasFeatures.Area(
            name="Buffer Room", 
            description=[" "])


        #Set starting stats for the player
        self.gameState.player.intoxication = 30


        #101 - BEDROOM
        bedroom101 = AreasFeatures.Area(
            name="Bedroom", 
            description=["You are in your bedroom. It's furnished with a bed, chest of drawers, a large shelf, an armchair and a desk. "
            "Atop the desk there is a computer. Dirty laundry, miscellaneous papers and empty alcohol "
            "bottles are strewn about the floor. On the walls there are a few decorations and a window looking out to the south. "
            "To your west is a door leading to your bathroom. To the north is another door your kitchen/living room area."
            "\n\nIt's been a long day, you're drunk, and you just want to hit the hay..."],
            **{"size":2})

        #Links
        door101A = StandardFeatures.StandardOpenDoor(
            description=["A wooden door. It leads to your apartment's bathroom."],
            keywords="door,west,wooden door,west door,bathroom door"
        )

        door101B = StandardFeatures.StandardOpenDoor(
            description=["A wooden door. It leads to your apartment's kitchen/living room."],
            keywords="door,north,wooden door,north door,living room door,livingroom door,kitchen door,kitchen/living room door"
        )
        bedroom101.addTransition(UniqueFeatures.TransitionBed101(
            self.gameState,
            self.buildZone200
        ))

        #Features
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["It's the newest Macintosh model - a uMac. You're lucky you haven't had to pawn it for cash given how poor you are "
            "these days.\nIf you claimed you used it for mostly productive purposes you'd be lying. These days you mainly use "
            "it to download and play hundreds of Steam games, and for other forms of entertainment not mentioned in polite society."],
            keywords="computer,compy,comp,your comp,computer,your computer,beep-boop,your beep-boop",
            **{"useDescription":"You're far to drunk to do anything worthwhile on the computer, let alone to remember your password."}
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["They're painted white. You've never liked your bedroom walls very much. The paint job is cracked and faded in various "
            "spots, most of which you've tried to cover with photos, paintings and posters."],
            keywords="wall,walls,bedroom wall,bedroom walls"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["A beige recliner. You try not to think about how many hours you've spent sitting here getting wasted."],
            keywords="armchair,chair,bedroom chair,your armchair,your chair,your bedroom chair,my armchair,my chair,my bedroom chair"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["The desk's faded blue paint is marred by several moisture stains. It primarily exists to hold the computer, and extra bottles."],
            keywords="desk, computer desk, your desk, your computer desk"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["The dirty laundry covers seemingly a third of your bedroom floor. You'd at least push into a orderly heap if you weren't so drunk and tired. Time to get to bed..."],
            keywords="laundry,dirty laundry,clothes,clothing,dirty clothing,dirty clothes"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["An assortment of photos, paintings and posters you've put up on the wall."],
            keywords="decorations,decoration"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["They show a series of dreamlike scenes. All are captioned by quotes from famous philosophers and theologians. The most prominant shows a person "
            "staring at their reflection in a mirror. A quote from Immanuel Kant at the bottom reads \"God is a necessary postulate for moral reason, for "
            "only he can garuntee that happiness will be proportioned to virtue.\""],
            keywords="posters,poster"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["Some of these are reproductions of works by famous impressionists. Others are scenes from the Bible. The largest painting shows an artist's "
            "rendition of Jesus bending down to comfort a leper. You notice with surprise that the leper's face is turned defiantly away, "
            "something you don't remember seeing before."],
            keywords="paintings,painting,artwork,art"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["Little windows to better days. They're photos of you, your friends and your family and a few places you've visited. Your walls were once "
            "covered with photos of church experiences. After a while they became too painful to look at."],
            keywords="photo,photos,pictures,photographs,photograp,family photos,family photo"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["They're a mix of pizza delivery menus, receipts, written notes and long-overdue bills. You're far too tired to sort through "
            "these right now. Like usual."],
            keywords="papers,scraps,scrap papers,scrap paper,miscellaneous papers,miscellaneous paper"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["A few dozen empty bottles of beer lay scattered next to your armchair. Staring at these just depresses you."],
            keywords="bottles,bottle,empty bottles,empty bottle,alcohol bottles,alcohol bottle,booze bottle,booze bottles"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["Where you keep all your clothing apart from your shoes and coat(which are in the small closet in the your living room). The top is dusty "
            "and covered with stains."],
            keywords="drawers,chest,chest of drawers,dresser"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["This sturdy oak shelf houses various books and some personal effects. On it's top level rests a few candles and some religious items."],
            keywords="shelf,wooden shelf,oak shelf,bedroom shelf"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["An assortment of about four dozen books. Among them are classic works about theology, philosophy and history as well as modern fantasy and "
            "sci-fi novels. You've read every one of them from cover to cover. If you're so smart, how did your life go so wrong?"],
            keywords="book,books,tomes,tome,paperback,paperbacks"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["These white and red advent candles are arranged in a semicircle. You remember receiving these as a gift from a fellow priest."],
            keywords="candles,candle,advent candles"
        ))
        bedroom101.addFeature(AreasFeatures.Feature(
            description=["It looks south out to your apartment's parking lot. Beyond it, you can see a few buildings and streets beneath a overcast night sky. "
            "If it was day, you could catch just a glimpse of the glimmering ocean out this window - an ocean you grew you up with and adore. But it's dark now."],
            keywords="window,windows"
        ))


        #Items
        bedroom101.addItem(StandardItems.Whiskey(**{
            "notTakenDesc":"A half-full bottle of whiskey is sitting on your desk.",
            "initPickupDesc":"You pick up the half-full bottle. It's dirt cheap and tastes insipid, but more potent than most whiskey. A personal favorite."
        }))

        bedroom101.addItem(UniqueItems.Bible())
        bedroom101.addItem(UniqueItems.Crucifix())

        #102 - BATHROOM
        bathroom102 = AreasFeatures.Area("Bathroom",
            ["You are in your bathroom. It's tiny and hasn't been cleaned in months. In here there is a toilet, shower, "
            "wastebasket, sink, sink mirror and a sink cabinet. To your east is a door leading to your bedroom."
            "\n\nYou're drunk and just want to go to sleep..."],
            **{"size":1})

        #Links
        door102A = StandardFeatures.StandardOpenDoor(
            ["A wooden door. It leads to your apartment's bedroom."],
            "door,east,wooden door,east door,bedroom door"
        )
        door101A.makeSibling(door102A)
        bathroom102.connect(bedroom101, door102A)
        bedroom101.connect(bathroom102, door101A)


        #Features
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["The white-tiled linoleum floor has several dirty footprint marks around it."],
            keywords="floor,ground,down,bathroom floor"
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["You haven't cleaned it in ages, so much of it is covered in grime and mold."],
            keywords="toilet,john"
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["They are painted a robin's egg blue. You've always liked the colour. Too bad so much of the paint is peeling off."],
            keywords="walls,wall,bathroom walls,bathroom wall"
        ))
        bathroom102.addFeature(UniqueFeatures.BathroomSink102())
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["This circular mirror is set into the wall just above your sink. It's dirty and needs a good dusting and "
            "wiping. You notice there are some small red marks in top left corner of the mirror."],
            keywords="mirror,bathroom mirror,my mirror",
            **{
                "useDescription":"Your face stares back at you. It's seen better days."
            }
        ))
        bathroom102.addFeature(AreasFeatures.Container(
            description=["A small, white cabinet set beneath your sink. Utterly fascinating."],
            keywords="cabinet,sink cabinet,bathroom cabinet,medicine cabinet",
            **{
                "insideDesc":"Inside there are a few bars of soap, some toilet paper and some cleaning supplies."
            }
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["It's very ordinary toilet paper. Value brand."],
            keywords="toilet paper,tp",
            **{
                "useDescription":"You don't need to at the moment.",
                "size":1
            }
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["There's a toilet plunger and some cleaning solution. You should probably use these to clean the place "
            "at some point, but not now. Sleep calls..."],
            keywords="cleaning supplies,plunger,cleaner,supplies",
            **{
                "size":1
            }
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["A few bars of soap.\n\n*YAWN*"],
            keywords="soap,bar of soap,soap bar",
            **{
                "size":1
            }
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["They look like bloodstains. You can't help but think they almost look a bit like a face grinning at you. "
            "They're probably from one one of the many times you've blacked out in here."],
            keywords="red marks,red stains,marks,bloodstains,blood stains"
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["It's your shower. Nothing particularly interesting about it."],
            keywords="shower,bathroom shower,my shower",
            **{
                "useDescription":"Not a chance. Right now you need sleep, not a shower."
            }
        ))
        bathroom102.addFeature(AreasFeatures.Feature(
            description=["An orange wastebasket that's overflowing with garbage."],
            keywords="wastebasket,waste basket,garbage,garbage can,garbage bin,rubbish bin"
        ))


        #Items


        #Enemies

        #103 - LIVING AREA
        livingArea103 = AreasFeatures.Area("Living Area",
            ["You are in your living area. It's divided between a living room and a tiny kitchen. Like the rest of your apartment "
            "it's in a state of neglect. Several garbage bags are strewn across the floor and even on your couch. In the living "
            "room there is a couch, a large painting, a few windows, a large bookshelf and a closet. In the "
            "kitchen there is a fridge, a sink and several drawers."
            "To the south is a door leading back to your bedroom. To the north is a door that exits your apartment suite."
            "\n\nYou're exhausted and drunk, and your body longs for sleep..."],
            **{"size":3})

        #Links
        door103A = StandardFeatures.StandardOpenDoor(
            ["A wooden door. It leads to your apartment's bedroom."],
            "door,south,wooden door,south door,bedroom door"
        )
        door103A.makeSibling(door101B)
        livingArea103.connect(bedroom101, door103A)
        bedroom101.connect(livingArea103, door101B)

        door103B = StandardFeatures.StandardUnopenableDoor(
            ["The exit to your apartment. It leads into the hallway of my floor."],
            "door,north,wooden door,north door,hallway door,hall door,apartment door",
            "You're exhausted and in no state to leave your aparetment right now. You need to get some sleep."
        )
        livingArea103.connect(bufferRoom, door103B)


        #Features
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["If you had to judge whether the kitchen or living room floor is less filthy you'd say the latter. After "
            "all, smaller spaces can't fit as much mess as large ones. You can't believe you once had the willpower to clean your floors on a weekly basis."],
            keywords="living room floor,kitchen floor,living area floor,floor,ground,down"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["These dull white walls are covered with puncture marks from tacks and nails. Once upon a time, a decent "
            "collection of paintings hung on the walls of your living room."],
            keywords="living room walls,kitchen walls,living area walls,walls,wall,ground,living room wall,kitchen wall,living area wall"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["It's a black, leather couch that seats three. A few full garbage bags are piled on top of it. You've never been one for chores."],
            keywords="couch,my couch,sofa,my sofa"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["This painting shows an Islamic mullah, a Jewish rabbi and a Christian priest enjoying a picnic together. "
            "Guests used to comment that it seemed to make them feel welcome. Back when you had guests that is."],
            keywords="painting,large painting,my painting,my large painting"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["Some look east and another south of your apartment. Unfortunately, any good views they might offer of the city are are obstructed "
            "by trees and buildings. Most of them don't even let in sunlight properly."],
            keywords="windows,living room window,window,living room windows,living area window, living area windows"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["This small library contains a wide assortment of old university texts, theological and philosophical treatises, books from your childhood "
            "and a great many literary classics. You never did much traveling, you always seemed more interested in learning from ideas than from places."],
            keywords="books,my books,book collection,library,small library"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["It's a very sturdy and heavy shelf edged with marble engravings. It holds a small library of books, mementos, some collectables and a bust "
            "of Saint Aeas."],
            keywords="bookshelf,shelf,bookcase,shelves,my bookcase,my bookshelf"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["There are so many relics of your past here. Photos, sketches of imaginary worlds, awards for academic excellence, letters from friends...\n\n"
            "You stumble across a certificate you were awarded at a university boxing club - \"Toughest Opponent\". True. Though you never acquired much skill, "
            "you sure as hell could take a lot of punishment - and you never once backed down from a fight."],
            keywords="mementos,photos,sketches,awards,letters"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["These are heaps upon heaps of trading cards, pogs, ancient coins, figurines, comic books and other items from your past. There's even an "
            "old Outdoor Explorer pocket knife from your childhood."],
            keywords="collectables,cards,coins,comics,comic books"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["This small, retractable knife is meant for use while hiking and camping. The blade's only three inches long, but it's still sharp."],
            keywords="knife,pocket knife,pocketknife,outdoor explorer knife",
            **{"getDescription":"You figure playing with a knife in your current state isn't the best idea. It can wait until morning."}
        ))
        livingArea103.addFeature(UniqueFeatures.BustOfAeas103())
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["The sink is filled with a veritable mountain of filthy dishes, some of which are covered in mould. It stinks of spoiled food "
            "and grease."],
            keywords="sink,my sink,kitchen sink,dishes,dirty dishes,filthy dishes"
        ))
        livingArea103.addFeature(AreasFeatures.Feature(
            description=["Eight or nine of these litter your apartment. All of them are overflowing with all manner of trash, from pizza boxes to spoiled food "
            "to beer bottles."],
            keywords="garbage,garbage bag,garbage bags"
        ))

        #Containers
        livingRoomCloset103 = AreasFeatures.Container(
            description=["This small closet is situated next to the exit to your apartment."],
            keywords="closet,my closet"
        )
        livingArea103.addFeature(livingRoomCloset103)

        kitchenDrawers103 = AreasFeatures.Container(
            description=["These store various utensils, pots, pans and other kitchen implements."],
            keywords="kitchen drawers,drawers,your drawers,your kitchen drawers,drawer,kitchen drawer"
        )
        livingArea103.addFeature(kitchenDrawers103)

        kitchenFridge103 = AreasFeatures.Container(
            description=["It stores perishable food. In other words, a fridge."],
            keywords="fridge,refridgerator,my fridge",
            **{
                "insideDesc":"The shelves are mostly bare except for a few scraps."
            }
        )
        livingArea103.addFeature(kitchenFridge103)

        #Items
        livingRoomCloset103.addItem(StandardItems.LeatherJacket(**{
            "notTakenDesc":"A lone leather jacket is hanging in the closet."
        }))
        kitchenFridge103.addItem(StandardItems.PizzaSlice(**{
            "notTakenDesc":"A large slice of pizza is on the shelf."
        }))


        #Items


        #Enemies


        #104 - PROLOGUE EXIT


        spawnLocation = bedroom101

        return spawnLocation

    def buildZone200(self):
        introMusic = None
        self.gameState.backgroundMusic = introMusic

        bufferRoom = AreasFeatures.Area(
            name="Buffer Room", 
            description=[" "])

        #Set starting stats for the player
        self.gameState.player.intoxication -= 15


        #101 - BEDROOM
        bedroom201 = AreasFeatures.Area(
            name="Bedroom", 
            description=["You are in your bedroom. It's furnished with a bed, chest of drawers, a large shelf, an armchair and a desk. "
            "Atop the desk there is a computer. Dirty laundry, miscellaneous papers and empty alcohol "
            "bottles are strewn about the floor. On the walls there are a few decorations and a window looking out to the south. "
            "To your west is a door leading to your bathroom. To the north is another door your kitchen/living room area."
            "\n\nScreams are coming from your living area..."],
            **{"size":2})

        spawnLocation = bedroom201

        return spawnLocation