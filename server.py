import threading
import socket
import time
import random


COMMANDS = ['join', 'create', 'leave', 'bet', 'drawCard', 'removeCard', 'openCard', 'startGame', 'checkUserMoney', 'checkTableMoney', 'winner', 'ack']
PORT = 31597
MAX_USERS = 100
MAX_RANGE = 65535


class Room:
    def __init__(self, roomName, roomPW, baseBetting, baseMoney, host):
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

class PlayerHandler:
    def __init__(self):
        self.players = dict()
        self.playerCount = 0
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
        self.enqueue_message(newID, f'0 {newID} ack OK registered {newID}')
        return newID

class RoomHandler:
    def __init__(self):
        self.rooms = dict()

    def join(self, userID, roomID, roomPW):
        message = f'0 {userID} ack'
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
        self.rooms[roomID] = Room(roomName, roomPW, baseBetting, baseMoney, userID)

    def leave(self, userID, roomID):
            if userID in self.rooms[roomID].userList:
                del self.rooms[roomID].userList[userID]

roomHandler = RoomHandler()
playerHandler = PlayerHandler()
tempThread = threading.Thread(target=playerHandler.send_message_to_players)
tempThread.start()

def listen_tcp_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind(('localhost', PORT))
        serverSocket.listen(MAX_USERS)
        while True:
            accept_tcp_connection(serverSocket)

def accept_tcp_connection(serverSocket):
    newConnection, newConnectionAddr = serverSocket.accept()
    newThread = threading.Thread(target=listen_client_message, args=(newConnection, newConnectionAddr))
    newThread.start()

def listen_client_message(newConnection, newConnectionAddr):
    playerID = -1
    while True:
        clientMessage = str(newConnection.recv(2048))
        if clientMessage == '':
            if playerID != -1:
                #call leave
                del(playerHandler.players[playerID])
                return
        messageList = clientMessage.split()
        callerID = int(messageList[0])
        destinationID = int(messageList[1])
        clientCommand = messageList[2]
        args = messageList[3:]
        if callerID != playerID:
            newConnection.send(f'0 {callerID} ack badRequest callerIDNotMatched')
        if destinationID != 0:
            if playerHandler.enqueue_message(destinationID, clientMessage):
                playerHandler.enqueue_message(callerID, f'0 {callerID} ack OK forwarded {destinationID}')
            else:
                playerHandler.enqueue_message(callerID, f'0 {callerID} ack badRequest noSuchID {destinationID}')
        else:
            if callerID in playerHandler.players.keys():
                pass
            elif callerID == -1:
                if clientCommand is 'register':
                    playerID = playerHandler.register(args[0], newConnection)
                else:
                    newConnection.send(f'0 -1 ack badRequest wrongCommand')


tempThread = threading.Thread(target=listen_tcp_connection)
tempThread.start()
