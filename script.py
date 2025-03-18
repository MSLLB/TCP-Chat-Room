import threading
import socket


"""
Un TCP Chat Room est une application où plusieurs clients (utilisateurs) peuvent se connecter à un serveur 
via le protocole TCP pour envoyer et recevoir des messages en temps réel."""


host="0.0.0.0"#IP locale du PC ,les autres appareils sur le même Wi-Fi puissent se connecter à ton serveur
port=5505  #Le port, c'est pour identifier l'application. On évite 80 car c'est réservé pour le web (HTTP)


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
"""
socket.AF_INET

Ça signifie qu'on utilise l'adresse IPv4 (ex : 192.168.x.x).
Si tu voulais utiliser IPv6, ça serait AF_INET6.

socket.SOCK_STREAM

Cela signifie qu'on utilise TCP (Transmission Control Protocol).
TCP est fiable, car il établit une connexion stable entre le client et le serveur avant d'envoyer des données."""

server.bind((host,port))
"""
Le bind(), c'est quoi exactement ?

Quand tu crées un socket, c'est comme créer une connexion vide.
Mais pour que cette connexion écoute sur une adresse IP et un port spécifique, tu dois utiliser bind().

"""

server.listen(6)
"""
le listen() permet de mettre ton serveur en mode "écoute" pour accepter les connexions des clients.
6 veut dire que mon serveur peut accepter 6 connections simultanées ,
"""

clients=[]
nicknames=[]

def broadcast (message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f"{nickname} left the chat".encode("ascii"))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client,adress=server.accept()
        print(f"connected with{adress}")
        
        client.send("NICK".encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"nickaname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))
        client.send("connected to the server".encode("ascii"))

        thred=threading.Thread(target=handle,args=(client,))
        thred.start()


print("server is listening ...")
receive()


            


