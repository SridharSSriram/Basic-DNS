import threading
import time
import random
import socket as mysoc

def server():
    # setting up the socket to begin connections
    # .AF_INET refers to the address family (AF_INET6 or AF_UNIX)
    try:
        server_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # AF_INET address has to be a tuple
    server_binding = ('', 40007)
    server_socket.bind(server_binding)
    server_socket.listen(1)

    host = "grep.cs.rutgers.edu"
    print("[S]: Server host name is: ", host)

    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)

    clientsockid, addr = server_socket.accept()

    DNS_map = create_DNS_map()

    # continually accepts connections until the end of file is reached, then breaks out of loop
    while True:
        received_hostname = clientsockid.recv(100).decode('utf-8')
        if received_hostname is "PROJ1-HNS.txt EOF reached":
            break

        returned_tuple = []
        if DNS_map.get(received_hostname) is None:
            # generates the string "<hostname> - NS"
            returned_tuple.append(received_hostname)
            returned_tuple.append("-")
            returned_tuple.append("Error:HOST NOT FOUND")
        else:
            # generates the string "<hostname> <IP> <flag>"
            returned_tuple.append(received_hostname)
            returned_tuple.append(DNS_map[received_hostname][0])
            returned_tuple.append(DNS_map[received_hostname][1])

        returned_string = " ".join(returned_tuple)
        clientsockid.send(returned_string.encode('utf-8'))

        # Close the server socket
    server_socket.close()
    exit()


def create_DNS_map():
    TS_DNS_map = dict()
    with open("PROJ1-DNSTS.txt") as ts_map:
        for line in ts_map:
            # runs .rstrip() to remove trailing and leading whitespace
            string_read_from_file = line.rstrip()
            # test for empty strings
            if not string_read_from_file:
                continue
            # generating tuple from file line
            tuple = line.split()
            # key in map is the hostname
            key_hostname = tuple[0]
            # value in map is tuple of ip address and flag
            value_ip_flag = tuple[1::]

            TS_DNS_map[key_hostname] = value_ip_flag

    return TS_DNS_map


ts = threading.Thread(name='tsserver', target=server)
ts.start()
time.sleep(random.random() * 5)

input("Hit ENTER  to exit")

exit()