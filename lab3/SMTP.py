import base64
import ssl
from socket import *

msg = "\r\n I love computer networks!"
endMsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailServer
mailServer = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailServer
# Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailServer)
# Fill in end

recv1 = clientSocket.recv(1024).decode()
print("Output1: ", recv1)
if recv1[:3] != '220':
    print('220 reply not received from server.')
    exit()

# Send HELO command and print server response.
helloCommand = 'HELO quanghuy\r\n'
clientSocket.send(helloCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print("Output2:", recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
    exit()

tlsMsg = "starttls\r\n"
clientSocket.send(tlsMsg.encode())
recv3 = clientSocket.recv(1024).decode()
print("Output3: ",recv3)
if recv3[:3] != '220':
    print('Cannot start tls')
    exit()

wrappedSocket = ssl.wrap_socket(clientSocket,
                                ssl_version=ssl.PROTOCOL_SSLv23,)
while True:
    wrappedSocket.send("auth login\r\n".encode())
    print("Output4:", wrappedSocket.recv(1024).decode())

    account = input("account: ")
    wrappedSocket.send(base64.b64encode(account.encode())+'\r\n'.encode())
    print("Output5:", wrappedSocket.recv(1024).decode())

    password = input("password: ")
    wrappedSocket.send(base64.b64encode(password.encode())+'\r\n'.encode())
    recv6 = wrappedSocket.recv(1024).decode()
    print("Output6:", recv6)

    if recv6[:3] != '235':
        print("Failed to log in, please try again")
    else:
        break

# Send MAIL FROM command and print server response.
# Fill in start
mailFromMsg = "MAIL FROM: <"+account+">\r\n"
wrappedSocket.send(mailFromMsg.encode())
print("Output7:", wrappedSocket.recv(1024).decode())
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
while True:
    rcptMailAccount = input("ToMail:")
    rcptToMsg = "RCPT to: <"+rcptMailAccount+">\r\n"
    wrappedSocket.send(rcptToMsg.encode())
    recv8 = wrappedSocket.recv(1024).decode()
    print("Output8:", recv8)
    if recv8[:3] != '250':
        print("Invalid mailbox, please try again")
    else:
        break

# Fill in end

# Send DATA command and print server response.
# Fill in start
dataMsg = "DATA\r\n"
wrappedSocket.send(dataMsg.encode())
print("Output9:", wrappedSocket.recv(1024).decode())
# Fill in end

# Send message data.
# Fill in start
subject = input("Subject:")
wrappedSocket.send(("Subject: "+subject+"\r\n").encode())
wrappedSocket.send(("From: "+account+"\r\n").encode())
wrappedSocket.send(("To: "+rcptMailAccount+"\r\n").encode())
print("PLEASE ENTER MESSAGE")
while True:
    message = input()
    if message == "END":
        break
    wrappedSocket.send((message+"\n").encode())
# Fill in end

# Message ends with a single period.
# Fill in start
wrappedSocket.send("\r\n.\r\n".encode())
print("Output10:", wrappedSocket.recv(1024).decode())
# Fill in end

# Send QUIT command and get server response.
# Fill in start
wrappedSocket.send("QUIT\r\n".encode())
print("Output11:", wrappedSocket.recv(1024).decode())
# Fill in end
