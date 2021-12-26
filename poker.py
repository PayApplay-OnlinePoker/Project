# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

#imports
import random
import socket
import time
import threading
import library


#constants
CLIENT_CARD = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
CARD_NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
CLIENT_PATTEN = ["Spade", "Heart", "Diamond", "Clover"]
handCardList = [int(0) for i in range(17) ]
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush
SERVER_ADDR = 'onlinepoker.hopto.org'


class ClientSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
        self.socket.connect(SERVER_ADDR, library.PORT)
        self.sendMessageQueue = [] #any message added here will be sent to server
        self.receiveMessageQueue = [] #any message from server will be stored here
        self.sentMessageQueue = [] #any sent message will be stored here for further process
        self.receivedCommands = []
        self.receivedResponses = []
    def listen_server_message(self): #message listener
        while True:
            serverMessage = self.socket.recv(2048)
            if serverMessage == '':
                print('server connection closed')
                exit()
            self.receiveMessageQueue.append(serverMessage)
    def send_server_message(self): #message sender
        while True:
            if len(self.sendMessageQueue) > 0:
                message = str(self.sendMessageQueue.pop(0))
                self.socket.send(message.encode())
                self.sentMessageQueue.append(message)
            time.sleep(0.1)
    def sort_received_message(self):
        while True:
            for i in self.receiveMessageQueue:
                if i.split()[2] == 'response':
                    self.receivedResponses.append(i)
                else:
                    self.receivedCommands.append(i)
                self.receiveMessageQueue.remove(i)
            time.sleep(0.1)
    def handle_commands(self):
        while True:
            #handle received commands
            time.sleep(0.1)



#start socket
clientSocket = ClientSocket() #init socket connection

#start listening from server in a different thread so that listening would go concurrently
tempThread = threading.Thread(target=clientSocket.listen_server_message)
tempThread.start()

#start sending to server in a different thread so that sending would go concurrently
tempThread = threading.Thread(target=clientSocket.send_server_message)
tempThread.start()


#send registration message and receive response
def register(nickname):
    clientSocket.sendMessageQueue.append(f'-1 0 register {nickname}')
    while len(clientSocket.receiveMessageQueue) == 0:
        time.sleep(0.1)
    message = str(clientSocket.receiveMessageQueue.pop(0))
    messageList = message.split()
    assert(messageList[1] == messageList[4] and messageList[3] == 'registered') #quit if not true
    return messageList[1]


#init player handler
library.playerHandler.players[0] = library.Player('server', clientSocket, 0)
currentRoom = library.Room(0, lobby, '', 0, 0, 0)


#register
nickname = input("닉네임을 입력하세요. : ")
thisClient = library.Player(nickname, None, register(nickname))
library.playerHandler.players[thisClient.playerID] = thisClient


tempThread = threading.Thread(target=clientSocket.sort_received_message)
tempThread.start()


#fetch rooms
def fetch_rooms():
    sentMessage = f'{thisClient.playerID} 0 fetch rooms'
    clientSocket.sendMessageQueue.append(sentMessage)
    while f'0 {thisClient.playerID} response fetch rooms start' not in clientSocket.receivedResponses:
        time.sleep(0.1)
    rooms = []
    startIndex = clientSocket.receivedResponses.index(f'0 {thisClient.playerID} response fetch rooms start')
    clientSocket.receivedResponses.pop(startIndex)
    while clientSocket.receiveMessageQueue[startIndex] != f'0 {thisClient.playerID} response fetch rooms end':
        room = clientSocket.receivedResponses.pop(startIndex).split()[6:]
        rooms.append(library.Room(room[0], room[1], None, room[2], room[3], room[4]))
        time.sleep(0.01)
    clientSocket.receivedResponses.pop(startIndex)
    clientSocket.sentMessageQueue.remove(sentMessage)
    return rooms

#create room
def create(roomName, roomPW, baseBetting, baseMoney):
    sentMessage = f'{thisClient.playerID} 0 create {roomName} {roomPW} {baseBetting} {baseMoney}'
    clientSocket.sendMessageQueue.append(sentMessage)
    while True not in [i.startswith(f'0 {thisClient.playerID} response created') for i in clientSocket.receivedResponses]:
        time.sleep(0.1)
    #find the index of True and pop
    for i in clientSocket.receivedResponses:
        if i.startswith(f'0 {thisClient.playerID} response created'):
            retval = int(i.split()[-1])
            clientSocket.receivedResponses.remove(i)
            clientSocket.sentMessageQueue.remove(sentMessage)
            currentRoom.__init__(retval, roomName, roomPW, baseBetting, baseMoney, thisClient.playerID)
            return retval

#join room
def join(roomID, roomPW, roomList):
    sentMessage = f'{thisClient.playerID} 0 join {roomID} {roomPW}'
    clientSocket.sendMessageQueue.append(sentMessage)
    #add handling errors later
    while True not in [i.startswith(f'0 {thisClient.playerID} response joined') for i in clientSocket.receivedResponses]:
        time.sleep(0.1)
    for i in clientSocket.receivedResponses:
        if i.startswith(f'0 {thisClient.playerID} response joined'):
            startIndex = clientSocket.receivedResponses.index(i)
            clientSocket.receivedResponses.pop(startIndex)
            roomInfo = list(filter(lambda item : item.roomID == roomID, roomList))[0]
            currentRoom.__init__(roomID, roomInfo.roomName, roomPW, roomInfo.baseBetting, roomInfo.baseMoney, int(i.split()[-1]))
            while clientSocket.receivedResponses[startIndex] != f'0 {thisClient.playerID} response fetch users end':
                aUser = clientSocket.receivedResponses.pop(startIndex).split()[6:]
                library.playerHandler.players[int(aUser[0])] = library.Player(aUser[1], None, int(aUser[0]))
                if int(aUser[0]) != currentRoom.host:
                    currentRoom.userList.append(int(aUser[0]))
                currentRoom.userMoney[int(aUser[0])] = int(aUser[2])
            currentRoom.userMoney[thisClient.playerID] = currentRoom.baseMoney


#lobby
def lobby():
    print('현재 생성된 방')
    print('---------------')
    roomList = fetch_rooms()
    for i in roomList:
        print(f'ID : {i.roomID}, 방 이름 : {i.roomName}, 호스트 닉네임 : {i.host}')
        print(f'기본 판돈 : {i.baseBetting}$, 기본 지급금 : {i.baseMoney}\n')
    print('---------------')
    print("방 생성과 방 참가 중 하나를 선택해주세요. ")
    joinOrCreate = int(input("1.방 생성, 2.방 참가, 3.종료: "))
    if joinOrCreate == 1:#create
        print("방을 생성합니다. ")
        roomName = input("방 제목을 입력해주세요: ")
        roomPW = input("방 비밀번호를 입력해주세요: ")
        BASEMONEY = [50, 75, 100]
        print("초기 소지 금액을 선택해주세요.")
        choiceBaseMoney = int(input("1. 50$, 2. 75$, 3. 100$ : "))
        while choiceBaseMoney not in range(1, 4):
            print("1번, 2번, 3번 중 하나를 선택해주세요.")
        baseMoney = int(BASEMONEY[choiceBaseMoney -1])
        print("기본 베팅 금액을 설정해주세요. ")
        baseBetting = int(input("(1~10사이 숫자를 입력하세요.): "))
        while baseBetting not in range(1, 11):
            print("1~10사이 숫자를 입력해주세요.")
        print("호스트:", nickname, ", 방 제목:", roomName , ", 비밀번호:",roomPW, ", 초기 소지 금액:", str(baseMoney) +"$",", 기본 베팅 금액:", str(baseBetting) +"$")
        roomID = create(roomName, roomPW, baseBetting, baseMoney)
        thisClient.joinedRoom = roomID
        print("방이 생성되었습니다.")
    elif joinOrCreate == 2:#join
        joinRoomID = int(input("방 ID를 입력해주세요: "))
        if joinRoomID in [i.roomID for i in roomList]:
            joinRoomPW = int(input("비밀번호를 입력해주세요: "))
            join(joinRoomID, joinRoomPW, roomList)
            print("룸에 입장하셨습니다.")
        else:
            print("방이 존재하지 않습니다.")
    elif joinOrCreate == 3:
        print("게임을 종료합니다.")
        exit()
    else:
        print("잘못된 입력입니다.")
        return
    gameroom()


#gameroom
def gameroom():
    print('참가한 유저')
    for i in currentRoom.userList:
        print(f'닉네임 : {library.playerHandler.players[i].nickname}, 소지금 : {currentRoom.userMoney[i]}')


def leave(self):
    pass

def bet(check, call, allin, half, quarter, fold, money):
    pass

def drawCard(card, isHidden):
    pass

def removeCard(card):
    pass

def openCard(card):
    pass

def startGame(self):
    pass

def checkUserMoney(money):
    pass

def checkTableMoney(money):
    pass

def winner(ID, nickname):
    pass


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




#4장을 준다
#test = Gameplay()
playerHand = [] #사용자가 보는 것.
playerHandNum = [] #핸드의 숫자
playerHandPattern = []#핸드의 무늬
#CUI Part
'''
일단 서버와의 통신 없이.  CUI만 구현, 이후 통신이 구현 되면 필요한 부분 수정.
'''



while True:
    pass
'''
#초기 패 설정
'''

'''
for count in range(4):
    playerHand.append(number_to_card(test.card_draw()))
print_player_hand()

'''
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
    #playerHand.append(number_to_card(test.card_draw()))
    print(playTurn, "번째 카드는", playerHand[-1], "입니다.")
    playerHand[-1] = playerHand[-1] + "(open)"
    print_player_hand()

#히든 카드 1장 주기.
print("7번째 카드 입니다.")
#playerHand.append(number_to_card(test.card_draw()))
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
