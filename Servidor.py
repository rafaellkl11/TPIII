from socket import *
import matplotlib.pyplot as plt
import csv
from threading import Thread
import time
from plot_temperatures import plot_temperatures

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

# Variáveis de controle para as threads
server_running = False
results_running = False

def servidor():
    global server_running
    print('O servidor esta pronto esperando mensagens')
    while server_running:
        try:
            connectionSocket, addr = serverSocket.accept()
            id = connectionSocket.recv(1024).decode()
            temp = connectionSocket.recv(1024).decode()
            timestamp = connectionSocket.recv(1024).decode()

            dados = id+";"+temp[0:2]+";"+timestamp[0:16]
            dados = str(dados)
            
            with open('dados.csv', 'a') as arquivo:
                arquivo.write(dados+"\n")

            temp = int(temp[0:2])

            if(temp<15 or temp>35):
                res="Temperatura fora do padrão!"
                connectionSocket.send(res.encode())
            else:
                res="Dados armazenados com sucesso!"
                connectionSocket.send(res.encode())
            connectionSocket.close()
        except Exception as e:
            if not server_running:
                break # Exit loop if server is stopped externally
            print(f"Erro no servidor: {e}")

def resultados():
    global results_running
    while results_running:
        time.sleep(10)
        try:
            with open("dados.csv","r") as arquivo:
                ids = []
                for dado in arquivo:
                    dado = dado.split(";")
                    if len(dado) > 0 and dado[0] not in ids:
                        ids.append(dado[0])
            
            ids.sort()
            print(ids)

            for i in range(len(ids)):
                j = 0
                soma = 0
                media = 0
                with open ("dados.csv","r") as arquivo:
                    for dado in arquivo:
                        dado = dado.split(";")
                        if len(dado) > 1 and ids[i] == dado[0]:
                            try:
                                soma = soma + int(dado[1])
                                j = j + 1
                            except ValueError:
                                continue # Skip invalid temperature values
                if j > 0:
                    media = soma / j
                    print ("id: ",ids[i],"|","media: ",media)
            plot_temperatures()
        except FileNotFoundError:
            print("Arquivo dados.csv não encontrado. Nenhum dado para analisar.")
        except Exception as e:
            if not results_running:
                break # Exit loop if results thread is stopped externally
            print(f"Erro na análise de resultados: {e}")

def start_server():
    global server_running, servidor1
    if not server_running:
        server_running = True
        servidor1 = Thread(target=servidor)
        servidor1.start()
        print("Servidor iniciado.")
    else:
        print("Servidor já está em execução.")

def stop_server():
    global server_running, servidor1
    if server_running:
        server_running = False
        # Para fechar o socket do servidor e permitir que a thread do servidor termine
        # É necessário uma conexão para que o accept() seja liberado
        try:
            temp_socket = socket(AF_INET, SOCK_STREAM)
            temp_socket.connect(('localhost', serverPort))
            temp_socket.close()
        except ConnectionRefusedError:
            pass # Server might already be down or not accepting connections
        servidor1.join() # Espera a thread do servidor terminar
        print("Servidor parado.")
    else:
        print("Servidor não está em execução.")

def start_results_analysis():
    global results_running, resultados2
    if not results_running:
        results_running = True
        resultados2 = Thread(target=resultados)
        resultados2.start()
        print("Análise de resultados iniciada.")
    else:
        print("Análise de resultados já está em execução.")

def stop_results_analysis():
    global results_running, resultados2
    if results_running:
        results_running = False
        resultados2.join() # Espera a thread de resultados terminar
        print("Análise de resultados parada.")
    else:
        print("Análise de resultados não está em execução.")

# Menu principal
while True:
    print("\n--- Menu do Servidor ---")
    print("1. Iniciar Servidor")
    print("2. Parar Servidor")
    print("3. Iniciar Análise de Resultados (e plotar gráfico)")
    print("4. Parar Análise de Resultados")
    print("5. Sair")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        start_server()
    elif choice == '2':
        stop_server()
    elif choice == '3':
        start_results_analysis()
    elif choice == '4':
        stop_results_analysis()
    elif choice == '5':
        stop_server()
        stop_results_analysis()
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")

