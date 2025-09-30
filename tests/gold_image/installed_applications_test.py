import pytest
from helpers import files
from helpers import ubuntu


@pytest.mark.gold_image
class TestApplications:
    @pytest.mark.parametrize("application", files.parametrize("gold_image:required_applications"))
    def test_if_installed(self, application, ssh_host):
        """Required executables should be present in the system"""
        application_path = ubuntu.execute_cmd_remote(f"which {application}", ssh_host)

        assert application_path, f"Application {application} path should be present"
        assert ubuntu.is_execute_cmd_successful_remote(
            f"[[ -x {application_path} ]]", ssh_host
        ), f"Application {application} should be installed"

    def test_microcode(self, ssh_host):
        """For security reasons, amd64-microcode (or intel microcode) package must be installed"""

        assert ubuntu.is_packege_installed("amd64-microcode", ssh_host)

    def test_sddm_conf(self, ssh_host):
        """The sddm file should be defined to avoid the upgrader showing in the login screen"""

        # The expected content of the file (in this case, more than one is acceptable)
        expected = (
            "[Users]\nRememberLastUser=false\nHideUsers=upgrader",
            "[Users]\nRememberLastUser=false\nHideUsers=upgrader\n\n[Autologin]\nUser=wneclient",
        )

        contents = ubuntu.execute_cmd_remote("cat /etc/sddm.conf", ssh_host)
        assert contents in expected, "The file /etc/sddm.conf is not right"

    def test_apt_local_repo(self, ssh_host):
        """
        Packages will be managed via a local APT repo, so it's necessary
        to verify the directory is listed in the apt sources
        """
        expected = "deb [trusted=yes] file:///opt/debs/bionic/wnec/ bionic main"
        reuters_repo = ubuntu.execute_cmd_remote(
            "cat /etc/apt/sources.list.d/reuters-repo.list", ssh_host
        )

        assert expected == reuters_repo


@pytest.mark.gold_image
class TestCron:
    # pylint: disable=too-few-public-methods
    def test_cron_files(self, ssh_host):
        """Required CRON should be present in the /etc/cron.d directory"""

        files_expected = [
            "anacron",
            "facter-stats",
            "popularity-contest",
            "wnec-stats",
            "setBMCardProfiles",
        ]

        for file in files_expected:
            assert ubuntu.is_file_exist_remote(f"/etc/cron.d/{file}", ssh_host)
