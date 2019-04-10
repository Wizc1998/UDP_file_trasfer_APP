'''


            simple project to show transfer files using Udp socket
                               server portion
                       Copyright (C) 2019 Weizi Cai
                       cai.590@buckeyemail.osu.edu
                       
                       
'''

import hashlib
import os
import sys
import socket


# command line takes in this command:
# python3 ftps.py <local-port-on-System-2>

ServerPortNo = sys.argv[1]  

print ('=====   start to recieve file   =====')

ClientsSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
# socket.AF_INET is used for networking between server and client
# socket.SOCK_DGRAM is used for datagram transfering(UDP) 

ClientsSocket.bind(('', int(ServerPortNo)))

while True:
    seg, address = ClientsSocket.recvfrom(1024)
    if not data: break


    seg = seg.decode('ascii')
    # use string.find method to search for server port number
    position = seg.find(ServerPortNo)
    # store flag value from segment
    currentFlag = seg[len(ServerPortNo) + position]

    if currentFlag == '1':
        fileLengthStr = seg[len(ServerPortNo) + position + 1:]
        fileLength = int(fileLengthStr)
    if currentFlag == '2':
        targetFileName = seg[len(ServerPortNo) + position + 1:]
        targetFile = open('recv/'+targetFileName, 'wb')
    if currentFlag == '3':
        dataStr = seg[len(ServerPortNo) + position + 1:]
        targetFile.write(dataStr)

#close the file I/O
targetFile.close()

#now lets check whether the files matches


file1 = open(targetFileName, 'rb')
file2 = open("recv/"+targetFileName, "rb")

# Loop each truncate of these file to update the MD5 sums
while True:
    piece1 = file1.read(1000)
    piece2 = file2.read(1000)
    if piece1:
        md5_1.update(piece1)
        md5_2.update(piece2)

    else:
        break

print("MD5 hexdigest value after updated by files are as follow: ")
print()
print(md5_1.hexdigest())
print(md5_2.hexdigest())
print()
print()

if md5_1.hexdigest() == md5_2.hexdigest():
    print("the transferred file is bitwise identical to the original one.")

else: 
    print("the transferred file is NOT bitwise identical to the original one.")

    
# close streams
file1.close()
file2.close()


