import getpass
import json
import subprocess

USER = getpass.getuser()
HOME = "/home/%s/" % USER
BASHRC = HOME + ".bashrc"
ALIASES = HOME + ".bash_aliases"
I3CONF = HOME + "/.config/i3/config"
SAVE = HOME + "/.config/.vinrc/"

f = open("times.txt", "r")
r = json.loads(f.read())
f.close()
out = []
for e in r:
    if e[1] != str(subprocess.run(["stat", "-c %Y", e[0]], stdout=subprocess.PIPE).stdout)[3:-3]:
        subprocess.run(["cp", e[0].split("/")[-1], e[0]], stdout=subprocess.PIPE)
        out.append((e[0], str(subprocess.run(["stat", "-c %Y", e[0]], stdout=subprocess.PIPE).stdout)[3:-3]))
    else:
        out.append(e)

print(out)
f = open("times.txt", "w")
f.write(json.dumps(out))
f.close()