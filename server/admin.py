import os
import sys
import pickle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import common
import dbs_view as dbv
import dbs_exec as dbe

import socket
import threading
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1069
IP='127.0.0.1'
PORT=1070

def connectToServer():
    AdminSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    AdminSocket.bind((IP, PORT))
    AdminSocket.connect((SERVER_IP, SERVER_PORT))
    return AdminSocket

def main():
    try:
        AdminSocket = connectToServer()
        status  = dbe.createDatabase("database_admin")
        if not status[0]:
            print('Creation of DBS failed due to {}, program will be terminated...'.format(status[1]))
            sys.exit(1)
        print('Databases initialized...')
        status=dbe.addAdmin()
        
        # while True:
        #     data = AdminSocket.recv(1024)
        #     if data:
        #         clientSocket, key, details = pickle.loads(data)
        #         dbv.adminMenu(clientSocket, key, details)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        AdminSocket.close()
    
if __name__ == '__main__':
    main()