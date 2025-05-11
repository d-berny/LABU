"""Local Automated Backup - private way to store data"""

import os
from paramiko import SSHClient, AutoAddPolicy
from rich import pretty, print as pwint # inspect
pretty.install()

mozzi = SSHClient()
known_hosts = os.path.expanduser(os.path.join("~", ".ssh", "known_hosts"))
mozzi.load_host_keys(known_hosts)
mozzi.load_system_host_keys()
mozzi.set_missing_host_key_policy(AutoAddPolicy())
mozzi.connect("ip_address", port="port_number", username="username")
# inspect(mozzi, methods=True)

cmd = input("Command: ")

stdin, stdout, stderr = mozzi.exec_command(cmd)

pwint(f"STDOUT: {stdout.read().decode('utf8')}")
pwint(f"Return code: {stdout.channel.recv_exit_status()}")
pwint(f"STDERR: {stderr.read().decode('utf8')}")

stdin.close()
stdout.close()
stderr.close()
mozzi.close()
