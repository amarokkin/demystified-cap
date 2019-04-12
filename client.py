import socket, time, sys

message_set_ha_1 = "set,high,a"
message_set_ha_2 = "set,availability,a"
message_set_hc_1 = "set,high,c"
message_set_hc_2 = "set,consistency,c"
message_get = "get"


ec2_success_destination_name = "ec2-3-16-27-102.us-east-2.compute.amazonaws.com"
ec2_failure_destination_name = "ec2-3-19-57-29.us-east-2.compute.amazonaws.com"

ec2_success_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ec2_success_socket.connect((ec2_success_destination_name, 9823))

print("--------HIGH AVAILABLE (immediate response) --------")
ec2_success_socket.send(message_set_ha_1.encode("utf-8"))
time.sleep(.3)

ec2_success_socket.send(message_set_ha_2.encode("utf-8"))
time.sleep(.3)

ec2_success_socket.send(message_get.encode("utf-8"))
data = ec2_success_socket.recv(1024)
print("EC2-Reliable: " + data.decode("utf-8"))

# Open socket with EC2-failure
ec2_failure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ec2_failure_socket.connect((ec2_failure_destination_name, 9995))
ec2_failure_socket.send(message_get.encode("utf-8"))
data = ec2_failure_socket.recv(1024)
print("EC2-Failure: " + data.decode("utf-8"))
ec2_failure_socket.close()





print("--------HIGH CONSISTENCY (notice the pause to update) --------")
ec2_success_socket.send(message_set_hc_1.encode("utf-8"))
time.sleep(.7)

ec2_success_socket.send(message_set_hc_2.encode("utf-8"))
time.sleep(.7)

ec2_success_socket.send(message_get.encode("utf-8"))
data = ec2_success_socket.recv(1024)
print("EC2-Reliable: " + data.decode("utf-8"))

# Open socket with EC2-failure
ec2_failure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ec2_failure_socket.connect((ec2_failure_destination_name, 9995))
ec2_failure_socket.send(message_get.encode("utf-8"))
data = ec2_failure_socket.recv(1024)
print("EC2-Failure: " + data.decode("utf-8"))
ec2_failure_socket.close()

ec2_success_socket.close()