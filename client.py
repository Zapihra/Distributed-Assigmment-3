##code based on https://www.neuralnine.com/tcp-chat-in-python/ 
import socket
import threading

HOST = ""
PORT = 5612

HOST = input("Give the IP address: ")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
except:
    print("Something went wrong with the IP address")
    exit(1)

nickname = input("Choose your nickname: ")
room = input("Give name of the room: ")
print("whisper name message: message privately in chat")
print("exit: exit from the chat")

def receive():

    while True:
        try:
            message = s.recv(1024).decode('ascii')

            if message == 'NICK':
                s.send(nickname.encode('ascii'))
            elif message == 'ROOM':
                s.send(room.encode('ascii'))
            else:
                print(message)

        except WindowsError:
            print("You have either exited from chat or there is a connection issue")
            s.close()
            break

        except:
            print("An error has occurred!")
            s.close()
            break

def write():
    while True:

        data = input()
        x = data.split(' ', 2)

        if (data == "exit"):
            print("Closing...")
            s.close()
            return
        
        message = "{}: {}".format(nickname, data)

        if(x[0] == "whisper"):
            
            message = "{} {} {}: {}".format(x[0], x[1], nickname, x[2])
        
        try:
            s.send(message.encode('ascii'))
        except:
            print("sever has closed")
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
