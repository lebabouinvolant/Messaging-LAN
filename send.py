"""
Docstring for send:

Diverses conventions:
la requete discovery UDP est de forme HELLO/USERNAME/TCPPORT
toutes les requetes handshakes TCP seront de la forme HELLO/USERNAME/TCPPORT avec une taille fixée à 1024
"""

from typing import List
import socket
import threading



IP = "0.0.0.0"
UDPPORT = 1234
TCPPORT = 1235
USERNAME = "UNKNOWN"
broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcaster.bind((IP, UDPPORT))
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

TCPServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPServer.bind(("0.0.0.0", TCPPORT))



class Peer:
    Username = "Unknown"
    ip = ""
    port = 0
    Sock = None
    last_seen = 0
    def __init__(self, user, ip, port = 0, socket = None):
        self.Username = user
        self.ip = ip
        self.port = port
        self.Sock = socket
AllPeers : List[Peer] = [] 


def connect_to_peer(peer : Peer):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.connect((peer.ip, peer.port))
        Sock.send(f"HELLO/{USERNAME}/{TCPPORT}")
        peer.Sock = Sock



def sendHello():
    data = f"HELLO/{USERNAME}/{TCPPORT}"
    broadcaster.sendto(data.encode('utf-8'), ("192.168.1.255", UDPPORT))


def listenUDP():
    while True:
        data, addr = broadcaster.recvfrom(1024)
        clearedStr = data.decode('utf-8')
        parseHelloMessage(clearedStr, addr)

def findPeerFromUsername(username):
    for peer in AllPeers:
        if peer.Username == username:
            return peer
    return False


def listenTCP():
    TCPServer.listen()
    while True:
        socketPeerIncoming, addr = TCPServer.accept()
        data = socketPeerIncoming.recv(1024).decode('utf-8')
        parseHelloMessage(data, addr, socketPeerIncoming)

def parseHelloMessage(data, addr, socketPeerIncoming = None):
    try:
        if(data.split("/")[0] == "HELLO"):
            peer = findPeerFromUsername(data.split("/")[1])
            if peer != False:
                peer.ip = addr[0]
                peer.port = int(data.split("/")[2])
                peer.Sock = socketPeerIncoming
            else:
                NewPeer = Peer(data.split("/")[1], addr[0], int(data.split("/")[2]), socketPeerIncoming)
                AllPeers.append(NewPeer)
            return True
        return False
    except:
        return False

def handlePeer(peer : Peer):
    buffer = ""
    socketPeer = peer.Sock
    while True:
        data = socketPeer.recv(1024)
        if not data:
            break  # socket fermée
        buffer += data.decode("utf-8")
        while "\n" in buffer:
            msg, buffer = buffer.split("\n", 1)


sendHello()
#listen()