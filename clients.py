import threading
import socket
import datetime


nickname=input(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:First you have to pick up a nickname:')
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',5555))

commands_list=['nickname()','admin()','close()','kick()','ban()']
stop_loop=False


def receive():
	while True:
		global stop_loop
		if stop_loop:
			break
		try:
			message=client.recv(1024).decode('ascii')
			if message=='BANNED':
				print('You have been banned!')		
				stop_loop=True
			elif message=='NICKNAME':
				client.send(nickname.encode('ascii'))
			elif message.split(':')[1]=='Commands/':
				print('Here are the commands you can use:Close(),Admin(),Nickname(),Kick(),Ban()')
			elif message.split(':')[1]==('NEW_NICK'):
				print(message.split(':')[2])
			elif message.split(':')[1]==('ADMIN_PASS'):
				print(message.split(':')[2])
			elif message.split(':')[1]=='CLOSE':
				print('exit')
			elif message.split(':')[1]=='WRONG_C0MMAND':
				print('wrong command,pls check again')
			elif message.split(':')[1]=='KICK':
				if message.split(':')[2]==nickname:
					print('You have been kicked!')		
					stop_loop=True
				else:
					print(f'{message.split(":")[2]} was kicked from server!')
			elif message.split(':')[1]=='BAN':
				if message.split(':')[2]==nickname:
					print('You have been banned!')		
					stop_loop=True
				else:
					print(f'{message.split(":")[2]} was banned from server!')
			else:
				print(message)
		except:
			print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:An error occured! You have been disconnected.')
			client.close()
			break


def write():
	while True:
		if stop_loop:
			break
		your_input=input('')
		if your_input.endswith('()'):
			if your_input.lower() in commands_list:
				if your_input.lower()=='nickname()':
					new_nick=input('choose a new nick:')
					client.send(f"{nickname}:NEW_NICK:{new_nick}".encode('ascii'))
				elif your_input.lower()=='admin()':
					admin_pass=input('write admin pass:')
					client.send(f"{nickname}:ADMIN_PASS:{admin_pass}".encode('ascii'))
				elif your_input.lower()=='close()':
					client.send(f'{nickname}:CLOSE: '.encode('ascii'))
				elif your_input.lower()=='kick()':
					name_to_kick=input('choose the nickname you wanna kick:')
					with open('nicknames.txt','r') as f:
						if name_to_kick not in f.read():
							print('Wrong nickname')
						else:
							client.send(f'{nickname}:KICK:{name_to_kick}'.encode('ascii'))
				elif your_input.lower()=='ban()':
					name_to_ban=input('choose the nickname you wanna ban:')
					with open('nicknames.txt','r') as f:
						if name_to_ban not in f.read():
							print('Wrong nickname')
						else:
							client.send(f'{nickname}:BAN:{name_to_ban}'.encode('ascii'))
							with open('bans.txt','w') as f:
								f.write(f'{name_to_ban}\n')
			else:
				client.send(f'{nickname}:WRONG_C0MMAND:'.encode('ascii'))
		else:		
			client.send(f"{nickname}:{your_input}".encode('ascii'))

receive_thread=threading.Thread(target=receive)
receive_thread.start()
write_thread=threading.Thread(target=write)
write_thread.start()