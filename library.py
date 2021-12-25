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
        self.tableMoney = 0
        self.gameHandler = None

class Player:
    def __init__(self, nickname, socket, ID):
        self.nickname = nickname
        self.socket = socket
        self.messageQueue = []
        self.playerID = ID
        self.money = 0
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
                    playerHandler.enqueue_message(userID, message + f'OK joined {roomID}')
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
            playerHandler.enqueue_message(userID, f'0 {userID} response OK leaved {roomID}')
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

    def calculate_ranking(self): #hand-ranking
        global HAND_RANKING
        pass
