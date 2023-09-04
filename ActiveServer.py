# Active Life
# komunikacja: MADs - Raspberry - PC
# Program ver 1.0
# TCP server

import socket
import threading
import sys
import time
#import MadDataRead

HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
#HOST_IP = '192.168.8.163'
HOST_PORT = 502
HEADER_SIZE = 8

def MsgRecv():
    header_name = conn.recv(HEADER_SIZE).decode('utf-8')
    if not header_name:
        sys.exit(0)
    header_len = int(header_name)
    msg_recv = conn.recv(header_len).decode('utf-8')
    print(msg_recv)

def MsgSend(msg_send):
    conn.send("TEST".encode('utf-8'))
    print(msg_send)

print(f'Hostname: {HOST_NAME}')
print(f'IP Address: {HOST_IP}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST_IP, HOST_PORT))
s.listen(5)

print("Czekam na połączenie...")
conn, addr = s.accept()
print(f'Połączenie z: {addr[0]} na porcie: {addr[1]} zostało nawiązane')

if __name__ == "__main__":
    i = 1
    while True:
        t1 = threading.Thread(target=MsgSend('proba nr: '+str(i)))
        #t2 = threading.Thread(target=MsgSend(MadDataRead.MadData(0)))
        #t3 = threading.Thread(target=MsgSend(MadDataRead.MadData(1)))
        # t4 = threading.Thread(target=MsgRecv())
 
        t1.start()
        #t2.start()
        #t3.start()
        # t4.start()
        
        t1.join()
        #t2.join()
        #t3.join()
        # t4.join()
        
        i += 1
        time.sleep(3)

