##code based on https://www.neuralnine.com/tcp-chat-in-python/ 
import socket
import threading

HOST = ""
PORT = 5612


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

clients = []
nicknames = []
chatrooms = []

def broadcast(message, sender, nickname):
    if sender in clients:
        index = clients.index(sender)
        person = chatrooms[index]
    
        room = person[0]
    
        for pair in chatrooms:
        
            if pair[0] == room:
                pair[1].send(message)
    else:
        index = nicknames.index(nickname)
        person = chatrooms[index]
    
        room = person[0]
    
        for pair in chatrooms:
        
            if pair[0] == room and pair[1] != sender:
                pair[1].send(message)



def whisperClient(nick, message, sender):
    
    data = message
    index1 = clients.index(sender)
    sendPer = chatrooms[index1]
        
    if nick in nicknames:
        index2 = nicknames.index(nick)
        client = clients[index2]
        person = chatrooms[index2]
    
        if (person[0] == sendPer[0]):
            message = "whisper from " + data
            client.send(message.encode('ascii'))
            return


    sender.send('Did not find the nick'.encode('ascii'))
    


def handle(client, ):
    while True:
        try:
            
            message = client.recv(1024)
            
            data = message.decode('ascii').split(' ', 2)

            index = clients.index(client)
            nickname = nicknames[index]

            if (data[0] == "whisper"):
                whisperClient(data[1], data[2], client)
                continue
            
            broadcast(message, client, nickname)
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            clients.remove(client)
            
            
            broadcast('{} left!'.format(nickname).encode('ascii'), client, nickname)
            
            client.close()
            nicknames.remove(nickname)
            chat=chatrooms[index]
            chatrooms.remove(chat)

            break

def receive():
    while True:
        client, addr = s.accept()
        print("Connected with {}".format(str(addr)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        client.send('ROOM'.encode('ascii'))
        room = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        chatrooms.append([room, client])

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), client, nickname)
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
