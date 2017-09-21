'''
Created on Jan 23, 2015

@author: CanadianCavalry
'''
import Items
import UniqueFeatures
import StandardItems


#Misc
class Bible(Items.Readable):
    def __init__(self, **kwargs):
        name="Bible"
        description="Bound in black, NIV translation. "
        seenDescription="A small black bible is on the floor."
        keywords="bible,black bible,black book,book,NIV bible,NIV version bible,my bible"

        kwargs.update({
            "initPickupDesc":"You remember dissecting its passages in detail when you were in seminary.",
            "notTakenDesc":"Your bible is resting on the shelf."
        })

        super(Bible, self).__init__(name, description, seenDescription, keywords, **kwargs)

class Crucifix(Items.OffHandItem):
    def __init__(self, **kwargs):
        name="Crucifix"
        description="This exquisite silver crucifix was carved by a master sculptor. It was a gift from your parents to celebrate your priesthood."
        seenDescription="An elegant silver crucifix is on the ground."
        keywords="crucifix,cross,silver crucifix,silver cross,my cross,my crucifix"

        kwargs.update({
            "initPickupDesc":"Even now, looking at it gives you some hope. Maybe God will lift you out of your darkness yet...",
            "notTakenDesc":"An engraved silver crucifix is on the shelf."
        })

        super(Crucifix, self).__init__(name, description, seenDescription, keywords, **kwargs)