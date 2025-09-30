import yaml
import pytest
from helpers import files
from helpers import ubuntu
import env


@pytest.mark.gold_image
class TestDocker:
    def setup_class(self):
        # pylint: disable=attribute-defined-outside-init
        self.docker_compose = {"images": [], "names": []}
        ssh = ubuntu.ssh_connect(env.ip, env.username, env.password)
        ubuntu.copy_file_from_remote(
            "/wneclient/compose/docker-compose.yml", "./temp/docker_test.yml", ssh
        )
        # Get all defined images and names from the docker-compose file
        with open("./temp/docker_test.yml") as file:
            docker_config = yaml.load(file, Loader=yaml.FullLoader)

            for _, container in docker_config["services"].items():
                self.docker_compose["images"].append(container["image"])
                self.docker_compose["names"].append(container["container_name"])

        # Get all images present as returned by Docker itself
        command = ssh.exec_command("docker images")[1].read().decode("utf-8").strip()

        self.docker_images = command.split("\n")

    def test_systemd_and_executable(self, ssh_host):
        """
        Docker-compose should be present in the systemd service directory
        and its executable should be in the local bin
        """

        files_list = [
            "/etc/systemd/system/docker-compose-app.service",
            "/usr/local/bin/docker-compose",
        ]

        for path in files_list:
            ubuntu.is_file_exist_remote(path, ssh_host)

    def test_is_enabled_and_active(self, ssh_host):
        """Docker should be enabled and active in the init system"""
        # Note: There's no need to test if Docker is enabled because
        # this is handled by docker-compose
        # If Docker is not active that means it's not running
        assert ubuntu.is_service_active(
            "docker", ssh_host
        ), "Docker should be active in systemd (systemctl start docker)"

    def test_compose_is_enabled_and_active(self, ssh_host):
        """Docker-compose should be enabled and active in the init system"""

        # If Docker-compose is not active that means its not running
        assert ubuntu.is_service_active(
            "docker-compose-app", ssh_host
        ), "Docker-compose should be active in systemd (systemctl start docker-compose-app)"
        # If Docker-compose is not enabled that means that when the computer reboots
        # it won't run on its own
        assert ubuntu.is_service_enabled(
            "docker-compose-app", ssh_host
        ), "Docker-compose should be enabled in systemd (systemctl enable docker-compose-app)"

    @pytest.mark.parametrize("required", files.parametrize("gold_image:required_docker_images"))
    def test_images_are_present(self, required):
        """Docker should have all required images present after installation"""

        found = False

        for line in self.docker_images:
            if required in line:
                found = True
                break

        assert found, f'Required docker image "{required}" was not found'

    def test_docker_compose_config(self, ssh_host):
        """
        The Docker-Compose configuration file should be provided
        and match the versions of container images installed
        """

        config_file_path = [
            "/wneclient/compose/docker-compose.yml",
            "/wneclient/compose/..env",
        ]
        assert all(
            ubuntu.is_file_exist_remote(file_path, ssh_host) for file_path in config_file_path
        )

    def test_images_versions(self, ssh_host):
        """
        Compares the images listed in the docker-compose file with the images
        loaded in Docker.
        """

        for version in self.docker_compose["images"]:
            found = ubuntu.execute_cmd_remote(f"docker images {version} -q", ssh_host)

            # The version in compose should be returned by Docker, any return is considered valid
            assert len(found) > 0, f"expected image {version} is not loaded in docker"

    def test_docker_compose_env(self, ssh_host):
        """Docker compose ..env file should match with the expected content"""

        expected = (
            "CONTAINER_USER=1000:1000\nCOMPOSE_PROJECT_NAME=wneclient\nCOMPOSE_COMPATIBILITY=true"
        )
        environment = ubuntu.execute_cmd_remote("cat /wneclient/compose/..env", ssh_host)

        assert (
            expected == environment.strip()
        ), "Docker-compose ..env file does not have the expected content"

    def test_docker_ps(self, ssh_host):
        """
        Compares the images listed in the docker-compose with the containers
        that are up and running, they should match.
        """

        # docker ps and docker container ls are the exact same thing,
        # but it is encouraged to use the latter
        # https://www.docker.com/blog/whats-new-in-docker-1-13/

        for name in self.docker_compose["names"]:
            # Sqitch is not a mandatory running service
            if name != "sqitch":
                output = ubuntu.execute_cmd_remote(
                    f"docker container ls --filter name={name} --format {{{{.Status}}}}",
                    ssh_host,
                )
                assert len(output) > 0, f"Container {name} should be running"
                assert output[:2] == "Up", f"Container {name} should be running"
