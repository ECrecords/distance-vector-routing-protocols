# Comp429 distance-vector-routing-protocols
- Group 2: Jacob Hagen, Bum Jun Cho, Hao Lu, Elvis Chino-Islas

## Requirements to run the code
- Python3
- 4 linux machines (our test environments are configured with Amazon Linux 2 Kernel 5.10 AMI)
- Make sure the machines can talk to each other (e.g. ping)
- There are required packages needs to be installed
  - provided in requirements.txt file.

## How to run the program
- python3 topy.py
  - Depends on your configuration, python command may be 'python3' instead of 'python'

## Tasks
- Prepared Devlopement & testing environment
  - Github, 4 x Amazon AWS EC2 instance
- Created a Readme & basic architecture of the program along with:
  - list of functions
  - work priorities
  
 ## List of functions done by each member
 - Cho: Server, Read Topology files, Initialize Routing Table, Menu, Update
 - ### Elvis: 
 | Function            | Description                                                                                                                     | Cho  | Elvis | Hao  | Jacob |
 | ------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---- | ----- | ---- | ----- |
 | `menu`              | called when input is recived.                                                                                                   | - [] | - []  | - [] | - []  |
 | `recv_message`      | called when a connection in the selection has something to read.                                                                | - [] | - []  | - [] | - []  |
 | `get_ip`            | used to get ***this*** server's public ip.                                                                                      | - [] | - []  | - [] | - []  |
 | `find_id`           | <p> used to find the id of the given tuple, `(ip:str, port:int)`, if it is a <br> defined server, otherwise returns `None`.</p> | - [] | - []  | - [] | - []  |
 | `get_port`          | used to find the port of a given socket. *(unused)*                                                                             | - [] | - []  | - [] | - []  |
 | `handle_connection` | called when a connection is attempting to connect through the listening socket.                                                 | - [] | - []  | - [] | - []  |
 | `clean_up`          | called when the server exits, closes selector and all sockets.                                                                  | - [] | - []  | - [] | - []  |
 | `init_listr`        | used to create the listening socket.                                                                                            | - [] | - []  | - [] | - []  |
 | `print_commands`    | print supported commands.                                                                                                       | - [] | - []  | - [] | - []  |
 | `main`              | contains the runtime loop, sets up the event loop using a selector.                                                             | - [] | - []  | - [] | - []  |
 - Hao: Packets, Crush
 - Jacob:


