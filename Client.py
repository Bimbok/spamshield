import socket
import threading
from datetime import datetime

SERVER_HOST = '127.0.0.1'  # Server IP
SERVER_PORT = 5002
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
name = input('Name: ')

def listen():
    while True:
        msg = s.recv(1024).decode()
        print(f'\n{msg}')

t = threading.Thread(target=listen)
t.daemon = True
t.start()

while True:
    msg = input()
    if msg.lower() == 'q': break
    s.send(f'[{datetime.now().strftime("%H:%M")}] {name}: {msg}'.encode())
s.close()