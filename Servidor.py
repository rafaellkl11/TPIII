from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('O servidor esta pronto esperando mensagens')
i=0
while True:
	i=i+1
	print(i)
	connectionSocket, addr = serverSocket.accept()
	id = connectionSocket.recv(1024).decode()
	temp = connectionSocket.recv(1024).decode()
	timestamp = connectionSocket.recv(1024).decode()

	temp = int(temp)
	timestamp = float(timestamp)

	teste = id +" - "+ temp +" - "+ timestamp

	teste = str(teste)

	connectionSocket.send(teste.encode())
	connectionSocket.close()
