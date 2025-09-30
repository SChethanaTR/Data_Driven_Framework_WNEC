import pytest
from helpers import ubuntu


@pytest.mark.gold_image
class TestBlackMagic:
    """
    Tests related to the hardware installed device by BlackMagic.
    I don't believe in witchcraft, but in this specific case we
    need to make sure that blackmagic is present
    """

    def test_packages(self, ssh_host):
        """The system must have 'desktopvideo' and 'mediaexpress' installed"""

        assert ubuntu.is_packege_installed("desktopvideo", ssh_host)
        assert ubuntu.is_packege_installed("mediaexpress", ssh_host)

    def test_profile_reboot_script(self, ssh_host):
        """BlackMagic profiles should be set to 3, the script that ensures that should be present
        in the system. from ticket: https://jira.thomsonreuters.com/browse/WNEC-5781
        """

        script_path = "/usr/local/bin/reuters/post/setBMCardProfiles.sh"
        assert ubuntu.is_file_exist_remote(
            script_path, ssh_host
        ), "setBMCardProfiles.sh script was not found"

    def test_firmware(self, ssh_host):
        """Firmware of the BlackMagic card installed should be up-to-date"""

        output = ubuntu.execute_cmd_remote("DesktopVideoUpdateTool -l", ssh_host)

        # Third output line contains the install status
        assert len(output.split("\n")) >= 3, "Firmware is not installed or not up-to-date"
        assert (
            "Firmware is up to date" == output.split("\n")[2].strip()
        ), "Firmware is not installed or not up-to-date"

    def test_activate_profile(self, ssh_host):
        """All devices should show that profile 3 is active"""
        activate_profile_path = "/usr/local/bin/reuters/post/ActivateProfile"

        # ActivateProfile executable should be present
        assert ubuntu.is_file_exist_remote(activate_profile_path, ssh_host)

        for device_id in range(4):
            output = ubuntu.get_cmd_error_output_remote(
                f"{activate_profile_path} -d {device_id}", ssh_host
            )
            lines = output.split("\n")

            assert (
                len(lines) >= 12
            ), "Activateprofile did not return the expected result, is the card installed?"
            # The * character marks the selected profile, should appear on line 13 of the output
            assert "*" in lines[12], "Active profile should be set to [3]"

    def test_is_enabled_and_active(self, ssh_host):
        """DesktopVideoHelper should be enabled and active in the init system"""

        # If is not active that means its not running
        assert ubuntu.is_service_active(
            "DesktopVideoHelper", ssh_host
        ), "DesktopVideoHelper should be active in systemd (systemctl start DesktopVideoHelper)"
        # If is not enabled that means that when the computer reboots it won't run on its own
        assert ubuntu.is_service_enabled(
            "DesktopVideoHelper", ssh_host
        ), "DesktopVideoHelper should be enabled in systemd (systemctl enable DesktopVideoHelper)"

    def test_is_card_installed(self, ssh_host):
        """BlackMagic card should be physically installed in the machine as a hardware"""

        output = ubuntu.execute_cmd_remote("lspci", ssh_host).lower()
        assert "blackmagic" in output, "BlackMagic card is not listed as an installed hardware"
