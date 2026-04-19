
import socket
import threading
import joblib

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5002
model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
def clean_text(doc): ...  # From Step 1

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'Listening on {SERVER_HOST}:{SERVER_PORT}')

def check_spam(msg):
    vec = vectorizer.transform([clean_text(msg)]).toarray()
    return 'SPAM' if model.predict(vec)[0] == 1 else 'OK'

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            status = check_spam(msg)
            if status == 'SPAM':
                cs.send(b'[SPAM BLOCKED]')
                continue
            for client in client_sockets:
                client.send(msg.encode())
        except:
            client_sockets.remove(cs)
            break

while True:
    client_socket, addr = s.accept()
    client_sockets.add(client_socket)
    print(f'{addr} connected')
    t = threading.Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()