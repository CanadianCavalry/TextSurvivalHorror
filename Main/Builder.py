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

#Tutorial section
def buildCombatSimulator(gameState):
    #INTRO
    introText = "Welcome to the tutorial! This area is intended to allow you to learn the basic game commands and practice fighting with various weapons. That said, it is still quite easy to die, so don't get complacent. To get started head through the north door, but before you head out, take a look at the table and make sure you are suitibly equipped. There's no coming back here once you leave.\n\n To get your bearings, type \"look\". To get a closer look at anything, type \"look\" followed by the object."
    gameState.introText = introText

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

    armory001.addFeature(StandardFeatures.AlwaysOpenContainer(
        "The table is littered with all manner of useless junk, as well as a number of weapons, bottles and items of clothing.",
         "table,small table, metal table"))
    armory001.addFeature(StandardFeatures.Sign(
        ["The large metal sign looks very worn and rusted, and has been riveted straight into the metal wall. It appears that "
        "it has been here for a long time, and is not coming down any time soon."],
        "sign,metal sign, plaque, brass sign, brass plaque",
        "Tips for Newbies\n\n-Make sure you have a melee weapon and some armor before moving on.\n-Every "
        "weapon has different damage and accuracy. Bigger is not always better.\n-As a functioning alchoholic, you perform "
        "better with a bit of liquor in your system. It numbs your body, reducing incoming damage, and calms shaking hands, "
        "increasing accurracy. Don't go overboard though or you'll go downhill fast.\n\nTyping HELP will list all "
        "commands(not implemented yet), but a few you should get familiar with to start are:\nGET - Pick up things\nI - View your "
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
        "initPickupDesc":"You lift the axe from the table. It has a weight and heft that is comfortable in your hands."
    }))
    armory001.addItem(StandardItems.LeatherJacket())
    armory001.addItem(StandardItems.Flask())
    armory001.addItem(Items.Note(
        name="Strange Note",
        description="A hastily written note scrawled on a napkin.",
        seenDescription="There is a scrunched up note pinned to the table.",
        keywords="note,paper,napkin,page",
        contents="FOR TESTER USE ONLY\nDev commands are executed with \"/dev\":\n\ndylanwantsagun: Get some firepower.\n\n       -dev"
    ))
    
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
        "west,west door,door,metal door,steel door",
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
    door003A = StandardFeatures.StandardOpenMetalDoor(
        ["A steel door. It leads back out into the arena."],
        "east,east door,door,metal door,steel door")
    door003A.makeSibling(door002B)
    libraryFoyer003.connect(arena002, door003A)
    arena002.connect(libraryFoyer003, door002B)

    door003B = StandardFeatures.StandardOpenDoor(
        ["A heavy wooden door, oak or some kind of hardwood. It been smashed, as though something too large to fit forced it's way "
        "through into the library. It's hanging crooked on it's hinges and the frame has deep gouges in it."],
        "west,west door,door,wood door,wooden door,oak door,hardwood door")

    #Features
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
    
    libraryDeskDrawer.addItem(StandardItems.FirstAidKit(**{
        "notTakenDesc":"A first aid kit is lying in the drawer amongst the pens and loose paper."
        }))
    libraryFoyer003.addFeature(libraryDeskDrawer)

    #004 - LIBRARY EAST WING
    libraryEast004 = AreasFeatures.Area(
        "Library - East Wing", 
        ["This part of the library is a mess, books scattered across the floor, shelves knocked over or slanted precariously over "
        "the aisle. One massive shelf in particular is leaning so far over you're amazed it's still upright. There is what looks like"
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
    door005A = AreasFeatures.Link(
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
    bentHost007A.description = ["Though human, the twisted facial features and sadistic grin mark him as the puppet of an demonic creature. "
            "Long, deep slashes cover his exposed forearms and wrists, and his clothes are smeared in blood both dried and fresh. "
            "He carries a pair of scissors in one hand."]
    bentHost007A.seenDescription = "A wounded, blood soaked man carrying a pair of scissors is here with you."
    bentHost007A.corpse.addItem(StandardItems.CrossbowBolt(**{
        "notTakenDesc":"You find a crossbow bolt tucked into his waistband."
    }))
    bentHost007A.protectThing(crossbow007)
    generatorRoom007.spawnEnemy(bentHost007A, 1)


    #008 - UTILITIES ROOM
    utilitiesRoom008 = AreasFeatures.Area(
        "Utilities Room", 
        ["This room is quite large, and filled with all kinds of pipes, electrical conduits, and ventilation ducts. It seems "
        "to be a central utility room. Most of the equipment is in a state of disrepair, and several inches of water cover the floor. "
        "There is a narrow door on the wall to the south, and another one leading back the basement entrance to the west."],
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
    #arena002.addItem(key005A)

    gameState.addArea(spawnLocation)

def buildWorld(gameState):
    buildPrologue100(gameState)
    #buildAreaOne200(gameState)
    
def buildPrologue100(gameState):
    #INTRO
    introText = "Intro text still goes here."
    gameState.introText = introText

    #JACOBS ROOM
    jacobsRoom101 = AreasFeatures.Area("Jacob's Room", ["This small room is well furnished with all of the comforts \
you could ask for, including a bed, bookshelf, coffee table, dresser, tv and \
chairs.\nIt even contains a personal bathroom. On the far wall hangs a small \
painting next to the single window. Next to these is my closet. There is a door \
to the west leading to the residential wing."])
    
    #Links
    door101A = StandardFeatures.StandardOpenDoor(
        ["A hefty blue wooden door."],
        "east,door,east door,blue door,wood door,hallway"
    )
    
    #NPCs
    
    #Features
    jacobsRoom101.addFeature(AreasFeatures.Feature("This tall, wooden bookshelf is filled with books on a variety of my favorite subjects - notably theology, history and literature. It also includes \na large red bible (NIV version)", "bookshelf,shelf"))
    jacobsRoom101.addFeature(AreasFeatures.Feature("A beautiful painting by my brother, Fernando. It's of Jesus curing a blind man. The caption underneath reads 'Once I was blind, and now I see'. \nThe look of childlike surprise and utter gratitude on the mans face always fills me with hope.", "painting"))
    jacobsRoom101.addFeature(AreasFeatures.Feature("A very comfortable queen sized bed. I've been in the habit of making it immediately after waking since I was a very small child.", "bed,queen bed"))
    jacobsRoom101.addFeature(AreasFeatures.Feature("Contains my clothes","dresser"))
    jacobsRoom101.addFeature(AreasFeatures.Feature("Two very comfortable armchairs. I often sit here while praying.","chair,chairs,armchair,armchairs"))
    jacobsRoom101.addFeature(AreasFeatures.Feature("A small, personal bathroom complete with a sink, shower and toilet. Lately I've gotten into the habit of cleaning it on a weekly basis. \nIt often takes my mind off of my cravings.","bathroom,sink,toilet,shower"))
    jacobsRoom101.addFeature(UniqueFeatures.JacobRoomWindow101())
    jacobsRoom101.addFeature(AreasFeatures.Feature("This entertainment unit comes with a 42 inch LED, that includes cable and a PVR. On the bottom shelf are a variety of DVD's I've\n taken from The House library, as well as my personal collection of Dr. Who and Star Trek TNG box sets.","tv,entertinment stand,entertainment center"))              #Add ability to turn on)
    
    #Containers
    coffeeTable101 = StandardFeatures.AlwaysOpenContainer(
        "A heavy wood coffee table, about 2 feet high. Oak, if I had to guess. Looks brand new. There are a dozen or so papers and notes scattered across the top of it. ",
        "coffee table,table"
    )
    jacobsRoom101.addFeature(coffeeTable101)
    closet101 = AreasFeatures.Container(
        "A fairly small closet, but big enough to hold a few sets of clothes. I haven't had much use for it since I've been here. Don't even remember what I put in it.",
        "closet",
        **{"openDesc":"The closet opens easily, though a little noisily.", "closeDesc":"The door slides closed."}
    )
    jacobsRoom101.addFeature(closet101)
    
    #Items
    coffeeTable101.addItem(StandardItems.Note("Notice on New Policies", "A note given to the residents about changes to the facilities policies since Father Malachi took over.", "A notice on house policy changes is on the table.", 1, "note,policy note,notice,policy notice,changes notice,policy changes notice", "There be changes to the policy, bitches."))
    coffeeTable101.addItem(Items.Item("Guide to House Services", "To be filled", "A guide to house services is on the table.", 1, "guide,house guide,services guide,house services guide"))
    coffeeTable101.addItem(Items.Item("Rejuvinax Note", "To be filled", "A note about Rejuvinax is on the table.", 1, "note,rejuvinax note,drug note"))
    closet101.addItem(Items.Alchohol("Flask of Scotch", "A small silver flask which holds about 4 oz. I received this as a gift from a friend form church before they realized I had a problem. I'm sure they regretted giving it to me once they found out.", "There is a small silver flask on the floor.", 1, "flask,whiskey,scotch,silver flask,flask of scotch,alcohol,booze", "You unscrew the cap and drain the remaining liquid from the flask. Delicious.",10))
    closet101.addItem(StandardItems.LeatherJacket())
    
    gameState.addArea(jacobsRoom101)
    
    #FIRST FLOOR HALLWAY
    firstFloorHallway102 = AreasFeatures.Area("First Floor Hallway", 
["The Residents wing contains all of the private living spaces for House residents. It includes 3 \
floors with ten rooms each. Featuring a  gingerbread-coloured carpet and vermillion walls with fancy, five-bulbed lamps set \
into them, the hallway is large and airy with an upper-class feel. Rooms 101-105 are on the east side of the hallway and Rooms \
106-110 are on the west. Room 106 is my room, and the door to Room 104 is ajar. A set of stairs that leads up to the second \
floor of the Residents wing can be accessed through this hallway. To the SOUTH is a door that leads into the Main Lobby, and another \
door to the NORTH leads into the Essential Services area of the Residents Wing."])
    
    #Links
    door102A = StandardFeatures.StandardOpenDoor(["A hefty blue wooden door. The room number is 106."], "west,door,west door,blue door,room 106,106,door 106,jacobs door,jacob door,my room")
    door102A.makeSibling(door101A)
    jacobsRoom101.connect(firstFloorHallway102, door101A)
    firstFloorHallway102.connect(jacobsRoom101, door102A)
