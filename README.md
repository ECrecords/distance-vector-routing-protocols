# Comp429 distance-vector-routing-protocols
- Group 2: Jacob Hagen, Bum Jun Cho, Hao Lu, Elvis Chino-Islas

## Requirements / installation to run the code
- Python3
- 4 linux machines (our test environments are configured with Amazon Linux 2 Kernel 5.10 AMI)
- Make sure the machines can talk to each other (e.g. ping)
  - pre-configured ports in the topology file must be opened (firewall configuration)
- There are required external packages that need to be installed
  - provided in requirements.txt file.
  - command to install pakcages:
    - pip install -r requirements.txt 

## How to run the program
- python3 topy.py
  - Depends on your configuration, python command may be 'python' instead of 'python3'
  - make sure you run Python3

## Tasks that are done
- Prepared Devlopement & testing environment
  - Github, 4 x Amazon AWS EC2 instance
  - Firewall configuration, connectivity testing (using ping and tcp connection)
- Created a Readme & basic architecture of the program along with:
  - Topology diagram
  - list of functions
  - work priorities
  - meeting schedules
  
 ### Codes (Functions) with Individual Contributions
 | Function               | Description                                                                                                         | Cho | Elvis | Hao | Jacob |
 | ---------------------- | ------------------------------------------------------------------------------------------------------------------- | --- | ----- | --- | ----- |
 | `Server_State Class`   | Contains the server's information including timer, id, ip, port, routing table, network topology, packets, etc      | ☒   | ☒     | ☒   | ☒     |
 | `get_ip`               | used to get ***this*** server's public ip.                                                                          | ☐   | ☒     | ☐   | ☐     |
 | `get_port`             | used to find the port of a given socket. *(unused)*                                                                 | ☐   | ☒     | ☐   | ☐     |
 | `find_id`              | used to find the id of the given tuple, `(ip:str, port:int)`, if it is adefined server, otherwise returns `None`.   | ☐   | ☒     | ☐   | ☐     |
 | `chkInf`               | handles 'Infinity' cost when cost is used for calculation                                                           | ☒   | ☐     | ☐   | ☐     |
 | `print_commands`       | print supported commands.                                                                                           | ☐   | ☒     | ☐   | ☐     |
 | `per_update`           | Handling Timer for periodic message exchange                                                                        | ☐   | ☒     | ☐   | ☐     |
 | `main`                 | contains the runtime loop, sets up the event loop using a selector.                                                 | ☒   | ☒     | ☐   | ☐     |
 | `menu`                 | called when input is recived.                                                                                       | ☒   | ☒     | ☒   | ☒     |
 | `display`              | display current routing table of the server.                                                                        | ☒   | ☐     | ☐   | ☐     |
 | `server`               | Initial server function to get topology filename and updating time interval value.                                  | ☒   | ☒     | ☐   | ☐     |
 | `readTopFile`          | Read topology file to establish topology and initial routing table.                                                 | ☒   | ☒     | ☐   | ☐     |
 | `createRouteTable`     | create initial routing table using topology file.                                                                   | ☒   | ☒     | ☐   | ☐     |
 | `init_listr`           | used to create the listening socket.                                                                                | ☐   | ☒     | ☐   | ☐     |
 | `Update`               | The link cost between two servers                                                                                   | ☒   | ☐     | ☐   | ☐     |
 | `step`                 | Using 'send_message' function, send routing update to neighbors right away and reset periodic timer                 | ☒   | ☐     | ☐   | ☐     |
 | `bellmanford`          | Calculates new routing table based on the new Distance Vector Received                                              | ☒   | ☐     | ☐   | ☒     |
 | `recv_message`         | called when a connection in the selection has something to read.                                                    | ☒   | ☒     | ☐   | ☐     |
 | `handle_connection`    | called when a connection is attempting to connect through the listening socket.                                     | ☐   | ☒     | ☐   | ☐     |
 | `send_message`         | send routing update message in JSON format to neighbors                                                             | ☒   | ☐     | ☐   | ☐     |
 | `formMessage`          | Create routing update message to be sent out to neighbors                                                           | ☒   | ☐     | ☐   | ☐     |
 | `packets`              | Display number of distance vector (packets) this server has received sinc ethe last invocation of this information. | ☒   | ☐     | ☐   | ☒     |
 | `disable`              | Disable the link to a given server. Doing this "closes" the connection to a given server with server-ID             | ☒   | ☐     | ☒   | ☐     |
 | `crash`                | Close all connections. This is to simulate server crashes. Close all connections on all links.                      | ☐   | ☐     | ☐   | ☒     |
 | `send_message_crash`   | send crash messages to all neighbors to alert                                                                       | ☐   | ☐     | ☒   | ☐     |
 | `eliminateCrashServer` | When a server is crashed, it eliminates the server from it's routing table and topology                             | ☐   | ☐     | ☒   | ☐     |
 | `clean_up`             | called when the server exits, closes selector and all sockets.                                                      | ☐   | ☒     | ☐   | ☐     |



