from prettytable import PrettyTable
import sys, traceback
import socket
import selectors
import json

from time import sleep
from requests import get

# used for updating routing table periodicly
#import schedule 

#constant 
FAILED_SEND_MAX = 3

# used to hold needed data & structures 
class Server_State:
    def __init__(self):
        self.sel                = None
        self.id                 = None
        self.ip                 = None
        self.port               = None
        self.listener_fd        = None
        self.timeout_interval   = None
        self.routing_table      = None
        self.servers            = None
        self.neighbors          = None
        self.updatedIDs         = []
        self.failed_con         = {}


# used to get public ip
def get_ip() -> str:
    return get('https://api.ipify.org').content.decode('utf8')

# input ip and port and return if it is a known server
def find_id(state: Server_State, t_ip: str, t_port: int) -> int:
    t_id: int = None

    for server in state.servers:
        id, ip, port = server
        if t_ip == ip and t_port == port:
            t_id = id
    
    return t_id
    

# used to get the port number of a specified socket
def get_port(sock: socket.socket) -> int:
    try:
        port = sock.getsockname()[1]
    except:
        port = None
        print("failed to retrieve port")
    finally:
        return port

# Read Topology File to create a list of Servers in the network and this server's neighbors
def readTopFile(file_name):
    
    # Open Topology file and read each line
    with open(file_name, 'r') as file:
        topology = file.read().splitlines()
    
    # number of servers and neighbors
    n_servers = int(topology[0])
    n_neighbors = int(topology[1])

    # list of servers and neighbors
    servers = [row.split() for row in topology[2:2+n_servers]]
    neighbors = [row.split() for row in topology[2+n_servers:2+n_servers+n_neighbors]]

    # This server's ID
    thisID = neighbors[0][0]
    thisPort=''
    thisIP = ''
    
    for server in servers:
        if server[0] == thisID:
            thisIP = server[1]
            thisPort = server[2]
            

    # return the lists and this server's ID
    return servers, neighbors, thisID, int(thisPort), thisIP


# Create Initial routing Table
def createRouteTable(state: Server_State):
    # Using Python Dictionary
    routingTable = {}

    # neighbor ID and the cost is pulled from neighbors information 
    neighborIDs = { i[1]:i[2]  for i in state.neighbors }

    # server IDs from the topology
    serverIDs = [ i[0] for i in state.servers ] 

    
    for serverID in serverIDs:
        if serverID in neighborIDs.keys():
            nexthop = serverID
            cost = neighborIDs[serverID]
            # add neighbor servers with cost to the routing table
            routingTable[serverID] = {'nexthop': nexthop, 'cost': cost}
            state.updatedIDs.append(serverID)
        else:
            # add non-neighbor servers with 'Infinity" cost to the routing table
            routingTable[serverID] = {'nexthop': 'n.a', 'cost': 'inf'}
            state.updatedIDs.append(serverID)
    
    # add this server to this server cost to the routing table
    routingTable[state.id] = {'nexthop': state.id, 'cost': '0'}
    state.updatedIDs.append(state.id)

    return routingTable

# display the routing table of this server
def display(routingTable):
    myTable = PrettyTable(["ID", "Next Hop", "Cost"])
    for item in routingTable:
        # Display the routing table with NON-Infinity cost links
        if routingTable[item]['cost'] != 'inf':
            myTable.add_row([item, routingTable[item]['nexthop'], routingTable[item]['cost']])
    myTable.sortby = "ID"        
    print(myTable)


# Initial server function to get topology filename and updating time interval value
def server(command: str):
    try:
        # Validate the command and Raise error if server command is not properly used
        if len(command) != 5 or command[0] != 'server' or command[1] != '-t' or command[3] != '-i':
            raise ValueError()
        
        else:
            # Get file name and time interval
            file_name = command[2]
            time_interval = int(command[4])
            
            return file_name, time_interval

    # Throw an error for invalid server function usages.
    except ValueError:
        print(f"""

Error: '{' '.join(command)}'. Invalid command usage.

Usage: server [-t FILE_NAME] [-i TIME_INTERVAL]

Distance Vector Protocol

options:
  -t FILE_NAME      Name of the topology file (ex: -t topology.txt)
  -i TIME_INTERVAL  Time interval between routing updates in seconds (ex: -i 30)
""")

def packets():
    pass

# our goal is to remove the disabled ID from our state.neighbors list and state.routingtable, 
# and we don't want this server to send any messages to the disabled server
# so that disabled server won't receive any meesage and update its list after the time.
# our state.neighbors list looks like this
#  [[thisserverID, neighborserverID, cost], [thisserverID, neighborserverID, cost], [thisserverID, neighborserverID, cost], .....]

def disable(state: Server_State, command:str):
    # we are on server1, disable <serverid>
    # ex) disable 3
    #check if that id is really our neighbor
    # if so
    dstServerID = command[1]
    state.routing_table[dstServerID]['cost'] = 'inf'
    state.updatedIDs.append(dstServerID)
    # remove serverid(ex: 3) from state.neighbors list
    for item in state.neighbors:
        if item[1] == dstServerID:
            state.neighbors.remove(item)


def crash():
    pass

def exit_func():
    pass

# Create message
def formMessage(state: Server_State):
    updatedIDs = (set(state.updatedIDs))
    nFields = len(updatedIDs)
    payload = {}
    
    #create header message
    header = { "header": { "n_update_fields": nFields, "server_ip": state.ip, "server_port": state.port } }

    #create payload message
    server_response_temp = []
    for item in updatedIDs:
        if item in state.routing_table.keys():
            cost = state.routing_table[item]['cost']
            for server in state.servers:
                if item == server[0]:
                    server_response_temp.append({'ip': server[1], 'port': server[2], 'id': server[0], 'cost': cost})

    payload["payload"] = server_response_temp
    header.update(payload)
    message = header
    return(message)

# Send routing table update to neighbors right away. Then reset updated list and timer.
def step(state: Server_State):
    if len(state.updatedIDs) != 0:
        message = formMessage(state)
        for neighbor in state.neighbors:
            for server in state.servers:
                if server[0] == neighbor[1]:
                    neighborIP = server[1]
                    neighborPort = server[2]
                    send_message(state, message, neighborIP, neighborPort)
        #reset updateIDs list after step
        state.updatedIDs.clear()
    else:
        print('routing table has not been updated. we are not sending routing table.')

class FAILED_SEND(OSError):
    pass

def send_message(state: Server_State, message, ip: str, port: int) -> bool:

    # used json.dumps instead of json.dump. It was throwing error with 'fp'
    # payload = json.dumps(state.routing_table).encode('utf-8')
    payload = json.dumps(message).encode('utf-8')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            try:
                s.settimeout(5)
                s.connect((ip, int(port)))
            except socket.timeout:
                print(f'error: timeout connecting to {ip}:{port}')
                raise FAILED_SEND()
            except socket.error:
                s.close()
                print(f'error: failed to connect to {ip}:{port}')
                raise FAILED_SEND()
            else:
                try:
                    s.sendall(payload)
                except socket.error:
                    print(f'error: failed to send message to {ip}:{port}')
                    raise FAILED_SEND()
                else:
                    return True
        except FAILED_SEND as err:
            t_id = find_id(state, ip, port)

            if not t_id:
                return
            
            if t_id in state.failed_con.keys():
                if (state.failed_con[t_id] == FAILED_SEND_MAX-1):
                    print(f'error: Server {t_id} has failed to communicate {FAILED_SEND_MAX} times')
                    state.failed_con.clear()
                else:
                    state.failed_con[t_id] += 1
            else:
                state.failed_con[t_id] = 1        

            return False
            


            

# update routing table with new cost and the list of updated servers
def update(state: Server_State, command:str):
    if command[1] != state.id:
        print(f"Error: \'{command}'. This server's ID is {state.id}")
    else:
        dstServerID = command[2]
        cost = command[3]
        state.routing_table[dstServerID]['cost'] = cost
        state.updatedIDs.append(dstServerID)
        
    
# this will be called upon reciving a message
def recv_message(state: Server_State, sock: socket.socket):
    message = sock.recv(1024)
    recv_payload = ''

    if message:
        recv_payload = json.loads(message)
        
    else:
        state.sel.unregister(sock)
        sock.close()
        return
    
    sender_id = None
    
    for server in state.servers:
        id, ip, _ = server
        if recv_payload['header']['server_ip'] == ip:
            sender_id = id
            
    if sender_id is None:
        print("ERROR: RECEIVED A MESSAGE FROM UNKNOWN SERVER")
        
    print(f"RECEIVED A MESSAGE FROM SERVER {sender_id}")
    
    # print recv_payload to test the type and the structure
    #print(type(recv_payload))
    #print(recv_payload)
    
    # commented out since we don't update the route table immediately without bellman ford algorithm.
    bellmanford(state, recv_payload, sender_id)
    
# Calculates new routing table based on the new Distance Vector Received
def bellmanford(state: Server_State, recv_payload, sender_id):
    # routingTable[serverID] = {'nexthop': nexthop, 'cost': cost}
    for dstID in state.routing_table.keys():
        myCost = chkInf(state.routing_table[dstID]['cost'])
        costToSender = chkInf(state.routing_table[sender_id]['cost'])
        costFromSenderToDst = ''
        for route in recv_payload['payload']:
            if route['id'] == dstID:
                costFromSenderToDst = chkInf(route['cost'])
        newCost = costToSender + costFromSenderToDst
        if newCost < myCost:
            temp = {'nexthop': sender_id, 'cost': newCost}
            state.routing_table[dstID].update(temp)


# check if cost is infinity
def chkInf(cost: str):
    if cost == 'inf':
        return float('inf')
    else:
        return int(cost)


def handle_connection(state: Server_State, sock: socket.socket) -> None:
    #TODO error handling

    # accepts incomming connection 
    # and set it to non-blocking
    conn, addr = sock.accept()
    conn.setblocking(False)

    # register connection to selector and
    # define it callback funtion as recv_message
    state.sel.register(conn, selectors.EVENT_READ, recv_message)

def clean_up(state: Server_State) -> None:

    # unregister STDIN from selector
    state.sel.unregister(sys.stdin.fileno())

    # check if listener exists
    if state.listener_fd is not None:
        # close and unregister listening soocket
        state.listener_fd.close()
        state.sel.unregister(state.listener_fd)

    # close selector
    state.sel.close()

def init_listr(state: Server_State) -> None:
    
    try:
        # create listening socket
        state.listener_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        state.listener_fd = None
        print(f'error: {err}')
    else:
        try:
            # bind it to specified port and all network interfaces
            state.listener_fd.bind(('', state.port))
        except socket.error as err:
            state.listener_fd = None
            print(f'error: {err}')
        else:
            #begin listening on socket
            state.listener_fd.listen(4)

            # set listening socket to non-blocking
            state.listener_fd.setblocking(False)
    
            # register listening socket to state selector
            # set its callback funtion to handle_connection
            state.sel.register(state.listener_fd, selectors.EVENT_READ, data=handle_connection)
    
            # get state.listener_fd into state
            state.listener_fd = state.listener_fd
    

def print_commands() -> None:
    print(
f"""
Commands:

server -t <topology-file-name> -i <routing-update-interval>
update <server-ID1> <server-ID2> <link-cost>
step
packets
display
disable <server-ID>
crash
exit\n""")

# wrappper used to hold the selection menu of the chat applciation
def menu(usr_input: str, state: Server_State) -> None:
    
    # splits the string by " " so addtional usr_input arguments can be read.
    usr_input = usr_input.split(" ")

    if "server" in usr_input[0]:
        if state.routing_table is not None:
            print("'server' command can only be used at startup")
        else:
            # Program starts with calling server function
            file_name, state.timeout_interval = server(usr_input)

            # Get topology information (servers in the topology, neighbors to this server, and this server's ID)
            state.servers, state.neighbors, state.id, state.port, state.ip = readTopFile(file_name)

            # Print this server's IP and ID
            print(f"This server's ID is {state.id}\n")

            # Use topology information above to initilize routing table
            state.routing_table = createRouteTable(state)

            # wrapper used to initiate the listening socket
            init_listr(state)

            # check if listener is created
            if state.listener_fd is None:
                print("error: failed to create listening socket")
                exit(1)

            # display routing table
            display(state.routing_table)

    elif "update" in usr_input[0] and state.routing_table is not None:
        update(state, usr_input)

    elif "step" in usr_input[0] and state.routing_table is not None:
        step(state)

    elif "packets" in usr_input[0] and state.routing_table is not None:
        print('TODO') #TODO

    elif "display" in usr_input[0] and state.routing_table is not None:
        # display routing table
        display(state.routing_table)
    
    elif "disable" in usr_input[0] and state.routing_table is not None:
        update(state, usr_input)
        

    elif "crash" in usr_input[0] and state.routing_table is not None:
        #TODO exit program correctly
        pass

    elif "exit" in usr_input[0]:
        #TODO update clean_up as needed
        clean_up(state)
        exit()

    elif state.routing_table is not None:
        print(f"'{' '.join(usr_input)}' is a invalid command")

    elif state.routing_table is None:
        print("use the 'server' command to initalize the server")

    else:
        print("error occured")

# main function
def main():
    try:
        print(f"""
Distance Vector Protocol ()
-------------------------------------------------------------""")
        print_commands()
        
        # delcare and init server state
        state = Server_State()

        # using selector to read STDIN
        state.sel = selectors.DefaultSelector()
        state.sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

        while True:
            print(">>", end=" ")
            sys.stdout.flush()
            event = state.sel.select(timeout=None)

            for key, mask in event:
                if key.fileobj == sys.stdin.fileno():

                    # reads input from stdin and strips whitespaces
                    usr_input = (sys.stdin.readline()).strip()

                    # ignore if string is empty 
                    # otherwise call menu with usr input
                    if usr_input:
                        menu(usr_input, state)
                else:
                    # handle connection request / recieve message
                    callback = key.data
                    callback(state, key.fileobj)
                        
    except SystemExit as message:
        print(message)
    except:
        traceback.print_exc()
        sys.exit()
        
# our main starts here    
if __name__ == "__main__":
    main()
