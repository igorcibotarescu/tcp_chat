import threading
import socket
import datetime


host=''
port=5555


server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message,user):
	for client in clients:
		if client!=user:
			client.send(message)

def handle(client):
	while True:
		try:
			message=client.recv(1024).decode('ascii')
			if len(message.split(":"))==2:
				if message.split(":")[1]=='':
					continue
				elif message.split(":")[1]!='Commands/':
					client.send(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:Your message:{message.split(":")[1]}'.encode("ascii"))
					broadcast(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:{message}'.encode('ascii'),client)
					continue		
			broadcast(message.encode('ascii'),' ')
		except:
			index=clients.index(client)
			clients.remove(client)
			client.close()
			nickname=nicknames[index]
			nicknames.remove(nickname)
			broadcast(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:{nickname} left the chat!'.encode('ascii'),client)
			break


def receive():
	while True:
		client,address=server.accept()
		print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:A user just connected with the ip address:{address}')
		client.send('NICKNAME'.encode('ascii'))
		nickname=client.recv(1024).decode('ascii')
		with open('bans.txt','r') as f:
			if nickname in f.read():
				print(f'{nickname} tried to access the server but is banned!')
				client.send('BANNED'.encode('ascii'))
				client.close()
				continue
		with open('nicknames.txt','a') as f:
			f.write(f'{nickname}\n')

		nicknames.append(nickname)
		clients.append(client)

		print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:Nickname of the user:{nickname}')
		broadcast(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:{nickname} just joined the chat'.encode('ascii'),client)
		client.send(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:You have succesfully connected to the server'.encode('ascii'))
		client.send(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:You can enter "Commands/" to find out more commands'.encode('ascii'))

		thread=threading.Thread(target=handle,args=(client,))
		thread.start()


print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:Server is waiting for users to connect...')
receive()

