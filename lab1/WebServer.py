from socket import *
import sys
import io

host = ''
port = 8898
bufferSize = 1024
backLog = 10

serverSocket = socket(AF_INET, SOCK_STREAM)

address = (host, port)

serverSocket.bind(address)

serverSocket.listen(backLog)

print('hnd\'s server is now listening on port %s' % port)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(bufferSize)
        filename = message.split()[1]
        print(filename[1:].decode('utf-8'))

        returnType = filename.decode('utf-8')[1:].split('.')[1]

        if(returnType == 'txt'):
            buffer = io.open(filename[1:], "r", encoding='utf-8')
            data = buffer.read()

            connectionSocket.send('\nHTTP/1.1 200 OK\n\r'.encode('utf-8'))
            connectionSocket.send('Content-Type: text/html; charset=utf-8\,\n\r\n\r'.encode('utf-8'))
            connectionSocket.send(data.encode('utf-8'))
            connectionSocket.close()

        elif (returnType == 'html'):
            buffer = io.open(filename[1:], "r", encoding='utf-8')
            data = buffer.read()

            connectionSocket.send('\HTTP/1.1 200 OK\n\r'.encode('utf-8'))
            connectionSocket.send('Content-Type: text/html; charset=utf-8\,\n\r\n\r'.encode('utf-8'))
            connectionSocket.send(data.encode('utf-8'))
            connectionSocket.close()

        elif(returnType == 'jpg'):
            buffer = io.open(filename[1:], "rb")
            data = buffer.read()

            connectionSocket.send('\nHTTP/1.1 200 OK\n\r'.encode('utf-8'))
            connectionSocket.send('Content-Type: imge/jpg\n\r\n\r'.encode('utf-8'))
            connectionSocket.send(data)
            connectionSocket.close()

        elif (returnType == 'mp3'):
            buffer = io.open(filename[1:], "rb")
            data = buffer.read()

            connectionSocket.send('\nHTTP/1.1 200 OK\n\r'.encode('utf-8'))
            connectionSocket.send('Content-Type: audio/mp3\n\r\n\r'.encode('utf-8'))
            connectionSocket.send(data)
            connectionSocket.close()

        elif (returnType == 'mp4'):
            buffer = io.open(filename[1:], "rb")
            data = buffer.read()

            connectionSocket.send('\nHTTP/1.1 200 OK\n\r'.encode('utf-8'))
            connectionSocket.send('Content-Type: video/mp4\n\r\n\r'.encode('utf-8'))
            connectionSocket.send(data)
            connectionSocket.close()
        else:
            raise IndexError()

    except(IOError, IndexError):
        buffer = io.open('404.html', "r", encoding='utf-8')
        data = buffer.read()
        connectionSocket.send('\HTTP/1.1 404 not found\n\r'.encode('utf-8'))
        connectionSocket.send(data.encode('utf-8'))
        connectionSocket.close()


