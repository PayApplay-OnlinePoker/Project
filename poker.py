# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

import random
import socket
import time
import threading


HAND_RANKING = ["HC", "OP", "TP", "TK", "S", "BS", "MT", "F", "FH", "FC", "SF", "BSF", "RSF"]
CLIENT_CARD = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
CLIENT_PATTEN = ["Spade", "Heart", "Diamond", "Clover"]
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush
SERVER_ADDR = 'onlinepoker.hopto.org'
PORT = 31597


id = -1


class Apicall:
    def join(self, roomID, roomPW):
        pass

    def create(self, roomName, roomPW, baseBetting, baseMoney):
        clientSocket.sendMessageQueue.append(f'{id} 0 {roomName} {roomPW} {baseBetting} {baseMoney}'

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
        clientSocket.sendMessageQueue.append("")


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

def number_to_card(number):
    if number in range(1, 14): #Spade
        this_card = CLIENT_PATTEN[0] + CLIENT_CARD[number - 1]
        return this_card
    elif number in range(14, 27): #Heart
        this_card = CLIENT_PATTEN[1] + CLIENT_CARD[number - 14]
        return this_card
    elif number in range(27, 40): #Diamond
        this_card = CLIENT_PATTEN[2] + CLIENT_CARD[number - 27]
        return this_card
    elif number in range(40, 53): #Clover
        this_card = CLIENT_PATTEN[3] + CLIENT_CARD[number - 40]
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
                message = str(receiveMessageQueue.pop(0))
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
                message = str(receivedAcks.pop(0))
                messageList = message.split()
                if messageList[3] != 'OK':
                    print(message)
                #보낸 메시지에서 찾아서 날려야 함.


clientSocket = ClientSocket()
tempThread = threading.Thread(target=clientSocket.listen_server_message)
tempThread.start()
tempThread = threading.Thread(target=clientSocket.send_server_message)
tempThread.start()
tempThread = threading.Thread(target=clientSocket.sort_received_messages)
tempThread.start()

#4장을 준다
test = Gameplay()
playerHand = []

#초기 패 설정
for count in range(4): 
    playerHand.append(number_to_card(test.card_draw()))
print_player_hand()

#카드 한장 버리기
print("1:" + playerHand[0], "2:" + playerHand[1], "3:" + playerHand[2], "4:" + playerHand[3])
removeCard = int(input("버릴 카드를 선택해주세요. : "))
del playerHand[removeCard - 1]

#카드 한장 오픈하기
print("1:" + playerHand[0], "2:" + playerHand[1], "3:" + playerHand[2])

openCard = int(input("오픈할 카드를 선택해주세요. : "))
playerHand[openCard -1] = playerHand[openCard - 1] + "(open)"

#SWAP
swap = playerHand[0] 
playerHand[0] = playerHand[openCard-1]
playerHand[openCard -1 ] = swap
print_player_hand()

#오픈 카드 3장 주기.
for playTurn in range(4, 7):
    print(playTurn, "번째 카드입니다.")
    playerHand.append(number_to_card(test.card_draw()))
    playerHand[-1] = playerHand[-1] + "(open)"
print_player_hand()

#히든 카드 1장 주기.
print("7번째 카드 입니다.")
playerHand.append(number_to_card(test.card_draw()))
print_player_hand()
