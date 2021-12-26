import time
import random


PORT = 31597
MAX_USERS = 100
MAX_RANGE = 65535
COMMANDS = ['join', 'create', 'leave', 'bet', 'drawCard', 'removeCard', 'openCard', 'startGame', 'checkUserMoney', 'checkTableMoney', 'winner', 'response']

class Room:
    def __init__(self, roomID, roomName, roomPW, baseBetting, baseMoney, host):
        self.roomID = roomID
        self.roomName = roomName
        self.roomPW = roomPW
        self.baseBetting = baseBetting
        self.baseMoney = baseMoney
        self.host = host
        self.userList = [host]
        self.gameHandler = None
        self.userMoney = {host:baseMoney}

class Player:
    def __init__(self):
        self.playerHand = []
        self.playerHandNum = []
        self.playerHandPattern = []
        self.playerHandRanking = []
        self.openCardList = []
        self.handCardList = [0 for i in range(17)]
        self.playerMoney = 0

    def clear(self):
        self.playerHand = []
        self.playerHandNum = []
        self.playerHandPattern = []
        self.playerHandRanking = []
        self.openCardList = []
        self.handCardList_Clear()

    def handCardList_Clear(self):
        self.handCardList = [0 for i in range(17)]

class PlayerHandler:
    def __init__(self):
        self.players = dict()

class RoomHandler:
    def __init__(self):
        self.rooms = dict()

roomHandler = RoomHandler()
playerHandler = PlayerHandler()

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

    def calculate_ranking(self, handCardList, playerHandNum, playerHandPattern): #hand-ranking
        CARD_PATTEN = ["S", "H", "D", "C"]
        global flushPattern
        royalStraightFlushCheck = 0
        backStraightFlushCheck = 0
        straightFlushCheck = 0
        fourCheck = 0
        flushCheck = 0
        flushList = []
        mountainCheck = 0
        backStraightCheck = 0
        straightCheck = 0
        startStraightNum = 0
        fullHoushCheck = 0
        tokCheck = 0
        pairCheck = 0
        highestNum = [0] * 13
        highestPattern = ["C"] * 13

        #
        #highCard 0
        #handcardList[:13] = number
        #handcardLust[13:] = pattern
        for idx in range(13):
            if handCardList[idx] >= 1:
                if highestNum[0] == 1:
                    pass
                else:
                    highestNum[0] = idx + 1

        for idx, tempNum in enumerate(playerHandNum):
            if highestNum[0] == tempNum:
                tempPattern = playerHandPattern[idx]
                if CARD_PATTEN.index(highestPattern[0]) > CARD_PATTEN.index(tempPattern):
                    highestPattern[0] = tempPattern

        for idx in range(13):
            #Onepair, TwoPair 1
            #00000020201111114 
            #playerHandNum = [13, 11, 12, 7, 9, 9, 7]
            #playerHandPattern = [C, C, C, C ,H, D, S]
            if handCardList[idx] == 2:
                pairCheck += 1
                if highestNum[1] == 1:
                    pass
                else:
                    highestNum[1] = idx + 1 #9

        for idx, tempNum in enumerate(playerHandNum):
            if highestNum[1] == tempNum:
                tempPattern = playerHandPattern[idx]
                if CARD_PATTEN.index(highestPattern[1]) > CARD_PATTEN.index(tempPattern):
                    highestPattern[1] = tempPattern

        for idx in range(13):
            #Three of kind 2
            if handCardList[idx] == 3:
                tokCheck += 1
                if highestNum[2] == 1:
                    pass
                else:
                    highestNum[2] = idx + 1

        for idx, tempNum in enumerate(playerHandNum):
            if highestNum[2] == tempNum:
                tempPattern = playerHandPattern[idx]

                if CARD_PATTEN.index(highestPattern[2]) > CARD_PATTEN.index(tempPattern):
                    highestPattern[2] = tempPattern

        #Straight 3
        for straightNum in range(6,13):
                if handCardList[straightNum] >= 1 and handCardList[straightNum - 1] >= 1 and handCardList[straightNum - 2] >= 1 and handCardList[straightNum - 3] >= 1 and handCardList[straightNum - 4] >= 1:
                    straightCheck += 1
                    temp = straightNum
                    if startStraightNum < temp:
                        startStraightNum = temp
                    straightList = [startStraightNum - i for i in range(5)]
                    straightList.sort()
                    highestNum[3] = straightList[-1]
                    for idx, tempNum in enumerate(playerHandNum):
                        if highestNum[3] == tempNum:
                            tempPattern = playerHandPattern[idx]
                            if CARD_PATTEN.index(highestPattern[3]) > CARD_PATTEN.index(tempPattern):
                                highestPattern[3] = tempPattern

        #BackStraight 4
        if handCardList[0] >= 1 and handCardList[1] >= 1 and handCardList[2] >= 1 and handCardList[3] >= 1 and handCardList[4] >= 1:
            backStraightCheck += 1
            highestNum[4] = 1
            for idx, tempNum in enumerate(playerHandNum):
                    if highestNum[4] == tempNum:
                        tempPattern = playerHandPattern[idx]
                        if CARD_PATTEN.index(highestPattern[4]) > CARD_PATTEN.index(tempPattern):
                            highestPattern[4] = tempPattern

        #Mountain 5
        elif handCardList[0] >= 1 and handCardList[9] >= 1 and handCardList[10] >= 1 and handCardList[11] >= 1 and handCardList[12] >= 1 :
            mountainCheck += 1
            highestNum[5] = 1
            for idx, tempNum in enumerate(playerHandNum):
                    if highestNum[5] == tempNum:
                        tempPattern = playerHandPattern[idx]
                        if CARD_PATTEN.index(highestPattern[5]) > CARD_PATTEN.index(tempPattern):
                            highestPattern[5] = tempPattern


        #Flush 6
        for idx, cardPatten in enumerate(handCardList[13: ]):
            if cardPatten >= 5:
                flushCheck += 1
                flushPattern = CARD_PATTEN[idx]
                for idx, listPatten in enumerate(playerHandPattern):
                    if listPatten == flushPattern:
                        flushList.append(playerHandNum[idx])
                flushList.sort()
                highestPattern[6] = flushPattern
                if 1 in flushList :
                    highestNum[6] = 1
                else:
                    highestNum[6] = flushList[-1]


        #FullHouse 7
        if (pairCheck >= 1 and tokCheck == 1) or (tokCheck >= 2):
            fullHoushCheck+= 1
            for idx in range(13):
                if handCardList[idx] == 3:
                    if highestNum[7] == 1:
                        pass
                    else:
                        highestNum[7] = idx + 1
                    for idx, tempNum in enumerate(playerHandNum):
                        if highestNum[7] == tempNum:
                            tempPattern = playerHandPattern[idx]
                            if CARD_PATTEN.index(highestPattern[7]) > CARD_PATTEN.index(tempPattern):
                                highestPattern[7] = tempPattern

        #FourCard 8
        for idx in range(13):
            if handCardList[idx] == 4:
                highestPattern[8] = "S"
                fourCheck += 1
                if highestNum[8] == 1:
                    pass
                else:
                    highestNum[8] = idx + 1

        #StraightFlush 9
        if straightCheck >= 1 and flushCheck >= 1:
            if straightList == flushList:
                highestNum[9] = int(straightList[-1])
                highestPattern[9] = flushPattern
                straightFlushCheck += 1

        #backStraightFlush
        if backStraightCheck >= 1 and flushCheck >= 1:
            if [1, 2, 3, 4, 5] == flushList:
                highestNum[10] = 1
                highestPattern[10] = flushPattern
                backStraightFlushCheck += 1

        #royalStraightFlush
        if mountainCheck >= 1 and flushCheck >= 1:
            if [1, 10, 11, 12, 13] == flushList:
                highestNum[11] = 1
                highestPattern[11] = flushPattern
                royalStraightFlushCheck += 1
#---    -------------------------------------------------------#
        #return ["랭크", "하이카드", "무늬"]

        if royalStraightFlushCheck >= 1:
            return ["Royal Straight Flush", highestNum[11], highestPattern[11]]

        elif backStraightFlushCheck>= 1:
            return ["Back Straight Flush", highestNum[10], highestPattern[10]]

        elif straightFlushCheck>= 1:
            return ["Straight Flush", highestNum[9], highestPattern[9]]

        elif fourCheck >= 1: #FourCard
            return ["Four Cards", highestNum[8], highestPattern[8]]

        elif fullHoushCheck >= 1:#FullHouse
            return ["Full House", highestNum[7], highestPattern[7]]

        elif flushCheck >= 1: #Flush
            return ["Flush", highestNum[6], highestPattern[6]]

        elif mountainCheck >= 1: #mountain
            return ["Mountain", highestNum[5], highestPattern[5]]

        elif backStraightCheck >= 1: #backstraight
            return ["Back Straight", highestNum[4], highestPattern[4]]

        elif straightCheck >= 1: #straight
            return ["Straight", highestNum[3], highestPattern[3]]

        elif tokCheck == 1: #Three of Kind
            return ["Three of kind", highestNum[2], highestPattern[2]]

        elif pairCheck >= 2:#TwoPair
            return ["Two Pair", highestNum[1], highestPattern[1]]

        elif pairCheck == 1:#OnePair
            return ["One Pair", highestNum[1], highestPattern[1]]

        else: #HighCard
            return ["High Card", highestNum[0], highestPattern[0]]

'''
class Card:
    def __init__(self, number):
        self.number = number
        self.name = number_to_card(number)
        '''
