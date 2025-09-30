from datetime import datetime
import pytest
from helpers import files
from helpers import ubuntu
import env


@pytest.mark.gold_image
class TestSystem:
    def test_os_version(self, ssh_host):
        """The OS should be Ubuntu 18.04 with buster debian version"""

        os = ubuntu.execute_cmd_remote('cat /etc/os-release | grep "PRETTY_NAME"', ssh_host)
        assert env.os_version in os, f"OS should be {env.os_version} and not {os}"
        assert "buster/sid" in ssh_host.exec_command("cat /etc/debian_version")[1].read().decode(
            "utf-8"
        ), "Debian version should be buster"

    @pytest.mark.parametrize(
        "required_partition", files.parametrize("gold_image:required_disk_partitions")
    )
    def test_disk_partitions(self, required_partition, ssh_host):
        """Disk partitions should be present and have the required format"""
        mountpoint = ubuntu.execute_cmd_remote(
            f'mount -l | grep "{required_partition["mountpoint"]} "', ssh_host
        )
        assert mountpoint, f'Could not find required partition "{required_partition["mountpoint"]}"'
        assert mountpoint.split()[4] == required_partition["fstype"]

    @pytest.mark.parametrize("path", files.parametrize("gold_image:required_directories"))
    def test_directories(self, path, ssh_host):
        """All required directories and their structures should be present"""
        res = ubuntu.is_folder_exist_remote(path, ssh_host)
        assert res, f'Directory "{path}" should exist'

    @pytest.mark.parametrize("expected", files.parametrize("gold_image:directory_ownership"))
    def test_directory_ownership(self, expected, ssh_host):
        """Key directories that should have the correct owner"""

        res = ubuntu.get_owner_of_folder_remote(expected["directory"], ssh_host)

        assert res == expected["owner"], (
            f'Directory {expected["directory"]} should be owned by '
            f'"{expected["owner"]}" and not by "{res}"'
        )

    def test_hostname(self, ssh_host):
        """The reported hostname should be wneclient"""
        assert ubuntu.execute_cmd_remote("hostname", ssh_host) == env.host_name
        assert ubuntu.execute_cmd_remote("cat /etc/hostname", ssh_host) == env.host_name
        assert ubuntu.execute_cmd_remote("cat /proc/sys/kernel/hostname", ssh_host) == env.host_name

    def test_utc_date(self, ssh_host):
        """The date of the system should be in UTC by default"""
        # https://jira.thomsonreuters.com/browse/WNEC-6205
        res = ubuntu.execute_cmd_remote(' date +"%Y-%m-%d %H:%M"', ssh_host)
        assert res == datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "System date should be in UTC"

    def test_image_version(self, ssh_host):
        """Gold image should be the latest version"""
        # https://jira.thomsonreuters.com/browse/WNEC-6217
        version = ubuntu.execute_cmd_remote("cat /wneclient/.version", ssh_host)
        assert (
            version == env.gi_version
        ), f'Gold Image version should be the latest: "{env.gi_version}" not "{version}"'


@pytest.mark.gold_image
class TestSystemUsers:
    def test_users(self, ssh_host):
        """Two users are mandatory, wnecadmin and upgrader.

        wnecadmin: This is the only user that should allow interactive login to the box.
        The intent is that this user will have all the privilege needed to 'administer' the box.

        upgrader: This is not an interactive user (i.e. you cannot 'log in' as upgrader).
        This user will be assumed by the upgrader container to perform package installs & rollbacks

        Note: This system uses the shadow password system.
        On those unices the pw_passwd field only contains an asterisk ('*') or the letter 'x',
        where the encrypted password is stored in a file /etc/shadow which is not world readable.
        Whether the pw_passwd field contains anything useful is system-dependent.
        """

        wnecadmin = ubuntu.execute_cmd_remote('getent passwd "wnecadmin"', ssh_host).split(":")
        upgrader = ubuntu.execute_cmd_remote('getent passwd "upgrader"', ssh_host).split(":")

        assert "x" == wnecadmin[1]
        assert "x" == wnecadmin[1]

        assert "1000" == wnecadmin[2]
        assert "1001" == upgrader[2]

        assert "1000" == wnecadmin[3]
        assert "1001" == upgrader[3]

        # >>> import spwd
        # >>> spwd.getspnam('wnecadmin')
        # TODO: gets shadow password, but it requires running as root

    def test_user_groups(self, ssh_host):
        """The main user (wnecadmin) should be in the Docker group"""
        # User should be in the docker group
        members = ubuntu.execute_cmd_remote("getent group docker", ssh_host).split(":")[3]
        assert "wnecadmin" in members

    def test_upgrader_group(self, ssh_host):
        """The user group 'upgrader' should have been created"""
        # Group upgrader should be present
        assert ubuntu.execute_cmd_remote("getent group upgrader", ssh_host)

    def test_upgrader_is_sudoer(self, ssh_host):
        """The 'upgrader' user should be in the sudoers permission list"""
        assert ubuntu.is_file_exist_remote("/etc/sudoers.d/upgrader", ssh_host)
