
'''


            simple project to show transfer files using Udp socket
                               client portion
                       Copyright (C) 2019 Weizi Cai
                       cai.590@buckeyemail.osu.edu
                       
                       
'''

import hashlib
import os
import sys
import socket

# the command line is python3 ftpc.py <IP-address-of-System-1> <remote-port-on-System-2> <troll-port-on-System-1> <local-file-to-transfer>

SenderAddress = sys.argv[1]   
serverPortNo = int(sys.argv[2])          
trollPortNo = int(sys.argv[3])
fileName = sys.argv[4]

Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
# socket.AF_INET is used for networking between server and client
# socket.SOCK_DGRAM is used for datagram transfering(UDP) 

# check the case that recv does not exist
if not os.path.exists('recv'):
    os.makedirs('recv')


#open the file I/O

file = open(fileName, 'rb')

filestat = os.stat(fileName)

print('=====   now start to transfer file   =====')

'''
# according to requirment, The payload of each UDP segment willcontain the remote IP (4 bytes) + remote port (2 bytes) 
 + flag (1 byte), followed by a actual segment

'''
NoOfBytesSeg = SenderAddress + str(serverPortNo) + '1' + str(filestat.st_size)

NameOfFileSeg = SenderAddress + str(serverPortNo) + '2' + fileName

datasegconst = SenderAddress + str(serverPortNo) + '3'

NoOfBytesSeg = NoOfBytesSeg.encode('ascii')
NameOfFileSeg = NameOfFileSeg.encode('ascii')

ip = socket.gethostbyname(socket.gethostname())

Sock.sendto(NoOfBytesSeg, (ip, trollPortNo))
Sock.sendto(NameOfFileSeg, (ip, trollPortNo))

# now send the actual data

while True:
    piece = file.read(1000)

    # Concatentates the datasegconst information
    segment = datasegconst + str(piece)
    
    if segment:
        Sock.sendto(segment.encode('ascii'), (ip, trollPortNo))
    else:
        break


#close the stream
Sock.close()

print ("reveiving information", repr(Sock.recv(1024)))
