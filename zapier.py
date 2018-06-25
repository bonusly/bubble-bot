# This code is modified from the source at:
# https://github.com/softScheck/tplink-smartplug

import socket
import argparse
import time

# You will need to forward the correct port
# Can also use ngrok: ./ngrok tcp <localip>:9999
ip =       ''   # Your IP goes here! (string)
port =     9999 # default for TP-Link plugs
duration = 5    # How many seconds bubble blower will be on (adjust as necessary)
version =  1    # If your plug doesn't work with v1, try v2

on =       '{"system":{"set_relay_state":{"state":1}}}'
off =      '{"system":{"set_relay_state":{"state":0}}}'

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
    key = 171
    result = "\0\0\0"+chr(len(string))
    for i in string:
            a = key ^ ord(i)
            key = a
            result += chr(a)
    return result

# Updated encryption comes from
# https://github.com/softScheck/tplink-smartplug/issues/22
def encrypt_v2(string):
    key = 171
    result = "\0\0\0"+chr(len(string))
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

def send_command(cmd):
	# Send command and receive reply
	try:
		sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock_tcp.connect((ip, port))
		if version == 2:
			sock_tcp.send(encrypt_v2(cmd))
		else:
			sock_tcp.send(encrypt(cmd))
		data = sock_tcp.recv(2048)
		sock_tcp.close()

		print "Sent:     ", cmd
		print "Received: ", decrypt(data[4:])
	except socket.error:
		quit("Cound not connect to host " + ip + ":" + str(port))


# Turn bubbles on, wait duration, turn bubbles off
send_command(on)
time.sleep(duration)
send_command(off)
