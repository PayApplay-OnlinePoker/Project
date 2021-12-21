# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

import random
hand_Rankings = ["HC", "OP", "TP", "TK", "S", "BS", "Mt", "F", "FH", "FC", "SF", "BSF", "RSF"] 
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush

class Gameplay:
    def generate_deck(self):
        deck = [i for i in range(1, 53)] #generate card deck
        self.deck = deck


    def card_draw(self):
        # 1. draw a card randomly from a list 
        drawCard = random.choice(self.deck)
        self.deck.remove(drawCard)
        return drawCard

    




'''
test = Gameplay()
test.generate_deck()
for i in range(52):
    print(test.card_draw())
'''
