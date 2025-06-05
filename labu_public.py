"""Local Automated Backup - private way to store data"""

import os
from paramiko import SSHClient, AutoAddPolicy
from rich import pretty, print as pwint
pretty.install()

# MOZZI'S RICH METHODS:
# from rich import inspect
# inspect(mozzi, methods=True)

class Mozzi():
    """server-side methods"""

    @staticmethod
    def connect():
        """Connects to Mozzi"""
        known_hosts = os.path.expanduser(os.path.join("~", ".ssh", "known_hosts"))
        mozzi.load_host_keys(known_hosts)
        mozzi.load_system_host_keys()
        mozzi.set_missing_host_key_policy(AutoAddPolicy())
        mozzi.connect("IP",port=0000,username="USERNAME",
            key_filename="PUB_KEY_LOC") # set!

    @staticmethod
    def remote_cmd(cmd):
        """Execute passed commands on Mozzi"""
        stdin, stdout, stderr = mozzi.exec_command(cmd)

        # CMD LOG:
        # pwint(f"STDOUT: {stdout.read().decode('utf8')}")
        # pwint(f"Return code: {stdout.channel.recv_exit_status()}")
        # pwint(f"STDERR: {stderr.read().decode('utf8')}")

        stdin.close()
        stdout.close()
        stderr.close()

    @staticmethod
    def back_up(local_dir, remote_dir):
        """Back up to Mozzi"""
        # makes the dir
        try:
            sftp.mkdir(remote_dir)
        except IOError:
            pass

        # copies all items from local to remote
        for item in os.listdir(local_dir):
            local_item = os.path.join(local_dir, item)
            remote_item = os.path.join(remote_dir, item)
            if os.path.isdir(local_item):
                Mozzi.back_up(local_item, remote_item)
            else:
                sftp.put(local_item, remote_item)
                pwint(f"Uploaded: {local_item} → {remote_item}")

    @staticmethod
    def move(dir_new, dir_old):
        """Move files from remote 'new' -> remote 'old' folder"""
        # makes the dir
        try:
            sftp.mkdir(dir_old)
        except IOError:
            pass

        # moves all items from new to old dir
        for item in sftp.listdir(dir_new):
            new_item = f"{dir_new}/{item}"
            old_item = f"{dir_old}/{item}"
            sftp.rename(new_item, old_item)
            pwint(f"Moved: {new_item} → {old_item}")
        # remote_cmd(f"mv {dir_new}* {dir_old}")

    @staticmethod
    def empty(remote_dir):
        """Empty remote dir"""
        # executes remote shell cmd
        Mozzi.remote_cmd(f"rm -rf {remote_dir}")
        # re-makes the dir
        sftp.mkdir(remote_dir)
        pwint(f"Emptied {remote_dir}")

mozzi = SSHClient()
Mozzi.connect()
sftp = mozzi.open_sftp()

LOCAL_PATH = "/home/berny/Private"
REMOTE_PATH_OLD = "/home/meow/LABU_Gaia_Private_OLD"
REMOTE_PATH_NEW = "/home/meow/LABU_Gaia_Private_NEW"

try:
    sftp.mkdir(REMOTE_PATH_NEW)
    sftp.mkdir(REMOTE_PATH_OLD)
except OSError:
    pass

if not sftp.listdir(REMOTE_PATH_NEW): # dir_new is empty
    Mozzi.back_up(LOCAL_PATH, REMOTE_PATH_NEW)

elif not sftp.listdir(REMOTE_PATH_OLD): # dir_old is empty
    Mozzi.move(REMOTE_PATH_NEW, REMOTE_PATH_OLD) # new -> old
    Mozzi.back_up(LOCAL_PATH, REMOTE_PATH_NEW)

elif sftp.listdir(REMOTE_PATH_NEW) and sftp.listdir(REMOTE_PATH_OLD): # dir_old & dir_new are full
    Mozzi.empty(REMOTE_PATH_OLD) # empty dir_old
    Mozzi.move(REMOTE_PATH_NEW, REMOTE_PATH_OLD) # dir_new -> dir_old
    Mozzi.back_up(LOCAL_PATH, REMOTE_PATH_NEW)

sftp.close()
mozzi.close()
