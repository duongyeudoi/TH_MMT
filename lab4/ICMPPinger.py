from socket import *
import os
import sys
import struct
import time
import select

# Request type
ICMP_ECHO_REQUEST = 8

# Reqquest type code
ICMP_CODE = getprotobyname('icmp')


# Checksum of packet
def checksum(string):
    string = bytearray(string)
    c_sum = 0
    count_to = (len(string) // 2) * 2
    count = 0

    while count < count_to:
        thisVal = string[count - 1] * 256 + string[count]
        c_sum = c_sum + thisVal
        c_sum = c_sum & 0xffffffff
        count = count + 2

    if count_to < len(string):
        c_sum = c_sum + string[len(string) - 1]
        c_sum = c_sum & 0xffffffff

    c_sum = (c_sum >> 16) + (c_sum & 0xffff)
    c_sum = c_sum + (c_sum >> 16)
    answer = ~c_sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


# Receive the ping from the socket
def receive_one_ping(my_socket, ID, timeout):
    time_left = timeout

    while True:
        # Started time
        started_select = time.time()
        # Provide access to a channel
        ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select

        # Check if the channel is empty
        if ready[0] == []:
            return "Request timed out."

        time_received = time.time()
        # Receive data from my socket
        rec_packet, addr = my_socket.recvfrom(1024)
        # ICMP header: bytes from 20 to 28 of the first 160 bits
        icmp_header = rec_packet[20:28]
        # Convert ICMP header into decimal
        icmp_type, code, my_checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)

        if type != 8 and packet_ID == ID:
            bytes_in_double = struct.calcsize("d")
            # Get the sequence value in the reply
            time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]
            return time_received - time_sent

        time_left = time_left - how_long_in_select

        if time_left <= 0:
            return "Request timed out."


# Send a single ping to an end system
def send_one_ping(my_socket, dest_addr, ID):
    my_checksum = 0
    # Create a header to send over to the end system with a zero checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    data = struct.pack("d", time.time())
    # Get the checksum
    my_checksum = checksum(header + data)

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network
        my_checksum = htons(my_checksum) & 0xffff
    else:
        # Get from host to network
        my_checksum = htons(my_checksum)
    # Recreate the header
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))


# Return time taken to perform a ping to an address
def do_one_ping(dest_addr, timeout):
    # Create new socket
    try:
        my_socket = socket(AF_INET, SOCK_RAW, ICMP_CODE)
    except error:
        if error.errno == 1:
            print("Failed to create socket with the given destination")

    my_ID = os.getpid() & 0xffff

    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout)

    my_socket.close()

    return delay


def ping(host, timeout=1):
    dest = gethostbyname(host)
    print("Pinging " + dest)
    while True:
        delay = do_one_ping(dest, timeout)
        print(delay)
        time.sleep(1)
    return delay


ping("facebook.com")
