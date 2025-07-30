import random
import time
from datetime import datetime
from socket import *
serverName = 'localhost'
serverPort = 12000


id = str(input("Digite o ID: "))
i=0

while (i!=10):
    temp = random.uniform(9,30)
    timestamp = datetime.now().timestamp()

    id = str(id)
    temp = str(temp)
    timestamp = str(timestamp)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    time.sleep(0.2)
    clientSocket.send(id.encode())
    time.sleep(0.2)
    clientSocket.send(temp.encode())
    time.sleep(0.2)
    clientSocket.send(timestamp.encode())
    time.sleep(0.2)
    modifiedSentence = clientSocket.recv(1024)
    print ('Resposta do servidor:', modifiedSentence.decode())
    clientSocket.close()
    i = i+1
    time.sleep(5)