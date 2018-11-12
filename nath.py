import threading
import socket as mysoc


def client():
    # setting up the RS socket
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client RS socket created\n")
    except mysoc.error as err:
        print('{} \n'.format("RS socket open error ", err))

    host = "ilab1.cs.rutgers.edu"
    print("[S]: Server host name is: ", host)
    rs_ip_addr = mysoc.gethostbyname(host)
    rs_server_binding = (rs_ip_addr, 55555)
    rs_socket.connect(rs_server_binding)

    # setting up the TS socket
    try:
        ts_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client TS socket created\n")
    except mysoc.error as err:
        print('{} \n'.format("TS socket open error ", err))

    # creating the file descriptor
    written_file = open("RESOLVED.txt","a")

    with open("PROJ1-HNS.txt") as hostname_file:
        for line in hostname_file:
            # runs .rstrip() to remove trailing and leading whitespace
            hostname = line.rstrip()

            # test for empty strings
            if not hostname:
                continue
            rs_socket.send(hostname.encode('utf-8'))

            # received RS message
            rs_response = rs_socket.recv(100)
            rs_tuple = rs_response.decode('utf-8').split()

            if rs_tuple[0] == hostname:
                if rs_tuple[2] == "A":
                    written_file.write(rs_response.decode('utf-8'))
                    written_file.write("\n")
            else:
                if rs_tuple[2] == "NS":
                    # if ts_socket already connected, then continue otherwise initiate connection
                    try:
                        ts_socket.send(hostname.encode('utf-8'))
                    except:
                        ts_ip_addr = mysoc.gethostbyname(rs_tuple[0])
                        ts_server_binding = (ts_ip_addr, 41414)
                        ts_socket.connect(ts_server_binding)
                        ts_socket.send(hostname.encode('utf-8'))

                    ts_response = ts_socket.recv(100)

                    written_file.write(ts_response.decode('utf-8'))
                    written_file.write("\n")

    # final signal indicating the transaction is over
    rs_socket.send("PROJ1-HNS.txt EOF reached".encode('utf-8'))
    rs_socket.close()
    ts_socket.close()
    exit()


t2 = threading.Thread(name='client', target=client)
t2.start()

input("Hit ENTER  to exit\n")

exit()


