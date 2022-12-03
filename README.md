# Comp429 distance-vector-routing-protocols
- Group 2: Jacob Hagen, Bum Jun Cho, Hao Lu, Elvis Chino-Islas

## Requirements to run the code
- Python3
- 4 linux machines (our test environments are configured with Amazon Linux 2 Kernel 5.10 AMI)
- Make sure the machines can talk to each other (e.g. ping)
- There are required external packages that need to be installed
  - provided in requirements.txt file.
  - command to install pakcages:
    - pip install -r requirements.txt 

## How to run the program
- python3 topy.py
  - Depends on your configuration, python command may be 'python3' instead of 'python'

## Tasks
- Prepared Devlopement & testing environment
  - Github, 4 x Amazon AWS EC2 instance
- Created a Readme & basic architecture of the program along with:
  - list of functions
  - work priorities
  
 ## Functions with Individual Contributions
 | Function            | Description                                                                                                       | Cho               | Elvis             | Hao               | Jacob             |
 | ------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------- | ----------------- | ----------------- | ----------------- |
 | `Server_State Class`| Contains the server's information including timer, id, ip, port, routing table, network topology, packets, etc    | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[X] </li> | <ul><li>[X] </li> |
 | `per_update`              | Handling Timer for periodic message exchange                                                                | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
  | `menu`              | called when input is recived.                                                                                    | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[X] </li> | <ul><li>[X] </li> |
 | `recv_message`      | called when a connection in the selection has something to read.                                                  | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `get_ip`            | used to get ***this*** server's public ip.                                                                        | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `find_id`           | used to find the id of the given tuple, `(ip:str, port:int)`, if it is adefined server, otherwise returns `None`. | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |  
 | `server`           | Initial server function to get topology filename and updating time interval value.                                 | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |  
 | `readTopFile`       | Read topology file to establish topology and initial routing table.                                               | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `createRouteTable`  | create initial routing table using topology file.                                                                 | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `display`  | display current routing table of the server.                                                                               | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `get_port`          | used to find the port of a given socket. *(unused)*                                                               | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `handle_connection` | called when a connection is attempting to connect through the listening socket.                                   | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `clean_up`          | called when the server exits, closes selector and all sockets.                                                    | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `init_listr`        | used to create the listening socket.                                                                              | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `print_commands`    | print supported commands.                                                                                         | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `main`              | contains the runtime loop, sets up the event loop using a selector.                                               | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `packets`  | Display number of distance vector (packets) this server has received sinc ethe last invocation of this information.        | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `disable`  | Disable the link to a given server. Doing this "closes" the connection to a given server with server-ID                    | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `crash`  | Close all connections. This is to simulate server crashes. Close all connections on all links.                               | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `send_message_crash`  | send crash messages to all neighbors to alert                                                                   | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `formMessage`  | Create routing update message to be sent out to neighbors                                                              | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `step`  | Using 'send_message' function, send routing update to neighbors right away and reset periodic timer                           | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `send_message`  | send routing update message in JSON format to neighbors                                                               | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `Update`  | The link cost between two servers                                                                                           | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `eliminateCrashServer`  | When a server is crashed, it eliminates the server from it's routing table and topology                       | <ul><li>[ ] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |
 | `bellmanford`  | Calculates new routing table based on the new Distance Vector Received                                                 | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[X] </li> | <ul><li>[X] </li> |
 | `chkInf`  | handles 'Infinity' cost when cost is used for calculation                                                                   | <ul><li>[X] </li> | <ul><li>[x] </li> | <ul><li>[ ] </li> | <ul><li>[ ] </li> |



