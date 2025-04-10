import socket

HOST = '0.0.0.0'
PORT = 50000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Listening on {HOST}:{PORT}")
    # Wait for a connection
    server_socket.settimeout(10)  # Set timeout to 10 seconds
    try:
        server_socket.accept()
    except socket.timeout:
        print("No connection within the timeout period.")
        exit(1)
    # Accept a connection
    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode())
            conn.sendall(data)