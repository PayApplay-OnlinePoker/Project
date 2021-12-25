import threading
import socket
import time
import random
import library


tempThread = threading.Thread(target=library.playerHandler.send_message_to_players)
tempThread.start()


def listen_tcp_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind(('localhost', library.PORT))
        serverSocket.listen(library.MAX_USERS)
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
                if library.playerHandler.players[playerID].joinedRoom != 0:
                    roomID = library.playerHandler.players[playerID].joinedRoom
                    library.roomHandler.rooms[roomID].userList.remove(playerID)
                    library.roomHandler.announce_leave(playerID, roomID)
                del(library.playerHandler.players[playerID])
            return
        messageList = clientMessage.split()
        callerID = int(messageList[0])
        destinationID = int(messageList[1])
        clientCommand = messageList[2]
        args = messageList[3:]
        if callerID != playerID:
            newConnection.send(f'0 {callerID} response badRequest callerIDNotMatched')
        elif destinationID != 0:
            if library.playerHandler.enqueue_message(destinationID, clientMessage):
                library.playerHandler.enqueue_message(callerID, f'0 {callerID} response OK forwarded {destinationID}')
            else:
                library.playerHandler.enqueue_message(callerID, f'0 {callerID} response badRequest noSuchID {destinationID}')
        else:
            if callerID in library.playerHandler.players.keys():
                if clientCommand == 'join':
                    if len(args) == 2:
                        library.roomHandler.join(callerID, args[0], args[1])
                    else:
                        library.playerHandler.enqueue_message(callerID, f'0 {callerID} response badRequest lenArgsNotMatched')
                elif clientCommand == 'fetch':
                    if args[0] == 'rooms':
                        library.roomHandler.fetch_room(callerID)
            elif callerID == -1:
                if clientCommand is 'register':
                    playerID = library.playerHandler.register(args[0], newConnection)
                else:
                    newConnection.send(f'0 -1 response badRequest wrongCommand')


tempThread = threading.Thread(target=listen_tcp_connection)
tempThread.start()
