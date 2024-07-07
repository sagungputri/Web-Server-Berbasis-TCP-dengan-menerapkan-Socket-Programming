import socket
import threading
import os
import time

def handle_client(client_socket, addr):
    try:
        start_time = time.time() 

        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        headers = request.split('\n')
        filename = headers[0].split()[1]

        try:
            f = open(filename[1:])
            response_body = f.read()

            response_header = 'HTTP/1.1 200 OK\r\n\r\n'
            client_socket.send(response_header.encode('utf-8'))
            for i in range(0, len(response_body)):
                client_socket.send(response_body[i].encode('utf-8'))
            client_socket.send('\r\n'.encode('utf-8'))

            end_time = time.time()
            print(f"Request from {addr} processed in {end_time - start_time:.5f} seconds.")
        except FileNotFoundError:
            response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'

            response_body = '<html>\r\n<body>\r\n    <h1>404 Not Found</h1>\r\n</body>\r\n</html>'

            client_socket.send(response_header.encode('utf-8'))

            for i in range(0, len(response_body)):
                client_socket.send(response_body[i].encode('utf-8'))
            client_socket.send('\r\n'.encode('utf-8'))

            end_time = time.time()
            print(f"Request from {addr} failed: File not found. Processed in {end_time - start_time:.5f} seconds.")
    finally:
        client_socket.close()


serverAddress = '127.0.0.1'
serverPort = 8000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(1)
print("Server is listening on port 8000...")

while True:
    client_socket, addr = serverSocket.accept()
    print(f"Accepted connection from {addr}")

    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()
