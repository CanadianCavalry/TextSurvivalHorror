import AreasFeatures
import StandardItems

def findMatchingInventory(player, keyword, matching):
    for key,item in player.inventory.iteritems():
        keyList = key.split(",")
        if keyword in keyList:
            matching.append(item)

    return matching
    
def findMatching(player, keyword, matching):
    for key,item in player.currentLocation.connectedAreas.iteritems():
        keyList = key.split(",")
        if keyword in keyList:
            matching.append(item)

    for key,item in player.currentLocation.itemsContained.iteritems():
        keyList = key.split(",")
        if keyword in keyList:
            matching.append(item)
            
    for key,item in player.currentLocation.enemies.iteritems():
        keyList = key.split(",")
        if keyword in keyList:
            matching.append(item)
            
    for key,item in player.currentLocation.NPCs.iteritems():
        keyList = key.split(",")
        if keyword in keyList:
            matching.append(item)
            
    for key,item in player.currentLocation.features.iteritems():
        keyList = key.split(",")
        if keyword in keyList:
            matching.append(item)
            
    for feature in player.currentLocation.features.itervalues():
        if (isinstance(feature, AreasFeatures.Container)) and (feature.isOpen == True):
            for key,item in feature.itemsContained.iteritems():
                keyList = key.split(",")
                if keyword in keyList:
                    matching.append(item)
            
    return matching

def findMatchingWithHolder(player, keyword, matching):
    matching = findMatching(player, keyword, matching)
    holder = None

    for key,item in player.currentLocation.itemsContained.iteritems():
            keyList = key.split(",")
            if keyword in keyList:
                holder = player.currentLocation
    
    for feature in player.currentLocation.features.itervalues():
        if (isinstance(feature, AreasFeatures.Container)) and (feature.isOpen == True):
            for key,item in feature.itemsContained.iteritems():
                keyList = key.split(",")
                if keyword in keyList:
                    holder = feature

    for key,item in player.inventory.iteritems():
        keyList = key.split(",")
        if (keyword in keyList) and (len(matching) == 0):
            matching.append(item)
            holder = player

    return matching, holder

def selectEnemy(matching):
    closest = None
    for match in matching:
        if not hasattr(match, "health"):
            return False
        if (not closest) or (match.distanceToPlayer < closest.distanceToPlayer):
            closest = match
        elif match.distanceToPlayer == closest.distanceToPlayer:
            if match.health < closest.health:
                closest = match
    return closest

def go(player, keyword):
    matching = findMatching(player, keyword, list())

    if len(matching) == 0:
        return "You can't go that way."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        #try:
        return matching[0].travel(player)
        #except AttributeError:
        #    return "I can't do that."

def use(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
            
    if len(matching) == 0:
        return "You do not see anything like that."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].use(player)
        except AttributeError:
            return "You can't use that."
    return

def useOn(player, targetKeyword, recipientKeyword):
    matchingTarget = list()
    for key,item in player.inventory.iteritems():           #first we find the item to be used, which will be an item
        keyList = key.split(",")
        if targetKeyword in keyList:
            matchingTarget.append(item)
            
    if len(matchingTarget) > 1:
        return "You need to be more specific"
    
    for key,item in player.currentLocation.itemsContained.iteritems():          #didn't find the item in the players inventory, so we
        keyList = key.split(",")                                                #search the room for it
        if targetKeyword in keyList:
            matchingTarget.append(item)
            
    if len(matchingTarget) == 0:
        return "You do not have any such item."
    elif len(matchingTarget) > 1:
        return "You need to be more specific"
    elif len(matchingTarget) == 1:
        target = matchingTarget[0]                                            #by here we have found the item to use if it exists
        
    matching = list()
    for key,item in player.currentLocation.features.iteritems():          #now we find the recipient, which will be a feature or link
        keyList = key.split(",")
        if recipientKeyword in keyList:
            matching.append(item)
            
    if len(matching) > 1:
        return "You need to be more specific."
                                                                            
    for key,item in player.currentLocation.connectedAreas.iteritems():      #Now we search in the links list
        keyList = key.split(",")
        if recipientKeyword in keyList:
            matching.append(item)
            
    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        recipient = matching[0]
            
    try:
        return target.useOn(player, recipient)
    except AttributeError:
        return "You cannot use that in that way."

def get(player, keyword):
    matching, holder = findMatchingWithHolder(player, keyword, list())
    
    if len(matching) > 0 and holder == player:
        return "You are already carrying that."

    if len(matching) == 0:
        return "You do not see any such item here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].get(holder, player)
        except AttributeError:
            return "You can't pick that up."

def drop(player, keyword):
    matching = findMatchingInventory(player, keyword, list())
            
    if len(matching) == 0:
        return "You do not have any such item."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].drop(player)
        except AttributeError:
            return "You can't drop that right now."

def attack(player, keyword):
    if keyword == "":
        keyword = "enemy"

    matching = findMatching(player, keyword, list())
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    #try:
    return player.attack(matching[0])
    #except AttributeError:
    #   return "I see no reason to attack that right now."
        
def heavyAttack(player, keyword):
    if keyword == "":
        keyword = "enemy"

    matching = findMatching(player, keyword, list())
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    try:
        return player.heavyAttack(matching[0])
    except AttributeError:
        return "I see no reason to attack that right now."

def shoot(player, keyword):
    if keyword == "":
        keyword = "enemy"

    matching = findMatching(player, keyword, list())
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    try:
        return player.attack(matching[0])
    except AttributeError:
        return "That isn't worth wasting ammo on."

def reload(player):
        return player.reload()

def defend(player):
    return player.defend()

def exorcise(player, keyword):
    if keyword == "":
        keyword = "enemy"

    matching = findMatching(player, keyword, list())
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    try:
        return player.exorcise(matching[0])
    except AttributeError:
        return "You can only exorcise demonic creatures."

def advance(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    try:
        return player.advance(matching[0])
    except AttributeError:
        return "That isn't an enemy."
    
def retreat(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    try:
        return player.retreat(matching[0])
    except AttributeError:
        return "That isn't an enemy."
            
def equip(player, keyword):
    matching = findMatchingInventory(player, keyword, list())
    matching = findMatching(player, keyword, matching)
            
    if len(matching) == 0:
        return "You are not carrying anything like that."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].equip(player)
        except AttributeError:
            return "That isn't something you can equip."

def wear(player, keyword):
    matching = findMatchingInventory(player, keyword, list())
    matching = findMatching(player, keyword, matching)
            
    if len(matching) == 0:
        return "You are not carrying anything like that."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].wear(player)
        except AttributeError:
            return "That isn't something you can put on."

def openThing(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
        
    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific."
    elif len(matching) == 1:
        try:
            return matching[0].open(player)
        except AttributeError:
            return "You can't open that."

def closeThing(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
        
    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific."
    elif len(matching) == 1:
        try:
            return matching[0].close(player)
        except AttributeError:
            return "You can't close that."

def unlock(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
        
    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific."
    elif len(matching) == 1:
        try:
            return matching[0].tryUnlock(None, player)
        except AttributeError:
            return "That doesn't have a lock."

def lock(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
        
    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific."
    elif len(matching) == 1:
        try:
            return matching[0].tryLock(None, player)
        except AttributeError:
            return "That doesn't have a lock."

def search(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)

    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific."
    elif len(matching) == 1:
        try:
            return matching[0].search(player)
        except AttributeError:
            return "You can't search that."

def drink(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) == 0:
        return "You do not see any such item here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].drink(player)
        except AttributeError:
            return "You can't drink that."

def eat(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) == 0:
        return "You do not see any such item here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].eat(player)
        except AttributeError:
            return "That isn't edible."

def wait(player):
    return player.wait()

def read(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) == 0:
        return "You do not see any such item here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].read(player)
        except AttributeError:
            return "That isn't something you can read."
    
def talk(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 0:
        return "You do not see anyone like that here."
    elif len(matching) == 1:
        try:
            return matching[0].talk(player)
        except AttributeError:
            return "I don't think it's very likely to respond."
    
def ask(player, keyword, dialogueKeyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 0:
        return "You do not see anyone like that here."
    elif len(matching) == 1:
        try:
            return matching[0].ask(dialogueKeyword)
        except AttributeError:
            return "I don't think it's very likely to respond."

def push(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)

    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].push(player)
        except AttributeError:
            return "Why would you want to push on that?"

def pull(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)

    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].pull(player)
        except AttributeError:
            return "Why would you want to pull on that?"

def cut(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)

    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].cut(player)
        except AttributeError:
            return "That doesn't particularly need to be cut..."

def sleep(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)

    if len(matching) == 0:
        return "You do not see anything like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].sleep(player)
        except AttributeError:
            return "That's not somewhere you'd particularly like to fall asleep."

def inventory(player):
    if len(player.inventory) == 0:
        return "You are not carrying anything."
    
    inventoryString = "Your current inventory:\n"
    for item in player.inventory.itervalues():
        inventoryString += item.name.title()
        if item.quantity > 1:
            inventoryString += " (" + str(item.quantity) + ")"
        inventoryString += "\n"
    return inventoryString

def stats(player):
    healthString = "Condition: " + player.getCondition()
    
    spiritString = "Spiritual Strength: " + player.getSpirit()

    intoxicationString = "Intoxication: " + player.getIntoxication()
        
    mainHandString = "Main hand: "
    if player.mainHand:
        mainHandString += player.mainHand.name
    else:
        mainHandString += "Nothing"
        
    offHandString = "Off hand: "
    if player.offHand:
        offHandString += player.offHand.name
    else:
        offHandString += "Nothing"
        
    armorString = "Armor: "
    if player.armor:
        armorString += player.armor.name
    else:
        armorString += "Nothing"
        
    statString = healthString + "\n"
    statString += intoxicationString + "\n"
    statString += spiritString + "\n\n"
    statString += mainHandString + "\n"
    statString += offHandString + "\n"
    statString += armorString + "\n"
    return statString

def look(player, keyword):
    #Check if this is a general look command
    if keyword == "":
        # if it is, describe the room and items in it     
        return player.currentLocation.lookAt(player)
    
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        autoTarget = selectEnemy(matching)
        if not autoTarget:
            return "You need to be more specific"
        matching[0] = autoTarget
    return matching[0].lookAt(player)

def displayHelp():
    helpText = ("List of common commands. Words in parenthesis () are optional\n\n"
    "look: Describe the room you are in (used by default when entering an area.\n"
    "look (at) something: Take a closer look at something.\n"
    "get/drop something: Pick something up or drop something in your inventory.\n"
    "go direction: Travel in a direction, or through a door/path.\n"
    "use something: Trigger the \"default\" use of an object. ie. sleep in a bed, turn on a sink etc..\n"
    "use item on something: Use an item or object on something in the room.\n"
    "unlock/lock something: Locks or unlocks a door or container. You may need a key.\n"
    "drink/eat something: Consume an item.\n"
    "equip item: Equip a weapon or piece of armor.\n"
    "attack (something): Uses your currently held weapon.\n"
    "heavy attack (something): Stronger, but less accurrate. Chance to stun.\n"
    "shoot: Attack with a ranged weapon.\n"
    "reload: Reload the currently equipped weapon (requires ammo).\n"
    "exorcise (something): Effect varies depending on the target.\n"
    "defend: spend your turn dodging.\n"
    "advance/retreat (on/from) (something): move towards or away from something.\n"
    "open/close something: open or close a door or container.\n"
    "read something: read a sign, note or book.\n\n"
    "There are many other circumstantial commands to discover. Use the environment to your advantage. Try different approaches!")

    return helpText


#Dev commands
def devCommand(player, command):
    if command == "dylanwantsagun":
        player.addItem(StandardItems.WeskersRevolver())
        return "Now I just feel sorry for the demons."
    elif command == "goodtogo":
        player.heal(500)
        return "Pumped up"
    elif command == "cleanasawhistle":
        player.decreaseIntox(100)
        return "Sober"
    elif command == "barneyismyhero":
        player.increaseIntox(100)
        return "Hammered"
    elif command == "heyzeus":
        player.increaseSpirit(100)
        return "Saintly"
    elif command == "walkindude":
        player.decreaseSpirit(100)
        return "The Antichrist"