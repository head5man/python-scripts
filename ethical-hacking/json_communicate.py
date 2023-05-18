import json
import socket

def send(connection, data):
    json_data = json.dumps(data).encode("utf-8")
    connection.send(json_data)

def receive(connection):
    json_data = ""
    while True:
        try:
            json_data = json_data + connection.recv(1024).decode("utf-8")
            return json.loads(json_data)
        except ValueError:
            continue