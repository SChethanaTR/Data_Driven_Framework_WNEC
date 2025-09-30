from pathlib import Path
import subprocess
from wait_for import wait_for
import paramiko


def is_packege_installed(package: str, ssh=None) -> bool:
    """Detects if a specific package is installed in the system
    Args:
        package (str): Package name
    Returns:
        bool: True if package installed else False
    """
    run_cmd = ["dpkg", "-s", package]
    if ssh:
        output = execute_cmd_remote(" ".join(run_cmd), ssh)
    else:
        output = subprocess.run(run_cmd, stdout=subprocess.PIPE, universal_newlines=True).stdout

    # Second line contains the install status
    return "installed" in output.split("\n")[1]


def is_service_active(service, ssh=None):
    """Validate Service is active
    Args:
        service (str): service name
    Returns:
        bool: True if service active else False
    """
    run_cmd = ["systemctl", "is-active", service]
    if ssh:
        output = ssh.exec_command(" ".join(run_cmd))[1].read().decode("utf-8")
    else:
        output = subprocess.run(run_cmd, stdout=subprocess.PIPE, universal_newlines=True).stdout
    return "active" in output


def is_service_enabled(service, ssh=None):
    """Validate Service is enabled
    Args:
        service (str): service name
    Returns:
        bool: True if service enabled else False
    """
    run_cmd = ["systemctl", "is-enabled", service]
    if ssh:
        output = ssh.exec_command(" ".join(run_cmd))[1].read().decode("utf-8")
    else:
        output = subprocess.run(run_cmd, stdout=subprocess.PIPE, universal_newlines=True).stdout
    return "enabled" in output


def up_docker_container(service_name, file_path, ssh=None, detached_mode=True, recreate=True):
    """Up Docker Compose File
    Args:
        service_name (str): service name
        file_path: absolute path of docker-compose.yaml to be run
        detached_mode: keep true to run docker container in background
        recreate: keep true to re-create docker from fresh image
    Returns:
        bool: True if docker container run successful else False
    """
    run_cmd = ["docker-compose", "-f", file_path, "-p", service_name, "up"]
    if detached_mode:
        run_cmd.append("-d")
    if recreate:
        run_cmd.append("--force-recreate")
    if not is_docker_container_up(service_name, ssh=ssh):
        if ssh:
            ssh.exec_command(" ".join(run_cmd))
        else:
            subprocess.run(run_cmd)
    return wait_for(
        is_docker_container_up,
        func_args=[service_name, ssh],
        fail_condition=False,
        timeout=120,
        delay=2.0,
    )


def down_docker_container(service_name, file_path, ssh=None):
    """Down Docker Compose File
    Args:
        service_name (str): service name
        file_path: abslute path of docker-compose.yaml to be run
    Returns:
        bool: True if docker container stop successful else False
    """
    run_cmd = ["docker-compose", "-f", file_path, "down"]
    if ssh:
        ssh.exec_command(" ".join(run_cmd))
    else:
        subprocess.run(run_cmd)
    return wait_for(
        is_docker_container_up,
        func_args=[service_name, ssh],
        fail_condition=True,
        timeout=120,
        delay=5.0,
    )


def is_docker_container_up(container_name, ssh=None):
    """Validate docker container is running
    Args:
        container_name (str): container name to be validated
    Returns:
        bool: True if container is running else False
    """
    # pylint: disable=unused-variable
    run_cmd = [
        "docker",
        "container",
        "ls",
        "--filter",
        f"name={container_name}",
        "--format",
        "{{.Status}}",
    ]
    if ssh:
        stdin, stdout, stderr = ssh.exec_command(" ".join(run_cmd))
        output = stdout.read().decode("utf-8")
    else:
        output = subprocess.run(run_cmd, stdout=subprocess.PIPE, universal_newlines=True).stdout
    return len(output) > 0 and output[:2] == "Up"


def ssh_connect(ip_address, username, password):
    """Connect to ubuntu machine vai ssh
    Args:
        ip_address (str): IP address of ubuntu machine to be connected
        username (str): Username of login user
        password (str): Password of login user
    Returns:
        SSHClient: Object of SSHClient class
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    return ssh


def copy_file_to_remote(src, dst, ssh, sftp=None):
    """Copy file to remote machine dst path from local srs path
    Args:
        src (str): Source file path
        dst (str): Destination file path
        ssh (str): Object of SSHClient class
    """
    file_name = dst.split("/")[-1]
    file_path = dst.replace(file_name, "")
    ssh.exec_command(f"mkdir -p {file_path}")
    if not sftp:
        sftp = ssh.open_sftp()
    sftp.put(src, dst)
    sftp.close()


def copy_file_from_remote(src, dst, ssh):
    """Copy file to remote machine dst path from local srs path
    Args:
        src (str): Source file path
        dst (str): Destination file path
        ssh (str): Object of SSHClient class
    """
    file_name = dst.split("/")[-1]
    file_path = dst.replace(file_name, "")
    Path(file_path).mkdir(parents=True, exist_ok=True)
    sftp = ssh.open_sftp()
    sftp.get(src, dst)
    sftp.close()


def setup_aws_cli(ssh_host, password=None):
    if not "aws" in execute_cmd_remote("which aws", ssh_host):
        print("Amazon CLI was not detected in the system")
        print("Downloading Amazon CLI")
        progress_res = execute_cmd_remote(
            "curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip",
            ssh_host,
        )
        print(progress_res)
        is_execute_cmd_successful_remote("unzip awscliv2.zip", ssh_host)
        is_execute_cmd_successful_remote(f"echo {password} | sudo -S ./aws/install", ssh_host)
        is_execute_cmd_successful_remote("rm -f awscliv2.zip", ssh_host)
        is_execute_cmd_successful_remote("rm -rf aws", ssh_host)

    # Check for boto and AWS configuration
    if not execute_cmd_remote("aws configure get aws_access_key_id", ssh_host):
        print("AWS Credentials are not set, please set them now")
        aws_id = input("Enter aws_access_key_id : ")
        aws_key = input("Enter aws_secret_access_key : ")
        is_execute_cmd_successful_remote("mkdir -p ~/.aws/", ssh_host)
        cmd = (
            f'echo "[default]\naws_access_key_id = {aws_id}\naws_secret_access_key '
            f'= {aws_key}" > ~/.aws/credentials'
        )
        assert is_execute_cmd_successful_remote(cmd, ssh_host), "Unable to save aws credentials"


def is_execute_cmd_successful_remote(run_cmd, ssh):
    return ssh.exec_command(run_cmd)[1].channel.recv_exit_status() == 0


def delete_file_remote(file_path, ssh):
    return ssh.exec_command(f"rm {file_path}")[1].channel.recv_exit_status() == 0


def create_folder_remote(folder_path, ssh):
    return ssh.exec_command(f"mkdir -p {folder_path}")[1].channel.recv_exit_status() == 0


def is_file_exist_remote(file_abs_path, ssh):
    is_file = ssh.exec_command(f'[[ -f "{file_abs_path}" ]]')[1].channel.recv_exit_status() == 0
    is_symlink = ssh.exec_command(f'[[ -L "{file_abs_path}" ]]')[1].channel.recv_exit_status() == 0
    return is_file and not is_symlink


def is_folder_exist_remote(folder_path, ssh):
    is_dir = ssh.exec_command(f'[[ -d "{folder_path}" ]]')[1].channel.recv_exit_status() == 0
    is_symlink = ssh.exec_command(f'[[ -L "{folder_path}" ]]')[1].channel.recv_exit_status() == 0
    return is_dir and not is_symlink


def get_owner_of_folder_remote(folder_path, ssh):
    return execute_cmd_remote(f"ls -ld {folder_path}", ssh).split()[2]


def execute_cmd_remote(run_cmd, ssh):
    # pylint: disable=unused-variable
    stdin, stdout, stderr = ssh.exec_command(run_cmd)
    stderr.read().decode("utf-8").strip()
    return stdout.read().decode("utf-8").strip()


def get_cmd_error_output_remote(run_cmd, ssh):
    return ssh.exec_command(run_cmd)[2].read().decode("utf-8").strip()
