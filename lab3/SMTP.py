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

recv = clientSocket.recv(1024).decode()
print("Output1: ", recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
helloCommand = 'HELO gmail\r\n'
clientSocket.send(helloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print("Output2:", recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')




# Send MAIL FROM command and print server response.
# Fill in start
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
# Fill in end

# Send DATA command and print server response.
# Fill in start
# Fill in end

# Send message data.
# Fill in start
# Fill in end

# Message ends with a single period.
# Fill in start
# Fill in end

# Send QUIT command and get server response.
# Fill in start
# Fill in end
