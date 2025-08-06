from socket import *
from threading import Thread
from datetime import datetime
import time
import matplotlib.pyplot  as plt
import numpy as np
import matplotlib.dates as mdates

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

def servidor():
	print('O servidor esta pronto esperando mensagens')
	while True:
		connectionSocket, addr = serverSocket.accept()
		id = connectionSocket.recv(1024).decode()
		temp = connectionSocket.recv(1024).decode()
		timestamp = connectionSocket.recv(1024).decode()

		dados = id+";"+temp[0:2]+";"+timestamp[0:16]
		dados = str(dados)
		
		arquivo = open('dados.csv', 'a')
		arquivo.write(dados+"\n")
		arquivo.close()

		temp = int(temp[0:2])

		if(temp<15 or temp>35):
			res="Temperatura fora do padrão!"
			arquivo = open('dados.csv', 'a')
			connectionSocket.send(res.encode())
		else:
			res="Dados armazenados com sucesso!"
			connectionSocket.send(res.encode())
		connectionSocket.close()

def resultados():
	while True:
		time.sleep(10)
		arquivo = open("dados.csv","r")
		ids = []
		for dado in arquivo:
			dado = dado.split(";")
			if (ids == None):
				ids.append(dado[0])
			else:
				if (not(dado[0] in ids)):
					ids.append(dado[0])
		arquivo.close()
		
		ids.sort()
		print(ids)

		i=0

		
		while (i!=len(ids)):
			j = 0
			soma = 0
			media = 0
			arquivo = open ("dados.csv","r")
			for dado in arquivo:
				dado = dado.split(";")
				if (ids[i] == dado[0]):
					soma = soma + int(dado[1])
					j = j + 1
			media = soma / j
			print ("id: ",ids[i],"|","media: ",media)
			arquivo.close()
			i = i + 1
		
		plt.ion()

		fig, ax = plt.subplots(figsize = (12,6))
		idsGrf = {}

		arquivo = open ("dados.csv","r")
		
		for dado in arquivo:
			id, temp, data = dado.strip().split(";")
			id = int(id)
			temp = int(temp)
			timestamp = datetime.strptime(data, "%Y-%m-%d %H:%M")

			if id not in idsGrf:
				idsGrf[id] = {'tempos': [], 'valores': [], 'linha': None}
			idsGrf[id]['tempos'].append(timestamp)
			idsGrf[id]['valores'].append(temp)

			# Atualizar o gráfico
			ax.clear()

			for g, dados_g in idsGrf.items():
				ax.plot(dados_g['tempos'], dados_g['valores'], marker='o', label=f'id {g}')

			# Configurações do gráfico
			ax.set_title("Gráfico em Tempo Real por id")
			ax.set_xlabel("Tempo")
			ax.set_ylabel("Valor")
			ax.legend()
			ax.grid(True)

			# Formatação de datas no eixo X
			ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
			fig.autofmt_xdate()

			plt.pause(0.2)  # Simula tempo de chegada de novos dados
		arquivo.close()
		print("teste1")

		# Desligar modo interativo ao final
		plt.ioff()
		print("teste2")
		plt.show()
		print("teste3")

servidor1 = Thread(target=servidor)
resultados2 = Thread(target=resultados)

servidor1.start()
resultados2.start()