import os
from helpers import files, ubuntu
from helpers.api import API
from testdata.FileDistribution import distribution_process as dp
import env


class FileDistributor:
    DISTRIBUTION_PROTOCOL = ["ftp", "ftps", "sftp"]
    DISTRIBUTION_STATUS_MAP = {"stop": 0, "start": 1, "pause": 2, "resume": 1}
    payload_map = {
        "ftp": dp.ftp_distribution_payload,
        "ftps": dp.ftps_distribution_payload,
        "sftp": dp.sftp_distribution_payload,
        "smb23": dp.smb_distribution_payload,
    }

    def create_server(self, protocol, directory="/testAuto"):
        protocol = protocol.lower()
        publichost = env.ftp_host if protocol == "ftp" else env.ftps_host
        ssh = ubuntu.ssh_connect(publichost, env.username, env.password)
        is_server_running = ubuntu.is_docker_container_up(protocol, ssh=ssh)
        if protocol == "sftp":
            directory = (
                f"/wneclient/data/QA/sftp{directory}"
                if not directory.startswith("/wneclient/data/QA/sftp")
                else directory
            )
            ubuntu.create_folder_remote(directory, ssh)
            is_server_running = ubuntu.is_execute_cmd_successful_remote("uptime", ssh)
        if not is_server_running:
            file = f"testdata/FileDistribution/{protocol}_distribution.yml"
            env_key_path = f"services.{protocol}_server.environment"
            files.update_yml_file(
                file,
                env_key_path,
                publichost=publichost,
                ftp_user_name=env.dist_username,
                ftp_user_pass=env.dist_password,
            )
            ssh.exec_command(f"mkdir -p /wneclient/data/QA/{protocol}")
            file_src = "temp/docker-compose.yaml"
            file_dest = f"/wneclient/data/QA/{protocol}/docker-compose.yaml"
            ubuntu.copy_file_to_remote(file_src, file_dest, ssh)
            os.remove(file_src)
            is_server_running = ubuntu.up_docker_container(protocol, file_dest, ssh=ssh)
        ssh.close()
        assert is_server_running

    def create_distribution_process(self, protocol, **kwarg):
        protocol = protocol.lower()
        distribution_host = env.ftps_host if protocol == "ftps" else env.ftp_host
        payload = dict(self.payload_map[protocol])
        if protocol != "SMB23":
            payload["uri"] = distribution_host

        if protocol == "sftp":
            payload["username"] = env.username
            payload["password"] = env.password
        elif protocol == "SMB23":
            payload["username"] = env.smb_username
            payload["password"] = env.smb_password
        else:
            payload["username"] = env.dist_username
            payload["password"] = env.dist_password
        for k, v in kwarg.items():
            payload[k] = v
        if protocol == "SMB23":
            return API().post(f"{env.api_url}/distributionprocesses", payload)
        else:
            return API().post("/distributionprocesses", payload)

    def remove_all_disribution_process(self):
        response, status = API().get("/distributionprocesses")
        assert status == 200, "Unable to get distribution processes list"
        for process in response:
            API().delete(f'/distributionprocesses/{process["id"]}')

    def get_distribution_path(self, protocol, filename):
        return f"{dp.distribution_base_directory[protocol]}/testAuto/{filename}"
