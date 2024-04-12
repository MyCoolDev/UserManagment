import socket
import threading
import json
import datetime

import utils
import DataStructures.connections as connections
from DataStructures.connections import Connection

# list[connection]
live_connections = []

# connections with missed data like username
# for now it's only username
wait_list_connections = []

# server global vars
server = None

def main():
    global server
    try:
        # load the config from the config file
        config = utils.load_config("config/config.ini")

        # create the server socket
        server = socket.socket()

        IP = config["SOCKET"]["SERVER_ADDRESS"]
        PORT = int(config["SOCKET"]["SERVER_PORT"])

        server.bind((IP, PORT))
        server.listen(int(config["SOCKET"]["MAX_USERS"]))

        utils.server_print("The server is online on: " + IP + "/" + str(PORT))

        # load users into the server
        while True:
            client_socket, client_address = server.accept()
            con = Connection(client_address, client_socket)

            # check if there is a connection from the same computer
            # a multi connections from the same computer is not allow!
            if client_address in [c.data['address'] for c in live_connections] + [c.data['address'] for c in wait_list_connections]:
                client_socket.close()

            wait_list_connections.append(con)
            thread = threading.Thread(target=handle_client, args=[con])
            thread.start()

def handle_client():
    pass