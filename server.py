import threading
import socket
import time


COMMANDS = ['join', 'create', 'leave', 'bet', 'drawCard', 'removeCard', 'openCard', 'startGame', 'checkUserMoney', 'checkTableMoney', 'winner']
PORT = 31597
MAX_USERS = 100


class Room:
    def __init__(self, roomName, roomPW, baseBetting, baseMoney, host):
        self.roomName = roomName
        self.roomPW = roomPW
        self.baseBetting = baseBetting
        self.baseMoney = baseMoney
        self.host = host
        self.userList = [host]
        self.tableMoney = 0

class Player:
    def __init__(self, nickname, socket, ID):
        self.nickname = nickname
        self.socket = socket
        self.messageQueue = []
        self.playerID = ID

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
        callerID = clientMessage[0]
        destinationID = clientMessage[1]
        command = clientMessage[2]
        args = clientMessage[3:]
        if destinationID != 0:
            if playerHandler.enqueue_message(destinationID, clientMessage):
                enqueue_message(callerID, f'0 {callerID} ack sent {clientMessage}')
            else:
                enqueue_message(callerID, f'0 {callerID} ack noSuchID {clientMessage}')
        else:
            pass #Server API handle

