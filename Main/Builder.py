'''
Created on Jun 30, 2014

@author: Thomas
'''
import AreasFeatures
import StandardFeatures
import UniqueAreas
import UniqueFeatures
import Items
import StandardItems
import UniqueItems
import Enemies
import UniqueEnemies
import NPCs
import UniqueNPCs

def buildCombatSimulator(gameState):
    #INTRO
    introText = "Welcome to the combat simulator. This area is intended to allow you to practice fighting with various weapons. To get started head through the north door, but before you head out, take a look at the table and make sure you are suitibly equipped. There's no coming back here once you leave.\n\n To get your bearings, type \"look\". To get a closer look at anything, type \"look\" followed by the object."
    gameState.introText = introText

    #Combat Test Environment
    #ARMORY
    armory = AreasFeatures.Area("Armory", ["This tiny, cramped room is lined on all sides by large steel cages packed with weapons of every kind. Sadly, they are all locked. On the metal table in the center of the room is a small collection of items, and a large sign is bolted to the east wall titled \"Tips for newbies\". There is a door to the north."])
    arenaDoorA = StandardFeatures.StandardOpenMetalDoor("A heavy steel door. It appears to have some sort of mechanism built into it that locks it once you pass through.", "north,north door,door,metal door,steel door")
    
    table = StandardFeatures.AlwaysOpenContainer("The table is littered with all manner of useless junk, as well as a number of weapons, bottles and items of clothing.", "table,small table, metal table")
    armory.addFeature(table)
    armorySign = StandardFeatures.Sign("The large metal sign takes up a large portion of the east wall. It reads \"Please ensure you are prepared before continuing to the test arena. Good luck\"", "sign,metal sign, plaque, brass sign, brass plaque", "Tips for Newbies\n\n-Make sure you have a melee weapon and some armor before moving on. Ammo is scarce.\n-Every weapon has different damage and accuracy. Bigger is not always better.\n-As a functioning alchoholic, you perform better with a bit of liquor in your system. It numbs your body, reducing incoming damage, and calms shaking hands, increasing accurracy. Don't go overboard though or you'll go downhill fast.\n\n-Typing HELP will list all commands(not implemented yet), but a few you should get familiar with to start are:\nGET - Pick up things\nI - View your inventory\nEQUIP - Equip weapons or armor\nGO - Travel through doors or down halls\nOPEN - Open doors or containers")
    armory.addFeature(armorySign)
    armory.addItem(StandardItems.LongSword())
    armory.addItem(StandardItems.Crossbow())

    table.addItem(StandardItems.Axe())
    table.addItem(StandardItems.KitchenKnife())
    table.addItem(StandardItems.Revolver())
    table.addItem(StandardItems.RevolverAmmo())
    table.addItem(StandardItems.LeatherJacket())
    table.addItem(StandardItems.CrossbowBolt())
    table.addItem(StandardItems.CrossbowBolt())
    
    #ROOM 01 - ARENA
    combatRoom01 = AreasFeatures.Area("Arena", ["You are standing in a large, empty colosseum. Against the east wall is a massive sign carved from stone titled \"Combat Tips\". There is a single, steel door to the south."])    
    arenaDoorB = StandardFeatures.StandardLockedDoor("A heavy steel door. It has no handle or lock that you can see.", "south,door,metal door,steel door", None)
    arenaDoorB.makeSibling(arenaDoorA)
    combatRoom01.connect(armory, arenaDoorB)
    armory.connect(combatRoom01, arenaDoorA)

    combatSign = StandardFeatures.Sign("The large metal sign takes up a large portion of the east wall. It reads \"Please ensure you are prepared before continuing to the test arena. Good luck\"", "sign, stone sign, large sign", "Combat Tips\n\n-Every enemy has different strengths and weaknesses. Examining an enemy takes no time, and may yield life-saving information.\n-Heavy attacks are less accurate, but deal more damage and can even stun some foes.\n-Exorcising a demonic enemy can have numerous effects, but will often stun or incapacitate them. Some enemies are more resilient to exorcism than others.\n-Performing a heavy attack against a stunned enemy will often result in an execution.\n\n-Important combat commands:\nATTACK - Attack with an equipped weapon\nHEAVY ATTACK - Slower, stronger attack\nEXORCISE - Invoke your faith to weaken an enemy\nRELOAD - Reload your equipped gun(requires ammo)\nDEFEND - Give up your chance to strike to increase your chances of dodging the next attack.")
    combatRoom01.addFeature(combatSign)
    
    testDemon = Enemies.TestDemon()
    combatRoom01.spawnEnemy(testDemon)
    
    gameState.addArea(armory)

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
    door101A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door.", "east,door,east door,blue door,wood door,hallway")
    
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
    coffeeTable101 = StandardFeatures.AlwaysOpenContainer("A heavy wood coffee table, about 2 feet high. Oak, if I had to guess. Looks brand new. There are a dozen or so papers and notes scattered across the top of it. ", "coffee table,table")
    jacobsRoom101.addFeature(coffeeTable101)
    closet101 = StandardFeatures.UnlockedContainer("A fairly small closet, but big enough to hold a few sets of clothes. I haven't had much use for it since I've been here. Don't even remember what I put in it.", "closet", "The closet opens easily, though a little noisily.", "The door slides closed.")
    jacobsRoom101.addFeature(closet101)
    
    #Items
    coffeeTable101.addItem(StandardItems.Note("Notice on New Policies", "A note given to the residents about changes to the facilities policies since Father Malachi took over.", "A notice on house policy changes is on the table.", "A notice on house policy changes is on the table.", 1, "note,policy note,notice,policy notice,changes notice,policy changes notice", "There be changes to the policy, bitches."))
    coffeeTable101.addItem(Items.Item("Guide to House Services", "To be filled", "A guide to house services is on the table.", "A guide to house services is on the table.", 1, "guide,house guide,services guide,house services guide"))
    coffeeTable101.addItem(Items.Item("Rejuvinax Note", "To be filled", "A note about Rejuvinax is on the table.", "A note about Rejuvinax is on the table.", 1, "note,rejuvinax note,drug note"))
    closet101.addItem(StandardItems.Alchohol("Flask of Scotch", "A small silver flask which holds about 4 oz. I received this as a gift from a friend form church before they realized I had a problem. I'm sure they regretted giving it to me once they found out.", "There is a small silver flask on the floor.", "There is a small silver flask tucked into the corner of the closet.", 1, "flask,whiskey,scotch,silver flask,flask of scotch,alcohol,booze", "You unscrew the cap and drain the remaining liquid from the flask. Delicious.",10))
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
    door102A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door. The room number is 106.", "west,door,west door,blue door,room 106,106,door 106,jacobs door,jacob door,my room")
    door102A.makeSibling(door101A)
    jacobsRoom101.connect(firstFloorHallway102, door101A)
    firstFloorHallway102.connect(jacobsRoom101, door102A)
    
    door102B = StandardFeatures.StandardOpenDoor("A hefty blue wooden door. The room number is 104.", "east,door,east door,blue door,room 104,104,door 104")
    
    #mainLobby109
    door102C = StandardFeatures.StandardOpenDoor("A set of thick metal double doors. The sign above them reads \"Main Lobby\".", "south,door,south door,metal door,double doors,lobby,main lobby")
    
    #essentialServices201
    door102D = StandardFeatures.StandardOpenDoor("A fairly ordinary wooden door. The sign above it reads \"Essential Services\".", "north,door,north door,essential services door,essential services")
    
    
    stairs102A = StandardFeatures.StandardUpwardStairs("A wide, well lit staircase which double back up to the second floor.", "up,upstairs,up stairs,up staircase,staircase,stairs,stairway")
    
    #NPCs
    firstFloorHallway102.addNPC(UniqueNPCs.SecurityGuards102())
    
    #Features
    firstFloorHallway102.addFeature(UniqueFeatures.ResidentsWingDoorsFirstFloor102())
    
    #MAIN LOBBY

    
    #ROOM 104
    cicerosRoom103 = AreasFeatures.Area("Room 104",
    ["This room belongs to a rather odd resident named Cicero, who I have developed something of a friendship  with recently. The books, \
pages, and  trinkets scattered all over the room are a testimony to Cicero's tendency to place all his focus on his personal projects \
and ignore everything else. It seems all the books are about mythology, and the pages are either notes of his or clips of papers \
he wrote at Oxford long ago. The trinkets are various curiousities owned by Cicero, some which of he's told me are valuable historical \
artifacts. The door to the hallway is to the west."])
    
    #Links
    door103A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door.", "west,door,west door,blue door,hallway")
    door103A.makeSibling(door102B)
    firstFloorHallway102.connect(cicerosRoom103, door102B)
    cicerosRoom103.connect(firstFloorHallway102, door103A)
    
    #NPCs
    cicerosRoom103.addNPC(UniqueNPCs.Cicero103())
    
    #Features
    
    #Containers
    
    #Items
    
    #SECOND FLOOR HALLWAY
    secondFloorHallway104 = AreasFeatures.Area("Second Floor Hallway", 
["This hall is nearly identical to the first floor. Rooms 201-205 are on the east side of the hallway and Rooms \
206-210 are on the west. The door to Rooms 201 and 205 are ajar. Two sets of stairs that lead to the first and third \
floor of the Residents wing can be accessed through this hallway."])
    
    #Links
    door104A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door. The room number is 201.", "east,door,east door,blue door,room 201,201,door 201")
    door104B = StandardFeatures.StandardOpenDoor("A hefty blue wooden door. The room number is 205.", "east,door,east door,blue door,room 205,205,door 205")
    
    stairs104A = StandardFeatures.StandardDownwardStairs("A wide, well lit staircase which goes both up to the third floor and down to the first floor.", "down,downstairs,down stairs,down staircase,staircase,stairs,stairway")
    stairs104A.makeSibling(stairs102A)
    firstFloorHallway102.connect(secondFloorHallway104, stairs102A)
    secondFloorHallway104.connect(firstFloorHallway102, stairs104A)
    
    stairs104B = StandardFeatures.StandardUpwardStairs("A wide, well lit staircase which goes both up to the third floor and down to the first floor.", "up,upstairs,up stairs,up staircase,staircase,stairs,stairway")
    
    #NPCs
    
    #Features
    secondFloorHallway104.addFeature(UniqueFeatures.ResidentsWingDoorsSecondFloor104())
    
    #Containers
    
    #Items
    
    #MICHEALS ROOM
    michealsRoom105 = AreasFeatures.Area("Room 201",
["This room is a mess. Bits of old food, dirty laundry, and other things whose origin you would rather not contemplate are scattered over\
every surface. The place reeks of cigarette smoke. So many used cigarette butts are littered over it that you feel like it's a room-sized ashtray. \
The door to the hallway is to the west."])
    
    #Links
    door105A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door.", "west,door,west door,blue door,hallway")
    door105A.makeSibling(door104A)
    secondFloorHallway104.connect(michealsRoom105, door104A)
    michealsRoom105.connect(secondFloorHallway104, door105A)
    
    #NPCs
    michealsRoom105.addNPC(UniqueNPCs.Micheal105())
    
    #Features
    michealsRoom105.addFeature(AreasFeatures.Feature("Everything in this room is completely disgusting. I'd really rather not look to closely.", "mess,garbage,cigarettes,butts,cigarette butts,stuff,food,old food,room,things"))
    
    #Containers
    
    #Items
    
    #ASTRIDS ROOM
    astridsRoom106 = AreasFeatures.Area("Room 205",
["This room belongs to Astrid, a slender, middle aged woman. The place is as immaculate and tidy as ever. Unlike most \
of the other residents in the House, Astrid has completely rearranged the furnishings in her room to suit her needs. \
She even got permission from the management to move out one of the two armchairs that come with every room so she could \
place a tall, gaudy mirror in its place. The centrepiece of the room is a large table upon which pictures of Astrid and \
her various trophies and awards are arranged; I always think of this as Astrid's shrine to herself. The door to the hallway is to the west."])
    
    #Links
    door106A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door.", "west,door,west door,blue door,hallway")
    door106A.makeSibling(door104B)
    secondFloorHallway104.connect(astridsRoom106, door104B)
    astridsRoom106.connect(secondFloorHallway104, door106A)
    
    #NPCs
    astridsRoom106.addNPC(UniqueNPCs.Astrid106())
    
    #Features
    
    #Containers
    
    #Items
    
    #THIRD FLOOR HALLWAY
    thirdFloorHallway107 = AreasFeatures.Area("Third Floor Hallway", 
["This hall is nearly identical to the first floor. Rooms 301-305 are on the east side of the hallway and Rooms \
206-210 are on the west. The door to Room 308 is ajar. A staircase leads down to the second floor from here."])
    
    #Links
    door107A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door. The room number is 308.", "west,door,west door,blue door,room 308,308,door 308")
    
    stairs107A = stairs104A = StandardFeatures.StandardDownwardStairs("A wide, well lit staircase which goes down to the second floor.", "down,downstairs,down stairs,down staircase,staircase,stairs,stairway")
    stairs107A.makeSibling(stairs104B)
    secondFloorHallway104.connect(thirdFloorHallway107, stairs104B)
    thirdFloorHallway107.connect(secondFloorHallway104, stairs107A)
    
    #NPCs
    
    #Features
    thirdFloorHallway107.addFeature(UniqueFeatures.ResidentsWingDoorsThirdFloor107())
    
    #Containers
    
    #Items
    
    #ROSES ROOM
    rosesRoom108 = AreasFeatures.Area("Room 308",
["Rose - a talented artist - has hung up at least a dozen of her works on the walls of this room. Most of them are either charcoal \
sketches or oil paintings of individuals surrounded by fairylike creatures that evoke the individuals moods. \
All of the pieces project a lot of raw emotion. There are also a few pictures of Rose's friends, her mother, and a few posters \
of her favourite bands. The door to the hallway is to the east."])
    
    #Links
    door108A = StandardFeatures.StandardOpenDoor("A hefty blue wooden door.", "east,door,east door,blue door,hallway")
    door108A.makeSibling(door107A)
    thirdFloorHallway107.connect(rosesRoom108, door107A)
    rosesRoom108.connect(thirdFloorHallway107, door108A)
    
    #NPCs
    rosesRoom108.addNPC(UniqueNPCs.Rose108())
    
    #Features
    
    #Containers
    
    #Items
    
    #MAIN LOBBY
    mainLobby109 = AreasFeatures.Area("Main Lobby",
["The lobby features an elegant water fountain near the entrance and a large reception desk in the middle of it. A woman standing \
in front of the reception desk appears quite agitated, and is arguing with the two receptionists on duty. NORTH of you is the door to the Quarters area of the \
Residential Wing. At the SOUTH end of the lobby is the exit that leads out to the rest of the city. Two security guards in front of it."])
    
    #Links
    door109A = StandardFeatures.StandardOpenDoor("A set of thick metal double doors. The sign above them reads \"Residents Wing\".",
"north,door,north door,metal door,double doors,residents wing,resident wing")
    door109A.makeSibling(door102C)
    mainLobby109.connect(firstFloorHallway102, door109A)
    firstFloorHallway102.connect(mainLobby109, door102C)
    
    #Need to add door to outside
    
    #NPCs
    mainLobby109.addNPC(UniqueNPCs.SecurityGuards109())
    mainLobby109.addNPC(UniqueNPCs.Hayley109())
    
    #Features
    mainLobby109.addFeature(AreasFeatures.Feature("The water fountain is beautifully crafted out of marble. In front of it is a pedestal that reads \"And be not drunk \
with wine, wherein is excess, but be filled with the spirit. (Ephesians 5:18)\". You are dismayed to find that \"Not even God can save you!\" is carved in big, ugly letters next to the verse from Ephesians. How strange and disgusting! Strange that you've never noticed this \
vandalism before. You can't imagine who would be stupid enough to do something like this in a room patrolled by security guards 24 7.", "fountain,water,water fountain,waterfountain"))
    mainLobby109.addFeature(AreasFeatures.Feature("A large, sermicircular, oak table. The two receptionists working behind it appear to be trying to calm down a very upset young woman.","reception desk,desk"))
    mainLobby109.addFeature(UniqueFeatures.MainLobbyExteriorDoor109())
    
    #Containers
    
    #Items
    
def buildAreaOne200(gameState):
    jacobsRoom201 = UniqueAreas.interrogationRoom201()
    gameState.addArea(jacobsRoom201)