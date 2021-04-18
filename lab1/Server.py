# Import socket module
from socket import *

# Import IO module
import io

# Define server variables
host = ''  # Default local host
port = 9999  # Port number
size = 1024  # Buffer size
nCnt = 5  # Maximum number of queued connection


# Receive request from client and send response
def response():
    # Create a TCP server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Bind the socket to server address and server port
    serverSocket.bind((host, port))
    # Listen to nCnt connections at a time
    serverSocket.listen(nCnt)
    while True:
        print('Server is ready...')
        # Set up a new connection from the client
        connectionSocket, clientAddr = serverSocket.accept()
        # Receives the request message from the client
        message = connectionSocket.recv(size)
        print(message.decode('utf-8'), '::',
              message.split()[0].decode('utf-8'), ':',
              message.split()[1].decode('utf-8'))
        # Parse the request to determine the specific file being requested
        filename = message.split()[1]
        print(filename.decode('utf-8'), '||', filename[1:].decode('utf-8'))

        try:
            returnType = filename.decode('utf-8')[1:].split('.')[1]
            # Get the requested file from the server’s file system
            if returnType == 'txt' or returnType == 'html':
                buffer = io.open(filename[1:], "r", encoding="utf-8")
                data = buffer.read()
                # Create an HTTP response message consisting of the requested file preceded by header lines
                connectionSocket.send('\nHTTP/1.1 200 OK\n'.encode('utf-8'))
                # Set content type!!! which can display Chinese characters
                connectionSocket.send('Content-Type: text/html; charset=utf-8\n\n'.encode('utf-8'))
                data = data.encode('utf-8')

            elif returnType == 'jpg':
                buffer = io.open(filename[1:], "rb")
                data = buffer.read()
                connectionSocket.send('\nHTTP/1.1 200 OK\n'.encode('utf-8'))
                connectionSocket.send('Content-Type: image/jpg\n\n'.encode('utf-8'))

            elif returnType == 'mp3':
                buffer = io.open(filename[1:], "rb")
                data = buffer.read()
                connectionSocket.send('\nHTTP/1.1 200 OK\n'.encode('utf-8'))
                connectionSocket.send('Content-Type: audio/mp3\n\n'.encode('utf-8'))

            elif returnType == 'mp4':
                buffer = io.open(filename[1:], "rb")
                data = buffer.read()
                connectionSocket.send('\nHTTP/1.1 200 OK\n'.encode('utf-8'))
                connectionSocket.send('Content-Type: video/mp4\n\n'.encode('utf-8'))

            else:
                raise IndexError()

        except (IOError, IndexError):
            # If a browser requests a file that is not present in your server
            # Server return a “404 Not Found” error message
            buffer = io.open('404.html', "r", encoding="utf-8")
            data = buffer.read()
            connectionSocket.send('HTTP/1.1 404 not found\n\n'.encode('utf-8'))
            data = data.encode('utf-8')

        # Send the response over the TCP connection to the requesting browser
        connectionSocket.send(data)
        # Close the client connection socket
        connectionSocket.close()


response()
