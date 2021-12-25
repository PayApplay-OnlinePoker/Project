# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

import random
import socket
import time
import threading

CLIENT_CARD = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
CARD_PATTEN = ["S", "H", "D", "C"]
CARD_NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
CLIENT_PATTEN = ["Spade", "Heart", "Diamond", "Clover"]
handCardList = [int(0) for i in range(17) ]
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush
SERVER_ADDR = 'onlinepoker.hopto.org'
PORT = 31597


id = -1


class Apicall:
    def join(self, roomID, roomPW):
        pass

    def create(self, roomName, roomPW, baseBetting, baseMoney):
        clientSocket.sendMessageQueue.append(f'{id} 0 {roomName} {roomPW} {baseBetting} {baseMoney}')

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

    def winner(self, ID, nickname):
        pass

    def register(self, nickname):
        clientSocket.sendMessageQueue.append(f"-1 0 {nickname}")


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

def HandRankingReturn(handCardList, playerHandNum, playerHandPattern):
    global CARD_PATTEN
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



    #-
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
    

        






#----------------------------------------------------------#

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

def print_player_hand():
    global playerHand
    print("지금 가지고 계신 패는",  ','.join(playerHand) ,'입니다.')

class ClientSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(SERVER_ADDR, PORT)
        self.sendMessageQueue = []
        self.receiveMessageQueue = []
        self.sentMessageQueue = []
        self.receivedAcks = []
        self.receivedCommands = []
    def listen_server_message(self):
        while True:
            serverMessage = self.socket.recv(2048)
            self.receiveMessageQueue.append(serverMessage)
    def send_server_message(self):
        while True:
            if len(self.sendMessageQueue) > 0:
                message = str(self.sendMessageQueue.pop(0))
                self.socket.send(message.encode())
                self.sentMessageQueue.append(message)
            time.sleep(0.1)
    def sort_received_messages(self):
        while True:
            if len(self.receiveMessageQueue) > 0:
                message = str(self.receiveMessageQueue.pop(0))
                messageList = message.split()
                command = messageList[2]
                if command is 'ack':
                    self.receivedAcks.append(message)
                else:
                    self.receivedCommands.append(message)
            time.sleep(0.1)
    def handle_ack_messages(self):
        while True:
            if len(self.receivedAcks) > 0:
                message = str(self.receivedAcks.pop(0))
                messageList = message.split()
                if messageList[3] != 'OK':
                    print(message)



clientSocket = ClientSocket()
tempThread = threading.Thread(target=clientSocket.listen_server_message)
tempThread.start()
tempThread = threading.Thread(target=clientSocket.send_server_message)
tempThread.start()
tempThread = threading.Thread(target=clientSocket.sort_received_messages)
tempThread.start()

#4장을 준다
test = Gameplay()
playerHand = [] #사용자가 보는 것.
playerHandNum = [] #핸드의 숫자
playerHandPattern = []#핸드의 무늬
#CUI Part
'''
일단 서버와의 통신 없이.  CUI만 구현, 이후 통신이 구현 되면 필요한 부분 수정.
'''


userList = []
roomList = {"Hello" : 1234}
nickname = input("닉네임을 입력하세요. : ")
while nickname in userList: #리스트에 있는 유저 닉네임과 비교, 만약 같은 닉네임이 있으면 생성 제한.
    print("이미 존재하는 닉네임입니다.")
    nickname = input("닉네임을 다시 입력하세요. : ")

while True:
    print("방 생성과 방 참가 중 하나를 선택해주세요. ")
    joinOrCreate = int(input("1.방 생성, 2.방 참가, 3.종료: "))

    if joinOrCreate == 1:#create

        print("방을 생성합니다. ")
        createRoomName = input("방 제목을 입력해주세요: ")

        createRoomPW = input("방 비밀번호를 입력해주세요: ")

        BASEMONEY = [50, 75, 100]
        print("초기 소지 금액을 선택해주세요.")zzzzz
        choiceBaseMoney = int(input("1. 50$, 2. 75$, 3. 100$ : "))
        while choiceBaseMoney not in range(1, 4):
            print("1번, 2번, 3번 중 하나를 선택해주세요.")
        createBaseMoney = int(BASEMONEY[choiceBaseMoney -1])

        print("기본 베팅 금액을 설정해주세요. ")
        createBaseBetting = int(input("(1~10사이 숫자를 입력하세요.): "))
        while createBaseBetting not in range(1, 11):
            print("1~10사이 숫자를 입력해주세요.")
        print("호스트:", nickname, ", 방 제목:", createRoomName , ", 비밀번호:",createRoomPW, ", 초기 소지 금액:", str(createBaseMoney) +"$",", 기본 베팅 금액:", str(createBaseBetting) +"$")
        print("방이 생성되었습니다.")    
        break



    elif joinOrCreate == 2:#join
        joinRoomName = input("방 제목을 입력해주세요: ")
        if joinRoomName in roomList:
            joinRoomPW = int(input("비밀번호를 입력해주세요: "))
            if joinRoomPW == roomList[joinRoomName]:
                print("룸에 입장하셨습니다.")
                break
            else:
                print("비밀번호가 일치하지 않습니다.")
                continue
        else:
            print("방이 존재하지 않습니다.")
            continue

    elif joinOrCreate == 3:
        print("게임을 종료합니다.")
        quit()

    else:
        print("잘못된 입력입니다.")

'''
#초기 패 설정
'''

for count in range(4): 
    playerHand.append(number_to_card(test.card_draw()))
print_player_hand()

#카드 한장 버리기
print("1:" + playerHand[0], "2:" + playerHand[1], "3:" + playerHand[2], "4:" + playerHand[3])
removeCard = int(input("버릴 카드를 선택해주세요. : "))
del playerHand[removeCard - 1]
del playerHandNum[removeCard - 1]
del playerHandPattern[removeCard - 1]

#카드 한장 오픈하기
print("1:" + playerHand[0], "2:" + playerHand[1], "3:" + playerHand[2])

openCard = int(input("오픈할 카드를 선택해주세요. : "))
playerHand[openCard -1] = playerHand[openCard - 1] + "(open)"

#PlayerHandSWAP
swap = playerHand[0] 
playerHand[0] = playerHand[openCard-1]
playerHand[openCard -1 ] = swap

#PlayerHandNumSWAP
swap = playerHandNum[0] 
playerHandNum[0] = playerHandNum[openCard-1]
playerHandNum[openCard -1 ] = swap

#PlayerHandPatternSWAP
swap = playerHandPattern[0] 
playerHandPattern[0] = playerHandPattern[openCard-1]
playerHandPattern[openCard -1 ] = swap

print_player_hand()

#오픈 카드 3장 주기.
for playTurn in range(4, 7):
    playerHand.append(number_to_card(test.card_draw()))
    print(playTurn, "번째 카드는", playerHand[-1], "입니다.")
    playerHand[-1] = playerHand[-1] + "(open)"
    print_player_hand()

#히든 카드 1장 주기.
print("7번째 카드 입니다.")
playerHand.append(number_to_card(test.card_draw()))
print_player_hand()

for i in playerHandNum:
    handCardList[i - 1] += 1
for j in playerHandPattern:
    if j == "S":
        handCardList[13] += 1
    elif j == "H":
        handCardList[14] += 1
    elif j == "D":
        handCardList[15] += 1
    else:
        handCardList[16] += 1


print("당신의 패는", HandRankingReturn(handCardList, playerHandNum, playerHandPattern), "입니다.")
