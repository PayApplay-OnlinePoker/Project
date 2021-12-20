import threading


COMMANDS = ['join', 'create', 'leave', 'bet', 'drawCard', 'removeCard', 'openCard', 'startGame', 'checkUserMoney', 'checkTableMoney', 'winner']
PORT = 31597


class Room:
    def __init__(self, roomName, roomPW, baseBetting, baseMoney, host):
        self.roomName = roomName
        self.roomPW = roomPW
        self.baseBetting = baseBetting
        self.baseMoney = baseMoney
        self.host = host
        self.userList = [host]

class Player:
    def __init__(self, nickname, socket):
        self.nickname = nickname
        self.socket = socket


def accept_tcp_connection():
    pass
