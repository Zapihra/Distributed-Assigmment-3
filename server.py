import socket
import threading

HOST = ""
PORT = 5612


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)


clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message) 

def whisperClient(nick, message, sender):
    
    data = message
        
    if nick in nicknames:
        index = nicknames.index(nick)
        client = clients[index]
        message = "whisper from " + data
        client.send(message.encode('ascii'))

    else:
        sender.send('Did not find the nick'.encode('ascii'))
    


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            
            data = message.decode('ascii').split(' ', 2)

            if (data[0] == "whisper"):
                whisperClient(data[1], data[2], client)
                continue
            
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, addr = s.accept()
        print("Connected with {}".format(str(addr)))

        client.send('Nickname'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()