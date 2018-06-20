# This code is modified from the source at:
# https://github.com/softScheck/tplink-smartplug

import socket
import argparse
import time

# Set target IP, port and command to send
ip = # Your IP goes here! (string)
port = 9999 # default for TP-Link plugs
duration = 5 # How many seconds bubble blower will be on, adjust as necessary
version = 0.1

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = "\0\0\0\0"
	for i in string:
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171
	result = ""
	for i in string:
		a = key ^ ord(i)
		key = ord(i)
		result += chr(a)
	return result

cmd = '{"system":{"set_relay_state":{"state":1}}}'

# Send command and receive reply
try:
	sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_tcp.connect((ip, port))
	sock_tcp.send(encrypt(cmd))
	data = sock_tcp.recv(2048)
	sock_tcp.close()

	print "Sent:     ", cmd
	print "Received: ", decrypt(data[4:])
except socket.error:
	quit("Cound not connect to host " + ip + ":" + str(port))


time.sleep(duration)
cmd = '{"system":{"set_relay_state":{"state":0}}}'

# Send command and receive reply
try:
	sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_tcp.connect((ip, port))
	sock_tcp.send(encrypt(cmd))
	data = sock_tcp.recv(2048)
	sock_tcp.close()

	print "Sent:     ", cmd
	print "Received: ", decrypt(data[4:])
except socket.error:
	quit("Cound not connect to host " + ip + ":" + str(port))
