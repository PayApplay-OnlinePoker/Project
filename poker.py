# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

import random
HAND_RANKING = ["HC", "OP", "TP", "TK", "S", "BS", "MT", "F", "FH", "FC", "SF", "BSF", "RSF"]
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush

class Apicall:
    def join(self, roomID, roomPW):
        pass

    def create(self, roomName, roomPW, baseBetting, baseMoney):
        pass

    def leave(self):
        pass

    def bet(self, check, call, allin, half, quarter, fold, money):
        pass

    def drawCard(self, card, isHidden):
        pass

    def removeCard(self, card):
        pass

    def openCard(self, card):
        pass

    def startGame(self):
        pass

    def checkUserMoney(self, money):
        pass

    def checkTableMoney(self, money):
        pass

    def winner(ID, nickname):
        pass


class Gameplay:
    def __init__(self):
        self.generate_deck()

    def generate_deck(self): #generate card deck
        deck = [i for i in range(1, 53)]
        self.deck = deck


    def card_draw(self): #draw a card
        # 1. draw a card randomly from a list
        drawCard = random.choice(self.deck)
        self.deck.remove(drawCard)
        return drawCard

    def calculate_ranking(self): #hand-ranking
        global HAND_RANKING
        pass
