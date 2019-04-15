# Demystified CAP

This mini-lab demonstrates an interpretation of CAP in that we can't have consistency and availability during a partition. This is demonstrated by having:

## About the Lab
1) Two AWS EC2 instances that each imitate a "database". This is done by containing a variable that can be set and get.
2) Creating a socket connection between the local machine and the first EC2 instance, let's call it EC2-Reliable. The local machine can set and get the variable on this machine.
3) Creating a socket connection between the local machine and the second EC2 instance, let's call it EC2-Failure. The local machine can only get the variable on this machine.
4) Creating a socket connection between EC2-Reliable and EC2-Failure. EC2-Reliable attempts to set the variable on EC2-Failure. It only succeeds sometimes. This is implemented by adding a delay when setting the variable on EC2-Failure to demonstrate that the connection can't be made immediately.

## High Availability
This lab demonstrates high availability (HA) when you run it because the results from getting the variable on EC2-Success and EC2-Failure return immediately, but the results are different in that the set order is set(high), set(available). EC2-Success returns available, as it should, while EC2-Failure returns high. This is because EC2-Failure didn't get updated before returning it's value after a partition.

## High Consistency
This lab demonstrates high consistency (HC) when you run it because the results from getting the variable on EC2-Success and EC2-Failure match up, but it takes some time to get the results. In this example, we set(high), set(consistency) and both EC2-Success and EC2-Failure return consistency after a partition.

## If you wish to run this on your own
1) Start up two AWS EC2 instances
2) Put them on the same Security Group
3) Add the correct Inbound rules to the security group: All TCP for your local machine IP, All TCP for the security group (so that the EC2 instances can communicate with each other)
4) Update ec2_failure_destination_name on ec2-reliable.py and client.py
5) Update ec2_success_destination_name on client.py
6) Add ec2-reliable.py to your EC2-Success machine - scp -i {path_to_.pem_file} {path_to_ec2-reliable.py}:~
7) Add ec2-failure.py to your EC2-Failure machine - scp -i {path_to_.pem_file} {path_to_ec2-failure.py}:~
8) Run the python files on both your EC2-Success and EC2-Failure machines
9) Run the client.py file on your local machine
10) MAKE SURE TO CLOSE YOUR EC2 INSTANCES TO AVOID CHARGES
