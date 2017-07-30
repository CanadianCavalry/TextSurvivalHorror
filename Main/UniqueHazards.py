'''
Created on Jul 5, 2014

@author: Thomas
'''
import AreasFeatures
import random

#Jacobs Room

class LeaningBookshelf(AreasFeatures.Hazard):
    
    def __init__(self):
        description = ["The bookshelf is leaning badly to one side, and appears to be on the verge of collapse. It's filled with heavy, leather-bound volumes and must weigh a ton. You suspect a good shove would knock it over.", "Theres little left of the bookshelf aside from the pile of books and splintered wood in the aisle."]
        keywords = "leaning bookshelf,bookshelf,crooked bookshelf,broken bookshelf,bookcase,leaning bookcase,shelf,leaning shelf,crooked shelf"
        triggerDesc = "Suprisingly, it doesn't move at first, and it looks like it's sheer weight will keep it upright. After a few seconds it finally begins to tip, picking up speed before coming crashing down in a hail of books and woodem shrapnel."

        kwargs = {}

        super(LeaningBookshelf, self).__init__(description, keywords, triggerDesc, **kwargs)
        
    def trigger(self, player):
        resultString = self.triggerDesc
        self.state += 1
        if player.currentLocation.enemies:
            enemyHit = player.currentLocation.enemies[random.choice(player.currentLocation.enemies.keys())]
            enemyHit.takeDamage(100)

            if enemyHit.name == "Winged Demon":
                resultString += "\nThe Winged Demon attempts to leap aside, but it's bulk in addition to the narrow confines of the library make it impossible. It let's out an angonizing screech as the shelf crashes down on top of it."
                if enemyHit.health > 0:
                    stunDesc = "\nThe demon roars as it tries to free itself from under the remains of the shelf."
                    recoveryDesc = "The demon finally manages to toss the shattered remains of the shelf aside as it climbs to it's feet."
                else:
                    resultString += "\nAs the dust settles, you can see the demon lying motionless under the pile of debris."
            elif enemyHit.name == "Hellhound":
                resultString += "\nThe Hellhound snarls and lunges towards you just as the shelf comes crashing down on top of it. It yelps in pain as the mass of books and broken shelves smash it into the floor."
                if enemyHit.health > 0:
                    stunDesc = "\nThe hound thrashes and barks as it tries to free itself from under the remains of the shelf."
                    recoveryDesc = "The hellhound finally rips itself free from the pile of debris and leaps to attack."
                else:
                    resultString += "\nAs the dust settles, battered and broken Hellhound lying motionless, half buried by debris."
            else:
                resultString += "\nThe " + enemyHit.name + " is crushed under the falling shelf."
                if enemyHit.health > 0:
                    stunDesc = "\nThe impact sends it hurtling backwards, smashing into the wall before being half-buried under books and debris. It struggles to free iteself."
                    recoveryDesc = "The demon frees itself from under the broken shelf."
                else:
                    resultString += "\nAs the dust settles, battered and broken " + enemyHit.name + " lying motionless, half buried by debris."

            if enemyHit.health > 0:
                enemyHit.makeStunned(4, stunDesc, recoveryDesc)
                enemyHit.helpless = True
                enemyHit.distanceToPlayer = 1

        return resultString

    def push(self, player):
        resultString = "You throw yourself into the side of the shelf. "
        resultString += self.trigger(player) 
        return resultString, True

    def pull(self, player):
        return "Pulling on that will likely just und up with you crushed underneath it."