import socket, time, random
import _pickle as pickle
from _thread import *

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)  # 26.21.99.133
PORT = 5050
HEADER = 64
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connections = 0
players = {}
lasers = {}
start = False

try:
	server.bind((SERVER_IP, PORT))
except socket.error as e:
	print(str(e))
	print("[SERVER] Server could not start")
	quit()

def handle_client(conn, addr, p):
	global connections, players, start, HEADER

	data = conn.recv(2)
	greeting = data.decode("utf-8")
	print(f"[LOG] Player {p} say {greeting} to the server")

	players = {'1': {'x':200, 'y':550, 'lives':5, 'ready':False},
			   '2': {'x':200, 'y':0, 'lives':5, 'ready':False}}

	conn.send(p.encode())
	inital_data = pickle.dumps(players)
	conn.send(inital_data)

	while True:
		try:
			data = conn.recv(2048)
			#print(f'[LOG] Server recieved data from player {p}')
			if not data:
				break

			p_data = pickle.loads(data)  # {'x':x, 'y':y, 'lives':lives, 'ready':False}

			#if both_ready(players):  # 'MOVE x y'
			players[p]['x'] = p_data['x']
			players[p]['y'] = p_data['y']
			players[p]['lives'] = p_data['lives']
			players[p]['ready'] = p_data['ready']
			
			send_data = pickle.dumps(players)
			'''
			{'1':{'x':x, 'y':y, 'lives':lives, 'ready':False}, 
			'2':{'x':x, 'y':y, 'lives':lives, 'ready':False}}
			'''
			conn.send(send_data)
			#print(f'[LOG] Server sent data to player {p}')

		except Exception as e:
			print(e)
			break
	
	conn.close()
	connections -= 1
	print(f"[DISCONNECTED] Player {p} disconnected")

def get_uid():
	return random.randrange(1000, 9999)

def both_ready(players):
	return players['1']['ready'] and players['2']['ready']

print(f"[SERVER] Server started with local ip {SERVER_IP}")
server.listen()
print("[SERVER] Waiting for connections")

while True:
	conn, addr = server.accept()
	print(f"[LOG] Player {addr} connected to the server")
	connections += 1
	p = '1'
	if connections%2 == 0:
		p = '2'
	start_new_thread(handle_client, (conn, addr, p))

print(f"[SERVER] Server offline")