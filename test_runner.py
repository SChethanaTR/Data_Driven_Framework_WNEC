#!/bin/python3
# pylint: skip-file
from helpers import ubuntu
from plugins.aws_secrets import pytest_configure
import subprocess, os, sys

root_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
os.chdir(root_dir)
pytest_configure()

import env

os.environ["IP"] = env.ip
ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
ubuntu.setup_aws_cli(ssh, env.password)
ssh.close()

# Create temp Directory to save temporary file
if not os.path.exists(env.temp_dir):
    os.mkdir(env.temp_dir)


def main(argv):
    """WNE Client Backend automated tests run script"""
    command = [sys.executable, "-m", "pytest"]
    command += argv
    print(f'Command executed: > {" ".join(command)}')

    # Execute final compiled run command
    subprocess.run(command)


if "__main__" == __name__:
    main(sys.argv[1:])
