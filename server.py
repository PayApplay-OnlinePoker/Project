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

class RoomHandler:
    def __init__(self):
        self.rooms = dict()

    def join(self, userID, roomID, roomPW):
        if roomID in self.rooms.keys():
            if roomPW == self.rooms[roomID].roomPW:
                if len(self.rooms[roomID].userList) < 4:
                    self.rooms[roomID].userList.append(userID)
                    playerHandler.players[userID].money = self.rooms[roomID].baseMoney

                else:
                    playerHandler.enqueue_message(userID, f'0 {userID} ack roomIsFull')
            else:
                playerHandler.enqueue_message(userID, f'0 {userID} ack passwordNotMatched')
        else:
            playerHandler.enqueue_message(userID, f'0 {userID} ack noSuchRoomID')

    def create(self, userID, roomName, roomPW, baseBetting, baseMoney):
        roomID = random.randint(1, 65536)
        while roomID not in self.rooms.keys():
           roomID = random.randint(1, 65536)
        self.rooms[roomID] = Room(roomName, roomPW, baseBetting, baseMoney, userID)

    def leave(self, userID, roomID):
            if userID in self.rooms[roomID].userList:
                del self.rooms[roomID].userList[userID]

roomHandler = RoomHandler()
playerHandler = PlayerHandler()

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
        clientMessage = newConnection.recv(2048).split()
        callerID = int(clientMessage[0])
        destinationID = int(clientMessage[1])
        clientCommand = clientMessage[2]
        args = clientMessage[3:]
        if destinationID != 0:
            if playerHandler.enqueue_message(destinationID, clientMessage):
                playerHandler.enqueue_message(callerID, f'0 {callerID} ack sent {clientMessage}')
            else:
                playerHandler.enqueue_message(callerID, f'0 {callerID} ack noSuchID {clientMessage}')
        else:
            if callerID in playerHandler.players.keys():
                pass
            elif callerID == -1:
                pass


