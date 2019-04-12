import socket, sys, time, multiprocessing
from signal import *

ec2_failure_destination_name = "ec2-3-19-57-29.us-east-2.compute.amazonaws.com"

HOST, PORT = "0.0.0.0", 9823
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen(1)

def clean(*args):
	serversocket.close()
	sys.exit(0)
for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
	signal(sig, clean)

(connection, address) = serversocket.accept()
database_key = ""
received_bytes = bytearray()
received_bytes_decoded = ""
num_sets = 0

while True:
	try:
		received_bytes = connection.recv(1024)
		received_bytes_decoded = received_bytes.decode("utf-8")
	except OSError:
		(connection, address) = serversocket.accept()
		continue

	if (len(received_bytes_decoded) < 1):
		(connection, address) = serversocket.accept()
		continue

	dictionary = received_bytes_decoded.split(",")
	print("Dictionary: " + received_bytes_decoded)
	if (dictionary[0] == "get"):
		print(database_key)
		connection.send(database_key.encode("utf-8"))
	elif (dictionary[0] == "set"):
		if len(dictionary) != 3:
			continue
		database_key = dictionary[1]

		# Open a socket with ec2-failure if num_set % 2 = 0 and close immediately after
		if num_sets % 2 == 0:
			ec2_failure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ec2_failure_socket.connect((ec2_failure_destination_name, 9995))
			ec2_failure_socket.send(received_bytes)
			ec2_failure_socket.close()
		elif dictionary[2] == "c":
			message_sleep = "sleep"
			ec2_failure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ec2_failure_socket.connect((ec2_failure_destination_name, 9995))
			ec2_failure_socket.send(message_sleep.encode("utf-8"))
			ec2_failure_socket.send(received_bytes)
			ec2_failure_socket.close()
		num_sets += 1
	else:
		fail = "You suck"
		connection.send(fail.encode("utf-8"))