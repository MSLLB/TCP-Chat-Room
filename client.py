import threading
import socket

nickname=input("enter a valid nickname :")

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('192.168.1.5',5505))


def receive():
    while True:
         try:
            message=client.recv(1024).decode("ascii")
            if message=="NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)  # Affiche les messages du serveur, y compris "connected to the server"
         except:
            print("an error occurred !")
            client.close()
            break


def write():
    while True:
        message=f'{nickname} : {input(" ")}'
        client.send(message.encode("ascii"))


receive_thread=threading.Thread(target=receive)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()

