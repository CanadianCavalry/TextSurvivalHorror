'''
Created on Jun 30, 2014

@author: Thomas
'''
import Commands
import StateControl

class Parser(object):
    
    def __init__(self):
        self.command = ""
        self.target = ""
        self.recipient = ""
        self.state = None
        
    def loadState(self, state):
        self.state = state
        
    def addRecipient(self, position, inputArray):
        while position < len(inputArray):
            self.recipient += inputArray[position].lower() + " "
            position += 1
        self.recipient = self.recipient.strip()
        return
        
    def parse(self, inputString):
        self.state.player.setLastAction(None)
        inputString = inputString.lower()
        inputArray = inputString.split()                 #Break apart their input into the action and the target(or object)
        
        self.command = ""
        self.target = ""
        self.recipient = ""
        
        for word in inputArray:                         #remove unnecessary prepositions from the input
            if word in ("the","of","to","from","at","through","towards","away"):
                inputArray.remove(word)
        
        if len(inputArray) < 1:                          #Check for an empty input string
            return None
    
        self.command = inputArray.pop(0)
        
        #Command specific secondary words and targets
        if self.command == "heavy":
            nextCom = inputArray.pop(0)
            if nextCom == "attack":
                self.command = "heavy attack"

        if self.command == "advance":
            if inputArray:
                nextCom = inputArray[0]
                if nextCom == "on":
                    inputArray.pop(0)

        if self.command == "retreat":
            if inputArray:
                nextCom = inputArray[0]
                if nextCom == "from":
                    inputArray.pop(0)


        #Determine target, parse complex commands
        if len(inputArray) >= 1:    
            for word in inputArray:
                if ((self.command == "use") and (word == "on")) or ((self.command == "ask") and (word == "about")):                  #check if the command is a two word command
                    self.command += (" " + word)
                    self.addRecipient(inputArray.index(word) + 1, inputArray)           #Start adding the rest of the words to the recipient, starting with the 
                    break                                                               #position after "on". Then end the loop so we skip the rest of the words
                self.target += word + " "
            self.target = self.target.strip()
        
        if (self.command == "go") or (self.command == "travel") or (self.command == "move") or (self.command == "walk") or (self.command == "run"):
            self.command = "go"
            resultString = Commands.go(self.state.player, self.target)
        elif (self.command == "north") or (self.command == "south") or (self.command == "east") or (self.command == "west"):
            resultString = Commands.go(self.state.player, self.command)
            self.command = "go"
        elif (self.command == "n"):
            resultString = Commands.go(self.state.player, "north")
            self.command = "go"
        elif (self.command == "s"):
            resultString = Commands.go(self.state.player, "south")
            self.command = "go"
        elif (self.command == "e"):
            resultString = Commands.go(self.state.player, "east")
            self.command = "go"
        elif (self.command == "w"):
            resultString = Commands.go(self.state.player, "west")
            self.command = "go"
        elif (self.command == "use") or (self.command == "activate"):
            self.command == "use"
            resultString = Commands.use(self.state.player, self.target)
        elif (self.command == "use on"):
            resultString = Commands.useOn(self.state.player, self.target, self.recipient)
        elif (self.command == "get") or (self.command == "take") or (self.command == "acquire") or (self.command == "grab") or (self.command == "fetch") or (self.command == "procure") or (self.command == "attain"):
            resultString = Commands.get(self.state.player, self.target)
        elif (self.command == "drop") or (self.command == "discard") or (self.command == "ditch"):
            resultString = Commands.drop(self.state.player, self.target)
        elif (self.command == "attack"):
            resultString = Commands.attack(self.state.player, self.target)
        elif (self.command == "heavy attack"):
            resultString = Commands.heavyAttack(self.state.player, self.target)
        elif (self.command == "shoot"):
            resultString = Commands.shoot(self.state.player, self.target)
        elif (self.command == "reload"):
            resultString = Commands.reload(self.state.player)
        elif (self.command == "defend") or (self.command == "guard"):
            resultString = Commands.defend(self.state.player)
        elif (self.command == "exorcise"):
            resultString = Commands.exorcise(self.state.player, self.target)
        elif (self.command == "advance"):
            resultString = Commands.advance(self.state.player, self.target)
        elif (self.command == "retreat"):
            resultString = Commands.retreat(self.state.player, self.target)
        elif (self.command == "equip"):
            resultString = Commands.equip(self.state.player, self.target)
        elif (self.command == "wear"):
            resultString = Commands.wear(self.state.player, self.target)
        elif (self.command == "open"):
            resultString = Commands.openThing(self.state.player, self.target)
        elif (self.command == "close"):
            resultString = Commands.closeThing(self.state.player, self.target)
        elif (self.command == "unlock"):
            resultString = Commands.unlock(self.state.player, self.target)
        elif (self.command == "lock"):
            resultString = Commands.lock(self.state.player, self.target)
        elif (self.command == "search") or (self.command == "check") or (self.command == "scrutinize") or (self.command == "analyze") or (self.command == "inspect"):
            resultString = Commands.search(self.state.player, self.target)
        elif (self.command == "drink"):
            resultString = Commands.drink(self.state.player, self.target)
        elif (self.command == "wait"):
            resultString = Commands.wait(self.state.player)
        elif (self.command == "read"):
            resultString = Commands.read(self.state.player, self.target)
        elif (self.command == "talk"):
            resultString = Commands.talk(self.state.player, self.target)
        elif (self.command == "ask about"):
            resultString = Commands.ask(self.state.player, self.target, self.recipient)
        elif (self.command == "push"):
            resultString = Commands.push(self.state.player, self.target)
        elif (self.command == "pull"):
            resultString = Commands.pull(self.state.player, self.target)
        elif (self.command == "cut"):
            resultString = Commands.cut(self.state.player, self.target)
        elif (self.command == "look") or (self.command == "examine"):
            self.command == "look"
            resultString = Commands.look(self.state.player, self.target)
        elif (self.command == "inventory") or (self.command == "inv") or (self.command == "i") or (self.command == "items") or (self.command == "stuff"):
            self.command == "inventory"
            resultString = Commands.inventory(self.state.player)
        elif (self.command == "help") or (self.command == "?") or (self.command == "commands") or (self.command == "controls"):
            self.command == "help"
            resultString = Commands.displayHelp()
        elif (self.command == "char") or (self.command == "stats"):
            self.command == "stats"
            resultString = Commands.stats(self.state.player)
        elif (self.command == "save"):
            resultString = StateControl.save(self.state)
        elif (self.command == "quit") or (self.command == "exit"):
            resultString = StateControl.quit()
        elif (self.command == "/dev"):
            resultString = Commands.devCommand(self.state.player, self.target)
        else:
            resultString = "I don't understand that."
            
        self.state.player.setLastAction(self.command)
            
        return resultString