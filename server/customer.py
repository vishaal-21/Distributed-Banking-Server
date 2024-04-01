import threading
import socket
import dbs_exec as dbe
import dbs_view as dbv
import common
import os
import sys
import pickle
# To use the common.py module

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1069
IP = '127.0.0.1'
PORT = 1071

def connectToServer():
    CustomerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CustomerSocket.bind((IP, PORT))
    CustomerSocket.connect((SERVER_IP, SERVER_PORT))
    return CustomerSocket

def main():
    try:
        CustomerSocket = connectToServer()
        status = dbe.createDatabase("database_customer")
        if not status[0]:
            print('Creation of DBS failed due to {}, program will be terminated...'.format(
                status[1]))
            sys.exit(1)
        print('Databases initialized...')

        while True:
            data = CustomerSocket.recv(1024)
            if data:
                clientSocket, key, details = pickle.loads(data)
                dbv.customerMenu(clientSocket, key, details)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        CustomerSocket.close()

if __name__ == '__main__':
    main()