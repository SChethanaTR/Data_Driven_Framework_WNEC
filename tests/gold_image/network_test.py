import pytest
from helpers import ubuntu


@pytest.mark.gold_image
class TestNetwork:
    def test_hosts_file(self, ssh_host):
        """The file /etc/hosts should allow Docker to use host based networking"""
        hosts = ubuntu.execute_cmd_remote("cat /etc/hosts", ssh_host)

        assert (
            "127.0.0.1 localhost db" in hosts
        ), '"127.0.0.1 localhost db" was not found in the hosts file'
        assert "127.0.1.1 wne" in hosts, '"127.0.0.1 wne" was not found in the hosts file'

    def test_upgrader_ssh(self, ssh_host):
        """Upgrader user should have a defined .ssh directory/file"""

        assert ubuntu.is_folder_exist_remote(
            "/home/upgrader/.ssh", ssh_host
        ), "/home/upgrader/.ssh should exist"

    def test_http_external_connection(self, ssh_host):
        """The box should have access to external http servers. i.e: The internet"""
        status_code = ubuntu.execute_cmd_remote(
            'curl -is "https://www.reuters.com" | head -n 1', ssh_host
        ).split()[1]
        assert status_code == "200", "The box should have access to the internet"
