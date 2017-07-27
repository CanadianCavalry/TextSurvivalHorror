import AreasFeatures

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

def go(player, keyword):
    matching = findMatching(player, keyword, list())

    if len(matching) == 0:
        return "You can't go that way."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].travel(player)
        except AttributeError:
            return "I can't do that."

def use(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
            
    if len(matching) == 0:
        return "You do not see anything like that."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return matching[0].use()
        except AttributeError:
            return "I can't use that."
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
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return player.attack(matching[0])
        except AttributeError:
           return "I see no reason to attack that right now."
        
def heavyAttack(player, keyword):
    if keyword == "":
        keyword = "enemy"

    matching = findMatching(player, keyword, list())
            
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
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
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return player.attack(matching[0])
        except AttributeError:
            return "I see no reason to attack that right now."

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
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return player.exorcise(matching[0])
        except AttributeError:
            return "I can only exorcise demonic creatures."

def advance(player, keyword):
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
    
    if len(matching) == 0:
        return "There is nothing like that here."
    elif len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
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
        return "You need to be more specific"
    elif len(matching) == 1:
        try:
            return player.retreat(matching[0])
        except AttributeError:
            return "That isn't an enemy."
            
def equip(player, keyword):
    matching = findMatchingInventory(player, keyword, list())
    #matching = findMatching(player, keyword, matching)
            
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
    #matching = findMatching(player, keyword, matching)
            
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
            return matching[0].read()
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
        return player.currentLocation.lookAt()
    
    matching = findMatching(player, keyword, list())
    matching = findMatchingInventory(player, keyword, matching)
            
    if len(matching) == 0:
        return "You don't see anything like that here."
    if len(matching) > 1:
        return "You need to be more specific"
    elif len(matching) == 1:
        return matching[0].lookAt()