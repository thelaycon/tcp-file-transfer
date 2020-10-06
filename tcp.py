import threading
import os
import argparse
import socket
from datetime import datetime
from tqdm import tqdm



def recvfull(sock, bufSize, msg_len, desc):
    msg = b""
    loop = tqdm(range(msg_len), unit="bits", unit_divisor=4000,desc=desc)
    while len(msg) < msg_len:
        data = sock.recv(bufSize)
        loop.update(len(data))
        if not data:
            break
        msg += data
    loop.close()
    return msg


def writeData(sc, name, msg):
    with open("received/"+name, "wb") as f:
        f.write(msg)
        sc.sendall("Done".encode())
        sc.close()
        print("Received {} \n ".format(name))

def readWriteData(sc, name, buffSize, length):
    #Read Data
    msg = recvfull(sc, buffSize, length, "Receiving {}".format(name))

    #Write data
    writeData(sc, name, msg)
    
    #log file
    with open('server.log', 'a') as f:
        f.write("{0}: Received {1}\n".format(datetime.now(), name))



def server(ip, port, headerLength, buffSize):
    """TCP Server function """

    #Create directory to receive files if not existing
    if not os.path.isdir("received"):
        os.mkdir("received")

    #Create server log file
    if not os.path.isfile('server.log'):
        open('server.log', 'a').close()

    #Create Stream socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((ip, port))
    sock.listen(1)

    print("Listening at {0} with header length of {1} characters\nReceiving {2} bytes at a time in buffer\n".format(ip+":"+str(port), headerLength, buffSize))

    while True:
        #Accept new connections
        sc, addr = sock.accept()

        print("Accepted connection from {}".format(addr))


        #Read data header
        length, name = recvfull(sc, 20, headerLength, "Fetching headers").decode("ascii").split(":")
        length = int(length)
        name = name.strip()

        #Read and Write data
        thread = threading.Thread(target=readWriteData, args=(sc, name, buffSize, length), daemon=True)
        thread.start()


def client(ip, port, size, name, path, headerLength):
    '''TCP Client'''

    #Create client log file
    if not os.path.isfile('client.log'):
        open('client.log', 'a').close()

    #Set Header
    header = size + b":" + name
    header = header + b" "*(headerLength-len(header))
    
    if len(header) > headerLength:
        raise ValueError("Content length too short")

    #Set message
    with open(path, "rb") as f:
        msg = f.read()
        msg = header +  msg
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(msg)
    
    #log file
    with open("client.log", "a") as f:
        f.write("{0}: Sent {1}\n".format(datetime.now(), name.decode())) 
    resp = sock.recv(1024)
    print(resp.decode())
    sock.close()


choices = {"server":server, "client":client,}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TCP server to send files over a network")
    parser.add_argument("role", help="Servrer or Client", choices=choices)
    parser.add_argument("--path", help="Path to file to send", type=str)
    parser.add_argument("--port", help="Port to listen to or connect to. Default:1069", default=1069, type=int)
    parser.add_argument("--ip", help="IP Address to listen to or connect to. Default:127.0.0.1", default="127.0.0.1", type=str)
    parser.add_argument("--header", help="Header length: size + file_name. Default:40", default=40, type=int)
    parser.add_argument("--buff", help="Buffer size for storing data", type=int, default=4000)

    # Parse arguments

    args = parser.parse_args()
    func = choices[args.role]
    if args.role == "server":
        func(args.ip, args.port, args.header, args.buff)
    elif args.role == "client":
        if not args.path:
            raise ValueError("Please specify file path with --path option")
        size = str(os.path.getsize(args.path))
        name = os.path.basename(args.path)
        func(args.ip, args.port,size.encode(), name.encode(), args.path, args.header)


