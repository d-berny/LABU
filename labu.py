"""Local Automated Backup - private way to store data"""

import os
from paramiko import SSHClient, AutoAddPolicy
from rich import pretty, print as pwint
pretty.install()

# from rich import inspect
# inspect(mozzi, methods=True)

def connect():
    """Connects to Mozzi"""

    known_hosts = os.path.expanduser(os.path.join("~", ".ssh", "known_hosts"))
    mozzi.load_host_keys(known_hosts)
    mozzi.load_system_host_keys()
    mozzi.set_missing_host_key_policy(AutoAddPolicy())
    mozzi.connect("IP",port="PORT",username="USERNAME",key_filename="PUB_KEY")

def pass_cmd():
    """Execute passed commands on Mozzi"""

    cmd = input("Command: ")
    stdin, stdout, stderr = mozzi.exec_command(cmd)

    pwint(f"STDOUT: {stdout.read().decode('utf8')}")
    pwint(f"Return code: {stdout.channel.recv_exit_status()}")
    pwint(f"STDERR: {stderr.read().decode('utf8')}")

    stdin.close()
    stdout.close()
    stderr.close()

def back_up(local_dir, remote_dir):
    """Back up to Mozzi"""

    try:
        sftp.mkdir(remote_dir)
    except IOError:
        pass

    for item in os.listdir(local_dir):
        local_item = os.path.join(local_dir, item)
        remote_item = os.path.join(remote_dir, item)
        if os.path.isdir(local_item):
            back_up(local_item, remote_item)
        else:
            sftp.put(local_item, remote_item)
            print(f"Uploaded: {local_item} → {remote_item}")

mozzi = SSHClient()
connect()
sftp = mozzi.open_sftp()


LOCAL_PATH = "/home/berny/Documents/Private"
REMOTE_PATH = "/home/meow/LABU_Gaia_Private"


back_up(LOCAL_PATH, REMOTE_PATH)
# pass_cmd()


sftp.close()
mozzi.close()

# Issue: no sync, just addition!
