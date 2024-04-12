import socket
import threading
import json
import datetime

import utils
import DataStructures.connections as connections
from DataStructures.connections import Connection
# from DataBaseManagement import

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
    except Exception as e:
        utils.server_print(str(e))
    finally:
        print("Server is close!")

def handle_client(con: Connection):
    try:
        # send the client that the connection has been successful.
        # response (json) format: {event: '', data?: {}}
        con.connection.send(json.dumps({'event': 'connection_initialized'}).encode())
        utils.server_print("A new connection has been initialized, " + str(con.data))

        # for now, we assume that the user is automatically in the wait list.
        while True:
            # read the client request to the server.
            # request (json) format: {method: ('POST' || 'GET'), event: '', data: {}}
            request = json.loads(con.connection.recv(1024).decode())

            if not ('method' in request.keys() and 'event' in request.keys()):
                con.connection.send(json.dumps({'event': 'bad_formatting'}).encode())
                continue

            if (request['method'] == "POST") and not('data' in request.keys()):
                con.connection.send(json.dumps({'event': 'bad_formatting'}).encode())
                continue

            # take the current datetime immediately.
            time = datetime.datetime.now()

            if con.status == connections.Status.Wait:
                if request["method"] == 'POST':
                    if request["event"] == "login":
                        pass


    except:
        pass
    finally:
        pass