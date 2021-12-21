import threading
import socket


COMMANDS = ['join', 'create', 'leave', 'bet', 'drawCard', 'removeCard', 'openCard', 'startGame', 'checkUserMoney', 'checkTableMoney', 'winner']
PORT = 31597
MAX_USERS = 100
playerHandler = PlayerHandler()


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
    def __init__(self, nickname, socket):
        self.nickname = nickname
        self.socket = socket

class PlayerHandler:
    def __init__(self):
        self.players = []
        self.playerCount = 0


def listen_tcp_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind(('localhost', PORT))
        serverSocket.listen(MAX_USERS)
        while True:
            newConnection, newConnectionAddr = serverSocket.accept()
            newThread = threading.Thread(target=accept_tcp_connection, args=(newConnection, newConnectionAddr))
            newThread.start()

def accept_tcp_connection(newConnection, newConnectionAddr):
    while True:
        clientMessage = newConnection.recv(2048)
