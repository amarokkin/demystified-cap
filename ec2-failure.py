import socket, sys, time
from signal import *

# Open for ec2-reliable
HOST, PORT = "0.0.0.0", 9995
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen(2)

def clean(*args):
	serversocket.close()
	sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
	signal(sig, clean)

(connection, address) = serversocket.accept()
database_key = ""
received_bytes_decoded = ""
while True:
	try:
		received_bytes_decoded = connection.recv(1024).decode("utf-8")
	except OSError:
		(connection, address) = serversocket.accept()
		continue

	if (len(received_bytes_decoded) < 1):
		(connection, address) = serversocket.accept()
		continue

	dictionary = received_bytes_decoded.split(",")
	if (dictionary[0] == "sleep"):
		time.sleep(5)
	elif (dictionary[0] == "get"):
		connection.send(database_key.encode("utf-8"))
	elif (dictionary[0] == "set"):
		if len(dictionary) != 3:
			continue
		database_key = dictionary[1]
	else:
		fail = "You suck"
		connection.send(fail.encode("utf-8"))