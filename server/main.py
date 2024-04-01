import os
import sys
import threading
import socket
import dbs_exec as dbe
import dbs_view as dbv

import common

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1069
LISTEN_COUNT = 10


def createServerSocket(serverIP=SERVER_IP, serverPort=SERVER_PORT, listenCount=LISTEN_COUNT):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))
    serverSocket.listen(listenCount)
    return serverSocket


def handleClient(client: socket.socket, address: any, specialServerSocket: dict) -> None:
    status = common.recvEncryptedMessage(client, 0)
    if not status[0] or status[1] == '':
        print('TODO FIX HANDLE CLIENT')
        quit()
    key = int(status[1])
    print(status)
    dbv.loginMenu(client, key, address, specialServerSocket)


def main():
    status = dbe.createDatabase('database_main')
    if not status[0]:
        print('Creation of DBS failed {}, program will be terminated...'.format(status[1]))
        sys.exit(1)
    print('Databases initialized...')

    dbv.loadMenus()
    print('Menu text loaded...')

    serverSocket = createServerSocket()
    print('Server socket is now available...')

    specialServerSocket = {}
    for server_type in ["admin", "customer"]:
        clientSocket, address = serverSocket.accept()
        print('Made connection with Server ', address)
        specialServerSocket[server_type] = (clientSocket, address)
    print("Ready for Clients...")

    while True:
        clientSocket, address = serverSocket.accept()
        print('Made connection with ', address)
        threading.Thread(target=handleClient, args=(
            clientSocket, address, specialServerSocket)).start()

if __name__ == '__main__':
    main()  