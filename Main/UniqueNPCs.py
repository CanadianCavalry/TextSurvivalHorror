'''
Created on Aug 23, 2014

@author: Thomas
'''
import NPCs

class BentHostSurvivor(NPCs.NPC):

    def talk(self, player):
        resultString = self.talkResponse
        if self.inventory:
            self.dropAllItems()
            resultString += "\n" + self.dropDesc
        return resultString

class BentHostSurvivorMale(BentHostSurvivor):
    def __init__(self):
        self.dropDesc = "Unable to speak properly, he wordlessly pulls something from his clothes and holds it out with a shaking hand. It tumbles to the floor."
        name = "Young Man"
        description = ["He looks injured, haggered and exhausted, not suprising considering he was recently freed from demonic possession. "
                    "He's curled up on the floor, and doesn't look like he'll be moving anytime soon."]
        seenDescription = "A young man is curled up on the floor here."
        talkResponse = "He mumbles something quietly under his breath that sounds like 'thank you'."
        keywords = "human,man,young man,survivor,victim"
        super(BentHostSurvivorMale, self).__init__(name, description, seenDescription, talkResponse, keywords)

class BentHostSurvivorFemale(BentHostSurvivor):
    def __init__(self):
        self.dropDesc = "With a look of gratitude, she silently holds out something clutched her hands and places it on the floor in front of you."
        name = "Young Woman"
        description = ["She looks injured, haggered and exhausted, not suprising considering she was recently freed from demonic possession. "
                "She's curled up on the floor, and it doesn't look like she'll be moving anytime soon."]
        seenDescription = "A young woman is curled up on the floor here."
        talkResponse = "She mumbles something quietly under her breath that sounds like 'thank you'."
        keywords = "human,woman,young woman,survivor,victim"
        super(BentHostSurvivorFemale, self).__init__(name, description, seenDescription, talkResponse, keywords)

#PROLOGUE NPCs

class SecurityGuards102(NPCs.NPC):
    
    def __init__(self):
        name = "Security Guards"
        description = "Big and muscular, they're both dressed in crimson body armour and sport heavy \
looking handguns holstered at their sides that gleam threateningly in the soft \
light of the hallway. On the backs of their armour the logo of a large white \
phoenix with the words \"Phoenix Security Corporation\" can be seen. I can't help \
miss the security the older management use to employ - Officers Brooks and O'Sullivan \
might have been strict, but at least they weren't intimidating."
        seenDesc = "Standing in the middle of the hallway are two security guards engaged in a discussion."
        talkResponse = "They don't seem to mind that I interrupted them. \"Well well, if it isn't Mr. Hunter!\" \
one of them says. \"You and the other residents here are very lucky to have us \
here. Trust us, you\'re in good hands!\""
        keywords = "guard,guards,security guard,security guards,officers"
        super(SecurityGuards102, self).__init__(name, description, seenDesc, talkResponse,keywords)
        self.addDialogue(NPCs.Dialogue("good hands,lucky,security",
"\"Well, of course you're in good hands! Now that we and Dr. Malachi are in charge \
of this superb facility I'd say every one of you junkies and derelicts are going to \
be just fine! And especially since you've been taking your new medication, eh? I bet \
it\'s doing wonders for you all!\""))
        
class Cicero103(NPCs.NPC):
    
    def __init__(self):
        name = "Cicero"
        description = "A small and silver-haired British fellow wearing an elegant, black night-robe with moccasins. Once \
a professor who taught Anthropology with a special focus on myth at Oxford, he suffered a stroke which destroyed his \
illustrious career. Cicero is an absent-minded and oft-tormented man whose profound frustration and sense of defeat \
caused by his stroke drove him to alcoholism. Despite all this, the stroke did not diminish his immense appetite for \
knowledge and he still studies and writes about mythology in his spare time. I find his thinking to be refreshingly \
unique and insightful, and he's one of the most gentle men I've ever met."
        seenDesc = "Cicero is sitting in an armchair in the corner of the room, rocking at a manic pace."
        talkResponse = "He looks up as if noticing you for the first time. \"Jacob, the one God loved! It is good to see \
as always, my friend. I am most unsettled today. The smoke and ash of Mount Vesuvius surrounds. It fills my lungs and \
throat, giving me terrible visions. Mischief! Wickedness! Horror!\" He is quite agitated."
        keywords = "cicero,british man,man,occupant,resident"
        super(Cicero103, self).__init__(name, description, seenDesc, talkResponse, keywords)
        
class Micheal105(NPCs.NPC):
    
    def __init__(self):
        name = "Micheal"
        description = "A long, tall drink of a man, Micheal is middle-aged fellow whose fingernails are greasy and yellowish \
from smoking. He's a former crystal meth addict who often blames his problems on his childhood and the neighborhood he grew up in. \
I find him negative, childish and try to avoid whenever possible."
        seenDesc = "This rooms sole occupant, Micheal, is sitting on his bed, fighting to light a half used cigarette."
        talkResponse = "He stops flicking his empty lighter for a moment and looks up. He briefly looks you over and then resumes his attempts. \
\"Oh, hey Jacob. What d'ya want?\" He coughs violently, his wheezing breath a clear indication of lungs severely damaged by excessive \
smoking. \"Is it just me, or is that junk they've been giving us not doing shit for you today?\""
        keywords = "micheal,man,smoking man,occupant,resident"
        super(Micheal105, self).__init__(name, description, seenDesc, talkResponse, keywords)
        
class Astrid106(NPCs.NPC):
    
    def __init__(self):
        name = "Astrid"
        description = "With hair that flows gracefully down her shoulders like an auburn waterfall and a gorgeous, slender figure, \
Astrid could have any man or woman she wanted if she wasn't so self-centered. The rumor is that she was an extremely successful \
cocaine dealer until she got hooked on her own wares. I find the coldness in her eyes unsettling."
        seenDesc = "Astrid, a tall slender woman, is standing in the bathroom combing her hair."
        talkResponse = "\"Why, hello Jacob!\" she coos. \"Forgive me for already being occupied and not offering you proper hospitality. \
The Rejuvenax they have been giving us seems to have to failed to silence my cravings today. And when the world takes something from \
Astrid, it's only right for Astrid to pamper herself even more than usual, no?\""
        keywords = "astrid,woman,tall woman,slender woman,occupant,resident"
        super(Astrid106, self).__init__(name, description, seenDesc, talkResponse, keywords)
        
class Rose108(NPCs.NPC):
    
    def __init__(self):
        name = "Rose"
        description = "A waifish teen who likes to dress in punk clothing, Rose is typically a very quiet and withdrawn soul."
        seenDesc = "You see Rose sitting on the ground with her arms around her legs, staring off into space."
        talkResponse = "She doesn't even look up. \"Yeah, sorry\", she says in a dead, toneless voice. \"I don't really want to talk to anyone right now. Please leave me alone.\""
        keywords = "rose,resident,occupant,woman,girl"
        super(Rose108, self).__init__(name, description, seenDesc, talkResponse, keywords)
        
class SecurityGuards109(NPCs.NPC):
    
    def __init__(self):
        name = "Security Guards"
        description = "Like all the rest of the security team recently hired by Father Malachi, the gear these two \
are sporting definitely seems overkill for looking after a rehab centre. They're wearing a full suit of crimson body \
armour and each carrying a rifle. They're starting to look very impatient with the young woman who's making such a fuss at the reception desk."
        seenDesc = "There are two security guards standing at either end of the receptionist desk look irritated."
        talkResponse = "One of them chuckles a little at the scene the young woman is causing. \"Sheesh!\" he says. \"She's like a little girl having a temper tantrum, huh?\""
        keywords = "guard,guards,security guard,security guards,officers,security"
        super(SecurityGuards109, self).__init__(name, description, seenDesc, talkResponse, keywords)
        
        self.addDialogue(NPCs.Dialogue("little girl,temper tantrum,girl,tantrum,temper,woman,irritated","Considering everything the House is doing for the people here, you think she'd show a little respect."))
        self.addDialogue(NPCs.Dialogue("rejuvinax,drug","One of the security guards grins at the mention of this. \"Yes, Rejuvenax! The drug that will make everything better!\" You try to explain that Rejuvenax isn't helping you at all today, but he doesn't seem to care or pay attention."))
        self.addDialogue(NPCs.Dialogue("father malachi,malachi,father,boss","\"A great man! Who else could put you all you addicts and crazies on the straight and narrow as well as him?\""))
        self.addDialogue(NPCs.Dialogue("management,new management,treatment","\"All of you residents seem to be complaining that we're so hard on you. But we protect you at every turn and give you a perfect drug to cure all your ills. Tell me - did the previous managment do that for you?\""))
        
class Hayley109(NPCs.NPC):
    
    def __init__(self):
        name = "Hayley"
        description = "Seldom have you seen someone as angry and exasperated as this twenty-something woman. There \
are tears in her eyes and her voice shakes with the fury as she angrily pounds the receptionist's desk with her fist. \
\"You people are RIDICULOUS!\" she yells. \"My best friend\'s mother just DIED a couple days ago, and all I'm asking \
you for is FIVE MINUTES TO TALK TO HER AND GIVE HER A HUG! I don't CARE if visiting hours are up! Can\'t you ignore the rules JUST THIS ONCE?!"
        seenDesc = "A woman standing in front of the reception desk appears quite agitated, and is arguing with the two receptionists on duty. "
        talkResponse = "\"Gleaning what you can from the conversation, you learn that the young woman just wants to visit one of residents - a \
friend of hers who's mother died a few days ago - and the management won't allow this as the resident's visiting hours are up for the week. You can't help but \
feel sympathy for her so you explain to the young woman that you're one of the residents of the house and that you might be able to help her out.\
She stops yelling and looks at you, seemingly surprised that there's anyone else left in the universe who can see reason. \"What? You...you can help me?\""
        keywords = "girl,woman,yelling girl,hayley,agitated girl"
        super(Hayley109,self).__init__(name, description, seenDesc, talkResponse, keywords)