import threading
import socket
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
    def __init__(self, nickname, socket, ID):
        self.nickname = nickname
        self.socket = socket
        self.messageQueue = []
        self.playerID = ID
        self.joinedRoom = 0

class PlayerHandler:
    def __init__(self):
        self.players = dict()
    def send_message_to_players(self):
        while True:
            for i in self.players:
                if len(i.messageQueue) > 0:
                    i.socket.send(i.messageQueue.pop(0))
            time.sleep(0.05)
    def enqueue_message(self, destinationID, message):
        if destinationID in self.players.keys():
            self.players[destinationID].messageQueue.append(message)
            return True
        else:
            return False
    def register(self, nickname, socket):
        newID = random.randint(1, MAX_RANGE)
        while newID in self.players.keys():
            newID = random.randint(1, MAX_RANGE)
        self.players[newID] = Player(nickname, socket, newID)
        self.enqueue_message(newID, f'0 {newID} response OK registered {newID}')
        return newID

class RoomHandler:
    def __init__(self):
        self.rooms = dict()
    def join(self, userID, roomID, roomPW):
        message = f'0 {userID} response'
        if playerHandler.players[userID].joinedRoom != 0:
            playerHandler.enqueue_message(userID, message + f'joinRoomError alreadyJoined {roomID} {playerHandler.players[userID].joinedRoom}')
        if roomID in self.rooms.keys():
            if roomPW == self.rooms[roomID].roomPW:
                if len(self.rooms[roomID].userList) < 4:
                    self.rooms[roomID].userList.append(userID)
                    playerHandler.players[userID].money = self.rooms[roomID].baseMoney
                    playerHandler.enqueue_message(userID, message + f'joined {self.rooms[roomID].host}')
                    for i in self.rooms[roomID].userList:
                        tempMessage = message + f' fetch users user {i} {playerHandler.players[i].nickname} {self.rooms[roomID].userMoney[i]}'
                        playerHandler.enqueue_message(
                else:
                    playerHandler.enqueue_message(userID, message + 'joinRoomError roomIsFull')
            else:
                playerHandler.enqueue_message(userID, message + 'joinRoomError passwordNotMatched')
        else:
            playerHandler.enqueue_message(userID, message + 'joinRoomError noSuchRoomID')
    def create(self, userID, roomName, roomPW, baseBetting, baseMoney):
        roomID = random.randint(1, MAX_RANGE)
        while roomID in self.rooms.keys():
           roomID = random.randint(1, MAX_RANGE)
        self.rooms[roomID] = Room(roomID, roomName, roomPW, baseBetting, baseMoney, userID)
        playerHandler.players[userID].joinedRoom = roomID
        playerHandler.enqueue_message(userID, f'0 {userID} response created {roomID}')
    def leave(self, userID, roomID):
        if userID in self.rooms[roomID].userList:
            self.rooms[roomID].userList.remove(userID)
            playerHandler.enqueue_message(userID, f'0 {userID} response leaved {roomID}')
            self.announce_leave(userID, roomID)
            playerHandler.players[userID].joinedRoom = 0
        else:
            playerHandler.enqueue_message(userID, f'0 {userID} response leaveRoomError notInThisRoom')
    def announce_leave(self, userID, roomID):
        for aUser in self.rooms[roomID].userList:
            playerHandler.enqueue_message(aUser, f'0 {aUser} leaved {userID}')
    def fetch_room(self, userID):
        playerHandler.enqueue_message(userID, f'0 {userID} response fetch rooms start')
        for i in roomHandler.rooms:
            playerHandler.enqueue_message(userID, f'0 {userID} response fetch rooms room {i.roomID} {i.roomName} {i.baseBetting} {i.baseMoney} {playerHandler.players[i.host].nickname}')
        playerHandler.enqueue_message(userID, f'0 {userID} response fetch rooms end')

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
            if handCardList[idx] == 2:
                pairCheck += 1
                if highestNum[1] == 1:
                    pass
                else:
                    highestNum[1] = idx + 1

                for idx, tempNum in enumerate(playerHandNum):
                    if highestNum[1] == tempNum:
                        tempPattern = playerHandPattern[idx]
                        if CARD_PATTEN.index(highestPattern[1]) > CARD_PATTEN.index(tempPattern):
                            highestPattern[1] = tempPattern

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
                    print(straightList)
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
            return ["RoyalStraightFlush", highestNum[11], highestPattern[11]]

        elif backStraightFlushCheck>= 1:
            return ["backStraightFlush", highestNum[10], highestPattern[10]]

        elif straightFlushCheck>= 1:
            return ["StraightFlush", highestNum[9], highestPattern[9]]

        elif fourCheck >= 1: #FourCard
            return ["FourCard", highestNum[8], highestPattern[8]]

        elif fullHoushCheck >= 1:#FullHouse
            return ["FullHouse", highestNum[7], highestPattern[7]]

        elif flushCheck >= 1: #Flush
            return ["Flush", highestNum[6], highestPattern[6]]

        elif mountainCheck >= 1: #mountain
            return ["mountain", highestNum[5], highestPattern[5]]

        elif backStraightCheck >= 1: #backstraight
            return ["backStraight", highestNum[4], highestPattern[4]]

        elif straightCheck >= 1: #straight
            return ["Straight", highestNum[3], highestPattern[3]]

        elif tokCheck == 1: #Three of Kind
            return ["Three of kind(Triple)", highestNum[2], highestPattern[2]]

        elif pairCheck >= 2:#TwoPair
            return ["TwoPair", highestNum[1], highestPattern[1]]

        elif pairCheck == 1:#OnePair
            return ["OnePair", highestNum[1], highestPattern[1]]

        else: #HighCard
            return ["HighCard", highestNum[0], highestPattern[0]]

def number_to_card(number):
    global playerHandNum
    global playerHandPattern
    if number in range(1, 14): #Spade
        this_card = CLIENT_PATTEN[0] + CLIENT_CARD[number - 1]
        cardPatten = CARD_PATTEN[0]
        cardNum = CARD_NUM[number - 1]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card
    elif number in range(14, 27): #Heart
        this_card = CLIENT_PATTEN[1] + CLIENT_CARD[number - 14]
        cardPatten = CARD_PATTEN[1]
        cardNum = CARD_NUM[number - 14]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card
    elif number in range(27, 40): #Diamond
        this_card = CLIENT_PATTEN[2] + CLIENT_CARD[number - 27]
        cardPatten = CARD_PATTEN[2]
        cardNum = CARD_NUM[number - 27]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card
    elif number in range(40, 53): #Clover
        this_card = CLIENT_PATTEN[3] + CLIENT_CARD[number - 40]
        cardPatten = CARD_PATTEN[3]
        cardNum = CARD_NUM[number - 40]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card

class Card:
    def __init__(self, number):
        self.number = number
        self.name = number_to_card(number)
