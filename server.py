# Written by Kyle D. Franke for Yao Liu's CS 457
# Binghamton University, 2018

import threading
import thread
import socket as socket_library
from os.path import isfile, isdir, getmtime, getsize
from subprocess import check_output
from time import time
from wsgiref.handlers import format_date_time

access_map_lock = threading.Lock()
# hash map for access times
access_map = {}

def process(client_connection, client_address):
    request = client_connection.recv(1024)

    if not request:
        return

    # read the first part of the HTTP GET request
    request = request[:request.find('\n')]

    # requirement 4, part 1: parse resource request
    # parse the resource name
    resource_name = request[4:]
    resource_name = resource_name[:resource_name.find(' ')]

    # build pathname for search within www directory
    resource_path = "./www" + resource_name
    http_response = None

    # requirement 4, part 2: build HTTP response
    if isfile(resource_path):

        # requirement 5: if it's in the directory, prepare
        # a valid successful response
        http_response = "HTTP/1.1 200 OK\n"
        http_response += "Date: " + str(format_date_time(time())) + '\n'
        http_response += "Server: Kyle's Awesome HTTP Server\n"
        http_response += "Last-Modified: " + \
                         str(format_date_time(getmtime(resource_path))) + \
                         '\n'
        http_response += "Accept-Ranges: bytes\n"
        http_response += "Content-Length: " + str(getsize(resource_path)) \
                         + '\n'
        http_response += "Content-Type: " + \
                         check_output(["file", "--mime-type", "-b", \
                         resource_path]) + '\n'

        with open(resource_path[2:]) as fp:
            for line in fp:
                http_response += line

        # print four items to stdout (later requirement)
        # also, update the access times
        access_map_lock.acquire()
        if resource_name not in access_map:
            access_map[resource_name] = 0
        access_map[resource_name] += 1
        stdout_message = resource_name + '|' + client_address[0] + \
                         '|' + str(client_address[1]) + '|' + \
                         str(access_map[resource_name])
        access_map_lock.release()
        print stdout_message
    else:
        http_response = "HTTP/1.1 404 Not Found\n"

    client_connection.sendall(http_response)
    # requirement 6: close socket connection to client after answering
    client_connection.close()
    thread.exit()

def main():
    # initialize our socket
    server_socket = socket_library.socket(socket_library.AF_INET,
                                          socket_library.SOCK_STREAM)
    server_socket.setsockopt(socket_library.SOL_SOCKET,
                             socket_library.SO_REUSEADDR, 1)

    # bind it to port 0, which lets the OS
    # pick available port for us at random 
    server_socket.bind(('', 0))

    # requirement 1: print hostname and socket port
    # gethostname() is static, getsockname() is not
    print("Host name: " + str(socket_library.gethostname()) + \
          ".cs.binghamton.edu")
    print("Chose port #" + str(server_socket.getsockname()[1]) + \
          " for the HTTP server to listen on.")

    DIRECTORY = "./www"

    # requirement 2: look for www resource directory
    if isdir(DIRECTORY):
        print("www directory found.")
    else:
        print("www directory not found in this directory.")
        print("Please ensure the directory exists and try again.")
        return 1

    server_socket.listen(1)

    print("Listening for connections...")

    # requirement 3: repeatedly listen for requests
    while True:
        client_connection, client_address = server_socket.accept()

        thread.start_new_thread(process, (client_connection, client_address,))

    return 0


# execute main
if main():
    print("\n")
    print("Exited with non-zero return value. An error has occurred.")
