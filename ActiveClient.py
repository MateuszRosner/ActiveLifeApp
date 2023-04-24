# Active Life
# komunikacja: MADs - Raspberry - PC
# Program ver 1.0
# TCP client

import socket
import threading
import sys

HOST_NAME = socket.gethostname()
# HOST_IP = socket.gethostbyname(HOST_NAME)
HOST_IP = '192.168.8.163'
HOST_PORT = 1025
HEADER_SIZE = 8

def MsgRecv():
    header_name = s.recv(HEADER_SIZE).decode('utf-8')
    if not header_name:
        sys.exit(0)
    header_len = int(header_name)
    msg_recv = s.recv(header_len).decode('utf-8')
    print(msg_recv)

def MsgSend(msg_send):
    msg_header = f'{len(msg_send):<{HEADER_SIZE}}'
    s.send(msg_header.encode('utf-8') + msg_send.encode('utf-8'))
    print("wysłane")
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_IP, HOST_PORT))
#s.listen(5)

# print("Czekam na połączenie...")
# conn, addr = s.accept()
# print(f'Połączenie z: {addr[0]} na porcie: {addr[1]} zostało nawiązane')

if __name__ == "__main__":

    while True:
        t = threading.Thread(target=MsgRecv)
        t.start()
        t.join()
    # msg = input(str("-> "))
    # MsgSend(msg)

