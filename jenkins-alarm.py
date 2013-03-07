# Free to use, share and modify. I'm not resposible for anything that blows up due to this code. 
# No liability. Use at your own risk. 
#
# @author: varunmehta

"""

This is a simple python program, which listens to a port (6667) and plays a sound when the build breaks or is fixed again. 
To run this program, just start it as

$ python jenkins-alarm.py

The json format received from the notification-plugin is:
		{
		   "name":"O.O.trunk",
		   "url":"job/O.O.trunk/",
		   "build":{
			  "full_url":"http://jenkins/job/O.O.trunk/6768/",
			  "number":6768,
			  "phase":"COMPLETED",
			  "status":"SUCCESS",
			  "url":"job/O.O.trunk/6768/"
		   }
		} 
		
"""

import os
import sys
import json
import socket

HOST = ""
PORT = 6667

# Listen for UDP messages from Jenkins
def listen_socket():
	# SOCK_DGRAM is the socket type to use for UDP sockets
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((HOST,PORT))
	#TODO: Check for timeout (should be infinity)
	data = sock.recv(2048)
	sock.close()
	return data


# Parse the JSON string coming in.
def parse_json(jenkins_response):
	response = json.loads(jenkins_response) 
	status = "NONE"
	name = "BUILD"
	if 'name' in response:
		name = response['name']
	if 'build' in response:
		build = response['build']
		if 'status' in build:
			status = build['status']
	
	name = name.strip().upper()
	status = status.strip().upper()
	return status
	
# TADA!
def play_sound(status):
	if status == 'FAILED':
		os.system("mpg123 /home/squealer/Music/alarm.mp3")
	elif status == 'UNSTABLE':
		os.system("mpg123 /home/squealer/Music/ambulance.mp3")
	elif status == 'FIXED' :
		os.system("mpg123 /home/squealer/Music/clapping.mp3")

# Main program (infinite loop!)
# TODO: Better logging
while 1:
	data = listen_socket()
	print "\nUDP Response from Jenkins:\n ", data
	status = parse_json(data)
	print "\nSTATUS: ", status, "--"
	play_sound(status)

