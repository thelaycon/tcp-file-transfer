# Simple TCP file transfer program

A simple TCP file transfer program to transfer files over a network.
Received files are saved under `./received` directory.



# Usage

Spining off a quick TCP server and Client is simple.

```
$ python tcp.py server

Listening at 127.0.0.1:1069 with header length of 40 characters
Receiving 4000 bytes at a time in buffer

```

```
$ python tcp.py client --path ~/user/files/art-of-war.pdf

$ Done
$

```

What's happening is simple. The server by default sets up a listening socket with `IPPROTO_TCP` protocol, which is ready to receive Stream data at **127.0.0.1:1069**. It also sets the length of the header which contains the filename and filesize to 40 characters. 
Except you are sending a **very large** file or a file whose name exceeds 40 characters, you might not really need to change the header size.

The server also reads **4000** bytes of data at a time into the buffer.
This is important because the traffic on the network may vary time to time. Increasing the size of the buffer using the `--buff` option will increase the speed of file transfer, but might leaded to some issues if the buffer becomes overwhelmed under large traffic.


# Specifying the path of file to transfer

Use the `--path` flag when calling the TCP client to specify the path of file to send.

```
$ python tcp.py client --path ~/user/files/art-of-war.pdf

$ Done
$

```

#Increasing the bytes size to read into Buffer

Using the `--buff` option to specify the size of bytes your server would be receiving at a time. Increasing the value leads to increase in file transfer speed.

```
$ python tcp.py server --buff 200000

Listening at 127.0.0.1:1069 with header length of 40 characters
Receiving 200000 bytes at a time in buffer

```

# Set Stream header length 

Just incase you are doing something wonderful that might make the length of **filename + filesize** be more than 40 characters, use the `--header` flag on **both** the TCP server and client


```
$ python tcp.py server --header 100

$ python tcp.py client --header 100 --path ~/user/files/art-of-war.pdf

```

# Full Help

Call the tcp.py with `-h` or `--help` flag.


```
$ python tcp.py -h

usage: tcp.py [-h] [--path PATH] [--port PORT] [--ip IP] [--header HEADER]
              [--buff BUFF]
              {server,client}

TCP server to send files over a network

positional arguments:
  {server,client}  Servrer or Client

optional arguments:
  -h, --help       show this help message and exit
  --path PATH      Path to file to send
  --port PORT      Port to listen to or connect to. Default:1069
  --ip IP          IP Address to listen to or connect to. Default:127.0.0.1
  --header HEADER  Header length: size + file_name. Default:40
  --buff BUFF      Buffer size for storing data

```

# Logging 

The program logs all sent and received files in `client.log` and `server.log` respectively.

```

$ ls
$ received tcp.py client.log server.log 

```


