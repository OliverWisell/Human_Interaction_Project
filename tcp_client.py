import socket  

HOST = '83.255.245.18'
PORT = 50000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    # Send data to the server
    client_socket.sendall(b'Hello, world')
    # Receive data from the server
    data = client_socket.recv(1024)

print('Received: {datadecode()}')