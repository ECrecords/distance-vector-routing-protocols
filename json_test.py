import json
import socket

with open('example_data.json', 'r') as f:
    data = json.load(f)

print(data)
payload = json.dumps(data).encode('utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('35.165.134.136', 4901))
    s.sendall(payload)